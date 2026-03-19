---
name: gcloud-billing-manaca
description: Query Gemini API usage and estimated costs across all Manaca Tech GCP projects using Cloud Monitoring API. Use when the user asks about Gemini billing, API costs, token usage, or wants a billing report for the contato@manaca.tech account.
---

# Gemini API Billing - Manaca Tech

Query Gemini API usage and estimated costs across all Manaca Tech GCP projects.

## Authentication

1. Check if `contato@manaca.tech` has a valid token:

```bash
gcloud auth print-access-token --account=contato@manaca.tech 2>/dev/null
```

2. If it fails with a reauthentication error, guide the user to run:

```bash
gcloud auth login contato@manaca.tech
```

Wait for the user to complete browser auth before proceeding.

## Project Registry

| Project ID                      | Name   |
|---------------------------------|--------|
| `gen-lang-client-0028842427`    | Saira  |
| `gen-lang-client-0487533939`    | Flora  |
| `gen-lang-client-0616161525`    | Teste  |
| `manafin`                       | Manafin|

## Metrics to Query

For each project, query the Cloud Monitoring REST API:

- **Input tokens**: `generativelanguage.googleapis.com/quota/generate_content_paid_tier_input_token_count/usage`
- **Request count**: `generativelanguage.googleapis.com/quota/generate_requests_per_model/usage`

Both are DELTA metrics. Use `aggregation.perSeriesAligner=ALIGN_SUM`.

### Date Range

- Default: current month (1st of current month to now)
- Support arguments like `--last 7d`, `--last 30d`, or explicit dates `2026-03-01 2026-03-16`
- Convert to ISO 8601 for the API `interval.startTime` / `interval.endTime`
- Use `aggregation.alignmentPeriod` matching the full range for totals, or `86400s` for daily breakdown

### Query Template

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token --account=contato@manaca.tech)
PROJECT="gen-lang-client-0028842427"
METRIC="generativelanguage.googleapis.com/quota/generate_content_paid_tier_input_token_count/usage"
START="2026-03-01T00:00:00Z"
END="2026-03-17T00:00:00Z"

curl -s \
  "https://monitoring.googleapis.com/v3/projects/${PROJECT}/timeSeries?filter=metric.type%3D%22${METRIC}%22&interval.startTime=${START}&interval.endTime=${END}&aggregation.alignmentPeriod=2592000s&aggregation.perSeriesAligner=ALIGN_SUM" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Data Extraction

Each timeSeries entry has:
- `metric.labels.model` -> model name (e.g. `gemini-2.5-flash`)
- `points[].value.int64Value` -> token count or request count

Deduplicate by `(model, period)` key -- the same model/period may appear in multiple timeSeries from different quota dimensions. Keep only one value per key.

## Pricing Table (USD per 1M tokens)

| Model                  | Input   | Output  | Thinking |
|------------------------|---------|---------|----------|
| gemini-2.5-flash       | $0.15   | $0.60   | $3.50    |
| gemini-2.5-flash-lite  | $0.075  | $0.30   | -        |
| gemini-2.0-flash       | $0.10   | $0.40   | -        |
| gemini-2.0-flash-exp   | $0.10   | $0.40   | -        |
| gemini-2.0-flash-lite  | $0.075  | $0.30   | -        |
| gemini-3-flash         | $0.15   | $0.60   | $3.50    |

**Note:** Cloud Monitoring only provides input token counts. Estimate output and thinking tokens as follows:
- Output tokens: 5% of input tokens (conservative ratio from SAIRA worker logs)
- Thinking tokens: ~1,105 tokens per request for models with thinking (gemini-2.5-flash, gemini-3-flash)
- Models without thinking column get $0 thinking cost

Exchange rate for BRL display: use 5.7 BRL/USD (or ask the user for current rate).

## Cost Calculation

For each (project, model) pair:

```
input_cost   = (input_tokens / 1,000,000) * input_price
output_cost  = (input_tokens * 0.05 / 1,000,000) * output_price
thinking_cost = (requests * 1105 / 1,000,000) * thinking_price   # only for flash/3-flash
total_cost   = input_cost + output_cost + thinking_cost
```

## Output Format

Present results as a markdown table grouped by project:

```
## Gemini API Billing Report
Period: Mar 1-16, 2026 | Account: contato@manaca.tech

### Projeto Saira (gen-lang-client-0028842427)
| Modelo              | Requests | Input Tokens | Custo Est. (USD) |
|---------------------|----------|-------------|-----------------|
| gemini-2.5-flash    | 9,199    | 14,017,629  | $38.72          |
| gemini-2.5-flash-lite| 24,489  | 32,300,272  | $3.80           |
| **Subtotal**        | **33,741** |           | **$42.53**      |

### Projeto Flora (gen-lang-client-0487533939)
...

### TOTAL GERAL
| Metrica         | Valor          |
|-----------------|----------------|
| Requests        | 36,253         |
| Input Tokens    | 49.3M          |
| Custo (USD)     | $46.33         |
| Custo (BRL)     | R$ 264.10      |
```

## Important Notes

- These are **estimates**. Output and thinking tokens are inferred, not measured.
- For exact costs, check: https://aistudio.google.com/apikey (Billing section)
- The billing account is `01AE3F-B61E1D-9168FD` (BRL currency)
- The spending cap is R$ 50.00/month -- warn if estimated cost approaches this limit
- Thinking tokens from gemini-2.5-flash are the main cost driver (~85% of total)
- If a project returns no data, it may need Cloud Monitoring API enabled
