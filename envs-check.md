---
name: envs-check
description: Verify git-crypt encryption status, GPG keys, and sync state of the private Envs repository (manaca-ale/Envs). This skill should be used when the user asks to check envs, verify encryption, check keys, or validate the Envs repo health.
---

# Envs Check

Verify the health and security of the encrypted Envs repository at `C:/secrets/Envs`.

## Repository Details

- **Remote:** `https://github.com/manaca-ale/Envs` (private)
- **Encryption:** git-crypt with GPG key for `contato@manaca.tech`
- **GPG Key ID:** `9A110931878AE3FA4A2427A842C023202209D382`

## What Gets Checked

1. **Prerequisites** — git-crypt and GPG are installed
2. **Repository** — git repo and git-crypt are initialized
3. **GPG keys** — private keys exist locally
4. **Authorized users** — git-crypt collaborators and matching local keys
5. **Encryption status** — which files are encrypted vs plaintext
6. **Remote sync** — local and GitHub are in sync
7. **Key backup** — GPG private key backup file exists

## Encrypted Files

| File | Content |
|------|---------|
| `envflora` | Flora project env vars |
| `envsaira` | SAIRA project env vars |
| `envleads` | Leads project env vars |
| `envclickuptelegram` | ClickUp/Telegram integration env vars |
| `envcoletoagentes` | Coleto Agentes env vars |
| `envmanafinance` | Mana Finance env vars |
| `Drive/Drive/client_secret_*.json` | Google OAuth client secret |
| `Drive/Drive/token_sheets.json` | Google Sheets OAuth token |

## Usage

Run the check script below. Save as `check_envs.sh`:

```bash
export PATH="$HOME/scoop/shims:$PATH"
bash check_envs.sh
```

### check_envs.sh

