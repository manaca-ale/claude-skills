# Edital Agent — Agente de Inscrição em Editais de Inovação

Agente especializado em ajudar a Manacá Tecnologias Sociais a se inscrever em editais de inovação, subvenção econômica e fomento à pesquisa aplicada no Brasil.

## 🔄 Bootstrap — Sincronização com GitHub (EXECUTAR SEMPRE NO INÍCIO)

Esta skill é versionada no monorepo https://github.com/manaca-ale/claude-skills e evolui continuamente. **Toda invocação deve começar verificando se há atualizações remotas.**

> **Arquitetura:** a skill vive na subpasta `edital-agent/` de um monorepo que agrega todas as skills do usuário. O repo git é o **parent** (`~/.claude/skills/` no ambiente do usuário — ajustar conforme SO). Operações git devem rodar a partir da raiz do monorepo, com paths filtrados para `edital-agent/` ao commitar.

### Fluxo obrigatório (auto-pull silencioso)

1. Localizar a raiz do monorepo:

   ```bash
   cd "C:/Users/aleco/.claude/skills"   # raiz do monorepo claude-skills
   # A skill vive em edital-agent/ dentro deste repo.
   ```

2. Validar que é um repositório git do remote correto:

   ```bash
   git remote get-url origin
   # Esperado: https://github.com/manaca-ale/claude-skills.git
   ```

   Se não for repo git, orientar o usuário a inicializar (ver `references/meta-skill-versioning.md` §4). Se o remote divergir, **parar e avisar** — não prosseguir com skill corrompida.

3. Buscar e comparar:

   ```bash
   git fetch origin main --quiet
   LOCAL=$(git rev-parse @)
   REMOTE=$(git rev-parse origin/main)
   BASE=$(git merge-base @ origin/main)
   ```

4. Agir conforme matriz:

   - `LOCAL == REMOTE` → já na última versão, prosseguir silenciosamente.
   - `LOCAL == BASE` (atrás) → `git pull origin main --ff-only --quiet` e logar commits trazidos.
   - `REMOTE == BASE` (à frente) → há commits locais não pushados; **não puxar**, avisar para consolidar antes.
   - Divergente → parar e pedir resolução manual.

5. Checar working tree sujo **dentro de `edital-agent/`**:

   ```bash
   git status --porcelain edital-agent/
   ```

   Se retornar linhas, **avisar usuário** — pode ser trabalho não commitado de execução anterior.

6. Registrar o evento em `edital-agent/.skill-sync.log` (ver `references/meta-skill-versioning.md` §5). Este arquivo está no `.gitignore` de `edital-agent/`.

### Tratamento de falhas
- **Sem rede:** prosseguir com versão local e marcar `status=OFFLINE` no log.
- **Sem remote configurado / não é repo git:** orientar usuário a executar o setup inicial (ver `references/meta-skill-versioning.md` §4).
- **Auth falha (repo privado):** orientar `gh auth login` ou configurar PAT.

### Nunca
- Pular o bootstrap "por rapidez".
- Fazer `git pull` sem `--ff-only` (pode criar merge commits espúrios).
- Rodar bootstrap com working tree sujo sem avisar.

Detalhes completos em `references/meta-skill-versioning.md` §1.

## Trigger

Use this skill when the user:
- Asks to analyze, review, or work on an "edital" (public tender for innovation)
- Wants to prepare a proposal/inscrição for a government funding call
- Asks about eligibility for a specific edital
- Wants to fill out annexes (Google Sheets/Docs) for a tender submission
- Mentions FAPES, FINEP, EMBRAPII, CNPq, FAPs, or similar agencies
- Says "edital", "inscrição", "proposta", "subvenção", "fomento"
- Asks to check, list, or prioritize editais on ClickUp
- Wants to sync edital status or progress with ClickUp
- Asks which editais are most urgent or need attention

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
| `references/clickup-editais.md` | ClickUp workspace IDs, status mapping, integration notes |

### Referências sobre Equipe

