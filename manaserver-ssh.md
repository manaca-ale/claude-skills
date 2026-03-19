---
name: manaserver-ssh
description: Access and operate host `manaserver` through SSH alias `manaserver`, focused on the n8n docker stack in `/home/ubuntu/n8n_run`. Use when requests mention n8n, webhooks, port 5678, docker status on manaserver, or restart/update operations there.
---

# Manaserver SSH

Connect to `manaserver` and operate the n8n stack with the host-specific sudo/docker-compose conventions.

## Connection

- Preferred: `ssh manaserver`
- Fallback:
  `ssh -i /C:/Users/aleco/manaserver.pem ubuntu@54.196.142.248`

## Known Topology

- Host user/home: `ubuntu`, `/home/ubuntu`
- Main project path: `/home/ubuntu/n8n_run`
- Compose file: `/home/ubuntu/n8n_run/docker-compose.yml`
- Stack services (config output): `n8n`
- Container observed: `n8n_run-n8n-1`
- Public port: `5678`
- Compose env highlights:
  - `WEBHOOK_URL=https://n8n.manaca.tech/`
  - timezone `America/Sao_Paulo`
  - volume `n8n_data` (`external: true`)

## Docker Runtime Note

- Docker daemon access requires `sudo -n`.
- Compose command available as `docker-compose` binary.
- Prefer `sudo -n docker-compose ...` to avoid interactive prompts.

## Quick Diagnostics

```bash
hostname
sudo -n docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
sudo -n docker-compose -f /home/ubuntu/n8n_run/docker-compose.yml config --services
sudo -n docker-compose -f /home/ubuntu/n8n_run/docker-compose.yml ps
```

## Common Operations

Restart/update n8n stack:

```bash
cd /home/ubuntu/n8n_run
sudo -n docker-compose pull
sudo -n docker-compose up -d
sudo -n docker-compose ps
sudo -n docker-compose logs -f --tail 200
```

## Safety Rules

- Do not remove `n8n_data` volume unless explicitly requested.
- Confirm webhook impact before restarts during business hours.
- Collect logs before and after any restart for rollback context.

## Exit Criteria

- Show executed commands.
- Show current container health/status.
- Report any unresolved issue requiring manual intervention.
