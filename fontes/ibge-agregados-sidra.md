# IBGE — API de Dados Agregados que alimenta o SIDRA

- ID: `ibge-agregados-sidra`
- Assunto: sociedade-e-trabalho
- Cobertura: Brasil; localidades conforme pesquisa
- Página lida: 2026-10-04
- Fonte primária: https://servicodados.ibge.gov.br/api/docs/agregados?versao=3
- Palavras-chave: SIDRA, censos, PNAD, agregados, API

Documentação oficial da API versão 3 que alimenta o SIDRA e disponibiliza pesquisas e censos do IBGE. Explica que cada tabela corresponde a um agregado e descreve rotas para listar agregados, localidades, metadados, períodos e variáveis, além de um gerador de consultas. É a entrada mais útil para construir consultas reproduzíveis com identificadores explícitos. A documentação foi lida, mas não executamos uma extração de valores. Nem toda tabela possui os mesmos recortes, categorias, unidades ou calendário, que devem ser descobertos nos metadados.

## Consulta e atualização

- Acesso: Documentação pública; autenticação, limites e licença específica não confirmados na leitura.
- Formatos: HTML (documentação), respostas de objetos/arrays documentadas; extração não executada
- API: https://servicodados.ibge.gov.br/api/v3/agregados
- Estado: Documentada; não executada por esta curadoria
- Revisão: Persistir tabela, variável, período, localidades, categorias e versão da consulta; conferir metadados e períodos antes de atualizar resultados.
- Licença: Não presumida: conferir termos específicos da fonte/dataset antes de redistribuir conteúdo.

## Cuidados

- Documentação e existência de rota não equivalem a teste de execução.
- Não combinar totais e subtotais sobrepostos.
- Dados agregados não descrevem indivíduos nem autorizam inferências causais.
