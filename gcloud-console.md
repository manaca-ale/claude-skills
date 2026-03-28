---
name: gcloud-console
description: "Operate Google Cloud Platform via gcloud CLI for the contato@manaca.tech account. Use when the user asks to manage GCP projects, APIs, IAM, billing, compute, storage, logging, Cloud Run, monitoring, or any other GCP service. This skill should NOT be used for Google Workspace operations (Docs, Sheets, Drive, Gmail) — use gws-cli for those."
---

# Google Cloud Platform — gcloud CLI

Operate any GCP service from the terminal using the `gcloud` CLI. Always specify `--project` explicitly — there is no default project.

## Account

- **Email:** `contato@manaca.tech`
- **CLI:** gcloud (Google Cloud SDK)

## Auth Preflight (run every time)

1. Check for a valid token:

```bash
gcloud auth print-access-token --account=contato@manaca.tech 2>/dev/null && echo "AUTH OK" || echo "AUTH EXPIRED"
```

2. If expired, re-authenticate:

```bash
gcloud auth login contato@manaca.tech
```

This command prompts for the account password directly (no browser). The password is stored in the environment variable `GOOGLE_ACCOUNT_PASSWORD` (loaded from `~/.claude/.env`). Never expose the password in output or logs.

3. After login, verify:

```bash
gcloud auth list
```

Confirm `contato@manaca.tech` is the active account.

## Projects Registry

Always use `--project=<PROJECT_ID>` in every command. Never assume a default.

| Project ID                     | Name                  | Notes            |
|--------------------------------|-----------------------|------------------|
| `gen-lang-client-0028842427`   | Saira                 | Gemini API       |
| `gen-lang-client-0487533939`   | Flora                 | Gemini API       |
| `gen-lang-client-0616161525`   | Teste                 | Gemini API       |
| `manaca-leads-55064`           | Manaca Leads Scraping |                  |
| `manafin`                      | Manafin               |                  |
| `manaleads-tech`               | manaleads             |                  |

To discover or confirm projects:

```bash
gcloud projects list --account=contato@manaca.tech
```

## Operations Cheat Sheet

### Projects

```bash
gcloud projects list
gcloud projects describe <PROJECT_ID>
```

### APIs / Services

```bash
gcloud services list --enabled --project=<PROJECT_ID>
gcloud services list --available --project=<PROJECT_ID> --filter="name:<search>"
gcloud services enable <API_NAME> --project=<PROJECT_ID>
gcloud services disable <API_NAME> --project=<PROJECT_ID>
```

### IAM

```bash
gcloud projects get-iam-policy <PROJECT_ID> --format=json
gcloud projects add-iam-policy-binding <PROJECT_ID> --member="user:<email>" --role="roles/<role>"
gcloud iam service-accounts list --project=<PROJECT_ID>
gcloud iam service-accounts create <NAME> --project=<PROJECT_ID> --display-name="<DESC>"
gcloud iam service-accounts keys create key.json --iam-account=<SA_EMAIL>
```

### Billing

```bash
gcloud billing accounts list
gcloud billing projects describe <PROJECT_ID>
gcloud billing budgets list --billing-account=<ACCOUNT_ID>
```

### Compute Engine

```bash
gcloud compute instances list --project=<PROJECT_ID>
gcloud compute instances describe <INSTANCE> --zone=<ZONE> --project=<PROJECT_ID>
gcloud compute instances start <INSTANCE> --zone=<ZONE> --project=<PROJECT_ID>
gcloud compute instances stop <INSTANCE> --zone=<ZONE> --project=<PROJECT_ID>
gcloud compute firewall-rules list --project=<PROJECT_ID>
gcloud compute firewall-rules create <RULE> --project=<PROJECT_ID> --allow=<PROTO:PORT> --source-ranges=<CIDR>
```

### Cloud Storage

```bash
gcloud storage ls --project=<PROJECT_ID>
gcloud storage buckets create gs://<BUCKET> --project=<PROJECT_ID> --location=<REGION>
gcloud storage cp <LOCAL_PATH> gs://<BUCKET>/<PATH>
gcloud storage cp gs://<BUCKET>/<PATH> <LOCAL_PATH>
gcloud storage ls gs://<BUCKET>/ --recursive
gcloud storage rm gs://<BUCKET>/<PATH>
```

### Cloud Logging

```bash
gcloud logging read "resource.type=<TYPE>" --project=<PROJECT_ID> --limit=50 --format=json
gcloud logging read "severity>=ERROR" --project=<PROJECT_ID> --freshness=1h --limit=20
gcloud logging tail "resource.type=<TYPE>" --project=<PROJECT_ID>
```

### Cloud Run

```bash
gcloud run services list --project=<PROJECT_ID> --region=<REGION>
gcloud run services describe <SERVICE> --project=<PROJECT_ID> --region=<REGION>
gcloud run deploy <SERVICE> --project=<PROJECT_ID> --region=<REGION> --source=. --allow-unauthenticated
gcloud run services logs read <SERVICE> --project=<PROJECT_ID> --region=<REGION> --limit=50
```

### App Engine

```bash
gcloud app describe --project=<PROJECT_ID>
gcloud app deploy --project=<PROJECT_ID>
gcloud app logs read --project=<PROJECT_ID> --limit=50
```

### Monitoring

```bash
gcloud monitoring dashboards list --project=<PROJECT_ID>
gcloud monitoring policies list --project=<PROJECT_ID>
gcloud monitoring metrics list --project=<PROJECT_ID> --filter="metric.type:<search>"
```

### Cloud SQL

```bash
gcloud sql instances list --project=<PROJECT_ID>
gcloud sql instances describe <INSTANCE> --project=<PROJECT_ID>
gcloud sql databases list --instance=<INSTANCE> --project=<PROJECT_ID>
```

### Secret Manager

```bash
gcloud secrets list --project=<PROJECT_ID>
gcloud secrets versions access latest --secret=<SECRET_NAME> --project=<PROJECT_ID>
gcloud secrets create <SECRET_NAME> --project=<PROJECT_ID> --data-file=<FILE>
```

### Cloud Monitoring REST API (for Gemini usage)

For detailed Gemini API metrics, refer to the `gcloud-billing-manaca` skill which has specific metric queries.

## Playwright Fallback

Use Playwright only when a feature requires the Cloud Console UI (dashboards, visual editors, or when gcloud CLI does not support the operation).

```bash
PWCLI="$HOME/.codex/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" open https://console.cloud.google.com --headed
"$PWCLI" snapshot
```

Login credentials are in `~/.claude/.env`:
- `GOOGLE_ACCOUNT_EMAIL` — the account email
- `GOOGLE_ACCOUNT_PASSWORD` — the account password

Fill the login form using these environment variables. Never hardcode or display the password.

## Safety Rules

- **Always specify `--project`** — never rely on a default project config.
- **Confirm before destructive operations**: `delete`, `stop`, `disable`, `remove-iam-policy-binding`, `rm`, firewall rule changes.
- **Never expose** tokens, passwords, or service account keys in output.
- **Prefer `--format=json`** for programmatic parsing, `--format=table` for human readability.
- **Use `--quiet`** only for non-destructive reads when suppressing prompts.
- For IAM changes, always show the current policy first, then propose the change.

## Session Learnings

(To be populated as issues are encountered)
