# Banco Mundial — API de indicadores e metadados

- ID: `economia-wb-api`
- Assunto: financas-e-economia
- Cobertura: Brasil e global
- Página lida: 2026-10-04
- Fonte primária: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api
- Palavras-chave: PIB, população, desemprego, saúde, internet, indicadores, economia, World Bank

API V2 de séries agregadas de países e regiões, com metadados, notas de fonte e formatos estruturados. Os snapshots deste repositório consultam Brasil e agregado mundial, preservando período e unidade; não são cotações em tempo real. A API dispensa chave. A atualidade da coleta não garante atualidade do período estatístico. Consultar também a documentação de parâmetros e a página de acesso/licenciamento.

## Consulta e atualização

- Acesso: Público, sem chave para indicadores V2
- Formatos: JSON, XML
- API: https://api.worldbank.org/v2/
- Estado: Consultar dados/ultima-coleta.json para execução real
- Revisão: Coleta manual seletiva; revisar snapshots a cada 30 dias ou antes de uso atual.
- Licença: https://datacatalog.worldbank.org/public-licenses — conferir termos específicos.

## Cuidados

- Datasets têm termos próprios; atribuir Banco Mundial e provedores indicados nos metadados.
- Dados anuais podem ter defasagem e revisões.
- Mundo é agregado, não média simples dos países.
