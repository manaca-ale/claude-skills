---
name: saira-prod-server-ssh
description: Access and operate the SAIRA server through SSH alias `saira-prod`, with known project paths and docker-compose topology for test and production. Default behavior is test-only; only act on production when the user explicitly requests production and confirms before execution.
---

# SAIRA Prod Server SSH

Connect to `saira-prod` and execute stack operations without rediscovering paths, compose files, or service names.

## Connection

- Preferred: `ssh saira-prod`
- Fallback:
  `ssh -i /C:/Users/aleco/key-saira-prod-v2.pem ubuntu@54.91.172.66`

## Known Topology

- Host user/home: `ubuntu`, `/home/ubuntu`
- Main repo path: `/home/ubuntu/saira`
- Main stack path: `/home/ubuntu/saira/services`
- ESP32 stack path: `/home/ubuntu/saira/esp32-server`
- Additional visible dirs: `/home/ubuntu/services`, `/home/ubuntu/saira-project`, `/home/ubuntu/saira-android`

Services from compose config:
- `services/docker-compose.test.yml`: `db`, `pgadmin`, `backend`, `web`, `api-gateway`
- `services/docker-compose.prod.yml`: `db`, `backend`, `api-gateway`, `web`
- `esp32-server/docker-compose.test.yml`: `esp32-receiver`
- `esp32-server/docker-compose.prod.yml`: `esp32-receiver`, `fake-worker`

Observed project/container groups:
- `saira-test-*` (test app stack)
- `saira-prod-*` (prod app stack)
- `saira-esp32-test-*` and `saira-esp32-prod-*` (ESP32 receiver stacks)
- `esp32-dashboard` (standalone container)

Observed public ports:
- prod: `3000`, `5000`, `8001`, `5432`, `5004`, `6380`
- test: `3001`, `5001`, `8002`, `5433`, `5002`, `5051`, `6381`

## Compose Runtime Note

This host uses `docker compose` plugin (not `docker-compose` binary).
Use `docker compose ...` commands.

## Environment Guardrail (Mandatory)

- Default scope: test containers/projects only (`saira-test-*`, `saira-esp32-test-*`, test ports/files).
- Do not run production commands by default.
- Run production commands only when the user explicitly asks for production.
- Before any production action, ask for confirmation with the exact command plan and wait for approval.
- If confirmation is not given, keep actions restricted to test scope.

## Quick Diagnostics

```bash
hostname
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker compose -f /home/ubuntu/saira/services/docker-compose.prod.yml ps
docker compose -f /home/ubuntu/saira/services/docker-compose.test.yml ps
docker compose -f /home/ubuntu/saira/esp32-server/docker-compose.prod.yml ps
docker compose -f /home/ubuntu/saira/esp32-server/docker-compose.test.yml ps
```

## Common Operations

Deploy/update prod app stack:

```bash
cd /home/ubuntu/saira
git fetch origin main
git reset --hard origin/main
cd services
docker compose -p saira-prod -f docker-compose.prod.yml up -d --build --force-recreate
```

Deploy/update test app stack:

```bash
cd /home/ubuntu/saira
git fetch origin develop
git reset --hard origin/develop
cd services
docker compose -p saira-test -f docker-compose.test.yml down
docker compose -p saira-test -f docker-compose.test.yml up -d --build --force-recreate
```

Deploy/update ESP32 prod receiver:

```bash
cd /home/ubuntu/saira/esp32-server
mkdir -p uploads ota config
docker compose -p saira-esp32-prod -f docker-compose.prod.yml down --remove-orphans
docker rm -f saira-esp32-prod-esp32-receiver-1 2>/dev/null || true
docker compose -p saira-esp32-prod -f docker-compose.prod.yml up -d --build --force-recreate
```

Deploy/update ESP32 test receiver:

```bash
cd /home/ubuntu/saira/esp32-server
mkdir -p uploads ota config
docker compose -p saira-esp32-test -f docker-compose.test.yml down --remove-orphans
docker rm -f saira-esp32-test-esp32-receiver-1 2>/dev/null || true
docker compose -p saira-esp32-test -f docker-compose.test.yml up -d --build --force-recreate
```

## Safety Rules

- Default to `develop/test` scope for all operational commands.
- Treat `main/prod` branch and `saira-prod-*`/`saira-esp32-prod-*` resources as protected scope.
- Execute production actions only after explicit user request plus explicit confirmation.
- Collect `docker ps` and targeted logs before restarts when troubleshooting.
- Do not run destructive commands (`down -v`, prune, database reset) unless explicitly requested.

## Exit Criteria

- Report exact commands executed.
- Report final status (`ps` + relevant logs/health endpoints).
- Highlight pending manual actions, if any.
