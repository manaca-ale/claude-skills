---
name: content-briefing
description: >
  Generates standardized content briefings for Manacá Tech's marketing agency from a
  Google Doc themes table. Accepts a URL with themes (DATA | FORMATO | TEMA | LEGENDA)
  and outputs a formatted Google Doc with complete briefings including strategic objectives,
  target audience, core message, tone guidelines, and format-specific scripts (Reels scenes,
  Carrossel cards, Post layouts). Use when the user asks to create briefings, generate pautas,
  brief the agency, or produce content briefs for social media.
---

# Content Briefing Generator — Manacá Tech

Generate professional content briefings for Manacá Tech's marketing agency from a themes table.

## Triggers

Use this skill when the user mentions any of:
- "briefing", "briefings", "brief"
- "pauta", "pautas"
- "agência", "conteúdo para agência"
- "criar briefing", "gerar briefing"
- Provides a Google Doc URL with a themes table

## Configuration

| Setting | Value |
|---------|-------|
| Google email | alecoleto@gmail.com |
| Template doc (copy source) | `1VwBbQV5-oihQ54CWYEKJsJxQHEjyy-_c8go0qqBJA_8` |
| Template doc name | `TEMPLATE — Briefing Manacá` |
| Existing briefings (reference) | `1sr0pkU6qiMV-QwDMV1GPBYbz1MKJ1P6oLrTOqMipQlE` |
| Output folder ID | `1xtwx-wDVxlAhrs__XW95KQ19L_4Xgk9j` |
| Output folder path | `07.00. Docs Manacá > Testes Agente Briefing` |

## Knowledge Base

Load these reference files to inform briefing generation:

| File | Purpose | When to load |
|------|---------|-------------|
| `references/brand-context.md` | Company identity, metrics, audiences, voice | Always (system context) |
| `references/briefing-templates.md` | Format-specific templates + formatting rules | Always (generation template) |
| `references/briefing-examples.md` | 3 real briefings as few-shot examples | Always (style reference) |
| `references/tone-matrix.md` | Tone calibration + guardrails + compliance | Always (tone + guardrails) |

**IMPORTANT**: Read ALL 4 reference files before generating any briefing. They are essential for maintaining consistency with the existing 9+ briefings already produced.

## Workflow

### Phase 0 — Input Collection

The skill accepts themes from **multiple input sources**. Detect which path to use:

#### Path A: Google Doc (MCP available)
If `mcp__google-docs__get_doc_as_markdown` is available AND the user provides a Google Doc URL:
1. Extract the document ID from the URL.
2. Read with `get_doc_as_markdown`. If empty, try `get_doc_content`.
3. Parse the themes table from the result.

#### Path B: File upload or paste (MCP NOT available)
If MCP Google Docs tools are NOT available, ask the user to provide the themes in one of these formats:
1. **Copy-paste the table** directly in the chat (most common)
2. **Excel/CSV file** — read with Python (`openpyxl` or `pandas`)
3. **Text file (.txt / .md)** — read with the Read tool
4. **Manual entry** — the user types themes one by one

When asking, say:
> "Não encontrei o MCP do Google Docs instalado. Você pode:
> 1. Colar a tabela de temas aqui no chat
> 2. Me passar um arquivo Excel (.xlsx) ou CSV com as colunas DATA | FORMATO | TEMA | LEGENDA
> 3. Digitar os temas manualmente
>
> Qual prefere?"

#### Parsing the themes table
Expected columns: **DATA | FORMATO | TEMA | LEGENDA**
- DATA: publication date
- FORMATO: Reels, Carrossel, Post único, Simples
- TEMA: content theme/title
- LEGENDA: caption text (may be empty)

The table can come in any format (Markdown table, tab-separated, CSV, pasted text). Parse flexibly — identify the columns by header names, not by position.

#### Output mode
- If MCP available → Google Docs output (one doc per briefing)
- If MCP NOT available → Word .docx output (see Phase 3 Fallback)

### Phase 1 — Parse and Confirm

1. Present parsed themes as a numbered list:
   ```
   Temas encontrados:
   1. [DATA] | [FORMATO] | [TEMA] | [com/sem legenda]
   2. ...
   ```
2. For each theme, classify:
   - **Format**: Reels / Carrossel / Post único
   - **Editoria**: Institucional / Educativo / Engajamento / Produto / Bastidores
   - **Legenda status**: provided or empty
3. Present classification and ask user to confirm before generating.

### Phase 2 — Briefing Generation

For each confirmed theme, generate a complete briefing following this process:

#### Step 2a: Load context
Read all 4 reference files if not already loaded.

#### Step 2b: Generate briefing content
For each theme, produce a briefing with this exact structure:

