#!/usr/bin/env python3
"""ClickUp integration for edital-agent skill.

Syncs edital tasks between ClickUp and local STATUS.md files.
Always uses Python requests for proper UTF-8 encoding.

Usage:
    python clickup_edital_sync.py list
    python clickup_edital_sync.py get <task_id>
    python clickup_edital_sync.py links <task_id>
    python clickup_edital_sync.py status <task_id> <new_status>
    python clickup_edital_sync.py comment <task_id> <text>
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from urllib.parse import urlparse

# Force UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

# ClickUp IDs (Manaca workspace)
WORKSPACE_ID = "90132913705"
SPACE_MANACA_ID = "901312961048"
FOLDER_CAPTACAO_ID = "901316670330"
LIST_EDITAIS_ID = "901324801079"

# Credentials
REPO_DIR = "C:/secrets/Envs"
ENV_FILE = os.path.join(REPO_DIR, "envclickuptelegram")
BASE_URL = "https://api.clickup.com/api/v2"

# Status mapping: ClickUp status -> edital-agent phase
STATUS_MAP = {
    "a fazer": "Pre-triagem",
    "claude": "Em producao (fases 1-5)",
    "revisao": "Fase 6 (Quality Review)",
    "subir para o drive": "Fase 5e -> Drive",
    "em andamento": "Ativo (equipe humana)",
    "parado": "Bloqueado",
    "complete": "Concluido",
    "cancelled": "Cancelado",
}


def _add_scoop_to_path():
    """Ensure scoop shims are on PATH (for git-crypt on Windows)."""
    scoop_shims = os.path.expanduser("~/scoop/shims")
    if os.path.isdir(scoop_shims) and scoop_shims not in os.environ.get("PATH", ""):
        os.environ["PATH"] = scoop_shims + os.pathsep + os.environ.get("PATH", "")


def ensure_envs_repo():
    """Clone and unlock the Envs repo if credentials are missing."""
    _add_scoop_to_path()

    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        os.makedirs(os.path.dirname(REPO_DIR), exist_ok=True)
        subprocess.run(
            ["git", "clone", "https://github.com/manaca-ale/Envs.git", REPO_DIR],
            capture_output=True, text=True, check=True,
        )

    needs_unlock = False
    if not os.path.exists(ENV_FILE):
        needs_unlock = True
    else:
        with open(ENV_FILE, "rb") as f:
            header = f.read(16)
            if b"\x00GITCRYPT" in header:
                needs_unlock = True

    if needs_unlock:
        subprocess.run(
            ["git-crypt", "unlock"], cwd=REPO_DIR,
            capture_output=True, text=True, check=True,
        )


def load_token():
    """Load ClickUp access token from the env file."""
    ensure_envs_repo()
    with open(ENV_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("CLICKUP_ACCESS_TOKEN="):
                return line.split("=", 1)[1]
    print("ERROR: CLICKUP_ACCESS_TOKEN not found in env file.")
    sys.exit(1)


def api_get(path, token, params=None):
    """GET request to ClickUp API."""
    r = requests.get(
        f"{BASE_URL}{path}",
        headers={"Authorization": token},
        params=params or {},
    )
    r.raise_for_status()
    return r.json()


def api_put(path, token, data):
    """PUT request to ClickUp API."""
    r = requests.put(
        f"{BASE_URL}{path}",
        headers={"Authorization": token, "Content-Type": "application/json"},
        json=data,
    )
    r.raise_for_status()
    return r.json()


def api_post(path, token, data):
    """POST request to ClickUp API (UTF-8 safe)."""
    r = requests.post(
        f"{BASE_URL}{path}",
        headers={"Authorization": token, "Content-Type": "application/json"},
        json=data,
    )
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def list_editais(token):
    """List all active edital tasks from ClickUp."""
    data = api_get(
        f"/list/{LIST_EDITAIS_ID}/task",
        token,
        params={"archived": "false", "include_closed": "false"},
    )
    tasks = data.get("tasks", [])
    print(f"Editais ativos: {len(tasks)}\n")
    print(f"{'ID':<12} {'Status':<20} {'Prazo':<14} {'Prior.':<8} {'Nome'}")
    print("-" * 90)

    for t in sorted(tasks, key=lambda x: int(x.get("due_date") or "9999999999999")):
        status = t.get("status", {}).get("status", "?")
        priority = (t.get("priority") or {}).get("priority", "-")
        due = t.get("due_date")
        if due:
            due_dt = datetime.fromtimestamp(int(due) / 1000)
            days = (due_dt - datetime.now()).days
            due_str = f"{due_dt.strftime('%d/%m/%Y')} ({days}d)"
        else:
            due_str = "sem prazo"
        print(f"{t['id']:<12} {status:<20} {due_str:<14} {priority:<8} {t['name']}")


def get_edital(token, task_id):
    """Get full edital task details."""
    t = api_get(
        f"/task/{task_id}",
        token,
        params={"include_markdown_description": "true"},
    )
    due = t.get("due_date")
    due_str = "sem prazo"
    if due:
        due_dt = datetime.fromtimestamp(int(due) / 1000)
        days = (due_dt - datetime.now()).days
        due_str = f"{due_dt.strftime('%d/%m/%Y')} ({days}d)"

    print(f"Nome: {t['name']}")
    print(f"ID: {t['id']}")
    print(f"Status: {t.get('status', {}).get('status', '?')}")
    print(f"Prioridade: {(t.get('priority') or {}).get('priority', '-')}")
    print(f"Prazo: {due_str}")
    print(f"URL: {t.get('url', '')}")

    assignees = [a.get("username", "?") for a in t.get("assignees", [])]
    if assignees:
        print(f"Responsaveis: {', '.join(assignees)}")

    tags = [tag.get("name", "") for tag in t.get("tags", [])]
    if tags:
        print(f"Tags: {', '.join(tags)}")

    md = t.get("markdown_description", "")
    if md:
        print(f"\nMarkdown description:\n{md}")

    desc = t.get("description", "")
    if desc:
        print(f"\nDescription:\n{desc}")

    attachments = t.get("attachments", [])
    if attachments:
        print(f"\nAnexos ({len(attachments)}):")
        for a in attachments:
            print(f"  - {a.get('title', '?')}: {a.get('url', '')}")


def extract_links(token, task_id):
    """Extract and categorize links from task markdown_description and attachments."""
    t = api_get(
        f"/task/{task_id}",
        token,
        params={"include_markdown_description": "true"},
    )

    md = t.get("markdown_description", "")
    attachments = t.get("attachments", [])

    # Extract URLs from markdown
    url_pattern = re.compile(r'https?://[^\s\)\]\"\'<>]+')
    raw_urls = url_pattern.findall(md)

    # Deduplicate
    seen = set()
    urls = []
    for u in raw_urls:
        u_clean = u.rstrip("/.,;:)")
        if u_clean not in seen:
            seen.add(u_clean)
            urls.append(u_clean)

    # Categorize
    result = {
        "google_docs": [],
        "google_forms": [],
        "google_sheets": [],
        "pdfs": [],
        "attachments": [],
        "other": [],
    }

    for url in urls:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        path = parsed.path.lower()

        if "docs.google.com" in host and "/document/" in path:
            result["google_docs"].append(url)
        elif "docs.google.com" in host and "/forms/" in path:
            result["google_forms"].append(url)
        elif ("docs.google.com" in host and "/spreadsheets/" in path) or \
             ("docs.google.com" in host and "/spreadsheet/" in path):
            result["google_sheets"].append(url)
        elif path.endswith(".pdf"):
            result["pdfs"].append(url)
        else:
            result["other"].append(url)

    # Add ClickUp attachments
    for a in attachments:
        result["attachments"].append({
            "title": a.get("title", "?"),
            "url": a.get("url", ""),
            "type": a.get("type", ""),
        })

    # Print results
    print(f"Links extraidos da tarefa '{t['name']}':\n")
    for category, items in result.items():
        if items:
            print(f"  {category}:")
            for item in items:
                if isinstance(item, dict):
                    print(f"    - {item['title']}: {item['url']}")
                else:
                    print(f"    - {item}")
    print()

    if not any(result.values()):
        print("  Nenhum link ou anexo encontrado.")

    return result


def update_status(token, task_id, new_status):
    """Update task status in ClickUp."""
    t = api_put(f"/task/{task_id}", token, {"status": new_status})
    print(f"Status atualizado: {t['name']} -> {t.get('status', {}).get('status', '?')}")


def add_comment(token, task_id, text):
    """Add a UTF-8 safe comment to a task."""
    r = api_post(f"/task/{task_id}/comment", token, {"comment_text": text})
    print(f"Comentario adicionado (ID: {r.get('id', '?')})")


def create_edital(token, name, due_date=None, tags=None):
    """Create a new edital task in the Editais list."""
    data = {"name": name}
    if due_date:
        # Parse dd/mm/yyyy to timestamp
        dt = datetime.strptime(due_date, "%d/%m/%Y")
        data["due_date"] = int(dt.timestamp() * 1000)
    if tags:
        data["tags"] = tags

    t = api_post(f"/list/{LIST_EDITAIS_ID}/task", token, data)
    print(f"Edital criado: {t['name']} (ID: {t['id']})")
    print(f"URL: {t.get('url', '')}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    token = load_token()
    cmd = sys.argv[1]

    if cmd == "list":
        list_editais(token)
    elif cmd == "get" and len(sys.argv) >= 3:
        get_edital(token, sys.argv[2])
    elif cmd == "links" and len(sys.argv) >= 3:
        extract_links(token, sys.argv[2])
    elif cmd == "status" and len(sys.argv) >= 4:
        update_status(token, sys.argv[2], sys.argv[3])
    elif cmd == "comment" and len(sys.argv) >= 4:
        add_comment(token, sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "create" and len(sys.argv) >= 3:
        due = sys.argv[3] if len(sys.argv) >= 4 else None
        create_edital(token, sys.argv[2], due)
    else:
        print(f"Comando desconhecido ou args faltando: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
