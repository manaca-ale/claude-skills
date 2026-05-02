---
name: llm-enrich
description: LLM Enrichment — Enriquecimento + Scoring de Leads via Claude Code
---

# LLM Enrichment — Enriquecimento + Scoring de Leads via Claude Code

Enriquece e scora leads do pipeline LeadsScraping usando WebSearch + WebFetch + training knowledge.
Substitui o Gemini scorer com custo zero de API.

Working directory: `C:\Manabot\LeadsScraping`

## Modo de gravacao (LOCAL vs PRODUCAO)

O helper `enrichers/llm_enrichment_helper.py` e o `scripts/hunter_fill.py` leem a env `LEADS_API_URL`:

- **Modo PROD** (default no `.env` da maquina do Alexandre): `LEADS_API_URL=https://leads-api.manaca.tech` -> os comandos `--action pending|save|stats` falam HTTP com a API de producao no manaserver. Hunter `/enrichment/email` tambem cai em prod. **Eh isso que voce quer 99% das vezes** -- garante que o trabalho de enriquecimento vai pro DB compartilhado.
- **Modo LOCAL** (LEADS_API_URL vazio/comentado): SQL direto em `data/leads.db`. So util para experimentar sem afetar prod.

Antes de comecar uma sessao, confirme em qual modo voce esta:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('mode:', 'REMOTE -> '+os.getenv('LEADS_API_URL') if os.getenv('LEADS_API_URL') else 'LOCAL')"
```

## Budget Hunter.io

Usado como fallback de email para leads alto-fit. Free tier: **50 searches + 100 verifications/mes** (reset dia 29).
Verifique o saldo no inicio da sessao se for processar mais que 5 leads:

```bash
python -c "from enrichers.hunter_enricher import HunterClient; from dotenv import load_dotenv; load_dotenv(); a = HunterClient().account(); s = (a or {}).get('requests', {}).get('searches', {}); print(f\"searches: used={s.get('used')} avail={s.get('available')}\")"
```

Se restarem menos de 10 searches, considere processar so leads de alta probabilidade de fit ate o reset.

## Subcommands

- `/llm-enrich` or `/llm-enrich run` — Enrich and score pending leads
- `/llm-enrich status` — Show enrichment dashboard
- `/llm-enrich rescore <filter>` — Re-score already scored leads

ARGUMENTS: $ARGUMENTS

## /llm-enrich status

Run this command and display the results in a formatted table:

```bash
cd /c/Manabot/LeadsScraping && python enrichers/llm_enrichment_helper.py --action stats
```

## /llm-enrich rescore

Same flow as `run` below, but query leads that already have `scored_at IS NOT NULL`. Use the filter from ARGUMENTS to narrow (e.g., `--source salic`, a CNPJ, or `--limit N`).

## /llm-enrich run

### Step 1: Get Pending Leads

```bash
cd /c/Manabot/LeadsScraping && python enrichers/llm_enrichment_helper.py --action pending --limit 5
```

If ARGUMENTS contains `--source X`, `--limit N`, or other filters, pass them through.
Parse the JSON output. Each lead has: `source`, `source_id`, `org_name`, `cnpj`, `company_activity`, `company_city`, `company_state`, `description`, `approved_value`, `approval_date`, `program_name`, `company_website`, `company_email`, `company_linkedin`, `company_instagram`, `source_extras`.

If no pending leads, report "Nenhum lead pendente para enriquecimento." and stop.

### Step 2: For Each Lead — Research + Enrich + Score

#### REGRAS CRITICAS (leia antes de comecar)

**1. Salvamento incremental obrigatorio**

Processe UM lead por vez nesta ordem estrita:
  a) Buscar 1 lead pendente (`--action pending --limit 1`)
  b) Pesquisar (WebSearch x3 + WebFetch se houver site)
  c) Classificar 13 campos + scorar contra 3 ICPs
  d) **SALVAR esse lead AGORA** via `--action save --data '{...}'`
  e) Step 3b: Hunter upgrade se aplicavel
  f) Soh DEPOIS de salvar e fazer o Hunter, pegar o proximo lead

**NUNCA** acumule dados de multiplos leads para salvar no fim. Se a sessao estourar
no lead 3, os leads 1 e 2 precisam estar persistidos. Em modo REMOTE
(LEADS_API_URL setada), cada save vai direto pra producao -- mais critico ainda
nao perder o que ja foi pesquisado.

**2. NUNCA pular um lead**

Mesmo quando a pesquisa web nao trouxer nada util (org pequena, sem site, sem
LinkedIn), voce DEVE:
  - Usar os dados do DB (CNAE, descricao, source_extras com ODS/temas/estagio)
  - Combinar com seu training knowledge para classificar
  - Marcar `"needs_review": true` no payload
  - Salvar mesmo assim com os campos que conseguiu inferir
  - **Seguir para o proximo lead**

NAO use a estrategia "vou pular este e tentar de novo amanha". Sempre salve
algum resultado. Pendentes soh voltam aa fila se voce nao chamar `--action save`
(o helper marca `llm_enriched_at` no save).

**3. Defesa contra estouro de contexto**

Cada lead consome ~5-7 tool calls. 5 leads ≈ 30 tool calls + analise.

  - Se um WebFetch retornar conteudo muito grande (>20KB), **extraia soh o
    necessario** (email de contato, nome do decisor + cargo, missao em 1-2
    frases) e DESCARTE o resto. Nao cite literalmente o HTML.
  - Se voce notar que esta em ~70% do limite de contexto antes de processar
    o ultimo lead, **TERMINE o lead atual** (salve + Hunter), depois reporte
    quantos foram processados e PARE. A proxima execucao pega o resto
    naturalmente da fila.
  - Prefira sempre **salvar o lead em andamento** antes de qualquer outra
    coisa quando contexto estiver enchendo.

**4. Email eh obrigatorio para fits (Hunter NAO eh primeira opcao)**

Se o lead tem chance >50% de virar fit (impacto mensuravel + porte minimo +
estagio operacional), voce DEVE tentar achar email ANTES de chamar
`--action save`. Ordem rigida:

  a) **WebFetch do site institucional**: home + `/contato` ou `/contact`
  b) **WebSearch** `"{org_name}" "@{dominio}" contato` -- noticias, press
     releases, Crunchbase/RocketReach surfacam emails em snippets
  c) **WebSearch** `"{founder_name}" email "{org_name}"` -- founder-led
     orgs frequentemente tem email em entrevistas/diretorios
  d) **Pattern fallback** `contato@{dominio}` se MX existe (basta ter
     dominio real)
  e) **Sem dominio** (LinkedIn/Insta only): deixe `company_email` vazio,
     anote em `scoring_reasoning` "outbound via LinkedIn DM". Nao fabrique.

**NAO pule pro Hunter sem fazer (a)-(c).** Hunter eh fallback PAGO
(50 searches/mes), nao primeira opcao. Erro classico observado:
"vou deixar Hunter resolver" -> Hunter nao acha -> lead fit fica sem email
e sai gerada quota a toa.

Apos save, o Step 3b (Hunter upgrade) cuida do upgrade se
`score >= 70 AND fit_for_manaca = true AND` email ainda eh generico
(`contato@/info@/faleconosco@`). Esse passo eh automatico e idempotente --
nao chame manualmente.

---

Process leads one at a time. For each lead:

#### 2a. Web Research

Execute these searches (adapt query based on available data):

1. **WebSearch**: `"{org_name}" {company_city}` — Find official site, news, institutional info
2. **WebSearch**: `"{org_name}" site:linkedin.com/company` — Find LinkedIn company page
3. **WebSearch**: `"{org_name}" site:instagram.com` — Find Instagram profile

If the first search finds a website URL, **WebFetch** it to extract:
- Contact emails (look for "contato", "fale conosco", mailto: links)
- **Decision-maker name and title** (look for "equipe", "diretoria", "lideranca", "quem somos") — extract the SPECIFIC PERSON whose title matches the ICP guidance for `decision_maker_titles`. Save as `contact_person_name` + `contact_person_title`.
- Mission/about text (look for "sobre", "missão", "quem somos")
- Technology hints (platform indicators, integrations mentioned)

Also try a targeted LinkedIn search for the decision-maker:
`WebSearch: "{org_name}" site:linkedin.com/in/ "{titulo do ICP}"` — e.g.
`"Instituto Vida" site:linkedin.com/in/ "Diretora Executiva"`

**MANDATORY: Email lookup for fit candidates.** If you suspect the lead will end with `fit=true` (impacto mensuravel + porte minimo), you MUST attempt to recover an email before saving. Do NOT skip this step to save context — outbound depends on it. Use this fallback chain (stop at first hit):

1. **WebFetch the institutional website** (home + `/contato` or `/contact`). If you see Cloudflare email obfuscation (`[email protected]` placeholders), continue to step 2.
2. **WebSearch** `"{org_name}" "@{dominio}" contato` — sometimes news/press releases or directories like Crunchbase/RocketReach surface the email in search snippets.
3. **WebSearch** `"{founder_name}" email "{org_name}"` — for founder-led small orgs the founder's personal/work email often shows in interviews or directories.
4. **Pattern fallback**: if the domain has MX records (run `enrichers/email_guesser.py` or just trust the domain) but no scraped email, save `contato@{dominio}` as best-guess and set `email_inferred=true` (or just flag in `scoring_reasoning`).
5. **No domain at all** (only LinkedIn / Instagram / Facebook): leave `company_email` empty and note in `scoring_reasoning` that outbound for this lead must go through LinkedIn DM. Don't fabricate.

When the website redirects to a domain-park page (HugeDomains, Sedo, GoDaddy parking) the original site is dead — search for the current site (`{org_name}` site oficial) before declaring no email. Update `company_website` if you find the new domain.

**Important**: If WebSearch returns no useful results for a small/unknown org, that's OK. Use the DB data (CNAE, description, funding source) combined with training knowledge to classify.

#### 2b. Classify and Enrich

Based on ALL gathered data (web + DB + training knowledge), determine:

| Field | Valid Values | How to Determine |
|-------|-------------|-----------------|
| `org_type` | `ONG`, `Empresa Social`, `Governo`, `Corporativo`, `Multinacional`, `Startup`, `Fundacao`, `Instituto`, `Associacao` | Legal name patterns ("Instituto", "Associacao", "Fundacao"), CNAE code, website content. Use `Multinacional` para B3-listed/grandes empresas com operacao internacional. |
| `inferred_industry` | Free text PT-BR | CNAE description + website "sobre" section + project description |
| `mission_summary` | 1-2 sentences PT-BR | Website mission text, or synthesize from description + activity |
| `size_estimate` | `1-10`, `11-50`, `51-200`, `201-500`, `500-1000`, `1001-5000`, `5000+` | LinkedIn employee count, website team page, funding level as proxy. Tiers grandes (500+) sao para ICP corporativo_esg. |
| `org_maturity` | `Inicial`, `Crescimento`, `Estabelecida`, `Madura` | Founded year, funding history, organizational complexity |
| `company_website` | URL | WebSearch result (only if confirmed real, not a directory listing) |
| `company_linkedin` | URL | WebSearch site:linkedin.com result |
| `company_instagram` | URL | WebSearch site:instagram.com result |
| `company_email` | Email | WebFetch from website contact page |
| `decision_maker_titles` | Comma-separated PT-BR titles | Website team page, LinkedIn. Use TITLES (NOT names — ver `contact_person_name`). Guidance por ICP: **corporativo_esg** = "Coordenacao de Sustentabilidade, Gerencia de ESG, Diretoria de Responsabilidade Social"; **negocios_impacto** = "CEO, Fundador, Fundadora, Diretor"; **terceiro_setor** = "Diretoria Executiva, Coordenacao de Projetos, Coordenacao Geral, Monitoramento e Avaliacao". |
| `contact_person_name` | Nome completo PT-BR (ex: "Maria Silva") | **OBRIGATORIO PARA OUTBOUND** — usado em `{nome_persona}` dos templates. Encontre via WebSearch `site:linkedin.com/in/ "{org_name}" "{cargo do ICP}"`, pagina "equipe"/"diretoria" do site, ou cabecalho de relatorios. Escolha a pessoa cujo cargo bate com a guidance de `decision_maker_titles` para o ICP. Se varios decisores: pegue o de cargo mais alto na area de impacto. Deixe vazio se nao tiver certeza — melhor fallback no `org_name` do que enviar "Ola, Joao Silva" pra pessoa errada. |
| `contact_person_title` | Cargo exato dessa pessoa em PT-BR (ex: "Coordenadora de Sustentabilidade") | Cargo da MESMA pessoa de `contact_person_name`. Diferente de `decision_maker_titles` (que e a lista canonica do ICP). |
| `tech_stack_likely` | Free text | Website technology indicators, org type norms |

#### 2c. Score Using ICP Rubric

**Read the ICP definitions from `config/icps.yaml`** to understand all active ICPs (3 canonicos: `corporativo_esg`, `negocios_impacto`, `terceiro_setor`).

The Manaca sells **consultoria de impacto socioambiental** com 2 tickets:
- **R$ 5-15k** (acessivel) para `negocios_impacto` e `terceiro_setor` — Flora SaaS incluso 6-12 meses
- **R$ 50k+** (corporativo) para `corporativo_esg` — grandes empresas com obrigacao ESG

A Flora e ferramenta de entrega, nao o produto. Pergunta-chave de qualificacao:
"Esta organizacao precisa estruturar, mensurar ou comprovar seu impacto socioambiental
com metodologia profissional e dados auditaveis?" Se sim, score alto.

For EACH active ICP in the YAML:
1. Read the `description`, `dimensions`, and `criteria` sections
2. Evaluate each binary criterion (true/false) based on your research
3. Compute dimension scores: sum of weights for true criteria (each dimension sums to 100)
4. Compute `impact_score` using the ICP's `weights` (mission, tech, budget, access)
5. Determine `fit` using the ICP's `fit_rule`

The YAML file is the single source of truth for:
- What dimensions to score
- What criteria to evaluate (with prompt questions)
- How to weight dimensions
- What determines fit
- Calibration examples

**Also determine confidence:**
- `needs_review` = true if you had very little data to work with (no web results, vague description, uncertain classification)

### Step 3: Save Each Lead

After enriching and scoring each lead, save it:

```bash
cd /c/Manabot/LeadsScraping && python enrichers/llm_enrichment_helper.py --action save --data '{
  "source": "...",
  "source_id": "...",
  "org_type": "ONG",
  "inferred_industry": "Educacao ambiental",
  "mission_summary": "Promove educacao ambiental...",
  "size_estimate": "11-50",
  "org_maturity": "Estabelecida",
  "company_website": "https://example.org",
  "company_linkedin": "https://linkedin.com/company/example",
  "company_instagram": "https://instagram.com/example",
  "company_email": "contato@example.org",
  "decision_maker_titles": "Diretor Executivo, Coordenador de Projetos",
  "contact_person_name": "Maria Silva",
  "contact_person_title": "Diretora Executiva",
  "tech_stack_likely": "Google Workspace, WhatsApp Business",
  "mission_alignment": 85,
  "tech_readiness": 70,
  "budget_indicator": 60,
  "decision_accessibility": 75,
  "themes": ["educacao", "meio ambiente"],
  "scoring_reasoning": "ONG com gestao de projetos sociais em multiplos municipios...",
  "needs_review": false,
  "icp_scores": {
    "corporativo_esg": {
      "mission_alignment": 25, "tech_readiness": 30, "budget_indicator": 20, "decision_accessibility": 35,
      "total_score": 28.0, "fit": false,
      "themes": ["impacto territorial"],
      "reasoning": "Pequeno, sem orcamento ESG estruturado nem porte para ticket >R$50k"
    },
    "negocios_impacto": {
      "mission_alignment": 72, "tech_readiness": 60, "budget_indicator": 45, "decision_accessibility": 80,
      "total_score": 65.3, "fit": true,
      "themes": ["cultura", "educacao"],
      "reasoning": "Precisa de consultoria para se posicionar como negocio de impacto"
    },
    "terceiro_setor": {
      "mission_alignment": 45, "tech_readiness": 50, "budget_indicator": 30, "decision_accessibility": 70,
      "total_score": 50.1, "fit": false,
      "themes": ["educacao"],
      "reasoning": "E negocio com fim lucrativo, nao OSC finalista"
    }
  }
}'
```

The helper computes `funding_score`, `impact_score`, `total_score`, and `fit_for_manaca` automatically from the sub-scores and the lead's existing `approved_value`/`approval_date`.

The `icp_scores` dict stores per-ICP scores in the `lead_icp_scores` table and automatically selects the best ICP as `best_icp_id`.

Contact fields (`company_website`, `company_linkedin`, `company_instagram`, `company_email`) use COALESCE — they only overwrite if the new value is non-empty, preserving existing data from other enrichers.

### Step 3b: Hunter.io upgrade (alto-fit only)

After the `--action save` returns a JSON like `{"status":"saved", "total_score":..., "fit_for_manaca":true}`, parse the response. Run Hunter.io fallback **ONLY** when ALL of these are true:

- `fit_for_manaca == true`
- `total_score >= 70`
- The saved lead does NOT yet have a named email — i.e. `company_email` is empty OR starts with `contato@`/`info@`/`faleconosco@`/`atendimento@`/`comunicacao@`

If yes, invoke the per-lead helper:

```bash
python scripts/hunter_fill.py --source <SRC> --source-id <ID>
```

Parse the returned JSON:
- `{"status":"saved", "email":..., "confidence":..., "position":..., "searches_remaining":N}` → add to the final report: **"Hunter upgrade: X@dominio (conf=Y, position)"**. The script already updated the DB.
- `{"status":"skipped", "reason":"..."}` → no action. Common reasons: `already_has_named_email`, `no_usable_domain` (LinkedIn/Wordpress/etc), `score_below_threshold` (defensivo, voce ja gateou antes), `not_fit`. Do NOT retry.
- `{"status":"no_email_found", ...}` → Hunter consumed 1-2 searches but did not return a high-confidence email. Note in report.
- `{"status":"skipped", "reason":"budget_exhausted"}` → Hunter quota exhausted. **STOP calling Hunter for the rest of this run.** Note prominently in the final report.
- `{"status":"error", ...}` → log and continue without retrying.

**Do NOT call Hunter for:**
- Leads that already saved with a named email (Hunter helper has its own gate, but skip the call to save token budget on this side too).
- Leads with `fit=false` or `total_score < 70`.
- Leads without a usable website (LinkedIn-only, etc).

At the end of the run, include `Hunter searches remaining: N` from the last successful Hunter call in the final report.

### Step 4: Report Progress

After processing all leads, show a summary table:

| Lead | Org Type | Best ICP | Score | Fit | Website Found |
|------|----------|----------|-------|-----|---------------|
| Instituto X | ONG | negocios_impacto | 78.5 | Sim | example.org |
| Hospital Y | Corporativo | - | 12.3 | Nao | - |
| ... | ... | ... | ... | ... | ... |

Then suggest: "Processar mais leads? Use `/llm-enrich run --limit N`"
