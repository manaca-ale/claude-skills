"""Reorganize an edital Drive folder into the standard 4-subfolder layout.

Standard layout (from SKILL.md Google Drive section):
  <NN>. <Edital>/
    00. COMECE AQUI - Caderno de Preenchimento.gdoc  (master doc — uploaded elsewhere)
    1. UPLOADS para a plataforma/
    2. DRAFTS para transcrever e assinar/
    3. REFERENCIA/
    4. POS-PRE-HABILITACAO/

Usage:
    python reorganize_drive.py \\
        --folder-id 1VoVwilqxh7c-kz2IXjMcSpy44idmEKrM \\
        --move-map move_map.json

Move-map JSON schema (optional; if omitted, only creates empty subfolders):
    [
      {"current_name": "CVs.pdf", "new_name": "CVs.pdf", "target_subfolder": "1. UPLOADS para a plataforma"},
      ...
    ]

Idempotent: if file already lives in target subfolder with correct name, skips.
"""
import argparse
import json
import sys
from pathlib import Path

from googleapiclient.discovery import build

sys.path.insert(0, str(Path(__file__).parent))
from drive_auth import get_creds

DEFAULT_SUBFOLDERS = [
    "1. UPLOADS para a plataforma",
    "2. DRAFTS para transcrever e assinar",
    "3. REFERENCIA",
    "4. POS-PRE-HABILITACAO",
]


def find_or_create_folder(drive, name, parent_id):
    q = (
        f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' "
        f"and name='{name}' and trashed=false"
    )
    r = drive.files().list(
        q=q, fields="files(id,name)", pageSize=5,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    hits = r.get("files", [])
    if hits:
        print(f"[FOUND]  Subfolder '{name}'")
        return hits[0]["id"]
    body = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    created = drive.files().create(body=body, fields="id", supportsAllDrives=True).execute()
    print(f"[CREATE] Subfolder '{name}' -> {created['id']}")
    return created["id"]


def find_file(drive, name, parent_id):
    q = f"'{parent_id}' in parents and name='{name}' and trashed=false"
    r = drive.files().list(
        q=q, fields="files(id,name,parents)", pageSize=5,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    hits = r.get("files", [])
    return hits[0] if hits else None


def move_and_rename(drive, file_id, current_parents, new_parent_id, new_name, old_name):
    remove_parents = ",".join(current_parents)
    body = {}
    if new_name != old_name:
        body["name"] = new_name
    drive.files().update(
        fileId=file_id,
        body=body if body else None,
        addParents=new_parent_id,
        removeParents=remove_parents,
        fields="id,name,parents",
        supportsAllDrives=True,
    ).execute()
    print(f"[MOVE]   '{old_name}' -> '{new_name}'")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder-id", required=True, help="Drive folder ID of the edital (<NN>. <Name>)")
    parser.add_argument("--move-map", help="Optional JSON with list of {current_name, new_name, target_subfolder}")
    parser.add_argument(
        "--layout", nargs="+", default=DEFAULT_SUBFOLDERS,
        help="Override subfolder names (defaults to 4-subfolder standard)",
    )
    args = parser.parse_args()

    creds = get_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    subfolder_ids = {}
    for name in args.layout:
        subfolder_ids[name] = find_or_create_folder(drive, name, args.folder_id)

    if not args.move_map:
        print("\nNo move-map provided; only created subfolders.")
        print(f"Folder URL: https://drive.google.com/drive/folders/{args.folder_id}")
        return

    with open(args.move_map) as f:
        moves = json.load(f)

    for m in moves:
        old_name = m["current_name"]
        new_name = m["new_name"]
        target = m["target_subfolder"]
        if target not in subfolder_ids:
            print(f"[WARN]   Unknown target subfolder '{target}' for '{old_name}'")
            continue
        target_id = subfolder_ids[target]
        existing = find_file(drive, old_name, args.folder_id)
        if existing is None:
            existing = find_file(drive, new_name, target_id)
            if existing:
                print(f"[SKIP]   '{new_name}' already in '{target}'")
                continue
            print(f"[MISS]   '{old_name}' not found")
            continue
        current_parents = existing.get("parents", [args.folder_id])
        move_and_rename(drive, existing["id"], current_parents, target_id, new_name, old_name)

    print("\n=== SUMMARY ===")
    print(f"Folder URL: https://drive.google.com/drive/folders/{args.folder_id}")
    for name, fid in subfolder_ids.items():
        print(f"  {name}: https://drive.google.com/drive/folders/{fid}")


if __name__ == "__main__":
    main()
