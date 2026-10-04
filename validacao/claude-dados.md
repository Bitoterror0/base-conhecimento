# Revisao estatica real do Claude

**📂 Painel de trabalho**
- Atual: revisão estática de `base.py`, `CONSUMIR.md`, `README.md`, do catálogo e do log de coleta. Concluída.
- Em andamento: nada pendente nesta demanda.
- Concluído: 5 defeitos com correção, mais melhorias e limitações separadas.
- Responsável: Claude (assistente principal), com a perspectiva de verificação adversarial e de dados. Nenhum subagente foi executado. Só li o texto colado e não sei quem escreveu o código.
- Validação: nenhum comando, teste ou ferramenta foi usado. Não vi `tests/`, `validacao/`, `INDICE.md`, os cartões nem os snapshots. O log de coleta foi lido como fornecido, sem reconferir.

## Recebimento e como consultarei a base

Recebi o escopo. Não tenho memória permanente da base, e ela não é carregada sozinha em nenhuma sessão. Só a consulto quando o pedido mandar ou quando a tarefa a exigir:

1. Leio `INDICE.md` (pequeno).
2. Rodo uma busca com limite, por exemplo no PowerShell: `python base.py query "inflação juros câmbio" --limit 3 --max-chars 5000`.
3. Leio de 2 a 5 cartões pertinentes e só os snapshots necessários, nunca a base inteira.
4. Na resposta, preservo link, unidade, período, `retrieved_at` e `cache_status`.
5. Para "hoje", preço, decisão financeira ou clínica, abro a fonte primária. Sem rede, aviso que uso um retrato histórico.

## Defeitos concretos (por gravidade)

**1. Unidade possivelmente perdida no Banco Mundial.**
- Problema: `'unit': p.get('unit','')` lê a unidade da observação. Pelo que conheço da WDI, esse campo costuma vir vazio, e a unidade está no nome do indicador (ex.: "(current US$)"). Se o snapshot real mostrar `unit: ""`, o `CONSUMIR.md` manda preservar uma unidade que não existe.
- Correção: gravar `unit_hint = metadata.get('name')` e `unit_status` (`declarada` ou `somente_no_nome`). Em `snapshot()`, avisar quando faltarem as duas coisas.
- Confiança: não conferi o snapshot real.

**2. Exceções fora da lista abortam o `refresh` sem relatório.**
- Problema: `except (OSError, ValueError, KeyError, TypeError)` não pega `http.client.IncompleteRead` (é `HTTPException`, não `OSError`). Também não pega `AttributeError`, que ocorre quando `.get` é chamado em item que não é dict, ou `.replace` em `valor` nulo ou numérico no BCB.
- Efeito: o cache fica preservado, porque a gravação é atômica. Mas `ultima-coleta.json` não é escrito e os IDs que deram certo ficam sem relatório.
- Correção:
```python
except Exception as e:  # por indicador; não captura KeyboardInterrupt
    report.append({'id': c['id'], 'status': 'failed_cache_preserved', 'error': type(e).__name__})
```

**3. Vazamento de caminho local em arquivo público.**
- Problema: `'error': str(e)[:240]` vai para `ultima-coleta.json`, num repositório público. A mensagem de `OSError` costuma incluir o caminho absoluto, que no Windows contém o nome do usuário.
- Correção: gravar a mensagem só se for `ValueError` próprio do código. Caso contrário, gravar `type(e).__name__`. Antes disso, substituir `str(root)` e `str(Path.home())` por `<repo>`.

**4. Validação incompleta das séries.**
- Problema: o código confere indicador e formato do ano, mas não confere o país (`countryiso3code != area`) nem períodos duplicados. No BCB, não verifica data duplicada nem ordem. O snapshot novo também pode trazer período mais antigo que o anterior e sobrescrevê-lo sem aviso.
- Correção:
```python
if p.get('countryiso3code') != area: raise ValueError('País divergente')
if len({v['period'] for v in valid}) != len(valid): raise ValueError('Período duplicado')
```
  Comparar o período máximo com o snapshot existente e registrar aviso de regressão.
- Observação: confirme `countryiso3code` em um snapshot real antes de tornar a checagem fatal.

**5. `cache_status` pode enganar.**
- Problema: `snapshot()` rotula "coleta recente" só por `retrieved_at`. Ignora uma tentativa posterior que falhou e a idade do último período. Além disso, `ultima-coleta.json` é sobrescrito com apenas os IDs da última execução, perdendo o estado dos demais.
- Correção: gravar `dados/status/<id>.json` com a última tentativa e seu resultado. Fazer `snapshot()` devolver `last_attempt_status`, `latest_period` e a idade do período em anos.

## Melhorias (não são defeitos)

- **Seleção e orçamento:** a lógica está coerente. Cartão inteiro, rodapé contado e `break` ao primeiro que não cabe, preservando o ranking.
  - Acrescentar desempate determinístico: `ORDER BY bm25(docs), id`.
  - Validar `--domain` e mostrar "domínio desconhecido" em vez de sugerir aumentar o orçamento.
- **Cobertura da busca:** sem radical nem sinônimo, "hospitais" não casa com "hospitalar". Opções: prefixo para termos com 5 ou mais letras (`"hospital"*`) ou campo `aliases`.
- **Cartões quase duplicados no catálogo:** `worldbank-indicators` e `economia-wb-api`, `oecd-api` e `oecd-api-practices`, `fred-api` e `fred-api-key`, `bcb-sgs-selic` e `bcb-sgs-json-metadata`. Eles consomem o `--limit`. Agrupar por `group` e mostrar um principal com referências aos filhos.
- **Direitos:** o cartão impresso não mostra licença, termos nem modo de acesso (chave, cadastro). Acrescentar `license`, `terms_url` e `access` ao catálogo e à saída.
- **Redirecionamento:** a checagem ocorre depois da requisição. Um `HTTPRedirectHandler` próprio bloquearia antes. O risco é baixo, porque não há credenciais.
- **BCB:** `ultimos/12` são 12 observações, não 12 meses. Em série diária, isso é cerca de 12 dias. A unidade vem de `config['metadata']` e não é validada contra a fonte.

## Limitações

- **Economia de tokens:** o limite é em caracteres, não em tokens nem em custo. Isso está dito corretamente no `CONSUMIR.md`. Medir exigiria um contador de tokens e comparação com e sem a base, o que não foi feito.
- **Catálogo colado:** só traz `id`, `name` e `domain`. `query()` precisa de `summary`, `topics`, `url`, `checked_on`, `review_after_days` e `cautions`. Se o arquivo real fosse assim, daria `KeyError`, que `main()` não captura. Assumo que o texto colado é um resumo, mas não verifiquei. Um validador de esquema ao carregar o catálogo evitaria o problema.
- **Parâmetros da API:** não conferi `mrnev`, `footnote=y` nem os endpoints contra a documentação atual.
- **Log de coleta:** `ok` e `points: 10` são coerentes com 2 áreas × 5 observações. Isso não prova período, unidade nem licença corretos.
- **Cartões:** a afirmação de que cada página foi efetivamente lida não pôde ser verificada.
- **Cache:** é evidência histórica, não dado atual. Dados de terceiros mantêm licenças próprias.