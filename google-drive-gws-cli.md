---
name: google-drive-gws-cli
description: "Operate Google Drive from terminal using `gws` (`@googleworkspace/cli`): install and verify CLI, configure OAuth (`gws auth setup` or `gws auth login`), inspect method schemas (`gws schema drive.resource.method`), and execute Drive commands for files, folders, shared drives, and permissions. Use when the user asks to list, search, upload, download, share, move, copy, or delete Drive items with this CLI."
---

# Google Drive Gws Cli

Use this skill whenever the user explicitly wants to operate Google Drive with the `gws` CLI.
Apply the lessons learned below by default.

## Quick Start

Run the preflight helper first:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/gws-drive-preflight.ps1 -CheckAuth
```

If `gws` is missing, install it:

```bash
npm install -g @googleworkspace/cli
```

Authenticate and verify:

```bash
gws auth setup
gws auth login -s drive
gws drive files list --params '{"pageSize": 5, "q": "trashed=false"}'
```

Check auth status:

```bash
gws auth status
gws auth list
```

## Workflow

1. Classify operation as read-only or write/delete.
2. Inspect method schema before building command:

```bash
gws schema drive.files.list
gws schema drive.files.create
```

3. Build command using explicit `--params` and `--json`.
4. Confirm with user before write/delete commands.
5. After write/delete, run a read-back verification and report resulting IDs/status.
6. When the task is Google Docs content editing, prefer native Google Docs structures (headings, tables, lists) over markdown-like text formatting.

## Command Patterns

Base syntax:

```bash
gws drive <resource> <method> --params '{"key":"value"}' --json '{"key":"value"}'
```

Global flags to prefer:
- `--format json|table|yaml|csv`
- `--dry-run` for risky changes
- `--page-all` for long listings
- `--upload <PATH>` for multipart create/update
- `--output <PATH>` for download/export
- `--account <EMAIL>` for account override

## Safety Rules

- Always confirm before `create`, `update`, `delete`, `copy`, `move`, `permissions.create`, `permissions.update`, and `emptyTrash`.
- Prefer `files.list` or `files.get` before mutating anything.
- Use `q: "trashed=false"` in list/search unless user asks for trash.
- Never expose credential files, tokens, or raw secrets in outputs.
- For Google Docs updates: never insert markdown table syntax (`| col |`) as plain text when a table is requested. Use native table elements.

## Session Learnings

- If login fails with `401 invalid_client`, validate `~/.config/gws/client_secret.json`.
- `client_id` must end with `.apps.googleusercontent.com` and must not equal `client_secret`.
- `gws auth setup` can require manual OAuth consent/client creation in Google Cloud Console, then run `gws auth login`.
- If `gws auth list` is empty, authentication was not completed.
- On some PowerShell environments (`gws 0.4.4`), `--params`/`--json` may fail with `Invalid --params JSON`. In this case:
  1. Re-check command shape with `gws schema ...`.
  2. Prefer helper commands when available (`gws docs +write`, `gws drive +upload`).
  3. If still blocked, use the Google Workspace MCP tools to complete Docs/Drive operations without markdown degradation.

## Helper Scripts

- `scripts/gws-drive-preflight.ps1`: check `node`, `npm`, `gws`, optional auth status.
- `scripts/gws-drive-list.ps1`: run a safe default listing with filters and pagination.

## References

- [references/drive-operations.md](references/drive-operations.md)