- `references/guia-equipe-editais.md` — Guia operacional da seção de equipe (tripé de avaliação, red flags, variantes de formato, fluxo de reescrita).
- `references/matriz-agencias-equipe.md` — Regras específicas de equipe por agência (FINEP, FAPESP, EMBRAPII, FAPs, prêmios, corporativos, internacionais) + 8 gatilhos automáticos de red-flag.
- `templates/equipe/` — 5 templates operacionais (súmula meta-template com 8 variantes, matriz de competências, plano de contratação, ICTs parceiras, exemplos de redação).
- `C:\Editais\Equipe\CVs-Canonicos\` — matéria-prima dos CVs (um arquivo por membro da equipe Manacá).

Also reference `c:\Editais\pesquisas\boas-praticas-editais-inovacao-br.md` for the full Deep Research on Brazilian tender best practices.

> **Referências atualizadas em abril/2026** com dados financeiros (R$567K faturamento, projeções 2030), 14 clientes, ICP/personas Flora, concorrentes, CPSI briefing SAÍRA e depoimentos de clientes. Fonte: `manac-geral`.

> **IMPORTANTE:** Cada arquivo de referência tem um campo `last_verified` no cabeçalho. Na Fase 2 (Elegibilidade), verificar se algum dado está vencido (especialmente certidões e receita). Se `next_review` já passou, avisar o usuário antes de prosseguir.

---

## Duas Trilhas

A skill opera em duas trilhas conforme a complexidade do edital. Determinar a trilha na Fase 1 (Ingestão).

### Trilha A — Prêmio/Award (5-20h)

Formulários online, sumários executivos, pitch videos/decks, PDFs de apoio.

**Fases:** Triagem → Ingestão (com Elegibilidade) → Sugestão de Projeto → Produção → Revisão de Qualidade → Checklist de Submissão

Fase 4 (Planejamento) é opcional. Fase 7 é um checklist simples integrado à revisão.

### Trilha B — Subvenção/Fomento (40-200h)

Anexos narrativos extensos, planilhas orçamentárias, protocolos ICT/IES, pacotes de evidência TRL.

**Fases:** Triagem → Ingestão → Elegibilidade → Sugestão → Planejamento de Documentos → Produção (5 sub-fases) → Revisão de Qualidade → Guia de Submissão → Post-Mortem

Todas as fases são obrigatórias.

### Critérios para classificar

| Indicador | Trilha A | Trilha B |
|-----------|----------|----------|
| Formato de submissão | Formulário online, pitch, PDF curto | Anexos narrativos, planilhas, certificados |
| Valor financeiro | < R$ 100k ou prêmio não-monetário | > R$ 100k subvenção/fomento |
| Duração do projeto | N/A ou < 6 meses | 12-36 meses |
| Exige parceria ICT/IES | Não | Frequentemente sim |
| Orçamento detalhado (rubricas) | Não | Sim, com justificativa SMART |
| Esforço estimado | 5-20h | 40-200h |

---

## Output: Local-First

**Output primário:** Arquivos locais em `c:\Editais\editais\<slug>\` para todo drafting, iteração e referência.
**Output arquival:** Google Docs nativos no Drive criados a partir do conteúdo finalizado (ao fim da Fase 5e ou da Produção).
**Output de submissão:** Formato que a plataforma do edital exige (PDF export, copy-paste em formulário, upload direto).

### Convenção de nomes dos arquivos locais

```
c:\Editais\editais\<slug>\
  STATUS.md                 # Estado atual do edital (obrigatório, atualizar a cada fase)
  00-triage.md              # Fase 0: Triagem
  01-edital-parsed.md       # Fase 1: Ingestão
  02-eligibility.md         # Fase 2: Elegibilidade
  03-project-suggestion.md  # Fase 3: Sugestão de Projeto
  04-document-plan.md       # Fase 4: Planejamento de Documentos (Trilha B)
  05a-data-pack.md          # Fase 5a: Data Assembly
  05b-narrativa-problema.md # Fase 5b: Narrativa Core (um arquivo por seção)
  05b-narrativa-metodologia.md
  05b-narrativa-mercado.md
  05c-equipe.md             # Fase 5c: Seções de Suporte
  05c-cronograma.md
  05c-pi.md
  05d-orcamento.md          # Fase 5d: Orçamento
  05e-documento-final.md    # Fase 5e: Integração + Polish
  06-quality-review.md      # Fase 6: Revisão de Qualidade
  07-submission-guide.md    # Fase 7: Guia de Submissão
  08-post-mortem.md         # Fase 8: Post-Mortem (após resultado)
```

**Regras:**
- Zero arquivos temporários (`tmp_*`, `chunk_*`, `ALL_REMAINING*`)
- Se precisar de rascunhos intermediários, usar sufixo `-draft` (ex: `05b-narrativa-problema-draft.md`) e deletar ao finalizar
- A convenção de nomes torna imediatamente claro em que fase o edital está

### STATUS.md (obrigatório)

Criar no início e atualizar a cada transição de fase:

```markdown
# <Nome do Edital>

