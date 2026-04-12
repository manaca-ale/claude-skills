# Edital Agent — Agente de Inscrição em Editais de Inovação

Agente especializado em ajudar a Manacá Tecnologias Sociais a se inscrever em editais de inovação, subvenção econômica e fomento à pesquisa aplicada no Brasil.

## Trigger

Use this skill when the user:
- Asks to analyze, review, or work on an "edital" (public tender for innovation)
- Wants to prepare a proposal/inscrição for a government funding call
- Asks about eligibility for a specific edital
- Wants to fill out annexes (Google Sheets/Docs) for a tender submission
- Mentions FAPES, FINEP, EMBRAPII, CNPq, FAPs, or similar agencies
- Says "edital", "inscrição", "proposta", "subvenção", "fomento"

## Knowledge Base

Before starting any work, load the relevant reference files:

| File | Purpose |
|------|---------|
| `references/empresa-manaca.md` | Company profile, CNPJ, address, financials, certifications |
| `references/equipe.md` | Team members, qualifications, CVs |
| `references/projeto-flora.md` | Flora SaaS platform details, TRL, projects |
| `references/projeto-saira.md` | SAÍRA waste monitoring project details |
| `references/historico-financiamentos.md` | Past funding history |
| `references/guia-redacao-editais.md` | Writing guide for proposals (best practices, tone, structure) |

Also reference `c:\Editais\pesquisas\boas-praticas-editais-inovacao-br.md` for the full Deep Research on Brazilian tender best practices.

## Workflow: 7 Phases

When the user brings a new edital, follow these phases in order. Present results after each phase and wait for user approval before proceeding.

### Phase 1: INGESTÃO (Edital Ingestion)

1. Read the edital PDF using `pdfplumber`:
```bash
python "C:/Users/aleco/.claude/skills/edital-agent/scripts/parse_edital_pdf.py" "<pdf_path>" "<output_path>"
```
2. Also read the full PDF directly to catch nuances the parser might miss
3. Extract and present a structured summary:
   - **Agência/Programa:** Name and type
   - **Objetivo:** What they're funding
   - **Valores:** Min/max per project, total budget
   - **Prazo:** Submission deadline or flow type
   - **Duração:** Project execution period
   - **Eixos/Áreas:** Thematic areas of interest
   - **Critérios de Avaliação:** Scoring criteria with weights
   - **Anexos necessários:** List of required documents
   - **Requisitos de elegibilidade:** Key eligibility requirements
4. Save structured output to `c:\Editais\editais\<slug>\edital-parsed.md`

### Phase 2: ELEGIBILIDADE (Eligibility Check)

Cross-reference edital requirements against `references/empresa-manaca.md`:

For each requirement, assign a traffic light:
- 🟢 **VERDE** — Fully meets requirement
- 🟡 **AMARELO** — Partially meets, action needed
- 🔴 **VERMELHO** — Does not meet, blocker

**Standard checks:**
1. Sede/localização da empresa
2. Tempo mínimo de CNPJ ativo
3. Receita bruta mínima / porte empresarial
4. Regularidade fiscal (CNDs)
5. Requisitos de parceria (ICT/IES)
6. TRL mínimo exigido
7. Área de atuação compatível
8. Pendências anteriores com a agência
9. Formato jurídico (ME, EPP, LTDA, etc.)

Present the eligibility report as a table and highlight **blockers** that need resolution.

Save to `c:\Editais\editais\<slug>\eligibility-report.md`

### Phase 3: SUGESTÃO DE PROJETO (Project Suggestion)

Based on the edital's areas of interest and scoring criteria:

1. Read the scoring criteria weights from Phase 1
2. Analyze which Manacá project best fits:
   - **Flora** — SaaS platform, transformação digital, gestão de impacto
   - **SAÍRA** — IA, visão computacional, cidades inteligentes, resíduos
   - **Novo projeto** — Something new combining Manacá's capabilities
3. Score each candidate against the merit criteria
4. Recommend the best fit with justification
5. Suggest the project angle that maximizes scoring

Save to `c:\Editais\editais\<slug>\project-suggestion.md`

