---
name: deep-research-prompt
description: >
  Generate optimized prompts for Google Deep Research and automatically execute them via Playwright.
  This skill should be used when the user wants to research best practices, tools, libraries,
  ready-made repositories, or architecture patterns before starting a project or feature.
  It transforms a rough research intent into a structured Deep Research brief, sends it to
  Gemini Deep Research via browser automation, and returns the results ready for implementation.
---

# Deep Research Prompt Generator + Automação

Transforma uma intenção de pesquisa em um prompt otimizado para Google Deep Research,
envia automaticamente via Playwright, e retorna o resultado pronto para implementar.

## Inputs to Confirm (Ask Only What Is Missing)

Before generating the prompt, confirm these essentials. Skip any the user already provided:

1. **Research topic** — What to research (technology, pattern, tool category, etc.)
2. **Goal** — What will be built or decided with the output (e.g., "build a real-time dashboard," "choose a queue system")
3. **Constraints** — Stack, budget, team size, timeline, or platform constraints (e.g., "Python only," "open-source only")

Do NOT ask more than these three questions. Infer everything else from context.

## Prompt Generation Workflow

### 1. Determine Language

Default to **English** for tech topics — broader, higher-quality results.
Use Portuguese only if the topic is inherently PT-BR domain (Brazilian regulations, PT-BR content strategy, etc.).

### 2. Classify Research Type

| Type | Focus | Example |
|------|-------|---------|
| **Tool/Library Selection** | Compare options, recommend best fit | "Best Python queue library for async pipelines" |
| **Architecture Pattern** | Design approaches, trade-offs | "Event sourcing vs CQRS for multi-tenant SaaS" |
| **Implementation Reference** | Ready-made repos, boilerplate, tutorials | "Open-source Streamlit dashboards with auth" |
| **Best Practices Survey** | Industry standards, pitfalls, guidelines | "Production-ready FastAPI project structure" |
| **Exploratory/Broad** | Landscape overview, emerging tools | "Current state of LLM-powered code review tools" |

### 3. Assemble the Prompt

Build the Deep Research prompt using this mandatory structure:

```
## Research Objective
[One paragraph: what to research and why. Be specific about the end goal.]

## Scope & Boundaries
- Technology stack: [specific languages, frameworks, platforms]
- Constraints: [budget, team size, timeline, licensing]
- Out of scope: [explicitly exclude tangential topics]

## Key Questions to Answer
1. [Most important question — usually "what are the best options?"]
2. [Second question — usually about trade-offs or architecture fit]
3. [Third question — usually about production readiness or scalability]
4. [Fourth question — usually about community/maintenance/ecosystem]
5. [Optional fifth question — edge cases, migration, or integration]

## Deliverable Format
For each tool/library/approach found:
- Name and repository/documentation link
- One-paragraph description of what it does
- Pros and cons (bullet points)
- Maturity indicators: GitHub stars, last commit date, release frequency, known adopters
- Code example or configuration snippet showing basic usage

Additionally provide:
- A comparison table of the top 3-5 options across key criteria
- A clear recommendation with justification
- Links to the most useful tutorials, blog posts, or example repositories

## Technical Context
- Audience: experienced developer implementing immediately after reading
- Prefer: actively maintained projects (commits within last 6 months)
- Prefer: solutions with good documentation and TypeScript/Python type support
- Include: GitHub repository links, not just documentation sites
```

### 4. Customize Per Research Type

After assembling the base structure, apply type-specific additions:

- **Tool/Library Selection** — Add: "Include a decision matrix comparing options on: performance, ease of integration, documentation quality, community size, and licensing."
- **Architecture Pattern** — Add: "Include real-world case studies from companies that implemented this pattern. Describe failure modes and when NOT to use it."
- **Implementation Reference** — Add: "Prioritize repos that are recently updated, well-documented, have CI/CD, and include tests. Note what needs adaptation for my use case."
- **Best Practices Survey** — Add: "Distinguish between universally accepted practices and opinionated preferences. Include references to official docs or RFCs."
- **Exploratory/Broad** — Add: "Organize by maturity level: production-ready, promising/beta, and experimental. Include timeline of key releases."

### 5. Final Polish

- Verify every section has specific, concrete language (no vague "look into X")
- Ensure the scope excludes at least one thing (prevents scope creep)
- Confirm the technical context matches the user's actual level and stack
- Replace all `[bracketed placeholders]` with real content

## Session Management (Persistent Login)

Google login is preserved across runs using a persistent Playwright browser profile at `~/.gemini-playwright-profile`.

### First-time setup

Run the login script once. It opens a browser, the user logs in manually (including 2FA), and the session is saved:

```bash
python "C:\Users\aleco\.claude\commands\deep-research-prompt\scripts\login_and_save.py"
```

### Checking session validity

```bash
python "C:\Users\aleco\.claude\commands\deep-research-prompt\scripts\login_and_save.py" --check
```

Returns exit code 0 if valid, 1 if expired. The `gemini_deep_research.py` script auto-detects existing sessions — if the profile exists and is valid, no login is needed. If the session expired, it will prompt for manual login.

### How it works

- `launch_persistent_context(~/.gemini-playwright-profile)` stores cookies, localStorage, and session data on disk
- All scripts (`login_and_save.py`, `gemini_deep_research.py`) share the same profile directory
- Sessions typically last days/weeks before expiring

## Execution via Playwright CLI

After generating the prompt, execute it automatically using the Playwright CLI wrapper.

```bash
export PWCLI="/c/Users/aleco/.codex/skills/playwright/scripts/playwright_cli.sh"
```

### Phase 1: Setup and Send (Claude does this interactively)

1. **Present the prompt** to the user in a code block and confirm: "Envio para o Gemini Deep Research agora?"