- **Fase atual:** 5b (Narrativa Core)
- **Trilha:** B (Subvenção)
- **Prazo:** 21/04/2026 | Dias restantes: 8
- **Bloqueadores:** Nenhum / Parceria ICT não formalizada
- **Última atualização:** 2026-04-13
- **Folder Drive:** [link] (quando criado)
```

---

## Google Drive — Workspace Arquival

Google Docs são criados ao finalizar a produção, não durante o drafting.

| Configuração | Valor |
|-------------|-------|
| Email | `contato@manaca.tech` |
| Pasta raiz "Editais e Prêmios" | `1bABxRYvxG7xoeFKfLVapB1-OLlMNWf5q` |
| Convenção de nomes de pastas | `NN. <Nome do Edital>` (NN sequencial por ano) |

### IDs de pastas de ano (cache)

| Ano | Folder ID |
|-----|-----------|
| 2026 | `1TsyJds0lk_wNuZURZPbaqmptPzNzxDN_` |
| 2025 | `1_QPRKXUX-F02AYb-igjQ4N9wecY_GvKc` |
| 2024 | `1_S6a17DyXKjLnw_cYmmzDYXBH-x7Fai1` |

> Se o ano não estiver na tabela, listar a pasta raiz com `list_drive_items` para encontrar ou criar.

### Padrão para criar e mover Google Docs

`create_doc` não aceita `folder_id`. Sempre criar e depois mover:

```
1. doc = mcp__google-docs__create_doc(user_google_email="contato@manaca.tech", title="...", content="...")
2. mcp__google-docs__update_drive_file(user_google_email="contato@manaca.tech", file_id=<doc_id>, add_parents=<edital_folder_id>, remove_parents="root")
```

### Quando criar no Drive

- **Trilha A:** Após aprovação da revisão de qualidade (Fase 6), criar o(s) documento(s) final(is) no Drive
- **Trilha B:** Após integração (Fase 5e), criar cada documento narrativo, planilha e anexo no Drive
- Sempre apresentar links do Drive ao usuário após cada documento criado

---

## ClickUp Integration (optional)

ClickUp is the source of truth for edital tracking. The Editais list lives at:
`Manacá > Captação de recursos e premiações > Editais` (List ID: `901324801079`)

See `references/clickup-editais.md` for all IDs and status mapping.

### Helper Script

```bash
python scripts/clickup_edital_sync.py list              # List active editais sorted by deadline
python scripts/clickup_edital_sync.py get <task_id>     # Full task details + markdown description
python scripts/clickup_edital_sync.py links <task_id>   # Extract & categorize links and attachments
python scripts/clickup_edital_sync.py status <id> <st>  # Update task status
python scripts/clickup_edital_sync.py comment <id> <tx> # Add UTF-8 safe comment
python scripts/clickup_edital_sync.py create <name> [dd/mm/yyyy]  # Create new edital task
```

### Extracting Links and Attachments

Edital links (Google Docs, Forms, PDFs) are stored in the task's `markdown_description`, NOT in `description` (which is often empty). The `links` command automatically:

1. Fetches the task with `?include_markdown_description=true`
2. Parses all URLs from the markdown content
3. Categorizes them: `google_docs`, `google_forms`, `google_sheets`, `pdfs`, `attachments`, `other`
4. Returns a structured dict for use in Phase 1 (Ingestion)

### ClickUp Status ↔ Edital Phase Mapping

| ClickUp Status | Edital Phase | When to set |
|----------------|-------------|-------------|
| `a fazer` | Pre-triage | Task created, not yet analyzed |
| `claude` | Phases 1-5 | Active production by Claude |
| `em andamento` | Active (human) | Team working manually |
| `revisão` | Phase 6 | Quality review |
| `subir para o drive` | Phase 5e → Drive | Docs ready, archive to Drive |
| `parado` | Blocked | External dependency or pending decision |
| `complete` | Done | Submitted or archived |
| `cancelled` | Cancelled | No-Go or missed deadline |

### When to Sync with ClickUp

| Phase | ClickUp Action |
|-------|---------------|
| Pre-phase (new edital) | `list` to find editais, `links` to extract edital docs |
| Phase 0 (Triage) | Update tags and priority based on Go/No-Go |
| Phase 1 (Ingestion) | `links` to get edital PDF, Google Docs/Forms from task |
| Phase transitions | `status` + `comment` with phase summary |
| Phase 5e (Drive) | Status → `subir para o drive`, comment with Drive folder link |
| Phase 6 (Review) | Status → `revisão` |
| Phase 7 (Submission) | Status → `complete`, comment with submission confirmation |

### Important: UTF-8 Encoding

**ALWAYS use the Python helper script or `requests` library for ClickUp API calls with Portuguese text.** Never use `curl` with inline JSON — it causes mojibake (garbled accents/cedillas) on Windows.

---

## Workflow: Fases

Apresentar resultados após cada fase e aguardar aprovação do usuário antes de prosseguir.

### Fase 0: TRIAGEM (Go/No-Go)

Antes de qualquer trabalho de análise, avaliar se vale a pena investir tempo neste edital.

**Scorecard de Triagem:**

| Dimensão | Peso | Score 1-5 | Justificativa |
|----------|------|-----------|---------------|
| Valor financeiro vs esforço estimado (R$/hora) | 30% | | |
| Probabilidade de ganhar (histórico, fit, concorrência) | 25% | | |
| Alinhamento estratégico (escalar SAÍRA, Flora SaaS, novo mercado) | 20% | | |
| Viabilidade de prazo (dias restantes vs esforço estimado) | 15% | | |
| Timing do desembolso (quando o recurso chega?) | 10% | | |

**Score ponderado = Σ(peso × score) → máximo 5.0**

| Score | Recomendação |
|-------|-------------|
| ≥ 3.5 | **GO** — Prosseguir com prioridade |
| 2.5–3.4 | **CONDICIONAL** — Prosseguir somente se não houver opção melhor |
| < 2.5 | **NO-GO** — Não investir tempo |

**Passo opcional:** Se o edital envolve agência, tipo de programa ou área temática desconhecida, rodar a skill `deep-research-prompt` antes de prosseguir para pesquisar melhores práticas.

### Bloco: Risco de Equipe (novo)

Ao avaliar Go/No-Go, responder:

1. **Há aderência de perfil?** A equipe atual tem alguém com aderência irrefutável ao tema do edital?
   - ✅ Sim → prosseguir.
   - ⚠️ Parcial → sinalizar necessidade de ICT parceira ou contratação.
   - ❌ Não → No-Go provável, salvo se houver plano claro de parceria.

2. **Há risco de CEO Super-Homem?** O perfil do edital vai exigir que a CEO acumule funções que ela não pode assumir com dedicação substancial?
   - Se o edital exige PR com ≥30h/semana em tema técnico e a Manacá não tem quem possa dedicar isso sem interromper operação → avaliar criticamente.

3. **Há restrições de elegibilidade relacionadas à equipe?** Consultar `matriz-agencias-equipe.md`:
   - Sócios podem ser pagos com recursos do fomento? (FINEP: não; FAPESP: sim com regras)
   - Exige PR doutor? (FACEPE BFI, alguns editais acadêmicos)
   - Exige Lattes atualizado de todos os membros? (a maioria das FAPs)

**Peso no scorecard:** tratar "risco-equipe" como um dos 5 critérios top do Go/No-Go (junto a aderência de tema, elegibilidade jurídica, viabilidade de prazo, fit orçamentário).

**Output:** `00-triage.md`

### Fase 1: INGESTÃO (Edital Ingestion)

1. **Setup workspace:**
   - Criar pasta local `c:\Editais\editais\<slug>\`
   - Criar `STATUS.md`
   - (Drive: criar pasta no Drive apenas se decisão GO confirmada — ver seção Google Drive)
2. **Parse PDF:**
   ```bash
   python "C:/Users/aleco/.claude/skills/edital-agent/scripts/parse_edital_pdf.py" "<pdf_path>" "<output_path>"
   ```
3. Também ler o PDF completo diretamente para captar nuances que o parser pode perder
4. Extrair e apresentar resumo estruturado:
   - **Agência/Programa:** Nome e tipo
   - **Objetivo:** O que estão financiando
   - **Valores:** Mín/máx por projeto, orçamento total
   - **Prazo:** Deadline de submissão ou tipo de fluxo
   - **Duração:** Período de execução do projeto
   - **Eixos/Áreas:** Áreas temáticas de interesse
   - **Critérios de Avaliação:** Critérios com pesos
   - **Anexos necessários:** Lista de documentos requeridos
   - **Requisitos de elegibilidade:** Requisitos-chave
5. **Determinar trilha:** Classificar como Trilha A ou B (ver tabela de critérios acima)

**Output:** `01-edital-parsed.md`

### Fase 2: ELEGIBILIDADE (Eligibility Check)

Cross-reference requisitos do edital contra `references/empresa-manaca.md`:

Para cada requisito, atribuir semáforo:
- 🟢 **VERDE** — Atende plenamente
- 🟡 **AMARELO** — Atende parcialmente, ação necessária
- 🔴 **VERMELHO** — Não atende, bloqueador

**Checks padrão:**
1. Sede/localização da empresa
2. Tempo mínimo de CNPJ ativo
3. Receita bruta mínima / porte empresarial
4. Regularidade fiscal (CNDs) — **calcular se certidões expiram antes da data de contratação**
5. Requisitos de parceria (ICT/IES)
6. TRL mínimo exigido
7. Área de atuação compatível
8. Pendências anteriores com a agência
9. Formato jurídico (ME, EPP, LTDA, etc.)

**Verificação de dados de referência:** Checar `last_verified` e `next_review` de cada arquivo de referência usado. Se algum campo relevante está vencido, avisar o usuário antes de concluir a elegibilidade.

Apresentar como tabela e destacar **bloqueadores** que precisam de resolução.

> **Trilha A:** Fases 1 e 2 podem ser combinadas em um único output se o edital for simples.

### Restrições de Equipe (derivadas da agência)

_Consultar `matriz-agencias-equipe.md` e copiar a coluna da agência identificada para cá._

#### Agência identificada: {FINEP | FAPESP | EMBRAPII | FAP estadual | Prêmio | Corporativo | Aceleradora | Internacional | Outro}

#### Regras aplicáveis:

- **Padrão documental exigido:** {Súmula FAPESP | CV livre FINEP | Lattes | Mini-bio | CV corporativo | CV internacional}
- **Regra de sócios:** {pró-labore permitido? contrapartida obrigatória? bolsa?}
- **Limite de terceiros/ICT:** {% permitido | rubrica correta}
- **Dedicação mínima típica do PR:** {Xh/semana}
- **Documentação obrigatória de parceiros:** {ACT, Carta de Anuência institucional, Carta individual, etc.}

#### Gatilhos de red-flag para esta agência:

{Listar os 4-5 triggers específicos da coluna da matriz}

#### Compatibilidade com a Manacá:

- Podemos atender ao padrão documental? ✅/⚠️/❌
- Podemos respeitar regra de sócios? ✅/⚠️/❌
- Temos equipe que atinge dedicação mínima? ✅/⚠️/❌
- Temos ICT parceira pronta (se necessária)? ✅/⚠️/❌ — se não, qual o plano?

**Output:** `02-eligibility.md`

### Fase 3: SUGESTÃO DE PROJETO (Project Suggestion)

Com base nas áreas de interesse e critérios de avaliação do edital:

1. Ler os pesos dos critérios da Fase 1
2. Analisar qual projeto da Manacá melhor se encaixa:
   - **Flora** — SaaS platform, transformação digital, gestão de impacto
   - **SAÍRA** — IA, visão computacional, cidades inteligentes, resíduos
   - **Novo projeto** — Algo novo combinando capacidades da Manacá
3. Pontuar cada candidato contra os critérios de mérito (tabela com pesos)
4. Recomendar o melhor fit com justificativa
5. Sugerir o ângulo do projeto que maximiza pontuação

### Configuração de Equipe Proposta

_Antes de detalhar o projeto, definir a configuração de papéis que o edital e a agência demandam._

#### Equipe Perfeita para Este Edital (perfil ideal)

| Papel necessário | Perfil ideal | Dedicação ideal |
|---|---|---|
| {PR / Coordenador} | {Doutor em X com N publicações no tema} | {X}h/sem |
| {CTO / Líder Técnico} | {Engenheiro com 10+ anos em Y} | {X}h/sem |
| {Pesquisador Júnior} | {Mestre em Z} | {X}h/sem |
| {Designer / UX} | {Senior com experiência em W} | {X}h/sem |

#### Mapeamento contra Equipe Real da Manacá

| Papel | Quem ocupa | Gap | Estratégia |
|---|---|---|---|
| {Papel 1} | {Pessoa da Manacá} | Nenhum / {descrever} | — / {redação compensatória / ICT / contratação / bolsa} |

#### Papéis a Preencher Via:

- **Contratação futura (Pessoal e Encargos):** {listar} — detalhar em `templates/equipe/plano-contratacao-futura.md` na fase 05c.2.
- **ICT parceira (Serviços de Terceiros):** {listar} — detalhar em `templates/equipe/icts-parceiras.md` na fase 05c.2.
- **Bolsa (TT / PIBIC / outra):** {listar se aplicável}.

#### Organograma Proposto

```
                  {PR / Coordenador Geral}
                           |
        +------------------+------------------+
        |                  |                  |
   {Líder Técnico}   {Líder Metodologia}   {Líder Comercial/Articulação}
        |                  |                  |
   {Equipe Tech}    {Equipe Impacto}    {Parceiros Externos}
        |
   {ICT Parceira — periferia}
