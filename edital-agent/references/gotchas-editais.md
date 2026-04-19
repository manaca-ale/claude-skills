# Gotchas — Editais e Integrações

> Pegadinhas descobertas em produção durante execução real de editais. Consultar antes de investir tempo debugando o que já foi resolvido.

---

## 1. Google Drive API

### 1.1 Shared Drives exigem `supportsAllDrives=True`

Se a pasta raiz do edital está em Shared Drive (My Drive compartilhado com a equipe), **toda chamada à Drive API** precisa:

```python
drive.files().list(
    q=..., fields=..., pageSize=...,
    supportsAllDrives=True,
    includeItemsFromAllDrives=True,
).execute()

drive.files().create(body=..., supportsAllDrives=True).execute()
drive.files().update(fileId=..., body=..., supportsAllDrives=True).execute()
```

**Sintoma sem isso:** `HttpError 404 File not found: <folder_id>` mesmo com ID correto.

**Fonte:** descoberta no Lab Procel 2026-04-16 depois de ~10min debugando.

### 1.2 Converter Markdown para Google Doc no upload

Para que um `.md` local vire um Google Doc editável (e não arquivo MD solto no Drive):

```python
body = {
    "name": "Nome do Doc",
    "parents": [folder_id],
    "mimeType": "application/vnd.google-apps.document",  # <-- força conversão
}
media = MediaFileUpload(local_md_path, mimetype="text/markdown")
drive.files().create(body=body, media_body=media, ..., supportsAllDrives=True).execute()
```

### 1.3 Update preserva ID/link; Create duplica

Para atualizar conteúdo de um Google Doc **sem quebrar o link** que já foi compartilhado (ex.: Caderno de Preenchimento atualizado depois de correções):

```python
drive.files().update(
    fileId=existing_doc_id,   # <-- mantém o mesmo fileId
    media_body=media,
    supportsAllDrives=True,
).execute()
```

**Não criar** um novo arquivo com `files().create()` se já existe — isso duplica e bagunça o histórico de links em ClickUp/STATUS.md.

### 1.4 `files.create` NÃO aceita `folder_id` diretamente

Para colocar um arquivo numa pasta específica do Drive, o padrão é passar `parents` no body:

```python
body = {"name": ..., "parents": [folder_id]}
```

Não existe parâmetro `folder_id` no método.

---

## 2. Autenticação (Drive, Sheets, Docs)

### 2.1 Preferência: `google-drive-envs` sobre `gws` CLI

Nesta máquina, **`gws` CLI não está autenticado por padrão** (storage=none, token_cache_exists=false). `gws auth login` exige browser e interação manual.

**Alternativa preferida** para scripts não-interativos: usar token OAuth pré-salvo pela skill `google-drive-envs`:

```python
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = "C:/secrets/Envs/Drive/Drive/token_sheets.json"
with open(TOKEN_PATH) as f:
    data = json.load(f)

creds = Credentials(
    token=data["token"],
    refresh_token=data["refresh_token"],
    token_uri=data["token_uri"],
    client_id=data["client_id"],
    client_secret=data["client_secret"],
    scopes=data["scopes"],
)
if not creds.valid:
    creds.refresh(Request())
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())
```

**Quando usar `gws` CLI ao invés de Envs:** apenas quando precisar de serviços que a skill `google-drive-envs` não cobre (Gmail, Calendar, Admin SDK, Forms, Chat). Para Drive/Docs/Sheets puro, Envs é mais confiável.

**Setup inicial do Envs (se os arquivos não existirem):** a skill `google-drive-envs` tem helper `ensure_envs_repo()` que faz `git clone` + `git-crypt unlock` automaticamente (requer GPG key + acesso ao repo privado `manaca-ale/Envs`).

### 2.2 Escopos OAuth do token Envs

Token atual tem: `spreadsheets`, `drive`. Se precisar Docs API direta (ex: `batch_update_doc` para formatação programática), o token precisa ser regenerado com escopo adicional `documents`.

---

## 3. Texto em português

### 3.1 Acentuação PT-BR desde o primeiro rascunho

**Regra:** todo texto que vá para documento de submissão deve ser escrito com acentuação completa desde o primeiro write. Corrigir depois é 10x mais caro (precisa ler todo o texto, re-uploadar Docs, etc).

