---
name: google-drive-envs
description: Access Google Drive and Sheets APIs using OAuth credentials stored in the encrypted Envs repo (manaca-ale/Envs). This skill should be used when the user asks to interact with Google Drive files, list/create/share documents, or operate Google Sheets — and needs the credentials from the Envs repo.
---

# Google Drive & Sheets Access (Envs Repo)

Operate Google Drive and Sheets APIs using OAuth credentials stored in the encrypted Envs repository.

## Credentials

| File | Path (Envs repo) | Purpose |
|------|-------------------|---------|
| Client Secret | `C:/secrets/Envs/Drive/Drive/client_secret_2_581712092014-*.json` | OAuth app identity |
| Token | `C:/secrets/Envs/Drive/Drive/token_sheets.json` | Authenticated token (Sheets + Drive scopes) |

**GCP Project:** `stone-victor-365916`
**Scopes:** `spreadsheets`, `drive`
**Owner email:** `alecoleto@gmail.com`

## Auto-Setup

The helper script automatically clones and unlocks the Envs repo if credentials are missing. Requirements:
- `git` and `git-crypt` installed (Windows: `scoop install git-crypt`)
- GPG private key imported (`gpg --import gpg-key-manaca-ale.asc`)
- GitHub access to `manaca-ale/Envs` (private repo)

## Authentication Helper

Save the script below as `drive_auth.py` and run:

```bash
# Validate credentials
python drive_auth.py check

# List recent files
python drive_auth.py list-files

# Search files by name
python drive_auth.py search "nome do arquivo"
```

### drive_auth.py

```python
#!/usr/bin/env python3
"""Google Drive/Sheets authentication helper using Envs repo credentials."""

import json
import os
import subprocess
import sys

REPO_URL = "https://github.com/manaca-ale/Envs.git"
REPO_DIR = "C:/secrets/Envs"
TOKEN_PATH = os.path.join(REPO_DIR, "Drive/Drive/token_sheets.json")
CLIENT_SECRET_DIR = os.path.join(REPO_DIR, "Drive/Drive")


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
    if not os.path.exists(TOKEN_PATH):
        needs_unlock = True
    else:
        with open(TOKEN_PATH, "rb") as f:
            header = f.read(16)
            if b"\x00GITCRYPT" in header:
                needs_unlock = True

    if needs_unlock:
        print("Files are encrypted. Running git-crypt unlock...")
        _run(["git-crypt", "unlock"], cwd=REPO_DIR)
        print("Unlock complete.")


def get_creds():
    """Load and refresh credentials from the Envs repo token file."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    ensure_envs_repo()

    with open(TOKEN_PATH) as f:
        try:
            token_data = json.load(f)
        except json.JSONDecodeError:
            print("ERROR: Token file is not valid JSON even after unlock.")
            print("Token may be corrupted. Re-authenticate by running create_sheets.py")
            sys.exit(1)

    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes"),
    )

    if creds.expired and creds.refresh_token:
        print("Token expired, refreshing...")
        creds.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
        print("Token refreshed and saved.")

    return creds


def check():
    """Validate credentials and print status."""
    creds = get_creds()
    print(f"Token valid: {creds.valid}")
    print(f"Token expired: {creds.expired}")
    print(f"Scopes: {creds.scopes}")
    print(f"Client ID: {creds.client_id[:20]}...")

    from googleapiclient.discovery import build
    drive = build("drive", "v3", credentials=creds)
    about = drive.about().get(fields="user").execute()
    print(f"Authenticated as: {about['user']['emailAddress']}")


def list_files(page_size=20):
    """List recent files in Google Drive."""
    from googleapiclient.discovery import build
    creds = get_creds()
    drive = build("drive", "v3", credentials=creds)
    results = drive.files().list(
        pageSize=page_size,
        fields="files(id, name, mimeType, modifiedTime)",
        orderBy="modifiedTime desc",
    ).execute()
    files = results.get("files", [])
    if not files:
        print("No files found.")
        return
    print(f"{'Name':<50} {'Type':<30} {'Modified':<25} {'ID'}")
    print("-" * 130)
    for f in files:
        print(f"{f['name'][:49]:<50} {f['mimeType'][:29]:<30} {f.get('modifiedTime','')[:24]:<25} {f['id']}")


def search_files(query):
    """Search files by name in Google Drive."""
    from googleapiclient.discovery import build
    creds = get_creds()
    drive = build("drive", "v3", credentials=creds)
    results = drive.files().list(
        q=f"name contains '{query}'",
        pageSize=20,
        fields="files(id, name, mimeType, modifiedTime)",
    ).execute()
    files = results.get("files", [])
    if not files:
        print(f"No files matching '{query}'.")
        return
    print(f"{'Name':<50} {'Type':<30} {'ID'}")
    print("-" * 100)
    for f in files:
        print(f"{f['name'][:49]:<50} {f['mimeType'][:29]:<30} {f['id']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: drive_auth.py <command> [args]")
        print("Commands: check, list-files, search <query>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "check":
        check()
    elif cmd == "list-files":
        list_files()
    elif cmd == "search" and len(sys.argv) >= 3:
        search_files(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Python Direct Usage

```python
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = "C:/secrets/Envs/Drive/Drive/token_sheets.json"

with open(TOKEN_PATH) as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data["refresh_token"],
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"],
)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Drive
drive = build("drive", "v3", credentials=creds)
results = drive.files().list(pageSize=20, fields="files(id, name, mimeType)").execute()

# Sheets
sheets = build("sheets", "v4", credentials=creds)
```

## Token Refresh

The token auto-refreshes when expired. If refresh fails, re-authenticate by running:

```bash
python "C:/secrets/Envs/Drive/Drive/create_sheets.py"
```
