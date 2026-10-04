"""Base pública: busca offline com orçamento e coleta limitada de indicadores oficiais."""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import unicodedata
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
STOP = set('de da do das dos e em na no nas nos o a os as para sobre quero dados fonte fontes'.split())
def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text.casefold()) if not unicodedata.combining(c))

def atomic(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as out:
            json.dump(obj, out, ensure_ascii=False, indent=2); out.write('\n')
            out.flush(); os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)

def catalogue(root=ROOT):
    rows=json.loads((root/'catalogo.json').read_text(encoding='utf-8'))
    if not isinstance(rows,list): raise ValueError('Catálogo deve conter uma lista')
    for s in rows:
        if not isinstance(s,dict) or not all(isinstance(s.get(k),str) for k in ('id','name','domain','summary','url','checked_on','access','license')):
            raise ValueError('Cartão sem campos obrigatórios')
        if not all(isinstance(s.get(k),list) and all(isinstance(x,str) for x in s[k]) for k in ('topics','cautions')):
            raise ValueError('Tópicos/cuidados inválidos')
        if not isinstance(s.get('review_after_days'),int) or s['review_after_days']<1: raise ValueError('Revisão inválida')
        dt.date.fromisoformat(s['checked_on'])
    return rows

def query(text, limit=3, max_chars=6000, domain=None, root=ROOT, today=None):
    if not 1 <= limit <= 10 or not 600 <= max_chars <= 20000 or not text.strip() or len(text)>500:
        raise ValueError('Consulta: 1–10 resultados, 600–20000 caracteres, texto de 1–500 caracteres.')
    rows = catalogue(root)
    if domain is not None and domain not in {s['domain'] for s in rows}: raise ValueError('Domínio desconhecido; consulte INDICE.md')
    terms = [t for t in re.findall(r'[a-z0-9]+', norm(text)) if t not in STOP][:30]
    if not terms:
        raise ValueError('Informe ao menos um assunto específico.')
    aliases={'hospitais':'hospital hospitalar','acoes':'acao acoes bolsa','ia':'inteligencia artificial ia','apis':'api apis'}
    terms=list(dict.fromkeys(t for term in terms for t in aliases.get(term,term).split()))[:40]
    # Índice em memória: nunca lê o cofre, rede ou PDFs. Textos não viram SQL executável.
    con = sqlite3.connect(':memory:')
    try:
        con.execute('CREATE VIRTUAL TABLE docs USING fts5(id UNINDEXED, search, tokenize="unicode61")')
        selected = [s for s in rows if domain is None or s['domain']==domain]
        for s in selected:
            searchable = ' '.join([s['name'],s['domain'],s['summary'],*s['topics']])
            con.execute('INSERT INTO docs VALUES (?,?)',(s['id'], norm(searchable)))
        hits = con.execute('SELECT id FROM docs WHERE docs MATCH ? ORDER BY bm25(docs), id LIMIT ?',
                           (' OR '.join('"'+t+'"' for t in terms),limit)).fetchall()
    finally:
        con.close()
    current = today or dt.date.today()
    chunks = []
    for (ident,) in hits:
        s = next(r for r in rows if r['id']==ident)
        age = (current-dt.date.fromisoformat(s['checked_on'])).days
        state = 'revalidar' if age<0 or age>s['review_after_days'] else 'catálogo dentro da revisão sugerida'
        card = f"## {s['id']} — {s['name']}\nFonte: {s['url']}\nLeitura: {s['checked_on']} | {state}\n"
        card += s['summary']+'\nCuidados: '+'; '.join(s['cautions'])+'\n'
        card += 'Acesso: '+s['access']+'\nLicença: '+s['license']+'\n'
        card += 'Metadados completos: fontes/'+s['id']+'.md\n'
        if len('\n'.join(chunks+[card]))>max_chars:
            break  # Não corta a URL, data ou os cuidados de um cartão.
        chunks.append(card)
    footer='\nCatálogo não garante dado atual. Para "hoje", decisões financeiras ou clínicas, revalide a fonte primária.\n'
    while chunks and len('\n'.join(chunks)+footer)>max_chars:
        chunks.pop()
    return '\n'.join(chunks)+footer if chunks else 'Nenhum cartão completo cabe ou corresponde à busca. Use termos específicos ou aumente o orçamento.\n'