2. **Open Gemini** in headed mode:

```bash
"$PWCLI" open https://gemini.google.com/app --headed
"$PWCLI" snapshot
```

3. **Handle login** — If snapshot shows `accounts.google.com`, first try running `login_and_save.py --check`. If session is expired, tell the user to run `login_and_save.py` to re-authenticate. Wait and re-snapshot.

4. **Activate Deep Research** — It is in the **"Ferramentas" (Tools) button**, NOT in the model selector dropdown. The model selector (Rápido/Raciocínio/Pro) does NOT contain Deep Research.

```bash
# Click the "Ferramentas" button (icon: page_info)
"$PWCLI" click <ferramentas_ref>
# In the menu that opens, click "Deep Research" (menuitemcheckbox)
"$PWCLI" click <deep_research_ref>
```

After activation, the input placeholder changes to "O que você quer pesquisar?" and a "Deep Research" chip with an X appears near the input.

5. **Insert the prompt** — The input is a contenteditable div. `fill` truncates at newlines. Use `eval` with `insertText` instead:

```bash
# Save prompt to temp file, then insert via DOM eval
"$PWCLI" click <textbox_ref>
"$PWCLI" eval "async (el) => { el.focus(); el.textContent = '<PROMPT_TEXT>'; el.dispatchEvent(new Event('input', {bubbles: true})); return 'done'; }" <textbox_ref>
```

6. **Send** — After inserting, snapshot to find "Enviar mensagem" button and click it:

```bash
"$PWCLI" snapshot
"$PWCLI" click <send_button_ref>
```

7. **Confirm the research plan** — After ~30 seconds, Gemini shows a research plan with a "Start research" button. Snapshot, find it, and click:

```bash
# Wait for plan to appear
sleep 30
"$PWCLI" snapshot
# The button has data-test-id="confirm-button"
"$PWCLI" click <start_research_ref>
```

### Phase 2: Wait for Results (Background — NO Claude polling)

After clicking "Start research", **do NOT poll with Claude**. Instead, run the bundled Python script in background. The script handles all polling internally and saves the result to a file.

**Output location**: Always save results to a `pesquisas/` folder inside the current working directory. Create the folder if it doesn't exist. Use a descriptive filename based on the research topic (e.g., `pesquisas/instagram_editais_scraping.md`).

```bash
mkdir -p pesquisas
python "C:\Users\aleco\.claude\commands\deep-research-prompt\scripts\gemini_deep_research.py" --wait-for-completion --output pesquisas/<topic_slug>.md
```

For the full flow (not wait-only):

```bash
mkdir -p pesquisas
python "C:\Users\aleco\.claude\commands\deep-research-prompt\scripts\gemini_deep_research.py" --prompt-file /tmp/deep_research_prompt.md --output pesquisas/<topic_slug>.md --poll-interval 60 --max-wait 1200
```

Run this command with `run_in_background: true`. Claude will be notified automatically when the script finishes. Deep Research typically takes 5-15 minutes.

**IMPORTANT**: Do NOT do manual polling with repeated snapshot/screenshot calls. Each tool call consumes tokens. The background script is free.

### Phase 3: Extract and Present (Claude resumes when notified)

When the background script completes:

1. Read the result file from the `pesquisas/` folder
2. Present the key findings to the user
3. Suggest: "Pronto para implementar com base nessa pesquisa. O que quer começar?"

### Gemini UI Reference (as of March 2026)

| Element | Location | Selector hint |
|---------|----------|---------------|
| Model selector | Bottom-left of input | `button "Abrir seletor de modo"` — has Rápido/Raciocínio/Pro |
| Ferramentas | Bottom of input, icon `page_info` | `button "Ferramentas"` — has Deep Research, Imagens, Canvas |
| Deep Research | Inside Ferramentas menu | `menuitemcheckbox "Deep Research"` |
| Input field | Center | `textbox "Insira um comando para o Gemini"` |
| Send button | Bottom-right of input | `button "Enviar mensagem"` (only visible when text is present) |
| Start research | Inside research plan card | `data-test-id="confirm-button"` |
| Still running | Anywhere in page | `img: stop` icon present |
| Completed | Result panel | `button "Exportar para as Planilhas"` present, no `stop` icon |
| Result text | Side panel | `eval innerText` on the panel container |

### Handling edge cases

- **Login required**: Snapshot shows `accounts.google.com` → tell user to log in manually
- **Captcha/verification**: Tell user to complete manually, then continue
- **Deep Research unavailable**: Fall back to regular Gemini prompt
- **Stale refs**: Re-snapshot after every click or navigation
- **Long prompts**: Use `eval` with `textContent` assignment (NOT `fill`, which truncates at newlines)

## Deep Research Best Practices Reference

1. **Specificity wins** — Concrete constraints ("Python 3.11+, async, <50ms latency") beat vague goals ("fast and modern")
2. **Explicit scope boundaries** — Always state what is OUT of scope to prevent topic expansion
3. **Request structured output** — Comparison tables, pros/cons lists make output parseable by Claude afterward
4. **Ask for evidence** — Stars, commit dates, adopters, benchmarks. Deep Research surfaces these only when asked
5. **Specify recency** — Ask for "actively maintained" and "commits within last 6 months"
6. **Technical level matters** — "For an experienced developer implementing immediately" produces better results
7. **Request code samples** — Deep Research includes actual snippets when explicitly asked
8. **Link preference** — Ask for GitHub repos, not just docs. Repos are more useful for Claude to analyze
9. **Comparison tables** — Always request one. Forces normalized findings and faster decisions
10. **One question per prompt** — Don't combine "which database?" and "which auth library?" in one prompt
