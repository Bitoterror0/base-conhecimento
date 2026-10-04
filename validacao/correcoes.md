# Integração da revisão do Claude

Em 04/10/2026, o Claude (`data-science-engineer`) recebeu código, método, catálogo resumido e log de coleta; fez revisão estática, sem ferramentas. Um segundo retorno (`security-compliance-officer`) avaliou por texto as regras de privacidade, método e métricas. Retornos completos estão nesta pasta. Não foram testes independentes executados pelo Claude.

Correções aplicadas pelo Codex e verificadas nos testes:

- Unidade/semântica: `unit_hint` e `unit_status` preservam nome/notas do indicador quando a API não declara unidade em campo separado.
- Erros por indicador são registrados por classe, sem mensagem bruta que possa conter caminho pessoal.
- País e período são validados; duplicatas e regressão do último período preservam cache anterior.
- Estado da última tentativa fica por indicador, além do relatório da rodada; leitura informa período e idade aproximada em anos.
- Redirecionamento para outro host/HTTP é bloqueado antes do pedido; catálogo tem validação mínima de esquema.
- Busca inclui acesso/licença, desempate determinístico e alguns aliases; domínio desconhecido é erro explícito.

Mantidos como limites: busca lexical, revisão editorial manual, licença por dataset, ausência de cotação em tempo real, nenhuma medição de tokens faturados, dados agregados sem análise individual. A revisão de privacidade não foi auditoria jurídica. O teste de preservação de cache inicialmente falhou por permissões de diretório temporário no Windows; o teste foi ajustado para um diretório normal do projeto e passou. Isso não foi falha de uma API de dados.
