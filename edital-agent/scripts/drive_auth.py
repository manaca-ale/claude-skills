"""Shared OAuth helper for Drive/Docs/Sheets scripts.

Loads token from the Envs repo (see skill `google-drive-envs` for provisioning).
All edital-agent Drive scripts import `get_creds()` from here.
"""
import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

TOKEN_PATH = "C:/secrets/Envs/Drive/Drive/token_sheets.json"


def get_creds():
    """Load OAuth credentials from the Envs repo, refreshing if expired."""
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
    return creds
