import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
import uuid
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import base

class BaseTests(unittest.TestCase):
    def test_queries_budget_accent_and_injection(self):
        for term in ('inflação Selic','saúde hospitais','Python API segurança','" OR 1=1 --'):
            result=base.query(term,max_chars=5000)
            self.assertLessEqual(len(result),5000)
        self.assertIn('bcb',base.query('Selic juros').lower())
        self.assertEqual(base.query('saúde hospitais'),base.query('saude hospitais'))

    def test_empty_and_invalid_queries(self):
        for term in ('','de da e'):
            with self.assertRaises(ValueError): base.query(term)
        with self.assertRaises(ValueError): base.query('PIB',limit=500)
        with self.assertRaises(ValueError): base.query('PIB',max_chars=50)

    def test_cards_complete_and_expiry_visible(self):
        result=base.query('Python',today=dt.date(2027,1,1))
        self.assertIn('revalidar',result)
        self.assertIn('Fonte: https://',result)
        self.assertIn('Cuidados:',result)
        # Sem truncar um cartão ao atingir um orçamento pequeno.
        result=base.query('Python',max_chars=600)
        self.assertLessEqual(len(result),600)

    def test_domain_restricts_ranking(self):
        result=base.query('dados economia',domain='saude')
        self.assertNotIn('bcb-sgs',result)

    def test_catalogue_metadata_and_links(self):
        rows=base.catalogue()
        self.assertEqual(len(rows),len({s['id'] for s in rows}))
        for s in rows:
            self.assertEqual(s['verification'],'page_read')
            self.assertTrue((base.ROOT/'fontes'/(s['id']+'.md')).exists())
            dt.date.fromisoformat(s['checked_on'])
            self.assertIsInstance(s['cautions'],list)

    def test_invalid_snapshot_id_rejected(self):
        with self.assertRaises(ValueError): base.snapshot('../../private')
        with self.assertRaises(ValueError): base.refresh(['all'])

    def test_bad_data_preserves_existing_cache(self):
        configs=json.loads((base.ROOT/'indicadores.json').read_text(encoding='utf-8'))
        c=configs[0]
        root=base.ROOT/('test-run-'+uuid.uuid4().hex)
        target=root/'dados'/'snapshots'/(c['id']+'.json')
        try:
            target.parent.mkdir(parents=True); target.write_text('preservar',encoding='utf-8')
            def broken(url):
                if '/indicator/NY.GDP' in url and '/country/' not in url:
                    return [{'pages':1},[{'id':c['code'],'name':'GDP'}]],'meta'
                return [{'pages':1},[{'countryiso3code':'BRA','indicator':{'id':c['code']},'date':'2024','value':True}]],'raw'
            with self.assertRaises(ValueError): base.collect(c,root,broken)
            self.assertEqual(target.read_text(),'preservar')
            with self.assertRaises(OSError): base.collect(c,root,lambda url: (_ for _ in ()).throw(OSError('offline')))
            self.assertEqual(target.read_text(),'preservar')
        finally:
            # Remove apenas os arquivos e diretórios que este teste criou.
            if target.exists(): target.unlink()
            for folder in (target.parent,target.parent.parent,root):
                if folder.exists(): folder.rmdir()

    def test_real_snapshots_periods_provenance(self):
        snapshots=list((base.ROOT/'dados'/'snapshots').glob('*.json'))
        self.assertEqual(len(snapshots),6)
        for file in snapshots:
            s=base.snapshot(file.stem)
            self.assertEqual(len(s['points']),10)
            self.assertEqual(set(p['area'] for p in s['points']),{'BRA','WLD'})
            self.assertTrue(s['not_realtime'])
            self.assertEqual(len(s['response_sha256']),3)
            self.assertIn('cache_status',s)
            self.assertTrue(all(p['period'].isdigit() for p in s['points']))
            self.assertIn('unit_hint',s)
            self.assertEqual(s['last_attempt']['status'],'ok')

    def test_failure_status_survives_other_collects_without_private_paths(self):
        root=base.ROOT/('test-run-'+uuid.uuid4().hex)
        root.mkdir(); (root/'indicadores.json').write_bytes((base.ROOT/'indicadores.json').read_bytes())
        try:
            with patch.object(base,'collect',side_effect=AttributeError('C:/private/person/failure')):
                r=base.refresh(['wb-pib'],root)
            self.assertEqual(r[0]['status'],'failed_cache_preserved')
            state=(root/'dados/status/wb-pib.json').read_text()
            self.assertNotIn('private',state)
            self.assertIn('AttributeError',state)
        finally:
            for f in (root/'indicadores.json',root/'dados/ultima-coleta.json',root/'dados/status/wb-pib.json'):
                if f.exists(): f.unlink()
            for folder in (root/'dados/status',root/'dados',root):
                if folder.exists(): folder.rmdir()

    def test_redirect_is_blocked_before_request_and_domain_error(self):
        req=base.urllib.request.Request('https://api.worldbank.org/v2/')
        with self.assertRaises(ValueError):
            base.SameHostRedirect().redirect_request(req,None,302,'',{},'https://evil.example/data')
        with self.assertRaises(ValueError): base.query('dados',domain='inexistente')

if __name__=='__main__': unittest.main()
