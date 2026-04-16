# Meta: Versionamento Contínuo da Skill (GitHub Sync)

**Propósito:** esta skill evolui a cada edital processado. Para que todo o aprendizado se acumule (e não se perca), ela é versionada em https://github.com/manaca-ale/claude-skills e se auto-sincroniza em duas pontas da execução.

---

## Modelo Operacional

```
┌─────────────────────────────────────────────────────────────┐
│  INVOCAÇÃO DA SKILL                                         │
├─────────────────────────────────────────────────────────────┤
│  1. Bootstrap (auto-pull silencioso)                        │
│     └─ git fetch + git pull --ff-only origin main           │
│                                                             │
│  2. Trabalho normal nas fases 00-08                         │
│     └─ (pode editar templates, references, SKILL.md)        │
│                                                             │
│  3. Consolidação Final (auto-push em main)                  │
│     └─ git add/commit/push com mensagem estruturada         │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Bootstrap (início da execução)

**Obrigatório em toda invocação da skill.**

### Fluxo

1. Ir para a pasta da skill:

   ```bash
   cd "$CLAUDE_SKILLS_HOME/edital-agent"
   # Windows típico: C:\Users\aleco\.claude\skills\edital-agent
   ```

2. Validar que é um repositório git com remote correto:

   ```bash
   git remote get-url origin
   # Esperado: https://github.com/manaca-ale/claude-skills.git
   ```

3. Buscar atualizações remotas:

   ```bash
   git fetch origin main --quiet
   ```

4. Comparar HEAD local com `origin/main`:

   ```bash
   LOCAL=$(git rev-parse @)
   REMOTE=$(git rev-parse origin/main)
   BASE=$(git merge-base @ origin/main)
   ```

5. Decisão:

   | Situação | Ação |
   |---|---|
   | `LOCAL == REMOTE` | Já atualizada. Prosseguir silenciosamente. |
   | `LOCAL == BASE` (atrás) | `git pull origin main --ff-only --quiet` e logar commits trazidos. |
   | `REMOTE == BASE` (à frente) | Há mudanças locais não pushadas. Não puxar; avisar para rodar consolidação primeiro. |
   | Divergente | Parar e pedir resolução manual ao usuário. |

6. Se working tree estiver sujo (`git status --porcelain` retorna linhas) ao iniciar: **avisar usuário** antes de seguir — pode ser trabalho não commitado de execução anterior.

### Log de bootstrap

Registrar resultado em `.skill-sync.log` (ignorado pelo git):

```
[2026-04-16T14:03:12] BOOTSTRAP edital=premio-mif-2026 status=UP_TO_DATE head=abc1234
[2026-04-16T14:03:12] BOOTSTRAP edital=lab-procel     status=PULLED  from=abc1234 to=def5678 commits=3
```

### Tratamento de erros

- **Sem rede:** `git fetch` falha → prosseguir com versão local e marcar `status=OFFLINE` no log. Consolidação final também vai falhar silenciosamente em push, deixando commits locais para push posterior.
- **Sem remote configurado:** orientar usuário a rodar o setup (ver `README.md` do pacote) ou executar:

  ```bash
  git init
  git remote add origin https://github.com/manaca-ale/claude-skills.git
  git fetch origin
  git checkout -t origin/main
  ```

- **Autenticação falha (repo privado):** orientar usuário a logar via `gh auth login` ou configurar PAT.

---

## 2. Consolidação Final (fim da execução)

**Obrigatório na Fase 08 de todo edital, ou quando a skill é encerrada explicitamente.**

### Critério: o que entra e o que não entra

**ENTRA (promover à skill):**

- Novos gotchas universais observados em `references/gotchas-editais.md`
- Templates melhorados que se aplicam a >1 agência
- Atualizações de dados da empresa em `references/empresa-base.md` (após confirmar com usuário)
- Novos exemplos de redação bem-sucedidos em `templates/equipe/exemplos-redacao-equipe.md` (parafraseados, sem dado sensível de cliente)
- Novos gatilhos R# de red-flag descobertos em `references/matriz-agencias-equipe.md`
- Correções de erros encontrados na skill
- Atualização dos CVs canônicos em `Equipe/CVs-Canonicos/` com novas credenciais da equipe
- Novas variantes de formato em `templates/equipe/sumula-curricular.md`

**NÃO ENTRA (fica no workspace `Editais/`, fora do repo da skill):**

- Conteúdo específico de um edital (narrativas, orçamentos, pitch)
- Dados sensíveis de clientes
- Documentos não anonimizáveis
- Rascunhos incompletos ou experimentais
- Arquivos grandes (PDFs de edital originais, exports)

### Fluxo

1. Detectar modificações:

   ```bash
   cd "$CLAUDE_SKILLS_HOME/edital-agent"
   git status --porcelain
   ```

2. Se vazio → nada a fazer, prosseguir.

3. Se há modificações → categorizar e montar commit message:

   **Tipos permitidos:**
   - `feat` — nova capacidade (template, variante, gatilho)
   - `fix` — correção de erro em template/referência
   - `docs` — melhoria de documentação/guia
   - `refactor` — reorganização sem mudança de comportamento
   - `learning` — aprendizado específico capturado como gotcha/exemplo
   - `chore` — manutenção (atualização de CV canônico, refs administrativas)

   **Escopos permitidos:**
   - `references` — arquivos em `references/`
   - `templates` — arquivos em `templates/`
   - `cv-canonico` — CVs em `Equipe/CVs-Canonicos/` (só se forem parte do repo da skill)
   - `skill-md` — mudança no SKILL.md
   - `guia` — atualização de guia operacional

   **Formato:**

   ```
   <tipo>(<escopo>): <resumo em 50 chars>

   Aprendizados do edital <slug> (<trilha A|B>):
   - <bullet 1>
   - <bullet 2>
   - <bullet 3>

   🤖 Captured during edital-agent run
   ```

4. Executar commit e push:

   ```bash
   git add <paths específicos — nunca git add -A cego>
   git commit -m "$(cat <<'EOF'
   <mensagem estruturada>
   EOF
   )"
   git push origin main
   ```

5. Registrar no `08-post-mortem.md` do edital:

   ```markdown
   ## Aprendizados promovidos à skill

   - **Commit:** <hash curto>
   - **Arquivos alterados:** <lista>
   - **Categoria:** <feat|fix|docs|...>
   - **Síntese:** <1 parágrafo>
   ```

### Tratamento de falhas na consolidação

- **Push falha (rede/auth):** commit fica local; registrar em `.skill-sync.log` como `status=PENDING_PUSH`. Próximo bootstrap avisará que há commits locais à frente.
- **Pre-commit hook falha:** corrigir e novo commit (nunca `--amend`).
- **Conflito no push (alguém já pushou):** `git pull --rebase origin main` e novo push. Se conflito real → avisar usuário.

---

## 3. Regras de Higiene

- **Sempre `git add` com paths específicos** (nunca `git add -A` ou `git add .`), para evitar promoção acidental de arquivos de edital ou credenciais.
- **Nunca pushar `.env`, tokens, ou credenciais** — se aparecer no diff, abortar e avisar.
- **Nunca amendar commits já pushados** — sempre criar novo commit.
- **Nunca forçar push em main** (`--force`) — mesmo que o hook permita.
- **Preservar histórico** — evitar `git reset --hard` em commits pushados.
- **Branch única:** a skill opera em `main` exclusivamente. Experimentações locais ficam em `wip/*` do workspace.

---

## 4. Primeiro Setup (uma vez só, pelo usuário)

Antes que o bootstrap funcione, a pasta local precisa ser um git checkout do repo. Ver `README.md` do pacote para o passo-a-passo de inicialização.

Cenários cobertos:
- Repo remoto vazio + skill local existente → inicializar local e fazer primeiro push.
- Repo remoto com conteúdo + skill local vazia → clone direto.
- Repo remoto com conteúdo + skill local com modificações → merge manual.

---

## 5. Observabilidade

Arquivo `.skill-sync.log` (no root da skill, gitignored) registra:

```
<timestamp> <evento> edital=<slug> status=<status> detalhe=<detalhe>
```

Eventos possíveis:
- `BOOTSTRAP` — início
- `PULLED` — trouxe commits do remoto
- `PUSHED` — enviou commits
- `PENDING_PUSH` — commit local não enviado
- `OFFLINE` — sem rede
- `CONFLICT` — requer ação manual
- `ERROR` — falha inesperada

Revisar o log na Fase 08 ajuda a validar que a consolidação funcionou.
