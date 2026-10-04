# Base de conhecimento compartilhada

Fontes públicas do Brasil com referências globais para Codex, Claude e pesquisa humana. Curadoria iniciada em **04/10/2026**. Combina finanças, bolsa, economia, tecnologia, saúde, sociedade, ciência, clima e energia.

**Comece pelo [índice compacto](INDICE.md)** e pelo [método de consulta](CONSUMIR.md). Cada cartão registra página efetivamente lida, acesso, API documentada quando houver, limitações e fonte primária. O catálogo não contém todos os mercados/datasets do mundo.

Leia também as [regras de privacidade e LGPD](PRIVACIDADE.md): estatísticas agregadas, finalidade definida e exclusão de dados individuais.

## Estrutura

- `fontes/`: cartões de resumos próprios e links oficiais.
- `indices/`: mapa por assunto; `catalogo.json`: registro estruturado.
- `dados/snapshots/`: observações públicas agregadas com período, metadados, data de coleta e hashes da resposta.
- `base.py`: busca offline com limite de texto e coleta manual seletiva.
- `tests/`: verificações de consulta, dados malformados, orçamento, defasagem e preservação de cache.
- `validacao/`: resultados e revisão independente do Claude, com escopo explícito.

## Usar

Requer Python 3.10+ com SQLite FTS5, sem dependências externas ou serviço pago. Exemplos:

```bash
python base.py query "bolsa CVM ações" --limit 3 --max-chars 5000
python base.py snapshot wb-populacao
python base.py refresh wb-pib wb-populacao
python -m unittest discover -s tests -v
```

A busca seleciona cartões por termos, com ranking FTS5; não é busca semântica. O limite refere-se à saída de caracteres, não a tokens faturados. Nenhum cartão é cortado sem a fonte, data ou cuidados. Não há atualização automática. APIs com chave/licença específica são apontadas, sem contornar restrições.

## Dados, atualidade e direitos

Snapshots representam períodos estatísticos, não preços atuais ou orientação médica. Coleta recente pode trazer anos antigos. Métodos, unidades e revisões devem acompanhar qualquer comparação. Provedores que ainda não têm snapshot ficam como **documentados, não coletados**; confira `dados/ultima-coleta.json`.

Os indicadores iniciais vêm do Banco Mundial/WDI; atribuição original e organizações produtoras ficam em cada snapshot. Consulte [licenças de dados](https://datacatalog.worldbank.org/public-licenses) e termos específicos da série. A transformação local seleciona cinco observações não vazias por área, reorganiza campos e preserva valores; nenhuma unidade é convertida. Não se atribui uma licença única a dados de terceiros ou a todas as fontes do catálogo. Não foram copiados artigos, manuais completos ou bases licenciadas de preços da bolsa.

Este repositório público guarda fontes, métodos e dados agregados. Notas pessoais, currículos privados, prontuários, credenciais e conversas completas ficam fora dele. O Obsidian contém um espelho dos cartões e o registro local de trabalho; sincronização é explícita, não automática.