```
Título: {TEMA}
Formato: {FORMATO}
Status: Em produção
{ONLY if Reels or video format: "Vídeo: [orientações de gravação]"}
{ONLY if needs photos: "Fotos: [orientações sobre fotos necessárias]"}
__________________________________________________________________________________________________________________

01. Briefing para a agência

Objetivo do conteúdo:
[2-5 paragraphs using GET WHO TO BY framework as strategic core]
[Explain WHY this content exists, what it should achieve, how it fits the strategy]

Público-alvo:
[Bulleted list of specific target audiences for THIS content]

Mensagem central:
[1-2 paragraphs with the ONE key insight/thesis the audience must internalize]

Tom e linguagem:
[4-6 bullet descriptors calibrated per tone-matrix.md]

{Format-specific fields from briefing-templates.md}

__________________________________________________________________________________________________________________

02. ROTEIRO COMPLETO {DO REELS / DO CARROSSEL / DO CARD}

{Format-specific script following briefing-templates.md structure}
```

#### Step 2c: Apply guardrails
Before presenting each briefing, verify:
- [ ] No invented statistics (only data from brand-context.md)
- [ ] No vague sustainability clichés (check tone-matrix.md banned terms)
- [ ] Compliance notes included for B2G-relevant content
- [ ] Tone matches the editoria × format from tone-matrix.md
- [ ] Structure matches the real examples from briefing-examples.md

#### Step 2d: Present for review
Show each generated briefing to the user. Wait for approval or revision requests before proceeding to the next one. If the user requests changes, regenerate the affected sections.

### Phase 3 — Write to Google Doc

After all briefings are approved, create ONE Google Doc per briefing.

#### Step 3a: Create doc from template (one per briefing)

For EACH approved briefing, create a separate Google Doc by copying the dedicated template:

```
copy_drive_file(
  file_id="1VwBbQV5-oihQ54CWYEKJsJxQHEjyy-_c8go0qqBJA_8",
  new_name="Briefing — {DATA} — {TEMA_SHORT}",
  parent_folder_id="1xtwx-wDVxlAhrs__XW95KQ19L_4Xgk9j",
  user_google_email="alecoleto@gmail.com"
)
```

**Naming convention**: `Briefing — DD-MM — {Tema resumido}`
- Examples: `Briefing — 06-02 — Reunião Planejamento Bastidores`
- Examples: `Briefing — 11-02 — Mulheres e Meninas na Ciência`
- Keep the name under ~60 characters; abbreviate the TEMA if needed

The template doc (`TEMPLATE — Briefing Manacá`) has a placeholder briefing with all the correct formatting pre-applied:
- Bold field labels (Título:, Formato:, Objetivo:, etc.)
- Bullet lists for Público-alvo, Tom e linguagem, Diretrizes técnicas
- Bold section headings (01. Briefing para a agência, 2. ROTEIRO COMPLETO)
- Horizontal rules (underscore lines)

The copy inherits ALL this formatting. The workflow is then: **delete the placeholder content → insert the real briefing content**. The new text inherits the formatting of the text it replaces.

#### Step 3b: Replace placeholder content with real briefing

The copied template has placeholder text with `{TAGS}`. Replace the entire body content:

1. **Get the template body length**:
   ```
   inspect_doc_structure(document_id=<new_doc_id>)
   ```
   Note `total_length`.

2. **Delete all placeholder content** (keep index 1, delete from 1 to total_length-1):
   ```
   batch_update_doc(
     document_id=<new_doc_id>,
     operations=[{"type": "delete_text", "start_index": 1, "end_index": <total_length - 1>}]
   )
   ```

3. **Insert the real briefing text** at index 1:
   ```
   batch_update_doc(
     document_id=<new_doc_id>,
     operations=[{"type": "insert_text", "index": 1, "text": "<full briefing text>"}]
   )
   ```

The text should follow the exact structure from Phase 2 with `\n` line breaks.

#### Step 3c: Re-apply formatting

After replacing content, the formatting from the template is lost. Re-apply it:

1. **Inspect the document** to get exact paragraph indices:
   ```
   inspect_doc_structure(document_id=<new_doc_id>, detailed=true)
   ```

2. **Bold field labels** using `batch_update_doc` with `format_text` operations.
   Use the paragraph start indices from inspect to find each label. Bold these:
   - Header fields: "Título:", "Formato:", "Status:" (and "Vídeo:" / "Fotos:" only when present)
   - Section heading: "01. Briefing para a agência"
   - Field names: "Objetivo do conteúdo:", "Público-alvo:", "Mensagem central:", "Tom e linguagem:", "Diretrizes técnicas:", "Elementos essenciais no card:"
   - Section heading: "2. ROTEIRO COMPLETO DO REELS/CARROSSEL/CARD"
   - Scene/card headings in the roteiro

3. **Bullet lists** using `update_paragraph_style` with `list_type="UNORDERED"`:
   - Público-alvo items
   - Tom e linguagem items
   - Diretrizes técnicas items (Reels)
   - Elementos essenciais items (Post único)

#### Step 3d: Verify each doc

For each created document:
```
get_doc_as_markdown(document_id=<new_doc_id>)
```
Verify: text is present, bold applied, bullets rendered.