**Por quê:** edital formal avaliado por humanos. Texto sem acentos sinaliza "descuido" e afeta percepção de qualidade antes mesmo da leitura do conteúdo.

### 3.2 Script de dicionário-cego NÃO funciona

Tentativa: dicionário `{"palavra_sem_acento": "palavra_com_acento"}` aplicado via regex.

**Por que falha:**
- Nomes próprios quebram: `"Marco Legal das Startups"` → `"Março Legal"` (Marco da Lei 14.063 virou mês por substituição "marco" → "março")
- Homógrafos: `"esta"` (pronome demonstrativo) vs `"está"` (verbo)
- Conjugações: `"para"` (preposição) vs `"pará"` (verbo) vs "Pará" (estado)
- Cobertura nunca é 100% — sempre sobram palavras fora do dicionário

**Abordagem confiável:** Claude ler o texto e reescrever com acentuação correta. Mais caro em tokens, mas é o único path que não introduz regressões em nomes próprios.

**Fonte:** aprendizado Lab Procel 2026-04-16 — perdemos ~1h em script de dicionário até detectar a corrupção do "Marco Legal".

---

## 4. Plataformas de submissão com login

### 4.1 Pedir screenshots ANTES de redigir

Se a plataforma de submissão do edital **exige login para ver os campos** dos formulários, algumas abas podem conter campos que não estão no PDF do edital nem no guia oficial (descobrimos isso com as abas EQUIPE e UNIDADES do Portal da Inovação Lab Procel).

**Ação obrigatória na Fase 1 (Ingestão):**
- Verificar se a plataforma tem login gate
- Se sim, **pedir screenshots das abas ao usuário** antes de redigir textos longos
- Mapear campo-a-campo (nome, tipo, limite de caracteres, obrigatoriedade) em `01-edital-parsed.md`

**Custo de ignorar isso:** descobrir na hora da submissão que falta dado não coletado → corrida contra o tempo → risco de submeter com erro.

### 4.2 Limites de caracteres variam por campo

Sempre extrair do mapeamento da plataforma (não do edital oficial, que pode omitir):
- Nome da ideia (limite típico 80-120 chars)
- Descrição curta (500-4950 chars)
- Descrição TRL (textarea livre, mas geralmente 2000-5000 chars)

**Dica:** gravar os limites em `01-edital-parsed.md` para validação automática dos textos gerados antes de copiar para a plataforma.

### 4.3 Playwright substitui screenshots manuais

Desde 2026-04, a abordagem canônica é mapear o formulário com Playwright em vez de pedir screenshots ao usuário. Ver [mapeamento-formularios-playwright.md](mapeamento-formularios-playwright.md) para o workflow completo.

**Quando cair no fluxo antigo (screenshots):** só se o Playwright CLI não estiver disponível (raro) ou se a plataforma tiver anti-bot muito agressivo (CAPTCHA por etapa, etc.).

### 4.4 FINEP FAP exige título da proposta ANTES de abrir o formulário

No FAP (forms.finep.gov.br), a linha do edital na lista "Iniciar Inscrição" tem **um textbox pequeno** ("Informe um título para a proposta") e um botão "Iniciar Inscrição". Clicar no botão sem preencher o textbox NÃO abre o form — apenas volta sem erro visível.

**Workaround:** preencher o textbox com título provisório (editável depois dentro do form) e só então clicar. Formulário abre em nova aba do browser.

### 4.5 Editais FINEP regionais: escolher o formulário correto

Programas como Mulheres Inovadoras e Centelha têm **formulários separados por região** (Centro-Oeste / Nordeste / Norte / Sudeste / Sul). Escolher conforme o **estado da sede do CNPJ**.

| UF da sede | Região | Formulário FAP |
|---|---|---|
| ES, MG, RJ, SP | Sudeste | "... - REGIÃO SUDESTE" |
| BA, PE, CE, MA, PI, RN, PB, AL, SE | Nordeste | "... - REGIÃO NORDESTE" |
| PR, SC, RS | Sul | "... - REGIÃO SUL" |
| AC, AM, AP, PA, RO, RR, TO | Norte | "... - REGIÃO NORTE" |
| DF, GO, MT, MS | Centro-Oeste | "... - REGIÃO CENTRO-OESTE" |

