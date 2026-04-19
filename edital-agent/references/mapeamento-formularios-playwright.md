# Mapeamento de Formulários Online via Playwright

> Workflow reutilizável para mapear formulários de submissão de editais que exigem login (FINEP FAP, SAGe/CNPq, SIGFAPES, Carambola, Portal da Inovação da Indústria, plataformas de FAPs estaduais).
>
> **Substitui** a prática antiga de "pedir screenshots ao usuário" (ainda presente em SKILL.md §Fase 1, etapa 6). Use esta abordagem sempre que a plataforma tiver campos que não aparecem no PDF do edital.

## Quando usar

- O edital aponta para uma plataforma online (URL de submissão).
- A plataforma exige login (CPF+senha, gov.br, usuário da agência).
- Os campos do formulário não estão integralmente documentados no PDF do edital.
- Há suspeita de abas/seções com campos específicos (tabelas de sócios, campos quantitativos, declarações numeradas).

## Pré-requisitos

- Playwright CLI disponível via wrapper:
  ```bash
  export PWCLI="$HOME/.codex/skills/playwright/scripts/playwright_cli.sh"
  ```
- Acesso de leitura ao diretório do edital em `c:\Editais\editais\<slug>\`.

## Workflow

### 1. Abrir o formulário em modo `--headed` e pedir login manual

```bash
"$PWCLI" open <URL-do-formulário> --headed
```

Mostrar no chat: *"O navegador abriu em [tela de login]. Por favor, faça login manualmente e me avise quando chegar à tela principal do formulário."*

Esperar o usuário dizer "pronto" antes de prosseguir.

### 2. Snapshot inicial e identificar a estrutura

```bash
"$PWCLI" snapshot
```

No snapshot (arquivo `.yml` em `.playwright-cli/`), localizar:
- Lista de abas/tabs (procurar `generic [ref=e##]: Critério I` ou `listitem ... tabpanel`)
- Botões de ação (Salvar, Validar, Verificar pendências, Enviar)
- Estrutura de campos da primeira aba

**Se a plataforma exige preencher título da proposta antes de abrir o form** (padrão FINEP FAP):
```bash
"$PWCLI" fill e<ref-textbox> "Título provisório"
"$PWCLI" click e<ref-botão-iniciar>
"$PWCLI" tab-select 1
"$PWCLI" snapshot
```

### 3. Iterar cada aba e extrair schema

Para cada aba (ex.: `Dados`, `Critério I`, `Critério II`...):

```bash
"$PWCLI" click e<ref-da-aba>
"$PWCLI" snapshot
```

Extrair campos do snapshot com Grep focado:

```
Grep pattern: ^\s*- (textbox|combobox|checkbox|radio|button)|generic \[ref=e\d+\]: [A-Z0-9]
```

Isso devolve labels + tipos + refs.

### 4. Capturar opções de comboboxes

Comboboxes só revelam opções **após click**:

```bash
"$PWCLI" click e<ref-combobox>
"$PWCLI" snapshot
```

Grep pelas opções:

```
Grep pattern: listitem \[ref=e\d+\] \[cursor=pointer\]:
```

Depois fechar antes de ir para o próximo:

```bash
"$PWCLI" press Escape
```

### 5. Capturar textos completos de declarações Sim/Não

Radios de declaração têm o texto integral no snapshot. Ler trecho específico com `Read offset:<linha> limit:<linhas>` para transcrever ipsis litteris.

As declarações precisam ser **citadas verbatim** no data-pack e conferidas antes de responder "Sim".

### 6. Consolidar em `07-form-fields.md`

Estrutura padrão (comprovada na sessão FINEP Mulheres Inovadoras 2026-04-19):

```markdown
# Mapeamento Completo — Formulário <nome> (região/variante)

**URL:** <url>
**Usuário logado:** <nome>
**Título da proposta:** `<título>`
**Estrutura:** <N> abas · **Total estimado:** ~<N> campos obrigatórios
**Ações:** <lista de botões no topo>

---

## Aba 1 — <NOME>

### 1.1 <subseção>
| # | Campo | Tipo | Fonte/Opções |
|---|---|---|---|
| 1 | Razão social | texto | CNPJ |

### 1.2 Declarações (N perguntas Sim/Não — **todas devem ser "Sim"**)
1. [texto integral da declaração 1]
2. [texto integral da declaração 2]

### 1.3 <combobox>
**<Label>** (combobox — N opções):
Opção 1 · Opção 2 · **Opção 3** ← nossa escolha · Opção 4

---

## Aba 2 — <NOME>

---

## Inventário de entregáveis

### Dados fatuais (confirmar com o usuário)
- [ ] Campo X

### Dados financeiros (crítico)
- [ ] Campo Z

### Narrativas (textboxes com limites fixos)
| Seção | Limite | Status |
|---|---|---|
| Resumo da Empresa | 3000 | ❌ redigir |

### Anexos/entregáveis externos
- [ ] Pitch em vídeo (link até N chars)
```

## Gotchas conhecidos

| Gotcha | Sintoma | Workaround |
|---|---|---|
| FINEP FAP exige título antes de abrir o form | "Iniciar Inscrição" não abre ao clicar direto | Preencher textbox `"Informe um título para a proposta"` e depois clicar |
| Form abre em nova aba do browser | tab-list muda | `"$PWCLI" tab-select 1` antes do próximo snapshot |
| Combobox só revela opções após click | Snapshot inicial não mostra opções | Click explícito no combobox + novo snapshot |
| Snapshot grande (>100KB) é truncado no chat | Output diz "Output too large, saved to tool-results/..." | Ler arquivo completo com `Read` + `Grep` cirúrgico |
| Refs mudam entre snapshots | Comando `click e<ref>` falha com "element not found" | Re-snapshot antes de cada interação importante |
| Aba às vezes precisa de segundo clique | Primeiro click não revela conteúdo | Click duplo ou aguardar carregamento e re-snapshot |

## Referência viva

O [c:/Editais/editais/premio-mulheres-inovadoras-finep-2026/07-form-fields.md](c:/Editais/editais/premio-mulheres-inovadoras-finep-2026/07-form-fields.md) é o exemplar canônico desta estrutura. Quando mapear um novo form, usar esse arquivo como template mental.

## Integração com fases da skill

| Fase do SKILL.md | O que fazer aqui |
|---|---|
| Fase 1 (Ingestão) | Se plataforma tem login → invocar este workflow; salvar `07-form-fields.md` ou integrar em `01-edital-parsed.md` |
| Fase 4 (Planejamento — Trilha B) | Usar o mapa para dimensionar esforço por seção |
| Fase 5a (Data Assembly) | O inventário do mapa alimenta `05a-data-pack.md` |
| Fase 6 (Quality Review) | Conferir narrativas × limites do form antes do advocate+red-team |
| Fase 7 (Submission Guide) | Cópia das regras operacionais do form (Salvar / Validar / Verificar pendências) |
