---
name: clickup-api
description: Access the ClickUp API using the Personal API Token stored in the encrypted Envs repo (envclickuptelegram). This skill should be used when the user asks to interact with ClickUp — list spaces, folders, lists, tasks, create/update tasks, or query ClickUp data.
---

# ClickUp API Access (Envs Repo)

Operate the ClickUp API using credentials from the encrypted Envs repository.

## Credentials

| Key | Source | Value Location |
|-----|--------|---------------|
| `CLICKUP_ACCESS_TOKEN` | `C:/secrets/Envs/envclickuptelegram` | Personal API Token |

**Token format:** `pk_272475891_...`
**API base URL:** `https://api.clickup.com/api/v2`

## Auto-Setup

The helper script automatically clones and unlocks the Envs repo if credentials are missing. Requirements:
- `git` and `git-crypt` installed (Windows: `scoop install git-crypt`)
- GPG private key imported (`gpg --import gpg-key-manaca-ale.asc`)
- GitHub access to `manaca-ale/Envs` (private repo)

## Helper Script

Save the script below as `clickup_api.py` and run:

```bash
# Check auth and list workspaces
python clickup_api.py check

# List spaces in a workspace
python clickup_api.py spaces

# List folders in a space
python clickup_api.py folders <space_id>

# List tasks in a list
python clickup_api.py tasks <list_id>

# Get task details
python clickup_api.py task <task_id>
```

### clickup_api.py

