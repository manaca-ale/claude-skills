---
name: flora-server-ssh
description: Access and operate the Flora EC2 host through SSH alias `Flora`, including Docker container checks and compose operations in `/home/ubuntu/flora-docker`. Default behavior is test-only; only act on production when the user explicitly requests production and confirms before execution.
---

# Flora Server SSH

Connect and run operational commands on host `Flora` without re-discovering paths and stack layout.

## Connection

- Preferred: `ssh Flora`
- Fallback:
  `ssh -i /C:/Users/aleco/MVP-FLORA.pem ubuntu@ec2-100-31-0-50.compute-1.amazonaws.com`

## Known Topology

- Host user/home: `ubuntu`, `/home/ubuntu`
- Main project path: `/home/ubuntu/flora-docker`
- Other visible dirs: `/home/ubuntu/impacto-mvp`, `/home/ubuntu/backup_flora`, `/home/ubuntu/backups`
- Compose files:
  - `/home/ubuntu/flora-docker/docker-compose.yml`
  - `/home/ubuntu/flora-docker/docker-compose.override.yml`
  - `/home/ubuntu/flora-docker/docker-compose.prod.yml`
- Stack services (config output):
  - `flora-db`, `flora-core`, `flora-worker`, `api-gateway`, `flora-frontend`, `flora-report`
- Running container name prefixes:
  - test: `test-*`
  - prod: `prod-*`

## Compose Runtime Note

Use `docker compose` plugin commands (not `docker-compose` binary).

## Environment Guardrail (Mandatory)

- Default scope: test containers/projects only.
- Do not run production commands by default.
- Before any production action, show the exact command plan and wait for explicit confirmation.

## Quick Diagnostics

```bash
hostname
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker compose -f /home/ubuntu/flora-docker/docker-compose.yml config --services
docker compose -f /home/ubuntu/flora-docker/docker-compose.yml ps
```

## Safety Rules

- Collect `docker ps` and targeted logs before any restart.
- Do not run destructive commands (`down -v`, prune, database reset) unless explicitly requested.
- Treat `prod-*` containers as protected scope requiring explicit confirmation.

## Exit Criteria

- Report exact commands executed.
- Report final container status and any health endpoint results.
- Highlight any pending manual actions.
