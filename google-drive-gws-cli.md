---
name: google-drive-gws-cli
description: "Operate Google Workspace from terminal using `gws` (`@googleworkspace/cli`): manage Drive, Docs, Sheets, Gmail, Calendar, Admin SDK, People, Forms, Chat, Apps Script, Vault, Classroom, and 25 total services. Use when the user asks to operate any Google Workspace service via CLI."
---

# Google Workspace GWS CLI

Use this skill whenever the user wants to operate any Google Workspace service with the `gws` CLI.
Apply the lessons learned below by default.

## Current Setup

- **CLI:** gws 0.4.4
- **OAuth project:** `stone-victor-365916` (owned by alecoleto@gmail.com)
- **Default account:** `contato@manaca.tech` (Workspace Super Admin, domain manaca.tech)
- **Other account:** `alecoleto@gmail.com`
- **Domain users:** contato@manaca.tech (admin), rayssa@manaca.tech (admin), suporte@manaca.tech
- **Customer ID:** C02qpzwdx

### Active Scopes (27)

drive, spreadsheets, gmail.modify, calendar, documents, presentations, tasks, pubsub, cloud-platform, contacts, directory.readonly, admin.directory.user, admin.directory.group, admin.reports.audit.readonly, admin.reports.usage.readonly, forms, forms.responses.readonly, script.projects, script.processes, chat.spaces, chat.messages, ediscovery, apps.groups.settings, cloud-identity.groups, classroom.courses, classroom.rosters, apps.licensing

### NOT available (APIs not enabled in GCP project)

- **Keep** (`auth/keep`) — enable Google Keep API in `stone-victor-365916`
- **Alert Center** (`auth/apps.alerts`) — enable Alert Center API in `stone-victor-365916`

### Re-authenticate with all scopes

```bash
gws auth login --account contato@manaca.tech --scopes "https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/presentations,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/pubsub,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/contacts,https://www.googleapis.com/auth/directory.readonly,https://www.googleapis.com/auth/admin.directory.user,https://www.googleapis.com/auth/admin.directory.group,https://www.googleapis.com/auth/admin.reports.audit.readonly,https://www.googleapis.com/auth/admin.reports.usage.readonly,https://www.googleapis.com/auth/forms,https://www.googleapis.com/auth/forms.responses.readonly,https://www.googleapis.com/auth/script.projects,https://www.googleapis.com/auth/script.processes,https://www.googleapis.com/auth/chat.spaces,https://www.googleapis.com/auth/chat.messages,https://www.googleapis.com/auth/ediscovery,https://www.googleapis.com/auth/apps.groups.settings,https://www.googleapis.com/auth/cloud-identity.groups,https://www.googleapis.com/auth/classroom.courses,https://www.googleapis.com/auth/classroom.rosters,https://www.googleapis.com/auth/apps.licensing"
```

Then open the URL manually with `start "" "<URL>"` (gws doesn't auto-open browser on this machine).

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
gws schema admin.users.list
gws schema forms.forms.get
```

3. Build command using explicit `--params` and `--json`.
4. Always use `--account contato@manaca.tech` for Workspace operations.
5. Confirm with user before write/delete commands.
6. After write/delete, run a read-back verification and report resulting IDs/status.
7. When the task is Google Docs content editing, prefer native Google Docs structures (headings, tables, lists) over markdown-like text formatting.

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
- On this machine, `gws auth login` does NOT auto-open the browser. Capture the URL from output and open manually with `start "" "<URL>"`.
- The `--full` flag only adds `pubsub` + `cloud-platform` to the default 7 scopes. For Workspace admin scopes (admin, people, forms, chat, etc.), use `--scopes` with explicit comma-separated list.
- Scopes `auth/keep` and `auth/apps.alerts` cause `invalid_scope` error unless their APIs are enabled in the GCP project `stone-victor-365916`.
- On some PowerShell environments (`gws 0.4.4`), `--params`/`--json` may fail with `Invalid --params JSON`. In this case:
  1. Re-check command shape with `gws schema ...`.
  2. Prefer helper commands when available (`gws docs +write`, `gws drive +upload`).
  3. If still blocked, use the Google Workspace MCP tools to complete Docs/Drive operations without markdown degradation.

## Helper Scripts

- `scripts/gws-drive-preflight.ps1`: check `node`, `npm`, `gws`, optional auth status.
- `scripts/gws-drive-list.ps1`: run a safe default listing with filters and pagination.

## References

- [references/drive-operations.md](references/drive-operations.md)