#### Output summary

After all docs are created, present a summary table to the user:

```
Briefings criados:
| # | Tema | Formato | Link |
|---|------|---------|------|
| 1 | {TEMA} | {FORMATO} | [abrir](link) |
| 2 | ... | ... | ... |

Pasta: 07.00. Docs Manacá > Testes Agente Briefing
```

### Phase 3 — Fallback: Word (.docx) output

**Use this path when Google Docs MCP tools are NOT available** (no `mcp__google-docs__*` tools loaded).

Generate `.docx` files locally using Python + `python-docx`:

```bash
pip install python-docx  # if not installed
```

For EACH approved briefing, create a Word document with this Python script pattern:

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Arial'
style.font.size = Pt(11)

# Header fields (bold label + normal value)
def add_field(doc, label, value):
    p = doc.add_paragraph()
    run_label = p.add_run(f"{label} ")
    run_label.bold = True
    run_label.font.size = Pt(11)
    p.add_run(value).font.size = Pt(11)

add_field(doc, "Título:", tema)
add_field(doc, "Formato:", formato)
add_field(doc, "Status:", "Em produção")
if video_orientacoes:
    add_field(doc, "Vídeo:", video_orientacoes)

# Horizontal rule
doc.add_paragraph("_" * 100)

# Section heading (bold)
p = doc.add_paragraph()
run = p.add_run("01. Briefing para a agência")
run.bold = True
run.font.size = Pt(12)

# Field with paragraph content
def add_section_field(doc, label, content):
    p = doc.add_paragraph()
    run = p.add_run(f"{label} ")
    run.bold = True
    p.add_run(content)

add_section_field(doc, "Objetivo do conteúdo:", objetivo_text)
# ... more fields ...

# Bulleted list
for item in publico_alvo_items:
    doc.add_paragraph(item, style='List Bullet')

# ... continue for all sections ...

# Save
filename = f"Briefing — {data} — {tema_short}.docx"
doc.save(filename)
```

**Output location**: Save `.docx` files to the current working directory.
**Naming**: Same convention as Google Docs: `Briefing — DD-MM — {Tema resumido}.docx`

Present the file paths to the user:
```
Briefings criados (Word):
| # | Tema | Formato | Arquivo |
|---|------|---------|---------|
| 1 | {TEMA} | {FORMATO} | Briefing — 06-02 — Reunião Planejamento.docx |
| 2 | ... | ... | ... |
```

### Phase 4 — Verification

**Google Docs mode**: For each created document:
1. Read it back:
   ```
   get_doc_as_markdown(document_id=<new_doc_id>, user_google_email="alecoleto@gmail.com")
   ```
2. Verify:
   - [ ] Briefing text is present and complete
   - [ ] Bold formatting applied to field labels and section headings
   - [ ] Bullet lists rendered for público-alvo, tom e linguagem, etc.
   - [ ] No template placeholders or artifacts remaining
3. Present all links in a summary table (see Phase 3 output format).

**Word fallback mode**: For each created `.docx`:
1. Open it with `python-docx` and read paragraphs back to verify content.
2. Verify bold and bullet formatting is applied.
3. Present file paths to the user.

## Generation Quality Standards

### Depth expectation
Each briefing should be **substantial** — comparable in length and detail to the real examples in `briefing-examples.md`. The agency needs enough context to produce content without further clarification. A typical briefing has:
- Objetivo: 100-250 words
- Público-alvo: 4-8 bullet items
- Mensagem central: 50-150 words
- Roteiro: 200-500 words depending on format

### Strategic thinking
The briefing is NOT just a reformatting of the TEMA. It should:
- Connect the theme to Manacá's strategic positioning
- Explain how this content serves the broader content strategy
- Identify the specific audience segment most relevant to this theme
- Craft a message that resonates with B2B/B2G decision-makers
- Provide creative direction that the agency can execute without guessing

### When LEGENDA is provided
- Use it as the creative compass — align the briefing to its tone and direction
- The roteiro should support the caption's narrative
- DO NOT contradict the caption
- Reference key hashtags from the caption as editorial signals

### When LEGENDA is empty
- Generate fuller creative direction (more detail in tom e linguagem)
- Include suggested caption in the roteiro section
- Give the agency more visual/editorial latitude but with clear guardrails
- Be more explicit about what the content should NOT be

## Common Pitfalls

| Pitfall | Prevention |
|---------|-----------|
| Generic briefings that could apply to any company | Always ground in Manacá's specific context, projects, and data |
| Inventing data not in brand-context.md | Cross-reference every statistic against brand-context.md |
| Roteiro too vague ("falar sobre impacto") | Provide specific text suggestions, scene descriptions, card copy |
| Ignoring format differences | Always use format-specific template from briefing-templates.md |
| Tone mismatch | Check tone-matrix.md for editoria × format calibration |
| Missing compliance guardrails for B2G content | Always include when público-alvo includes gestores públicos |
