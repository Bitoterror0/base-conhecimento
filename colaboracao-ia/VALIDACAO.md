# Validação da colaboração — 18/10/2026

Protocolo: versão 1.1.0. Escopo: estruturar e registrar o modo de trabalho da equipe.

## Divisão e participação efetiva

| Participante | Parte atribuída | Evidência recebida |
| --- | --- | --- |
| Codex | Conferir o destino no Git, organizar os arquivos e notas, revisar as contribuições e efetuar as gravações autorizadas. | Leitura do README e das regras de privacidade do repositório; preparação e conferência dos textos. A prova final de publicação fica no PR e no histórico Git. |
| Claude | Redigir o fluxo operacional e critérios de conclusão. | Resposta textual real do bridge, sem erro informado. Entregou fluxo, regras, critérios e modelo de registro. |
| Gemini | Propor matriz de responsabilidades e distinguir configuração, teste e funcionamento por tarefa. | Resposta textual real do bridge, sem erro informado. Propôs matriz e separação entre fonte atual e histórico. |

As consultas iniciais foram independentes: nenhum dos provedores recebeu a resposta do outro. Não houve divergência material que justificasse outra rodada. Codex adaptou critérios que pressupunham sucesso de todos para também contemplar falhas registradas e testes não aplicáveis.

## Modelos e limites

O cliente do Gemini informou `gemini-4-argon-high` no evento de inicialização. Isso é evidência da seleção reportada pelo cliente. Nesta consulta, a resposta do Claude não trouxe confirmação independente do modelo ou do esforço efetivo; a preferência configurada permanece separada dessa evidência.

Claude e Gemini trabalharam com texto fornecido. Não leram o Obsidian, não acessaram o Git e não fizeram pesquisa externa nesta tarefa. Codex executou as operações de registro. Não houve medição de tokens ou comparação de cotas.

## Organização documental

O protocolo geral é publicado nesta pasta. O registro local mantém índice atual, protocolo, estado/evidências e histórico de implantação separado. Informações antigas são preservadas como histórico, sem servirem como status atual.

O conteúdo selecionado para o Git foi revisado para excluir conversas, credenciais, contatos, caminhos pessoais e documentos privados. Não se trata de uma auditoria integral do repositório ou de um detector infalível de segredos.

## O que esta validação não comprova

- Operação permanente, sincronização dos três históricos ou acionamento enquanto o chat estiver inativo.
- Mesma disponibilidade, modelo ou ferramentas em tarefas futuras.
- Consumo igual entre contas ou economia medida.
- Autenticação ou inferência da API TypeSafe/Jev.
- Merge do pull request apenas porque os arquivos foram commitados.

Esta é uma mudança de documentação: a verificação pertinente é conferir conteúdo, links e gravações, sem inventar uma suíte de testes de software.


## Atualização de 30/10/2026 — versão 1.3.0

O usuário solicitou economia de contexto e consultas, mantendo os modelos e o esforço alto. A regra substitui o acionamento obrigatório dos outros dois em cada mensagem por colaboração proporcional: partes complementares em trabalhos complexos, contexto enxuto, reaproveitamento e revisão focada. Agentes entram quando o benefício justificar o custo de coordenação.

- **Claude:** recebeu o recorte da regra por consulta real e confirmou o alinhamento. Ressalvou que não guarda memória entre chamadas e depende das instruções/contexto carregados.
- **Gemini:** recebeu o mesmo recorte, sem a resposta do Claude, pelo ponto MCP corrigido. Confirmou recebimento e recomendou incluir um resumo mínimo do estado junto com as mudanças nas retomadas.
- **Codex:** integrou as ressalvas, conferiu os arquivos de destino e atualizou o protocolo compartilhado e o registro privado no Obsidian.

A seleção reportada foi Claude Opus 5.5/high e Gemini Argon High, sem inferir ferramentas ou pesquisa externa. Ambos apenas responderam ao texto fornecido: não leram o Git/Obsidian nem gravaram arquivos. O recebimento desta consulta não comprova aplicação em todas as sessões futuras. Não foi feita medição comparável de consumo e não se anuncia economia percentual ou equivalência entre cotas.

Publicação limitada ao protocolo geral e a este registro de validação, sem transcrição de conversas, dados pessoais, caminhos privados, credenciais, cache ou configurações das contas. Alteração documental conferida por leitura e comparação; não exige executar novamente testes de software. O PR permanece separado do merge.
