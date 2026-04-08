---
name: claude-usage
description: Interact with the local Claude Code usage dashboard (phuryn/claude-usage) — scan logs, view today's costs, check all-time stats, or launch the web dashboard. Use when the user asks about token usage, costs, session history, or wants to see the usage dashboard.
---

# Claude Usage Dashboard

Interact with the local claude-usage tool at `C:\Users\aleco\claude-usage`.

## Trigger

Activate when the user:
- Asks about Claude Code token usage or costs
- Wants to see today's usage or all-time stats
- Asks to open/start the usage dashboard
- Mentions "quanto gastei", "consumo", "tokens", "usage", "dashboard de uso"

## Commands

All commands run from `C:\Users\aleco\claude-usage\`.

### Scan logs
```bash
cd /c/Users/aleco/claude-usage && python cli.py scan
```
Incrementally scans `~/.claude/projects/` JSONL files into `~/.claude/usage.db`. Fast on re-runs.

### Today's summary
```bash
cd /c/Users/aleco/claude-usage && python cli.py today
```
Shows token counts and estimated costs by model for today. Present the output to the user in a readable format.

### All-time statistics
```bash
cd /c/Users/aleco/claude-usage && python cli.py stats
```
Shows total tokens, costs, top projects, and daily averages. Present the output clearly.

### Web dashboard
```bash
cd /c/Users/aleco/claude-usage && python cli.py dashboard --port PORT
```
Scans logs, then starts a web server with charts at `http://localhost:PORT`. Opens browser automatically.

## Workflow

### 1. Determine intent

- **Quick check**: run `today` or `stats` and present results inline
- **Deep analysis**: launch the web dashboard
- **Fresh data**: always run `scan` first if user asks for up-to-date numbers

### 2. Choose port for dashboard

Before launching the dashboard, check if the default port 8080 is free:
```bash
netstat -ano | findstr ":8080"
```
If occupied, try 8090, 9080, or 18080. Use `--port` flag.

### 3. Launch dashboard

Run with `run_in_background: true` and timeout of 600000ms so the server stays alive:
```bash
cd /c/Users/aleco/claude-usage && python cli.py dashboard --port PORT
```
Tell the user the URL and that they can press Ctrl+C in the terminal to stop it.

### 4. Interpret results

When showing CLI output:
- Highlight the **total estimated cost** prominently
- Note that costs are API pricing estimates — actual cost depends on subscription plan (Max/Pro vs API)
- If cache read is high relative to input, mention that caching is saving money
- Compare today's usage to daily average if both are available

## Cost context

The tool uses Anthropic API pricing. Key rates (April 2026):
- **Opus 4.6**: $15/MTok input, $75/MTok output
- **Sonnet 4.6**: $3/MTok input, $15/MTok output  
- **Haiku 4.5**: $0.80/MTok input, $4/MTok output
- Cache reads are 90% cheaper than input; cache writes are 25% more expensive

On Max subscription ($100-200/month), actual cost is the subscription fee, not per-token. The estimates are useful for understanding relative usage patterns, not actual billing.

## Database location

`~/.claude/usage.db` (SQLite). Can be queried directly if the user needs custom analysis:
```bash
sqlite3 ~/.claude/usage.db "SELECT ..."
```

Key tables: `sessions`, `turns`, `files_scanned`.