class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target=urllib.parse.urlparse(newurl); original=urllib.parse.urlparse(req.full_url)
        if target.scheme!='https' or target.hostname!=original.hostname:
            raise ValueError('Redirecionamento fora do provedor')
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def get_json(url):
    req=urllib.request.Request(url, headers={'User-Agent':'base-conhecimento/1.0 (public indicators)','Accept':'application/json'})
    with urllib.request.build_opener(SameHostRedirect()).open(req, timeout=25) as response:
        if response.status!=200: raise ValueError('HTTP inesperado')
        # Provedores abaixo usam HTTPS. Redirecionamento deve continuar no mesmo host autorizado.
        final=urllib.parse.urlparse(response.url)
        start=urllib.parse.urlparse(url)
        if final.scheme!='https' or final.hostname!=start.hostname: raise ValueError('Redirecionamento fora do provedor')
        raw=response.read(2_000_001)
        if len(raw)>2_000_000: raise ValueError('Resposta ultrapassa 2 MB')
    return json.loads(raw), hashlib.sha256(raw).hexdigest()

def collect(config, root=ROOT, fetch=get_json):
    # URLs são construídas exclusivamente por códigos validados; sem URL arbitrária ou credenciais.
    provider=config['provider']; code=config['code']; urls=[]
    if provider=='worldbank' and re.fullmatch(r'[A-Z0-9_.]+',code):
        meta_url=f'https://api.worldbank.org/v2/indicator/{code}?format=json'
        meta, mh=fetch(meta_url); urls.append(meta_url)
        if not isinstance(meta,list) or len(meta)!=2 or not meta[1] or meta[1][0].get('id')!=code:
            raise ValueError('Metadados do indicador inválidos')
        metadata=meta[1][0]; points=[]; hashes=[mh]; updates={}
        for area in config['areas']:
            if area not in ('BRA','WLD'): raise ValueError('Área não autorizada')
            url=f'https://api.worldbank.org/v2/country/{area}/indicator/{code}?format=json&mrnev=5&per_page=10&footnote=y'
            result,h=fetch(url); urls.append(url); hashes.append(h)
            if not isinstance(result,list) or len(result)!=2 or not isinstance(result[1],list):
                raise ValueError('Formato de série inválido')
            if result[0].get('pages',0)>1: raise ValueError('Paginação inesperada: preserve cache')
            updates[area]=result[0].get('lastupdated')
            valid=[]
            for p in result[1]:
                if not isinstance(p,dict) or p.get('countryiso3code')!=area: raise ValueError('País/formato divergente')
                value=p.get('value')
                if value is None: continue
                if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value): raise ValueError('Valor inválido')
                if p.get('indicator',{}).get('id')!=code or not re.fullmatch(r'\d{4}',str(p.get('date',''))): raise ValueError('Indicador/período divergente')
                valid.append({'area':area,'period':p['date'],'value':value,'decimal':p.get('decimal'),'unit':p.get('unit',''),'footnote':p.get('footnote','')})
            if not valid: raise ValueError('Área sem observações válidas: cache preservado')
            if len({p['period'] for p in valid})!=len(valid): raise ValueError('Período duplicado')
            points.extend(valid)
    elif provider=='bcb' and re.fullmatch(r'\d{1,6}',code):
        url=f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/12?formato=json'
        result,h=fetch(url); urls=[url]; hashes=[h]; metadata=config['metadata']; points=[]; updates={}
        if not isinstance(result,list) or not result or len(result)>12: raise ValueError('SGS fora do limite')
        for p in result:
            if not isinstance(p,dict) or not isinstance(p.get('valor'),str): raise ValueError('Formato SGS inválido')
            date=dt.datetime.strptime(p['data'],'%d/%m/%Y').date().isoformat()
            value=float(p['valor'].replace(',','.'))
            if not math.isfinite(value): raise ValueError('SGS inválido')
            points.append({'area':'BRA','period':date,'value':value,'unit':metadata['unit']})
        if len({p['period'] for p in points})!=len(points): raise ValueError('Período SGS duplicado')
    else: raise ValueError('Provedor/código inválido')
    latest={a:max(p['period'] for p in points if p['area']==a) for a in {p['area'] for p in points}}
    target=root/'dados'/'snapshots'/(config['id']+'.json')
    if target.exists():
        old=json.loads(target.read_text(encoding='utf-8'))
        for a,last in latest.items():
            previous=[p['period'] for p in old.get('points',[]) if p['area']==a]
            if previous and last<max(previous): raise ValueError('Regressão de período: cache preservado')
    snap={'id':config['id'],'provider':provider,'code':code,'retrieved_at':dt.datetime.now(dt.timezone.utc).isoformat(),
          'metadata':metadata,'source_urls':urls,'response_sha256':hashes,'points':points,
          'review_after_days':config['review_after_days'],'not_realtime':True,'latest_period':latest,'source_last_updated':updates,
          'unit_hint':metadata.get('name',''),'unit_status':'declarada' if metadata.get('unit') else 'consultar nome e notas do indicador'}
    atomic(target,snap)
    return snap

