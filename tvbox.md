---
name: tvbox
description: Connect to a TV Box over SSH (default host alias TanixW2), operate the media stack (containers, compose, configs, logs), and manage media files safely (search, move, rename, delete, verify). Use for maintenance, troubleshooting, automation, and operational tasks on the TV Box.
---

# Tvbox

## Scope

- Connect to TV Box via SSH using local alias (default `TanixW2`).
- Manage media stack services (`docker compose`, containers, configs, logs).
- Manage remote files (search, inspect, move, rename, delete, verify).

## Default Context

- Host alias: `TanixW2`
- Stack root: `/opt/media-server`
- Media root: `/mnt/media_geral`
- Common containers: `prowlarr`, `sonarr`, `radarr`, `qbittorrent`, `plex`, `overseerr`, `flaresolverr`, `whisparr`, `stash`

## Generic Workflow

1. Confirm SSH connectivity and target host.
2. Inspect current state before changing anything.
3. Apply the smallest possible change to satisfy the request.
4. Validate outcome with read-back checks.
5. Report exactly what changed (files, services, and paths).

## Safety Rules

- Prefer read-only inspection first.
- For destructive file actions, resolve exact path before execution.
- Avoid broad wildcard deletion or movement.
- Restart only affected containers, not the full stack, unless requested.
- Keep unrelated configs and user changes untouched.

## Task Patterns

### Stack Operations

- Check service/container status.
- Review and update compose or app config files.
- Restart targeted services and verify health.
- Collect logs for troubleshooting.

### File Operations

- Search files by name, pattern, or extension.
- Confirm metadata and uniqueness before moving/deleting.
- Move/rename files with deterministic destination paths.
- Verify post-change state (presence/absence, size, permissions).

### Troubleshooting

- Correlate errors with mounts, permissions, disk, or config.
- Apply minimal fix and re-test.
- Document final state and any residual risk.

## Bundled Script

Located at `C:/Users/aleco/.codex/skills/tvbox/scripts/tvbox-media.ps1`:
- `find`: search remote files.
- `delete`: remove exact remote path (`-Force` required to execute).