### Phase 4: PLANEJAMENTO DE DOCUMENTOS (Document Planning)

1. Map every required document from the edital
2. For each document, determine:
   - What needs to be written from scratch
   - What can be adapted from past winning documents
   - What requires external action (certidões, signatures, partnerships)
3. Create a **checklist** with every field/section that needs filling
4. Estimate effort for each document
5. Present the plan to the user for approval

### Phase 5: PRODUÇÃO DE DOCUMENTOS (Document Production)

**CRITICAL: Follow the writing guide in `references/guia-redacao-editais.md`**

For each document:

1. **Read the scoring criteria** — Know which criterion each section influences
2. **Write in formal Brazilian Portuguese:**
   - Third person or impersonal constructions
   - No colloquialisms, no hyperbolic adjectives
   - Technical register appropriate for government evaluators
   - Quantify everything: market size, user base, projected revenue, impact metrics
3. **Use Brazilian formats:**
   - Currency: R$ 1.000.000,00
   - Dates: 14 de abril de 2025
   - Percentages: 65%
4. **Structure narrative sections** following the flow:
   - Problema quantificado → Estado da arte (lacuna) → Solução proposta → Metodologia → Viabilidade
5. **For Google Sheets annexes** (budget tables, timeline, team):
   - Use MCP tools: `create_spreadsheet`, `modify_sheet_values`, `format_sheet_range`
6. **For Google Docs** (narrative sections):
   - Use MCP tools: `create_doc`, `batch_update_doc`, `create_table_with_data`
   - Follow patterns from `google-doc-from-template` skill for formatting

**Key writing principles:**
- Map each section to the scoring criterion it influences
- Lead with impact, follow with method
- Reference winning document patterns from `c:\Editais\00. Vencedores\`
- Use Theory of Change framework for impact sections
- Use TRL framework language for technology maturity
- Connect everything back to the edital's stated objectives
- Every budget item must link to a specific Work Package milestone

### Phase 6: REVISÃO DE QUALIDADE (Quality Review)

Self-review all produced documents:

1. **Completude:** Every required field filled? Every annex addressed?
2. **Consistência:** Numbers match across documents? Team names consistent? Dates aligned?
3. **Cálculos financeiros:** Budget totals correct? Percentages add up? Counterpart correctly calculated?
4. **Limites:** Word/character limits respected?
5. **Auto-avaliação:** Score the proposal against each merit criterion (0-10) with justification
6. **Sugestões de melhoria:** Identify weak points and suggest improvements

Present the review to the user. Iterate until approved.

### Phase 7: GUIA DE SUBMISSÃO (Submission Guide)

1. Produce a step-by-step submission guide for the platform (SIGFAPES, SAGe, FAP, etc.)
2. List all files to upload with exact naming conventions
3. Note any external actions still needed:
   - Certidões to obtain/renew
   - Signatures to collect
   - Partnership agreements to sign
   - ICT/IES protocols to formalize
4. Timeline of remaining tasks with deadlines

## Pitfalls and Known Issues

| Pitfall | Mitigation |
|---------|-----------|
| Google Sheets MCP may fail on large batch operations | Break into smaller batches of 20-30 cells |
| PDF parsing may miss tables formatted as images | Always also read PDF directly for verification |
| Company data in references may be outdated | Always ask user to confirm critical data (revenue, certifications) before submitting |
| Edital PDFs may have encoding issues | Use pdfplumber with UTF-8 encoding |
| Budget calculations must be exact | Always double-check with Python calculations, never rely on mental math |
| ICT/IES partnerships often need months to formalize | Flag this as early blocker in eligibility check |

## Important Notes

- **Language:** All proposal documents in formal Portuguese (pt-BR). Internal notes and code in English.
- **Workspace:** Working files go to `c:\Editais\editais\<edital-slug>\`
- **Never assume eligibility** — always verify with the user
- **Never skip the eligibility check** — some requirements are blockers that waste effort if not identified early
- **Reference winning documents** — The ZIP at `c:\Editais\00. Vencedores\` contains 13 documents from 5 winning proposals. Study their patterns.
- **The guia-redacao-editais.md is your bible** — Follow it for every section you write