```

**Output:** `03-project-suggestion.md`

### Fase 4: PLANEJAMENTO DE DOCUMENTOS (Document Planning) — Trilha B obrigatória

**Esta fase é obrigatória na Trilha B. Não prosseguir para Produção sem aprovação deste plano.**

**Template obrigatório:**

```markdown
# Document Plan — <Nome do Edital>

## Trilha: B | Esforço estimado: [X]h | Prazo: [data] | Dias restantes: [N]

### Matriz de Documentos

| # | Documento/Campo | Fonte | Status | Responsável | Horas Est. | Prioridade |
|---|----------------|-------|--------|------------|-----------|-----------|
| 1 | Sumário Executivo | Escrever do zero | Não iniciado | Claude | 3h | P1 |
| 2 | Dados empresa (Seção 2) | Copiar de empresa-manaca.md | Não iniciado | Claude | 0.5h | P2 |
| 3 | Proposta Técnica | Escrever do zero, ref vencedores | Não iniciado | Claude | 8h | P1 |
| 4 | Orçamento (Planilha) | Calcular baseado em WPs | Não iniciado | Claude | 3h | P1 |
| 5 | Protocolo ICT | Ação externa requerida | BLOQUEADO | Rayssa | N/A | P0 |
| 6 | Certidões | Verificar validade | A confirmar | User | 0.5h | P0 |