```python
#!/usr/bin/env python3
"""ClickUp API helper using token from Envs repo."""

import json
import os
import subprocess
import sys
import requests

REPO_URL = "https://github.com/manaca-ale/Envs.git"
REPO_DIR = "C:/secrets/Envs"
ENV_FILE = os.path.join(REPO_DIR, "envclickuptelegram")
BASE_URL = "https://api.clickup.com/api/v2"


def _run(cmd, **kwargs):
    """Run a shell command and return stdout."""
    result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        if result.stderr:
            print(result.stderr.strip())
        sys.exit(1)
    return result.stdout.strip()


def _add_scoop_to_path():
    """Ensure scoop shims are on PATH (for git-crypt on Windows)."""
    scoop_shims = os.path.expanduser("~/scoop/shims")
    if os.path.isdir(scoop_shims) and scoop_shims not in os.environ.get("PATH", ""):
        os.environ["PATH"] = scoop_shims + os.pathsep + os.environ.get("PATH", "")


def ensure_envs_repo():
    """Clone and unlock the Envs repo if files are not available."""
    _add_scoop_to_path()

    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        print(f"Envs repo not found at {REPO_DIR}. Cloning...")
        os.makedirs(os.path.dirname(REPO_DIR), exist_ok=True)
        _run(["git", "clone", REPO_URL, REPO_DIR])
        print("Clone complete.")

    needs_unlock = False
    if not os.path.exists(ENV_FILE):
        needs_unlock = True
    else:
        with open(ENV_FILE, "rb") as f:
            header = f.read(16)
            if b"\x00GITCRYPT" in header:
                needs_unlock = True

    if needs_unlock:
        print("Files are encrypted. Running git-crypt unlock...")
        _run(["git-crypt", "unlock"], cwd=REPO_DIR)
        print("Unlock complete.")


def load_token():
    """Load ClickUp access token from the env file."""
    ensure_envs_repo()

    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("CLICKUP_ACCESS_TOKEN="):
                return line.split("=", 1)[1]

    print("ERROR: CLICKUP_ACCESS_TOKEN not found in env file.")
    sys.exit(1)


def api_get(path, token):
    """Make a GET request to the ClickUp API."""
    r = requests.get(f"{BASE_URL}{path}", headers={"Authorization": token})
    r.raise_for_status()
    return r.json()


def check(token):
    """Validate token and list workspaces."""
    data = api_get("/team", token)
    teams = data.get("teams", [])
    if not teams:
        print("ERROR: No workspaces found. Token may be invalid.")
        sys.exit(1)
    print(f"Authenticated! Found {len(teams)} workspace(s):\n")
    for t in teams:
        print(f"  ID: {t['id']}  Name: {t['name']}  Members: {len(t.get('members', []))}")


def spaces(token):
    """List spaces in the first workspace."""
    teams = api_get("/team", token)["teams"]
    if not teams:
        print("No workspaces found.")
        return
    team_id = teams[0]["id"]
    data = api_get(f"/team/{team_id}/space?archived=false", token)
    spaces_list = data.get("spaces", [])
    print(f"Spaces in workspace '{teams[0]['name']}':\n")
    for s in spaces_list:
        print(f"  ID: {s['id']}  Name: {s['name']}")


def folders(token, space_id):
    """List folders in a space."""
    data = api_get(f"/space/{space_id}/folder?archived=false", token)
    folders_list = data.get("folders", [])
    if not folders_list:
        print("No folders found.")
        return
    print(f"Folders in space {space_id}:\n")
    for f in folders_list:
        lists = f.get("lists", [])
        print(f"  ID: {f['id']}  Name: {f['name']}  Lists: {len(lists)}")
        for lst in lists:
            print(f"    └─ List ID: {lst['id']}  Name: {lst['name']}")


def tasks(token, list_id):
    """List tasks in a list."""
    data = api_get(f"/list/{list_id}/task?archived=false", token)
    tasks_list = data.get("tasks", [])
    if not tasks_list:
        print("No tasks found.")
        return
    print(f"Tasks in list {list_id}:\n")
    print(f"{'ID':<12} {'Status':<15} {'Name'}")
    print("-" * 60)
    for t in tasks_list:
        status = t.get("status", {}).get("status", "?")
        print(f"{t['id']:<12} {status:<15} {t['name']}")


def task_detail(token, task_id):
    """Get task details."""
    t = api_get(f"/task/{task_id}", token)
    print(f"Task: {t['name']}")
    print(f"ID: {t['id']}")
    print(f"Status: {t.get('status', {}).get('status', '?')}")
    print(f"Priority: {t.get('priority', {}).get('priority', 'none') if t.get('priority') else 'none'}")
    print(f"URL: {t.get('url', '')}")
    if t.get("description"):
        print(f"\nDescription:\n{t['description']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: clickup_api.py <command> [args]")
        print("Commands: check, spaces, folders <space_id>, tasks <list_id>, task <task_id>")
        sys.exit(1)

    token = load_token()
    cmd = sys.argv[1]

    if cmd == "check":
        check(token)
    elif cmd == "spaces":
        spaces(token)
    elif cmd == "folders" and len(sys.argv) >= 3:
        folders(token, sys.argv[2])
    elif cmd == "tasks" and len(sys.argv) >= 3:
        tasks(token, sys.argv[2])
    elif cmd == "task" and len(sys.argv) >= 3:
        task_detail(token, sys.argv[2])
    else:
        print(f"Unknown command or missing args: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/team` | GET | List workspaces |
| `/team/{id}/space` | GET | List spaces |
| `/space/{id}/folder` | GET | List folders |
| `/folder/{id}/list` | GET | List lists |
| `/list/{id}/task` | GET | List tasks |
| `/list/{id}/task` | POST | Create task |
| `/task/{id}` | GET | Get task details |
| `/task/{id}` | PUT | Update task |
| `/task/{id}/comment` | POST | Add comment |

## Related Env Vars (same file)

| Variable | Purpose |
|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot for ClickUp notifications |
| `GOOGLE_API_KEY` | Gemini API key (used by the bot) |
| `GEMINI_MODEL` | Gemini model selection |
| `LLM_PROVIDER` | AI provider (gemini/ollama) |
| `AUTHORIZED_USERS` | Telegram user IDs allowed to use the bot |
