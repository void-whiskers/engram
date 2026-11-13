---
status: current
created: 2026-08-08
updated: 2026-08-08
tags: [standards, coding, containers, docker, security]
---

# Containerization & Docker Standard

> **Containers must be secure, stateless by default, non-root, and transparently persistent for data.**

---

## Core Containerization Rules

### 1. Data Persistence & File Access
- **Never Store State in Container Layers**: Application databases (SQLite, embedded state) and output data must not live solely inside container storage layers.
- **Host Filesystem Bind Mounts**: Prefer mounting host filesystem paths (e.g., `./data:/app/data`) over anonymous volumes. This ensures data is easily accessible, inspectable, and backed up from outside the container.

### 2. Least Privilege (Non-Root Users)
- **Never Run Containers as Root**: Unless explicitly required by system capabilities (e.g., low-port binding, mounting kernel filesystems), create and switch to a dedicated non-root user in the Dockerfile (`USER appuser` / `USER nextjs`).
- Ensure directory permissions (`chown -R appuser:appgroup /app/data`) are correctly set during image build.

### 3. Clean Configuration & Obsolete Tags
- Keep `docker-compose.yml` clean and modern (omit obsolete `version: '3.8'` tags).
- Use environment variables (`.env`) for host networking overrides (`host.docker.internal`).