### Dependências Externas (bloqueadores)

- [ ] Parceria ICT/IES — Responsável: [nome], Prazo: [data]
- [ ] Renovação de certidões — Responsável: contabilidade, Prazo: [data]
- [ ] Assinaturas necessárias — Responsável: [nome], Prazo: [data]

### Sequência de Produção

1. **5a. Data Assembly** — [X]h — Campos mecânicos, dados empresa, CVs
2. **5b. Narrativa Core** — [X]h — Problema → Metodologia → Mercado
3. **5c. Seções de Suporte** — [X]h — Equipe, cronograma, PI
4. **5d. Orçamento** — [X]h — Depende de 5b (WPs definidos)
5. **5e. Integração** — [X]h — Montagem final, cross-check
```

**Output:** `04-document-plan.md`

### Fase 5: PRODUÇÃO DE DOCUMENTOS (Document Production)

**CRITICAL: Seguir o guia de redação em `references/guia-redacao-editais.md`**

#### Regras gerais (ambas trilhas)

1. **Ler os critérios de pontuação** — Saber qual critério cada seção influencia
2. **Escrever em português brasileiro formal:**
   - Terceira pessoa ou construções impessoais
   - Sem coloquialismos, sem adjetivos hiperbólicos
   - Registro técnico apropriado para avaliadores governamentais
   - Quantificar tudo: tamanho de mercado, base de usuários, receita projetada, métricas de impacto
3. **Usar formatos brasileiros:**
   - Moeda: R$ 1.000.000,00
   - Datas: 14 de abril de 2025
   - Percentuais: 65%
4. **Estrutura narrativa:** Problema quantificado → Estado da arte (lacuna) → Solução proposta → Metodologia → Viabilidade
5. **Referenciar propostas vencedoras** de `c:\Editais\00. Vencedores\` como padrão de escrita

#### Trilha A — Produção direta

Escrever os documentos/respostas diretamente conforme o formato do edital (formulário, sumário executivo, pitch deck). Manter cada resposta dentro dos limites de caracteres/palavras.

#### Trilha B — 5 Sub-fases

##### 5a. Data Assembly (2-3h)

Preencher todos os campos factuais/mecânicos:
- Dados da empresa (CNPJ, sede, porte, receita, sócios)
- CVs narrativos da equipe (3-5 linhas por membro, conectando formação ao desafio do projeto)
- Histórico financeiro e de financiamentos
- Certidões e documentos legais

**Ação crítica:** Flaggar todo `[PREENCHER]` e `[CONFIRMAR]` encontrado nos arquivos de referência. Apresentar lista ao usuário para resolução ANTES de continuar.

**Output:** `05a-data-pack.md`

##### 5b. Narrativa Core (10-20h)

Escrever na ordem de maior peso na avaliação:
1. **Problema + Estado da Arte** (15% do espaço) — Dados quantificados com fontes (IBGE, IPEA, ABRELPE)
2. **Metodologia + Superação do risco tecnológico** (40% do espaço) — Arquitetura, algoritmos, frameworks, testes, métricas
3. **Mercado + Impacto ESG/ODS** (25% do espaço) — TAM/SAM/SOM, modelo de receita, Teoria da Mudança, SROI

Para cada seção, anotar explicitamente: "Esta seção endereça o critério [X] (peso [Y]%)."

> Nota: em Trilha B, a seção de equipe **não** deve ser tratada como anexo menor. Ela é o documento fiduciário da inovação — o avaliador está medindo risco de execução. Reservar tempo proporcional ao peso atribuído à equipe no edital (tipicamente 15-25% da nota).

**Output:** `05b-narrativa-problema.md`, `05b-narrativa-metodologia.md`, `05b-narrativa-mercado.md`

##### 5c. Seções de Suporte (5-10h)

- **Equipe:** Tríade obrigatória (científico + mercado + gestão). CVs narrativos, não Lattes bruto.
- **Cronograma:** Work Packages (WP1-WP4 típico para 24 meses), Gantt com caminho crítico, buffer entre WPs
- **Propriedade Intelectual:** Modelo de partilha (cotitularidade ou cessão com reversão)
- **Contrapartidas:** Financeira e/ou econômica, demonstrar com balanço patrimonial

#### 05c — Seção de Equipe (nova sub-divisão)

**Sub-fase 05c.1 — Team Fit Analysis** (`05c1-team-fit.md`):
- Consolidar o mapeamento de "equipe perfeita × equipe real" da Fase 03.
- Registrar gaps e estratégias definidas.
- Output: tabela clara de quem cobre o quê e o que falta.

**Sub-fase 05c.2 — CV Rewrite + Artefatos de Equipe** (pasta `05c2-artefatos-equipe/`):
- `cvs-customizados/<nome>.md` — um CV por membro, reescrito customizado para este edital usando o CV canônico em `Equipe/CVs-Canonicos/` como matéria-prima e a variante de formato definida em 04.
- `matriz-competencias.md` — preenchido a partir do template.
- `plano-contratacao-futura.md` — se houver vagas (Trilha B).
- `icts-parceiras.md` — se houver parceria.
- `narrativa-equipe.md` — a redação final que vai para a proposta, usando 3-5 exemplos de `exemplos-redacao-equipe.md` como base estilística.

**Variante de formato a aplicar:** derivada de `matriz-agencias-equipe.md` (consultar a linha "Variante de formato a usar" da coluna da agência).

**Output:** `05c-equipe.md`, `05c-cronograma.md`, `05c-pi.md`

##### 5d. Orçamento (3-5h)

**Depende de 5b** (WPs precisam estar definidos para vincular rubricas).

- Método SMART para cada rubrica (Specific, Measurable, Achievable, Relevant, Time-bound)
- Cálculos em Python, nunca matemática mental
- Verificar gatilhos de glosa: core dev terceirizado, equipamento em custeio, valores redondos, teto máximo sem granularidade

**Para Google Sheets:** Criar via `create_spreadsheet` → mover com `update_drive_file(add_parents=edital_folder_id, remove_parents="root")` → popular com `modify_sheet_values` + `format_sheet_range`. Quebrar em batches de 20-30 células.

**Output:** `05d-orcamento.md` (e planilha no Drive quando finalizado)

##### 5e. Integração + Polish (2-3h)

- Montar documento final consolidado
- Checar referências cruzadas: nomes da equipe no orçamento vs. seção equipe, datas no cronograma vs. milestones dos WPs, valores totais consistentes
- Verificar limites de palavras/caracteres
- Aplicar formatação para escaneabilidade (negrito em KPIs, tabelas comparativas, listas numeradas)

**Output:** `05e-documento-final.md`

**Após aprovação do usuário:** Criar Google Docs no Drive a partir do conteúdo final (ver seção Google Drive).

### Fase 6: REVISÃO DE QUALIDADE (Quality Review)

Auto-revisar todos os documentos produzidos com **dois passes:**

#### Pass 1 — Advocate (pontuação otimista)

1. **Completude:** Todo campo obrigatório preenchido? Todo anexo endereçado?
2. **Consistência:** Números batem entre documentos? Nomes consistentes? Datas alinhadas?
3. **Cálculos financeiros:** Totais corretos? Percentuais somam? Contrapartida calculada?
4. **Limites:** Limites de palavras/caracteres respeitados?
5. **Auto-avaliação:** Pontuar a proposta em cada critério de mérito (0-10) com justificativa

#### Pass 2 — Red Team (avaliador cético)

Pontuar como um avaliador que leu 50 propostas naquele dia e está cansado:

Para cada critério:
1. Escrever a **objeção mais forte** que um avaliador faria
2. Verificar se a proposta endereça adequadamente essa objeção
3. Dar nota considerando que o avaliador NÃO dará benefício da dúvida

#### Resultado

| Critério | Nota Advocate | Nota Red Team | Δ (confiança) | Objeção principal |
|----------|:------------:|:-------------:|:-----------:|-------------------|
| ... | | | | |
| **TOTAL** | /100 | /100 | | |

- **Δ < 10:** Alta confiança — proposta é sólida
- **Δ 10-20:** Média confiança — pontos a fortalecer
- **Δ > 20:** Baixa confiança — seções frágeis que precisam de reescrita

#### Calibração contra propostas vencedoras

Comparar explicitamente contra documentos em `c:\Editais\00. Vencedores\`:
- Contagem de palavras/chars por seção vs. templates vencedores
- Estrutura narrativa vs. propostas que ganharam em editais similares
- Densidade de quantificação (números por parágrafo)

Sugerir melhorias e iterar com o usuário até aprovação.

#### Checklist de Equipe (obrigatório — bloqueador se houver "Não")

Rodar antes de avançar para a Fase 07.

| # | Pergunta | Sim / Não / N/A | Ação se "Não" |
|---|---|---|---|
| 1 | **Integridade da Liderança:** há um (e apenas um) Coordenador/PR claramente designado com aderência irrefutável ao tema? | | Redefinir liderança ou articular ICT com PR adequado. |
| 2 | **Coerência de Dedicação:** somatório de horas bate com cronograma? Sem dedicações simbólicas? | | Revisar alocações; considerar contratação ou bolsa. |
| 3 | **Vínculos Fiscais:** sócios distintos de funcionários e terceiros, respeitando regras da agência sobre pró-labore? | | Reclassificar rubricas; consultar matriz-agencias. |
| 4 | **Blindagem do Core:** texto deixa explícito que engenharia central fica interna? | | Reescrever para afirmar internalização e limitar ICT à periferia. |
| 5 | **Sanidade Documental:** Lattes ≤6 meses de todos? Links funcionando? CVs respeitam limite de páginas? | | Atualizar Lattes antes da submissão. |
| 6 | **Avaliação Jurídica de Terceiros:** ICTs com ACT + Carta de Anuência Institucional + Carta Individual? | | Solicitar/assinar docs antes da submissão. |
| 7 | **Rastreabilidade da Sinergia:** governança e cadência descritas (daily, sprint, mensal)? | | Adicionar parágrafo de governança. |
| 8 | **Reescrita Sob Medida:** cada CV destaca o que ESTE edital mais valoriza? Tom correto (acadêmico/industrial/corporativo/internacional)? | | Rodar 05c.2 CV Rewrite novamente. |

#### Gatilhos Automáticos (R1-R8) — rodar contra a proposta

Cada gatilho de `matriz-agencias-equipe.md` (R1-R8) deve ser verificado:

- R1 Risco CEO Super-Homem
- R2 Risco de Terceirização do Core
- R3 Risco de Desenquadramento Documental
- R4 Risco Jurídico de Terceiros
- R5 Risco de Inexequibilidade
- R6 Risco de Equipe Inflada
- R7 Gap de perfil exigido
- R8 Risco de CV Genérico

Cada gatilho acionado → bloqueador ou mitigação explícita antes de prosseguir.

**Output:** `06-quality-review.md`

### Fase 7: GUIA DE SUBMISSÃO (Submission Guide)

**Template obrigatório:**

```markdown
# Guia de Submissão — <Nome do Edital>

