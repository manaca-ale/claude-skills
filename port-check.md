---
name: port-check
description: Diagnose port usage on Windows — find which processes occupy specific ports, list all listening ports, suggest free alternatives, and optionally kill blocking processes. Use when the user reports port conflicts, asks what is using a port, or needs a free port.
---

# Port Check

Diagnose and resolve port conflicts on Windows.

## Trigger

Activate when the user:
- Reports a port conflict or "address already in use" error
- Asks what is using a specific port
- Needs to find a free port for a service
- Wants to see all listening ports

## Workflow

### 1. Determine intent

Ask only if ambiguous. Common intents:
- **Check a specific port**: user mentions a port number
- **Find a free port**: user needs an available port for a service
- **List all ports**: user wants an overview of what's listening
- **Kill a blocking process**: user wants to free up a port

### 2. Diagnose

Run the appropriate commands based on intent:

**Check specific port(s):**
```bash
netstat -ano | findstr ":PORT_NUMBER"
```
Then identify the process:
```bash
tasklist //FI "PID eq <PID>" //FO CSV //NH
```

**List all listening ports with process names:**
```bash
netstat -ano | findstr "LISTENING"
```
Group results by PID and resolve each PID to a process name with `tasklist`.

**Find a free port:**
Check the requested port range (default: 8000-9999). Suggest 3 free alternatives near the desired port.

### 3. Report

Present results as a clear table:

| Port | PID | Process | Status |
|------|-----|---------|--------|

### 4. Suggest resolution

Based on findings:
- If Docker: suggest `docker compose stop` for unused stacks, or remapping ports
- If a known dev server: suggest using `--port` flag with an alternative
- If orphaned process: offer to kill it (ONLY with explicit user confirmation)
- If recurring: suggest changing the default port in the project config

### 5. Kill process (only if user explicitly asks)

NEVER kill a process without explicit user confirmation. When confirmed:
```bash
taskkill //PID <PID> //F
```
Verify the port is free after killing.

## Common port owners on this machine

- **Docker Desktop (com.docker.backend.exe)**: occupies many ports (3000-3006, 5432-5434, 6379, 8002, 8081, 9091, 9108-9109)
- **SSH (sshd)**: port 22
- **PostgreSQL**: ports 5432-5434 (via Docker)
- **Redis**: port 6379 (via Docker)
- **Steam**: port 27036
- **Plex**: port 32400

## Safety

- NEVER kill system processes (PID 0, PID 4, svchost, lsass, csrss, winlogon)
- NEVER kill Docker Desktop without asking — it manages multiple services
- Always confirm before killing any process
