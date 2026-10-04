# OCDE — boas práticas e limites da API

- ID: `oecd-api-practices`
- Assunto: financas-e-economia
- Cobertura: Global / serviço OCDE
- Página lida: 2026-10-04
- Fonte primária: https://www.oecd.org/en/data/insights/data-explainers/2024/11/Api-best-practices-and-recommendations.html
- Palavras-chave: APIs, cache, limites, versionamento, atualização

Guia operacional atualizado em março de 2026. Declara limite de 60 downloads por hora, também aplicável à interface CSV, e restrição de tráfego VPN/anonimizado. Recomenda cache, consulta contentconstraint para identificar mudanças e desenho eficiente das consultas.

## Consulta e atualização

- Acesso: Página pública; regras declaradas para o serviço Data Explorer.
- Formatos: HTML, Referência a consultas SDMX
- API: https://sdmx.oecd.org/public/rest/
- Estado: Documentada; não executada por esta curadoria
- Revisão: Consultar ValidFrom e versão via contentconstraint; reutilizar cache e recuperar dados após mudanças relevantes.
- Licença: não verificada; consultar termos

## Cuidados

- Limite publicado pode mudar; reler antes de operações recorrentes.
- Não usar VPN ou fontes anonimizadas para tentar contornar restrições.