## Plataforma
- **Nome:** [SIGFAPES / SAGe / JotForm / Portal próprio]
- **URL:** [link]
- **Login:** [email da conta]

## Arquivos para Upload

| # | Documento | Nome do arquivo | Formato | Tamanho máx | Status |
|---|----------|----------------|---------|-------------|--------|
| 1 | Proposta técnica | proposta-tecnica-manaca.pdf | PDF | 10MB | Pronto |
| 2 | Planilha orçamentária | orcamento-manaca.xlsx | XLSX | 5MB | Pronto |
| 3 | Vídeo pitch | [link YouTube] | URL | 2 min | Pendente |

## Passos de Submissão
1. Acessar [plataforma] com login [email]
2. Selecionar [categoria/programa]
3. Preencher campos do formulário: [lista de campos]
4. Upload dos arquivos na ordem acima
5. Revisar preview antes de submeter
6. Submeter e salvar comprovante

## Ações Externas Pendentes

| # | Ação | Responsável | Prazo | Status |
|---|------|------------|-------|--------|
| 1 | Gravar vídeo pitch | Rayssa | [data] | Pendente |
| 2 | Assinar protocolo ICT | Rayssa + NIT | [data] | Pendente |

## Checklist Pré-Submissão

- [ ] Todos os arquivos nos formatos corretos
- [ ] CNDs válidas na data de submissão E contratação
- [ ] Valores no orçamento batem com o corpo da proposta
- [ ] Nomes da equipe consistentes em todos os documentos
- [ ] Limite de caracteres/páginas respeitado em cada seção
- [ ] Comprovante de submissão salvo

