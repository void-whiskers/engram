---
status: current
created: 2026-08-08
updated: 2026-11-13
tags: [database, postgresql, grate, migrations, DDL, CRUD, docker-compose, standards]
---

# Database Architecture & Schema Management Standards

## Executive Summary

All databases across our applications MUST follow a strict separation of concerns between **Schema Management (DDL)** and **Application Runtime (CRUD)**:

1. **Schema migrations (DDL)** are exclusively executed at container startup by a dedicated **Grate DB Init Container** (`erikbra/grate:2.0.0`).
2. **Application code** is strictly prohibited from running schema DDL (`CREATE TABLE`, `ALTER TABLE`, ORM `create_all()`, `PRAGMA table_info`) at runtime. Applications perform ONLY **CRUD operations** (SELECT, INSERT, UPDATE, DELETE).
3. **Application containers** MUST NOT start until the `db-init` container completes all migration scripts successfully.

---

## 1. Directory & File Structure Conventions

Every database-backed service MUST organize migration SQL files in a dedicated `db/up/` directory:

```text
backend/
├── db/
│   ├── up/
│   │   ├── 0001_create_file_records.sql
│   │   ├── 0002_create_action_items.sql
│   │   ├── 0003_create_searx_cache.sql
│   │   └── 0004_add_indexes.sql
│   ├── database.py   (CRUD connection provider ONLY - NO DDL)
│   └── models.py     (Declarative ORM models ONLY)
```

- Migration scripts placed in `db/up/` MUST be named with sequential numeric prefixes (`0001_`, `0002_`, `0003_`).
- Every migration script MUST be **idempotent** (`CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`).
- **UP scripts are IMMUTABLE**. Once an `up` script is committed and applied, it must never be modified. If a fix is needed (e.g. a broken backfill or incorrect schema), you MUST create a new, sequentially numbered script. If an existing script absolutely must be modified, whoever administers the database must first remove the old script hash from the Grate schema by hand.

---

## 2. Docker Compose Pattern for Grate DB Init

The standard container stack definition in `docker-compose.yml` MUST configure the database, Grate init worker, and application service as follows:

```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: generic-app-db
    environment:
      - POSTGRES_USER=${POSTGRES_USER:-generic-app}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-generic-apppass}
      - POSTGRES_DB=${POSTGRES_DB:-generic-appdb}
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-generic-app} -d ${POSTGRES_DB:-generic-appdb}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  db-init:
    image: erikbra/grate:2.0.0
    container_name: generic-app-db-init
    volumes:
      - ./backend/db:/db   # Mount parent db folder so Grate finds /db/up/*.sql
    environment:
      - DOTNET_BUNDLE_EXTRACT_BASE_DIR=/tmp
      - HOME=/tmp
    entrypoint: /bin/sh -c
    command: '"./grate --sqlfilesdirectory=/db --connstring=\"Host=db;Port=5432;Database=${POSTGRES_DB:-generic-appdb};Username=${POSTGRES_USER:-generic-app};Password=${POSTGRES_PASSWORD:-generic-apppass};\" --databasetype=postgresql --schemaname=grate_generic-app --noninteractive --env=${GRATE_ENV:-Dev}"'
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ["CMD-SHELL", "echo 'init'"]
      interval: 5s
      timeout: 5s
      retries: 5
    depends_on:
      db:
        condition: service_healthy

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: generic-app-backend
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-generic-app}:${POSTGRES_PASSWORD:-generic-apppass}@db:5432/${POSTGRES_DB:-generic-appdb}
    depends_on:
      db:
        condition: service_healthy
      db-init:
        condition: service_completed_successfully   # App blocked until migrations complete
    restart: unless-stopped

volumes:
  postgres_data:
```

### Critical Container Wiring Rules:
- **Volume Mount**: Mount `./backend/db:/db` (NOT `./backend/db/up:/db`). Grate automatically scans `/db/up` for versioned `.sql` migration scripts.
- **Environment Flags**: Always supply `DOTNET_BUNDLE_EXTRACT_BASE_DIR=/tmp` and `HOME=/tmp` to allow Grate to execute under non-root container security policies.
- **Completion Guard**: Enforce `depends_on: db-init: condition: service_completed_successfully` on all backend applications.

---

## 3. Data Type Selection & OS Bounds

For file indexers, digital asset management, and NAS services, string column sizes in PostgreSQL MUST be explicitly bounded by POSIX / OS specifications:

| Field | Bound Rationale | PostgreSQL / SQLAlchemy Type | Description |
|---|---|---|---|
| `file_path` | POSIX `PATH_MAX` = 4096 bytes | `VARCHAR(4096)` | Full absolute path on Linux POSIX filesystems |
| `filename` | ext4 / Btrfs `NAME_MAX` = 255 bytes | `VARCHAR(255)` | Individual file name boundary |
| `extension` | Compound Ext Limit = 64 bytes | `VARCHAR(64)` | Fits compound extensions (e.g., `.tar.gz`, `.x86_64.appimage`) |
| `mime_type` | IANA RFC Standard = 128 bytes | `VARCHAR(128)` | Standard MIME type string |
| `sha256_hash` | Fixed SHA256 Hex = 64 bytes | `VARCHAR(64)` | Hexadecimal SHA-256 string |
| `category` | Enum Category = 64 bytes | `VARCHAR(64)` | System asset classification category |
| `status` | Lifecycle Enum = 32 bytes | `VARCHAR(32)` | File record status state |
| `summary` | Freeform Paragraph | `TEXT` | AI-generated summary paragraph |
| `enriched_data` | JSON String Blob | `TEXT` | Extracted ID3 / EXIF metadata string |

*Note: In PostgreSQL, `VARCHAR(n)` and `TEXT` share the identical internal `varlena` representation with zero query performance overhead. Enforcing explicit `VARCHAR` bounds guarantees data domain integrity.*

---

## 4. Migration Validation Protocol

Always verify your database migrations by directly checking the database tables after running them in a test or local environment.

Never assume a migration script (especially those containing regex, string parsing, or data backfills) worked perfectly without manually inspecting the resulting data state. A successful exit code from Grate only means the SQL syntax was valid; it does not guarantee the data mutation logic was correct.