```bash
#!/usr/bin/env bash
# check_envs.sh — Verify git-crypt encryption status and GPG keys for the Envs repo
# Usage: bash check_envs.sh [repo_path]

set -euo pipefail

REPO_PATH="${1:-C:/secrets/Envs}"
export PATH="$HOME/scoop/shims:$PATH"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

header() { echo -e "\n${CYAN}══════════════════════════════════════${NC}"; echo -e "${CYAN}  $1${NC}"; echo -e "${CYAN}══════════════════════════════════════${NC}"; }
ok()     { echo -e "  ${GREEN}✓${NC} $1"; }
warn()   { echo -e "  ${YELLOW}⚠${NC} $1"; }
fail()   { echo -e "  ${RED}✗${NC} $1"; }

ERRORS=0

# ── 1. Check prerequisites ──
header "1. Prerequisitos"

if command -v git-crypt &>/dev/null; then
  ok "git-crypt instalado: $(git-crypt --version 2>/dev/null || echo 'ok')"
else
  fail "git-crypt NAO encontrado"; ERRORS=$((ERRORS + 1))
fi

if command -v gpg &>/dev/null; then
  ok "GPG instalado: $(gpg --version 2>/dev/null | head -1)"
else
  fail "GPG NAO encontrado"; ERRORS=$((ERRORS + 1))
fi

# ── 2. Check repo ──
header "2. Repositorio"

if [ -d "$REPO_PATH/.git" ]; then
  ok "Repo git encontrado em $REPO_PATH"
else
  fail "Nao e um repo git: $REPO_PATH"; ERRORS=$((ERRORS + 1))
  echo -e "\n${RED}Abortando — repo nao encontrado.${NC}"
  exit 1
fi

if [ -d "$REPO_PATH/.git-crypt" ]; then
  ok "git-crypt inicializado"
else
  fail "git-crypt NAO inicializado neste repo"; ERRORS=$((ERRORS + 1))
fi

# ── 3. GPG keys ──
header "3. Chaves GPG"

KEY_COUNT=$(gpg --list-secret-keys --keyid-format LONG 2>/dev/null | grep -c "^sec" || true)
if [ "$KEY_COUNT" -gt 0 ]; then
  ok "$KEY_COUNT chave(s) privada(s) encontrada(s):"
  gpg --list-secret-keys --keyid-format LONG 2>/dev/null | grep -E "^(sec|uid)" | sed 's/^/    /'
else
  fail "Nenhuma chave GPG privada encontrada"; ERRORS=$((ERRORS + 1))
fi

# Check authorized git-crypt users
header "4. Usuarios autorizados no git-crypt"

GPG_DIR="$REPO_PATH/.git-crypt/keys/default/0"
if [ -d "$GPG_DIR" ]; then
  for f in "$GPG_DIR"/*.gpg; do
    KEYID=$(basename "$f" .gpg)
    ok "Key ID: $KEYID"
    if gpg --list-secret-keys "$KEYID" &>/dev/null; then
      ok "  → Chave privada disponivel localmente"
    else
      warn "  → Chave privada NAO encontrada localmente"
    fi
  done
else
  fail "Nenhum usuario autorizado encontrado"; ERRORS=$((ERRORS + 1))
fi

# ── 5. Encryption status ──
header "5. Status de criptografia"

cd "$REPO_PATH"
ENCRYPTED=0
NOT_ENCRYPTED=0

while IFS= read -r line; do
  status=$(echo "$line" | awk '{print $1}')
  file=$(echo "$line" | awk '{$1=""; print substr($0,2)}')
  if [ "$status" = "encrypted:" ]; then
    ok "ENCRYPTED: $file"
    ENCRYPTED=$((ENCRYPTED + 1))
  elif [ "$status" = "not" ]; then
    file=$(echo "$line" | sed 's/not encrypted: //')
    case "$file" in
      .gitattributes|.gitignore|.git-crypt/*|.claude/*) ;;
      *) warn "NOT encrypted: $file"; NOT_ENCRYPTED=$((NOT_ENCRYPTED + 1)) ;;
    esac
  fi
done < <(git-crypt status 2>/dev/null)

echo ""
echo -e "  Encrypted: ${GREEN}$ENCRYPTED${NC} | Not encrypted: ${YELLOW}$NOT_ENCRYPTED${NC}"

# ── 6. Remote sync ──
header "6. Sincronizacao com GitHub"

REMOTE=$(git -C "$REPO_PATH" remote get-url origin 2>/dev/null || echo "")
if [ -n "$REMOTE" ]; then
  ok "Remote: $REMOTE"

  LOCAL=$(git -C "$REPO_PATH" rev-parse HEAD 2>/dev/null)
  git -C "$REPO_PATH" fetch origin --quiet 2>/dev/null || true
  REMOTE_HEAD=$(git -C "$REPO_PATH" rev-parse origin/master 2>/dev/null || echo "")

  if [ "$LOCAL" = "$REMOTE_HEAD" ]; then
    ok "Local e remoto estao sincronizados"
  elif [ -n "$REMOTE_HEAD" ]; then
    warn "Local e remoto estao DESSINCRONIZADOS"
    warn "  Local:  $LOCAL"
    warn "  Remote: $REMOTE_HEAD"
  fi
else
  warn "Nenhum remote configurado"
fi

# ── 7. GPG key backup check ──
header "7. Backup da chave GPG"

BACKUP_PATH="c:/Users/Dell/Downloads/gpg-key-manaca-ale.asc"
if [ -f "$BACKUP_PATH" ]; then
  ok "Backup encontrado: $BACKUP_PATH"
else
  warn "Backup NAO encontrado em $BACKUP_PATH"
  warn "Exporte com: gpg --export-secret-keys --armor contato@manaca.tech > gpg-key-manaca-ale.asc"
fi

# ── Summary ──
header "Resumo"

if [ "$ERRORS" -eq 0 ]; then
  echo -e "  ${GREEN}Tudo OK — $ENCRYPTED arquivo(s) criptografado(s), sem erros.${NC}"
else
  echo -e "  ${RED}$ERRORS erro(s) encontrado(s). Verifique os itens acima.${NC}"
fi

exit $ERRORS
```

## Interpreting Results

- **Green ✓** — check passed
- **Yellow ⚠** — warning, non-critical
- **Red ✗** — error, action required

Exit code equals the number of errors found (0 = all OK).

## Common Fixes

- **git-crypt not found:** `scoop install git-crypt`
- **No GPG private key:** `gpg --import gpg-key-manaca-ale.asc`
- **Desynchronized:** `git push` or `git pull` from the Envs directory
- **Missing backup:** `gpg --export-secret-keys --armor contato@manaca.tech > gpg-key-manaca-ale.asc`