### Anexos de Equipe (obrigatórios antes de submeter)

- [ ] CVs / Súmulas de todos os membros cadastrados (no formato da agência)
- [ ] PDFs de Lattes atualizados (FAPs estaduais + FAPESP)
- [ ] ACT assinado com cada ICT parceira (ou minuta pré-acordada com previsão de assinatura)
- [ ] Carta de Anuência Institucional de cada ICT
- [ ] Carta de Anuência Individual de cada pesquisador externo
- [ ] Declaração de não-alienação de PI (quando exigida)
- [ ] Comprovante de credenciamento da ICT (quando aplicável — Unidade EMBRAPII, ISO, etc.)
- [ ] Atestados de Capacidade Técnica relevantes (ex: Instituto Arco da Rafaela)
- [ ] Termo de Dedicação (quando a agência exigir formalização de horas)
```

**Output:** `07-submission-guide.md`

### Fase 8: POST-MORTEM (após resultado)

Executar quando o resultado do edital for divulgado:

1. **Registrar resultado:** Ganhou / Perdeu / Lista de espera / Desistiu
2. **Se disponível:** Registrar nota obtida e feedback dos avaliadores
3. **Comparar:** Auto-avaliação da Fase 6 (advocate + red team) vs. resultado real
   - Se ganhou com red team > 70: boa calibração
   - Se perdeu com advocate > 80: calibração otimista demais → ajustar
4. **Analisar:** O que propostas vencedoras fizeram diferente (se visível)
5. **Atualizar:**
   - `references/guia-redacao-editais.md` com lições aprendidas
   - Arquivos de referência com dados novos gerados durante a proposta
   - `references/historico-financiamentos.md` com resultado
6. **Arquivar:**
   - Propostas vencedoras → `c:\Editais\00. Vencedores\`
   - Análises de resultados → `c:\Editais\99. Análises Pós-Resultado\`

### Aprendizados sobre Equipe

- O avaliador fez algum comentário sobre a seção de equipe? Qual?
- Algum gatilho de red-flag (R1-R8) se manifestou na avaliação?
- A variante de formato de CV escolhida foi a certa?
- Algum CV deveria ter destacado algo diferente?
- Houve algum gap de perfil não previsto? Vale contratar/formar para o próximo edital?
- Algum novo contato de ICT ou consultor que deve entrar na base? Registrar em `icts-parceiras.md` → Bloco 7.
- Atualizar os CVs canônicos em `Equipe/CVs-Canonicos/` com novas entregas/prêmios/contratos deste ciclo.

**Output:** `08-post-mortem.md`

## 🔁 Consolidação Final — Push de Aprendizados (EXECUTAR SEMPRE NO FIM)

Após concluir a Fase 08 (ou ao encerrar a skill por qualquer motivo), propagar aprendizados para o GitHub. Isso garante que o próximo edital se beneficie do que foi descoberto neste.

> **Arquitetura:** o repo git é o monorepo `~/.claude/skills/`. Esta skill ocupa a subpasta `edital-agent/`. Todos os `git add` precisam usar paths com prefixo `edital-agent/` para evitar promover acidentalmente mudanças de outras skills.

### Critério: o que entra e o que NÃO entra

**ENTRA (promover ao repo da skill):**
- Gotchas universais novos
- Templates melhorados aplicáveis a >1 agência
- Dados da empresa atualizados (após confirmar com usuário)
- Novos exemplos de redação parafraseáveis (anonimizados)
- Novos gatilhos R# descobertos
- Correções de erro
- Novas variantes de formato
- CVs canônicos atualizados com novas credenciais

**NÃO ENTRA (fica em `c:\Editais\editais\<slug>\`):**
- Conteúdo específico de um edital
- Dados sensíveis de clientes
- Rascunhos incompletos
- PDFs originais de editais

### Fluxo obrigatório

1. Detectar modificações **apenas na subpasta da skill**:

   ```bash
   cd "C:/Users/aleco/.claude/skills"   # raiz do monorepo
   git status --porcelain edital-agent/
   ```

2. Se vazio → nada a fazer; encerrar.

3. Se há modificações → categorizar e escrever **uma mensagem de commit estruturada**:

   ```
   <tipo>(<escopo>): <resumo ≤50 chars>

   Aprendizados do edital <slug> (Trilha <A|B>):
   - <bullet 1>
   - <bullet 2>

   🤖 Captured during edital-agent run
   ```

   Tipos: `feat`, `fix`, `docs`, `refactor`, `learning`, `chore`.
   Escopos: `references`, `templates`, `cv-canonico`, `skill-md`, `guia`.

4. Commitar e pushar diretamente em `main` **com paths dentro de `edital-agent/`**:

   ```bash
   # NUNCA usar `git add -A` cego — afetaria outras skills do monorepo.
   git add edital-agent/<path1> edital-agent/<path2>
   git commit -m "$(cat <<'EOF'
   <mensagem>
   EOF
   )"
   git push origin main
   ```

5. Registrar no `08-post-mortem.md` do edital:

   ```markdown
   ## Aprendizados promovidos à skill
   - **Commit:** <hash curto> — <link do commit no GitHub>
   - **Arquivos alterados:** <lista>
   - **Categoria:** <tipo>(<escopo>)
   - **Síntese:** <1 parágrafo>
   ```

### Regras de higiene absolutas

- **Sempre** `git add` com paths específicos, todos com prefixo `edital-agent/` — nunca cego.
- **Nunca** pushar `.env`, tokens, credenciais; se aparecer no diff, abortar.
- **Nunca** amendar commits já pushados.
- **Nunca** forçar push em `main` (`--force`).
- **Nunca** fazer `git reset --hard` em commits já enviados.
- **Nunca** stagear arquivos fora de `edital-agent/` a menos que o usuário autorize explicitamente (afeta outras skills).

### Tratamento de falhas
- **Push falha (rede/auth):** commit fica local; logar `PENDING_PUSH`. Bootstrap seguinte detecta.
- **Pre-commit hook falha:** corrigir e criar NOVO commit.
- **Conflito no push:** `git pull --rebase origin main` e push novamente.

Detalhes completos em `references/meta-skill-versioning.md` §2.

---

## Pitfalls and Known Issues

| Pitfall | Mitigation |
|---------|-----------|
| Google Sheets MCP may fail on large batch operations | Break into smaller batches of 20-30 cells |
| PDF parsing may miss tables formatted as images | Always also read PDF directly for verification |
| Company data in references may be outdated | Check `last_verified` dates; ask user to confirm critical data before submitting |
| Edital PDFs may have encoding issues | Use pdfplumber with UTF-8 encoding |
| Budget calculations must be exact | Always double-check with Python calculations, never rely on mental math |
| ICT/IES partnerships often need months to formalize | Flag as early blocker in eligibility check and triage scorecard |
| `create_doc` não aceita `folder_id` | Criar doc → mover com `update_drive_file(add_parents=<folder_id>, remove_parents="root")` |
| Numeração sequencial de pastas no Drive | Listar pasta do ano, contar itens existentes, incrementar NN |
| Google Doc perde formatação markdown | Usar `batch_update_doc` para aplicar negrito, headings e tabelas programaticamente |
| Doc criado fica no "Meu Drive" antes de mover | Sempre executar o `update_drive_file` imediatamente após o `create_doc` |
| Certidões têm validade de ~180 dias | Calcular expiração na Fase 2 e verificar se são válidas na data de contratação |
| Auto-avaliação tende a ser generosa | Usar dois passes (advocate + red team) na Fase 6 |
| Fase 5 gera arquivos temporários bagunçados | Seguir convenção de nomes rigorosa, zero `tmp_*` ou `chunk_*` |

## Princípios Operacionais — Equipe

- Tratar a seção de equipe como documento fiduciário (não como anexo burocrático).
- Sempre consultar `matriz-agencias-equipe.md` antes de definir formato de CV.
- Sempre usar `Equipe/CVs-Canonicos/` como matéria-prima — nunca começar do zero.
- Reescrita customizada em toda proposta nova (regra 05c.2) — CVs genéricos são red-flag.
- Rodar o Checklist de 8 Perguntas na Fase 06, sem exceção.
- Bloquear submissão se qualquer gatilho R1-R8 estiver ativo e não mitigado.
- Não inventar credenciais — só iluminar o que existe.
- Atualizar CVs canônicos após cada edital (Fase 08) como parte do post-mortem.

## Important Notes

- **Output primário:** Arquivos locais em `c:\Editais\editais\<slug>\` com convenção de nomes
- **Output arquival:** Google Docs nativos no Drive (pasta `Editais e Prêmios > <ano> > NN. <nome>`) criados ao finalizar produção
- **Nunca criar .md no Drive** — documentos editáveis no Drive devem ser Google Docs nativos
- **Language:** All proposal documents in formal Portuguese (pt-BR). Internal notes and code in English.
- **Never assume eligibility** — always verify with the user
- **Never skip the eligibility check** — some requirements are blockers that waste effort if not identified early
- **Reference winning documents** — The folder `c:\Editais\00. Vencedores\` contains 13 documents from 5 winning proposals. Study their patterns.
- **The guia-redacao-editais.md is your bible** — Follow it for every section you write
- **Sempre apresentar links do Drive** ao usuário após criar cada documento no Drive
- **STATUS.md é obrigatório** — Atualizar a cada transição de fase
- **Trilha A vs B** — Determinar na Fase 1, ajustar pipeline accordingly
- **Zero arquivos temporários** — Seguir convenção de nomes, deletar rascunhos ao finalizar
