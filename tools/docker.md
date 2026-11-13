---
status: current
created: 2026-08-28
updated: 2026-08-28
tags: [tools, docker, containers, compose, cli]
---

# Docker & Container CLI Tooling

> Operational guide for agents interacting with the Docker CLI and Docker Compose in local development environments. For architectural container guidelines, see [standards/coding/containers.md](../standards/coding/containers.md).

---

## 1. Environment Verification

Before running container-dependent commands, verify that the Docker daemon is active and responsive:

```bash
docker info >/dev/null 2>&1 || echo "Docker daemon is not running"
```

If the daemon is unreachable, do not attempt to force container execution; notify the user to start Docker Desktop or the system daemon.

---

## 2. Standard Operational Workflows

### Starting & Stopping Services
Always prefer repository `Makefile` targets (e.g. `make up`, `make down`, `make run`). When executing Docker directly:

```bash
# Start background services
docker compose up -d

# Check running status and health
docker compose ps

# Follow logs for a specific service
docker compose logs -f <service-name>

# Tear down services and networks
docker compose down
```

### Inspecting Container Health & Logs
When troubleshooting failed or crashing containers:

```bash
# View last 100 log lines with timestamps
docker logs --tail 100 -t <container-id-or-name>

# Inspect exit code and health status
docker inspect --format='{{.State.Status}} (ExitCode: {{.State.ExitCode}})' <container-name>
```

---

## 3. Hygiene & Resource Management

- **Isolated Execution**: Avoid leaving dangling orphan containers across test runs (`docker compose down --remove-orphans`).
- **Volume Awareness**: Never delete named volumes containing persistent state (`docker compose down -v`) unless explicitly instructed during a destructive reset.
- **Cache Cleanliness**: Clean up dangling intermediate build layers periodically via `docker image prune -f`.
