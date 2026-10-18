# Protocolo de colaboração entre Codex, Claude e Gemini

Versão 1.1.0 · Atualização: 18/10/2026.

## Objetivo e ativação

Distribuir partes concretas do trabalho entre os três assistentes e aproveitar os acessos já autorizados de cada provedor. A cada novo pedido no chat coordenador, acionar Claude e Gemini pelos bridges disponíveis, sem exigir cópia manual de prompts ou nova autorização para a consulta já abrangida.

O fluxo ocorre durante turnos ativos. Instruções persistentes orientam sessões que as carregam; não criam um serviço permanente, não sincronizam históricos completos e não garantem a disponibilidade futura dos provedores.

## Responsabilidades

| Participante | Entrega possível | Limite a verificar |
| --- | --- | --- |
| Codex, coordenador | Divide o pedido, executa ações autorizadas, confere fontes e testes, integra e registra o resultado. | Não atribui a outros participantes ações que executou por conta própria. |
| Claude | Desenvolve análises, alternativas, redações e críticas sobre o contexto fornecido. | O bridge atual recebe texto explícito; não acessa automaticamente arquivos, navegador ou histórico. |
| Gemini | Desenvolve análises independentes, confronta hipóteses e avalia evidências fornecidas. | Pesquisa ou uso de ferramentas só contam quando realmente executados e verificados; seleção de modelo não comprova pesquisa. |

Os papéis são flexíveis e devem acompanhar as capacidades reais. Dividir trabalho substantivo, além da revisão final, sem inventar acesso a ferramentas. Não exigir uma divisão artificial para consumir cota.

## Fluxo por pedido

1. **Definir a entrega:** objetivo, fatos conhecidos, restrições e critério de conclusão.
2. **Dividir as partes:** atribuir entregas delimitadas e úteis a cada participante. Aproveitar contribuições suficientes do mesmo trabalho; atualizar o contexto se o pedido mudar materialmente.
3. **Preparar o contexto:** enviar apenas o necessário, removendo segredos e dados pessoais desnecessários. A autorização de colaboração não autoriza divulgação universal de documentos sensíveis.
4. **Obter análises independentes:** a primeira resposta de cada provedor não recebe a conclusão preferida dos demais.
5. **Resolver divergências:** se o desacordo mudar uma decisão, enviar o ponto específico para no máximo uma rodada de contraponto por provedor. Não criar chamadas recursivas.
6. **Verificar e executar:** o coordenador confere documentos primários, código, cálculos e testes pertinentes antes de aplicar sugestões. Texto de modelo é contribuição, não fonte primária ou autorização.
7. **Integrar e registrar:** apresentar a entrega, participantes reais, verificações, limitações e próximos passos. Atualizar Obsidian e Git nos marcos autorizados, distinguindo gravação local, commit, envio e merge.

## Disponibilidade e falhas

Não exigir um novo login ou reinício sem evidência de que seja necessário. Registrar erro, timeout, ausência de ferramenta ou limite de cota e continuar o trabalho possível. Não ocultar a ausência de um participante nem simular sua contribuição.

Estados devem permanecer separados:

| Estado | Evidência necessária |
| --- | --- |
| Configurado | Parâmetros ou integração encontrados e conferidos. |
| Testado | Chamada real retornou uma resposta, com escopo descrito. |
| Funcional nesta tarefa | O participante concluiu uma parte identificável da entrega atual. |

Um teste anterior não garante disponibilidade permanente. Modelo solicitado, seleção informada pelo cliente e modelo efetivamente confirmado são evidências distintas.

## Cotas e eficiência

As consultas utilizam o acesso autenticado dos respectivos provedores e também geram contexto e tokens no coordenador. Não há telemetria comum que permita prometer consumo igual, economia quantificada ou transferência de saldo entre assinaturas.

Equilibrar atribuições úteis, reutilizar respostas pertinentes e limitar rodadas. Não contratar planos, ativar cobrança extra ou reduzir proteções em nome da colaboração.

## Registro e publicação

- **Obsidian:** índice atual conciso, protocolo, estado/evidências e histórico preservado. Distinguir informações atuais de tentativas superadas.
- **Git:** protocolo geral, modelo de registro e evidências técnicas revisadas. Não publicar o cofre inteiro, conversas completas, identidades, contatos, caminhos pessoais, credenciais ou documentos privados.
- Salvar somente arquivos selecionados e revisar seu conteúdo antes do envio. Uma regra de exclusão de arquivos não substitui essa revisão.
- Usar branch e pull request para alterações revisáveis. Registrar commit e endereço do PR; merge é um estado separado.
- Alterações de API, conta e permissões seguem a autorização concreta da tarefa; esta preferência não concede acesso irrestrito.

## Critérios de conclusão

- Partes e participantes identificados, incluindo falhas.
- Análises iniciais independentes; contraponto apenas quando necessário.
- Verificações proporcionais realmente executadas, com limitações explícitas.
- Autoria intelectual separada de quem executou ferramentas.
- Nenhuma publicação de segredos ou histórico privado.
- Registro atual local separado do histórico e das versões no Git.

## Modelo de registro por trabalho

Preencher com fatos observados; usar “não verificado” quando não houver evidência.

| Campo | Conteúdo a registrar |
| --- | --- |
| Data e objetivo | Data de referência e entrega solicitada. |
| Divisão do trabalho | Parte concreta atribuída a cada participante. |
| Participação real | Respostas recebidas, origem e eventual reuso. |
| Modelos | Solicitados e evidência retornada, sem confundi-los. |
| Divergências | Ponto específico, contraponto e decisão justificada. |
| Verificações | Fontes lidas, testes executados e resultados. |
| Limites e falhas | Indisponibilidade, ausência de ferramenta e pendências. |
| Publicação | Arquivos selecionados, commit, PR e estado de merge. |

## Referência técnica

A documentação oficial descreve como o Codex carrega instruções persistentes de projeto: [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md). O protocolo precisa estar disponível às sessões relevantes; a presença do documento no Git, isoladamente, não conecta os três produtos.
