# SEC — EDGAR APIs de filings e XBRL

- ID: `sec-edgar-api`
- Assunto: financas-e-economia
- Cobertura: Estados Unidos / emissores registrados
- Página lida: 2026-10-04
- Fonte primária: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- Palavras-chave: companhias, filings, demonstrações financeiras, XBRL, CIK

Documentação de APIs JSON para histórico de documentos e fatos XBRL de companhias. Descreve submissions, companyconcept, companyfacts e frames, usando CIK com dez posições. Informa atualização conforme disseminação de documentos e limitações de taxonomias, períodos e acesso automatizado.

## Consulta e atualização

- Acesso: Sem chave/autenticação para APIs descritas; respeitar as regras de acesso automatizado da SEC.
- Formatos: JSON, ZIP de arquivos em massa
- API: https://data.sec.gov/
- Estado: Documentada; não executada por esta curadoria
- Revisão: Recuperar um CIK e conceito por vez. A documentação descreve atualização durante o dia; validar timestamps e versões efetivamente retornadas.
- Licença: não verificada; consultar termos

## Cuidados

- Sem CORS: acesso direto no navegador não é suportado.
- Comparações exigem conferir unidade, ano fiscal, período e contexto XBRL.
