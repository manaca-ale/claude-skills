---
name: google-doc-from-template
description: >
  Cria um novo Google Doc a partir de um template existente, detectando automaticamente
  a formatação do template (fonte, cor, tamanhos, tabelas, capa, cabeçalhos/rodapés) e
  apresentando as regras detectadas para aprovação do usuário antes de criar o documento.
  Usar quando o usuário pedir para criar um documento seguindo o estilo/formatação de
  um template Google Docs existente.
---

# Criação de Documento a partir de Template Google Docs

Criar um novo Google Doc a partir de um template, detectando sua formatação,
aprovando as regras com o usuário e criando o documento com conteúdo novo.

## Inputs esperados do usuário

Coletar antes de iniciar (se não informados na mensagem):

1. **Template** — ID ou URL do Google Doc a usar como template
2. **Nome do novo documento**
3. **Conteúdo** — estrutura de seções, texto de parágrafos, dados das tabelas
4. **Pasta destino** no Google Drive (ID ou nome)
5. **Email Google** — conta que tem acesso ao Drive

## Fase 1 — Analisar o template

### 1a. Ler estrutura geral

```
inspect_doc_structure(detailed=True, document_id=<template_id>)
get_doc_as_markdown(document_id=<template_id>)
```

Identificar e anotar:
- `total_length` e número de elementos
- Presença de cabeçalho (`has_headers`) e rodapé (`has_footers`)
- Número e posição de tabelas
- Estrutura da capa (se existe página dedicada antes do conteúdo principal)
- Hierarquia de títulos (HEADING_1, HEADING_2, NORMAL_TEXT)

### 1b. Detectar formatação de texto

Usar `inspect_doc_structure(detailed=True)` e examinar os elementos para identificar:

| Propriedade | Como detectar |
|-------------|---------------|
| Fonte (font_family) | `inspect_doc_structure` mostra `font_family` por run de texto |
| Cor do texto | RGB dos runs (`foreground_color`) — converter para hex |
| Tamanho do corpo | `font_size` nos parágrafos NORMAL_TEXT |
| Tamanho dos headings | `font_size` nos parágrafos HEADING_1 / HEADING_2 |
| Negrito nos headings | `bold` nos runs de heading |
| Alinhamento da capa | `alignment` nos parágrafos da capa |
| Tamanho do título da capa | `font_size` no primeiro parágrafo significativo |

### 1c. Detectar formatação de tabelas

Usar `debug_table_structure(table_index=0)` em uma tabela do template para identificar:
- Número de colunas típico
- Conteúdo da primeira linha (verifica se é cabeçalho)
- Comparar bold/font_size da primeira linha vs demais linhas

### 1d. Detectar estrutura da capa

Se `inspect_doc_structure` mostrar seção de capa separada (page_break antes do SUMÁRIO
ou seção de introdução), identificar:
- Quantas linhas a capa tem
- Se é centralizada
- Padrão de conteúdo (nome do projeto / tipo do documento / data)

## Fase 2 — Apresentar regras detectadas ao usuário

Antes de qualquer criação, apresentar um resumo das regras detectadas no formato:

---
**Regras de formatação detectadas no template:**

| Elemento | Regra detectada |
|----------|----------------|
| Fonte | [nome da fonte] |
| Cor do texto | #[hex] |
| Corpo de texto | [N]pt, NORMAL_TEXT |
| Seções principais | HEADING_2, [N]pt, [negrito/normal] |
| Subseções | HEADING_1, [N]pt, [negrito/normal] |
| Cabeçalho de tabela | [N]pt, negrito |
| Corpo de tabela | [N]pt, sem negrito |
| Capa | [centralizada / alinhamento], [N]pt |
| Cabeçalho do doc | [presente / ausente] |
| Rodapé do doc | [presente / ausente] |

**Confirma estas regras? Ou deseja ajustar alguma antes de criar o documento?**

---

Aguardar confirmação ou correções do usuário antes de prosseguir.

## Fase 3 — Criar cópia do template

Copiar o template para herdar cabeçalho, rodapé e estilos base:

```
copy_drive_file(
  file_id=<template_id>,
  new_name="<nome_do_documento>"
)
```

Guardar o `file_id` do novo documento.

## Fase 4 — Deletar TODO o corpo

O template tem conteúdo existente. Deletar tudo antes de inserir conteúdo novo.

**4a. Inspecionar posições das tabelas:**
```
inspect_doc_structure(detailed=True)
```

**4b. Deletar tabelas de baixo para cima** (maior índice primeiro) em um único
`batch_update_doc` com operações `delete_text`. Ordem obrigatória: maior índice primeiro
para não deslocar posições das tabelas acima.

**4c. Re-inspecionar** para obter `total_length` atualizado (sem tabelas).

**4d. Deletar TODO o texto restante:**
```
batch_update_doc com delete_text start_index=1, end_index=total_length-2
```
Índice 0 é section_break — não deletável.

**Resultado:** documento com apenas cabeçalho e rodapé herdados. Corpo vazio.

## Fase 5 — Inserir conteúdo

**5a.** Estruturar o texto com marcadores `[[TABELA_N]]` onde as tabelas devem aparecer.

**5b.** Dividir em batches de ≤ 220 chars por operação `insert_text`.
Inserir em ordem crescente de índice (índice acumulado = soma dos chars já inseridos + 1).

