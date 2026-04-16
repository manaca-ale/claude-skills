"""Refresh content of existing Google Docs from local MD files.

Preserves the Drive fileId (and therefore the existing share link) while
replacing the document body. Useful when you need to update content after
corrections (e.g. PT-BR accent fixes) without breaking links already pasted
in ClickUp / STATUS.md / email threads.

Usage:
    python update_docs_content.py --manifest update_manifest.json

Manifest JSON schema:
    [
      {
        "local_md": "c:/Editais/editais/lab-procel/00-caderno-preenchimento.md",
        "drive_name": "00. COMECE AQUI - Caderno de Preenchimento",
        "parent_folder_id": "1VoVwilqxh7c-kz2IXjMcSpy44idmEKrM"
      },
      ...
    ]
"""
import argparse
import json
import sys
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

sys.path.insert(0, str(Path(__file__).parent))
from drive_auth import get_creds


def find_file(drive, name, parent_id):
    q = f"'{parent_id}' in parents and name='{name}' and trashed=false"
    r = drive.files().list(
        q=q, fields="files(id,name,mimeType,webViewLink)", pageSize=5,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    hits = r.get("files", [])
    return hits[0] if hits else None


def update_doc(drive, local_md, drive_name, parent_id):
    local_path = Path(local_md)
    if not local_path.exists():
        print(f"[SKIP]   Missing local: {local_path}")
        return None
    existing = find_file(drive, drive_name, parent_id)
    if not existing:
        print(f"[MISS]   '{drive_name}' not found in parent {parent_id}")
        return None
    media = MediaFileUpload(str(local_path), mimetype="text/markdown", resumable=False)
    updated = drive.files().update(
        fileId=existing["id"], media_body=media,
        fields="id,name,webViewLink,mimeType",
        supportsAllDrives=True,
    ).execute()
    print(f"[UPDATE] '{drive_name}' -> {updated['webViewLink']}")
    return updated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON")
    args = parser.parse_args()

    creds = get_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    with open(args.manifest) as f:
        entries = json.load(f)

    for e in entries:
        update_doc(drive, e["local_md"], e["drive_name"], e["parent_folder_id"])


if __name__ == "__main__":
    main()
