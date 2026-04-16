"""Upload edital artifacts to Google Drive (generic template).

Creates (or reuses) a subfolder `NN. <Nome do Edital>` inside the year folder
and uploads files listed in a manifest JSON. Supports MD -> Google Doc conversion
and subfolder organization.

Usage:
    python upload_to_drive.py \\
        --year-folder-id 1TsyJds0lk_wNuZURZPbaqmptPzNzxDN_ \\
        --edital-name "Lab Procel II" \\
        --manifest manifest.json

Manifest JSON schema:
    [
      {
        "local_path": "c:/Editais/editais/lab-procel/CVs.pdf",
        "drive_name": "CVs-Equipe.pdf",
        "mime": "application/pdf",
        "convert_to_gdoc": false,
        "subfolder": null  // or "1. UPLOADS para a plataforma"
      },
      ...
    ]

Idempotent: if file with same name exists in the target folder, updates it
instead of creating a duplicate.
"""
import argparse
import json
import sys
from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Import from the same directory
sys.path.insert(0, str(Path(__file__).parent))
from drive_auth import get_creds


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
        print(f"[FOUND]  Folder '{name}' -> {hits[0]['id']}")
        return hits[0]["id"]
    body = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    created = drive.files().create(body=body, fields="id", supportsAllDrives=True).execute()
    print(f"[CREATE] Folder '{name}' -> {created['id']}")
    return created["id"]


def find_existing_file(drive, name, parent_id):
    q = f"'{parent_id}' in parents and name='{name}' and trashed=false"
    r = drive.files().list(
        q=q, fields="files(id,name,mimeType)", pageSize=5,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    hits = r.get("files", [])
    return hits[0] if hits else None


def upload_one(drive, local_path, drive_name, mime, convert, folder_id):
    local_path = Path(local_path)
    if not local_path.exists():
        print(f"[SKIP]   Missing: {local_path}")
        return None
    existing = find_existing_file(drive, drive_name, folder_id)
    media = MediaFileUpload(str(local_path), mimetype=mime, resumable=False)
    if existing:
        updated = drive.files().update(
            fileId=existing["id"],
            media_body=media,
            fields="id,name,webViewLink,mimeType",
            supportsAllDrives=True,
        ).execute()
        print(f"[UPDATE] {drive_name} -> {updated['webViewLink']}")
        return updated
    body = {"name": drive_name, "parents": [folder_id]}
    if convert:
        body["mimeType"] = "application/vnd.google-apps.document"
    created = drive.files().create(
        body=body, media_body=media, fields="id,name,webViewLink,mimeType",
        supportsAllDrives=True,
    ).execute()
    print(f"[CREATE] {drive_name} -> {created['webViewLink']}")
    return created


def resolve_edital_folder(drive, year_folder_id, edital_name):
    """Find existing `<NN>. <edital_name>` folder (fuzzy) or create next NN."""
    q = (
        f"'{year_folder_id}' in parents and "
        f"mimeType='application/vnd.google-apps.folder' and "
        f"name contains '{edital_name}' and trashed=false"
    )
    r = drive.files().list(
        q=q, fields="files(id,name)", pageSize=10,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    hits = r.get("files", [])
    if hits:
        return hits[0]["id"], hits[0]["name"]
    # Count existing NN. subfolders to pick next prefix
    all_folders = drive.files().list(
        q=(
            f"'{year_folder_id}' in parents and "
            f"mimeType='application/vnd.google-apps.folder' and trashed=false"
        ),
        fields="files(id,name)", orderBy="name", pageSize=100,
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute().get("files", [])
    next_nn = len(all_folders) + 1
    folder_name = f"{next_nn:02d}. {edital_name}"
    folder_id = find_or_create_folder(drive, folder_name, year_folder_id)
    return folder_id, folder_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year-folder-id", required=True, help="Drive folder ID of the year (e.g. 2026)")
    parser.add_argument("--edital-name", required=True, help="Display name of the edital (e.g. 'Lab Procel II')")
    parser.add_argument("--manifest", required=True, help="Path to manifest JSON")
    args = parser.parse_args()

    creds = get_creds()
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    with open(args.manifest) as f:
        manifest = json.load(f)

    folder_id, folder_name = resolve_edital_folder(drive, args.year_folder_id, args.edital_name)
    print(f"\n== Edital folder: '{folder_name}' ({folder_id}) ==\n")

    subfolder_cache = {}

    def get_subfolder(name):
        if name not in subfolder_cache:
            subfolder_cache[name] = find_or_create_folder(drive, name, folder_id)
        return subfolder_cache[name]

    results = []
    for entry in manifest:
        sub = entry.get("subfolder")
        target = get_subfolder(sub) if sub else folder_id
        r = upload_one(
            drive,
            entry["local_path"],
            entry["drive_name"],
            entry.get("mime") or "application/octet-stream",
            entry.get("convert_to_gdoc", False),
            target,
        )
        if r:
            r["_subfolder"] = sub or ""
            results.append(r)

    print("\n=== SUMMARY ===")
    print(f"Folder URL: https://drive.google.com/drive/folders/{folder_id}")
    for r in results:
        sub_label = f"[{r['_subfolder']}] " if r.get("_subfolder") else ""
        print(f"  {sub_label}{r['name']}: {r['webViewLink']}")

    payload = {
        "folder_id": folder_id,
        "folder_name": folder_name,
        "folder_url": f"https://drive.google.com/drive/folders/{folder_id}",
        "files": [
            {"name": r["name"], "url": r["webViewLink"], "id": r["id"], "subfolder": r.get("_subfolder", "")}
            for r in results
        ],
    }
    print("\nPAYLOAD_JSON=" + json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