**5c.** Se o template tem capa: inserir quebra de página após a capa.
```
batch_update_doc com insert_page_break no índice logo após o último parágrafo da capa
```
Usar `inspect_doc_structure` para localizar o índice correto após inserir o texto.

## Fase 6 — Criar e popular tabelas

**CRÍTICO:** `create_table_with_data` tem bug quando há múltiplas tabelas no mesmo
documento — todo o conteúdo vai para a primeira tabela criada.

**Workflow correto:**

**6a.** Para cada marcador `[[TABELA_N]]` (de baixo para cima — maior índice primeiro):
  1. `inspect_doc_structure` → localizar índice exato do marcador
  2. `create_table_with_data(index=<índice_do_marcador>, table_data=[[""]])` — cria estrutura vazia
  3. `find_and_replace_doc` → remover o marcador `[[TABELA_N]]`

**6b.** Após criar TODAS as tabelas, popular de baixo para cima (última tabela primeiro):
  1. `debug_table_structure(table_index=N)` → obter `insertion_index` de cada célula
  2. `batch_update_doc` com `insert_text` por célula, de baixo para cima dentro de cada tabela
  3. Re-executar `debug_table_structure` se inserções anteriores alteraram índices

**Regras para inserção em células:**
- Usar `insert_text` no `insertion_index` (insert puro — sem `end_index`)
- Nunca cobrir o `\n` estrutural da célula → retorna `Invalid deletion range`
- Sempre modificar de baixo para cima (maior `insertion_index` primeiro)

## Fase 7 — Formatar

Aplicar as regras aprovadas na Fase 2. **Ordem obrigatória: estilos de parágrafo ANTES de font/cor.**

### 7a. Aplicar estilos de parágrafo (heading styles)

Heading styles sobrescrevem `font_family` — aplicar ANTES da fonte/cor:

```
update_paragraph_style(heading_level=2) → seções principais
update_paragraph_style(heading_level=1) → subseções
update_paragraph_style(heading_level=0) → corpo de texto (NORMAL_TEXT)
update_paragraph_style(alignment="CENTER") → capa (se necessário)
```

**ATENÇÃO:** Templates costumam herdar HEADING_2 como estilo padrão de todos os parágrafos.
Todos os parágrafos de corpo de texto devem ser explicitamente resetados para NORMAL_TEXT
(heading_level=0) — caso contrário aparecerão como `##` no markdown.

### 7b. Aplicar formatação de caracteres (APÓS estilos de parágrafo)

Em um único `batch_update_doc` por documento:

1. Full doc → `font_family`, `foreground_color` (cor de todo o texto)
2. Headings → `bold=true`, `font_size=<heading_size>`
3. Corpo → `bold=false`, `font_size=<body_size>`
4. Full range das tabelas → `bold=false`, `font_size=<table_size>`
5. Primeira linha de cada tabela → `bold=true`, `font_size=<table_size>`

Para o range da primeira linha de uma tabela: usar `debug_table_structure` e pegar
de `cells[0][0].range.start` até `cells[0][last_col].range.end`.

## Fase 8 — Mover para pasta destino

```
update_drive_file(file_id=<novo_id>, add_parents="<pasta_destino_id>")
```

## Fase 9 — Verificar (obrigatório)

```
get_doc_as_markdown(document_id=<id>)
```

Confirmar com o usuário:
- [ ] Cabeçalho e rodapé visíveis (herdados do template)
- [ ] Capa com conteúdo e alinhamento corretos
- [ ] Page break entre capa e conteúdo principal (se aplicável)
- [ ] Seções numeradas corretamente
- [ ] Tabelas com conteúdo correto (sem células vazias ou misturadas)
- [ ] Nenhum conteúdo do template original remanescente
- [ ] Formatação conforme regras aprovadas na Fase 2
- [ ] Documento na pasta destino correta

## Armadilhas conhecidas

| Problema | Causa | Solução |
|----------|-------|---------|
| Corpo de texto aparece como `##` | Template herda HEADING_2 como padrão | `update_paragraph_style(heading_level=0)` em todos os parágrafos de corpo |
| `create_table_with_data` coloca conteúdo na 1ª tabela | Bug da API com múltiplas tabelas | Criar estrutura vazia via `create_table_with_data`, popular via `debug_table_structure` + `batch_update_doc insert_text` |
| Fonte não muda após `format_text` | `update_paragraph_style` com heading_level sobrescreve `font_family` | Aplicar `format_text` (fonte/cor) SEMPRE APÓS `update_paragraph_style` (heading) |
| Índices incorretos ao popular células | Índices ficam stale após inserções | Popular de baixo para cima; re-executar `debug_table_structure` após inserções |
| `Invalid deletion range` | Range cobre `\n` estrutural da célula | Usar insert puro (sem `end_index`) ou `find_and_replace` |
| Índices errados após inserir título | Inserção em index fixo desloca tudo abaixo | Re-inspecionar com `inspect_doc_structure` após qualquer inserção antes de usar índices salvos |
| Rate limit (429) | 60 write requests/minute/user | Paralelizar apenas em documentos diferentes; sequenciar dentro do mesmo documento |
| Tabelas criadas fora de ordem | Inserção no índice do marcador | Criar tabelas de baixo para cima (maior índice primeiro) para preservar posições |