**Custo de errar:** a inscrição é invalidada; não há como transferir proposta entre regiões. A Manacá (sede em Vitória-ES) é **Sudeste**.

---

## 7. Dados da empresa — fonte de verdade

### 7.1 Contrato social pode estar desatualizado em references/

`references/empresa-manaca.md` é baseline, mas alterações contratuais recentes (saída de sócio, mudança de %, mudança de sede) podem não ter sido refletidas ainda.

**Sempre confirmar antes de declarar em formulário:**
- Composição societária (% de cada sócio)
- Endereço da sede
- Capital social
- Objeto social (CNAEs)

**Como validar:** baixar PDF mais recente do contrato social (Drive ou local) e conferir. Para Manacá, o contrato consolidado mais recente é `ALTERACAO 11.09.2025.pdf` (JUCEES NIRE 32203432394) — Rayssa 65% / Alexandre 35%, sem mais o Angelo.

**Fonte:** sessão Mulheres Inovadoras 2026-04-19 — STATUS.md estava com "Rayssa 45% / Alexandre 27,5%" (composição antiga com Angelo) e tivemos que corrigir em cima da hora.

### 7.2 Planilhas financeiras da empresa

Quando precisar de faturamento, custos, fluxo de caixa para um formulário quantitativo, pedir ao usuário os xlsx locais:

- `Receitas e Projeções.xlsx` — faturamento por ano (real + projeção)
- `Planejamento <ano>.xlsx` — orçamento planejado vs. real, breakdown mensal
- `Planejamento Financeiro e Estratégico Manaca -<ano1>_<ano2>.xlsx` — fluxo de caixa detalhado, item por item

Ler com `openpyxl` + `data_only=True`. A skill `spreadsheet` tem helpers mais sofisticados.

**Google Sheets da Rayssa:** algumas planilhas estão em conta pessoal da Rayssa (`manaca-ale` sem acesso). Nesses casos, pedir xlsx local em vez de forçar compartilhamento.

---

## 8. WebFetch vs Playwright

### 8.1 manaca.tech retorna 403 via WebFetch

Quando precisar extrair infos do site institucional (telefone, email, social media):

```
WebFetch(url="https://manaca.tech", prompt="...")
→ "Request failed with status code 403"
```

**Workaround:** usar Playwright:

```bash
export PWCLI="$HOME/.codex/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" tab-new https://manaca.tech
"$PWCLI" snapshot
# depois Grep no arquivo .yml por "mailto:", "wa.me", "linkedin.com/company", etc.
```

Custo: ~20 segundos a mais, mas funciona. Considerar o mesmo padrão para outros sites institucionais com anti-bot.

---

## 5. ClickUp

### 5.1 UTF-8 em comentários com texto PT-BR

Usar **sempre** `scripts/clickup_edital_sync.py comment ...` (que usa `requests` em Python). `curl` com `-d` inline corrompe acentos/cedilhas no Windows.

Ver `references/clickup-editais.md` para detalhes.

### 5.2 Links de edital ficam em `markdown_description`, não `description`

O campo `description` via API costuma vir vazio. URLs (Google Docs, Forms, PDFs do edital) estão em `markdown_description`. Usar `scripts/clickup_edital_sync.py links <task_id>` que já busca `?include_markdown_description=true`.

---

## 6. Versionamento da skill (monorepo)

### 6.1 `git add` sempre com paths `edital-agent/*`

A skill vive em subpasta do monorepo `~/.claude/skills/`. `git add -A` cego adicionaria mudanças de outras skills (content-briefing, deep-research-prompt, etc.) que não deveriam ir junto.

```bash
# CERTO:
cd ~/.claude/skills
git add edital-agent/SKILL.md edital-agent/references/foo.md

# ERRADO:
git add -A  # ou git add .
```

### 6.2 `git status --porcelain edital-agent/` filtra ruído

Para ver só mudanças da skill (ignorando outras skills do monorepo):

```bash
cd ~/.claude/skills
git status --porcelain edital-agent/
```
