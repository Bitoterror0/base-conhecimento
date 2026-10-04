# BCB — SGS / Selic diária

- ID: `bcb-sgs-selic`
- Assunto: financas-e-economia
- Cobertura: Brasil
- Página lida: 2026-10-04
- Fonte primária: https://dadosabertos.bcb.gov.br/pt_BR/dataset/11-taxa-de-juros---selic
- Palavras-chave: juros, Selic, política monetária, séries temporais

Catálogo da série SGS 11, taxa Selic diária calculada com operações compromissadas lastreadas em títulos públicos federais. Explica conceito, unidade, frequência e recursos para recuperação seletiva. A regra publicada para séries diárias exige filtros de período e limita cada solicitação a dez anos.

## Consulta e atualização

- Acesso: Catálogo público e recursos SGS documentados.
- Formatos: JSON, CSV, SOAP/WSDL, HTML
- API: https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados
- Estado: Documentada; não executada por esta curadoria
- Revisão: Frequência diária declarada. Selecionar série e janela curta; conferir último período disponível e registrar data de coleta.
- Licença: ODbL declarada no catálogo

## Cuidados

- A série 11 está em % ao dia; não confundir com meta Selic anual.
- Filtros de data obrigatórios; máximo de dez anos por requisição diária.