def refresh(ids, root=ROOT):
    configs=json.loads((root/'indicadores.json').read_text(encoding='utf-8'))
    known={x['id'] for x in configs}
    if not ids or set(ids)-known: raise ValueError('Informe IDs conhecidos; atualização nunca baixa todo o catálogo.')
    report=[]
    for c in configs:
        if c['id'] not in ids: continue
        try:
            s=collect(c,root); report.append({'id':c['id'],'status':'ok','points':len(s['points']),'retrieved_at':s['retrieved_at']})
        except Exception as e:
            # Mensagem pública não contém caminhos locais nem o texto bruto de exceções.
            report.append({'id':c['id'],'status':'failed_cache_preserved','error_type':type(e).__name__})
        atomic(root/'dados'/'status'/(c['id']+'.json'),{'attempted_at':dt.datetime.now(dt.timezone.utc).isoformat(),**report[-1]})
    atomic(root/'dados'/'ultima-coleta.json',{'attempted_at':dt.datetime.now(dt.timezone.utc).isoformat(),'results':report})
    return report

def snapshot(ident, root=ROOT):
    if not re.fullmatch(r'[a-z0-9-]+',ident): raise ValueError('ID inválido')
    s=json.loads((root/'dados'/'snapshots'/(ident+'.json')).read_text(encoding='utf-8'))
    age=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(s['retrieved_at'])).total_seconds()/86400
    s['cache_status']='revalidar' if age<0 or age>s['review_after_days'] else 'coleta recente; período pode ser antigo'
    status=root/'dados'/'status'/(ident+'.json')
    s['last_attempt']=json.loads(status.read_text(encoding='utf-8')) if status.exists() else {'status':'não registrado'}
    s['latest_period']={a:max(p['period'] for p in s['points'] if p['area']==a) for a in {p['area'] for p in s['points']}}
    s['period_age_years']={a:dt.date.today().year-int(period[:4]) for a,period in s['latest_period'].items()}
    if s['last_attempt'].get('status')=='failed_cache_preserved': s['cache_status']='última tentativa falhou; cache histórico preservado'
    return s

def main():
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser(description=__doc__); subs=p.add_subparsers(dest='cmd',required=True)
    q=subs.add_parser('query'); q.add_argument('text'); q.add_argument('--limit',type=int,default=3); q.add_argument('--max-chars',type=int,default=6000); q.add_argument('--domain')
    r=subs.add_parser('refresh'); r.add_argument('ids',nargs='+')
    s=subs.add_parser('snapshot'); s.add_argument('id')
    args=p.parse_args()
    try:
        if args.cmd=='query': print(query(args.text,args.limit,args.max_chars,args.domain),end='')
        elif args.cmd=='refresh':
            results=refresh(args.ids); print(json.dumps(results,ensure_ascii=False,indent=2)); return int(any(x['status']!='ok' for x in results))
        else: print(json.dumps(snapshot(args.id),ensure_ascii=False,indent=2))
    except (ValueError,OSError,json.JSONDecodeError) as e: p.exit(2,str(e)+'\n')
    return 0

if __name__=='__main__': raise SystemExit(main())
