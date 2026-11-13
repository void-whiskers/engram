---
status: current
created: 2026-08-08
updated: 2026-08-28
tags: [standards, coding, automation, build, ci]
---

# Automation & Task Runner Standard

> **Universal Entrypoint:** Every repository MUST use `make` as the universal task runner for local development and CI/CD pipelines.

---

## Why Make?

- **Consistency:** Developers can clone any project and intuitively run `make build`, `make test`, or `make run` without needing to remember project-specific incantations (like `npm run dev`, `poetry run start`, or `docker-compose up`).
- **Simplicity:** Makefiles wrap complex, multi-step shell commands, reducing human error.
- **CI/CD Integration:** CI pipelines can simply call `make test-full` instead of maintaining separate, complex pipeline configurations.

---

## Required Makefile Targets

Every project must implement (or stub) the following baseline targets:

### `build`
Compiles or builds the application (e.g., `docker compose build`, `npm run build`, `go build`).

### `run` / `up`
Starts the application locally (e.g., `docker compose up -d`).

### `down` / `stop`
Tears down the application and associated infrastructure locally.

### `test`
Executes backend or primary test suites.

### `test-ui`
Executes frontend test suites (if applicable).

### `lint`
Runs code formatting and linting (e.g., MegaLinter, `ruff`, `eslint`).

### `check`
Runs both linting and testing to verify code health before committing.

### `clean`
Removes build artifacts, cache directories (e.g., `__pycache__`, `.pytest_cache`), and generated files to reset the workspace.

---

## Examples

For examples of conforming Makefiles, refer to standard project Makefiles (e.g., Sift).

```makefile
# Example Makefile snippet
.PHONY: build test clean

build:
	docker compose build

test:
	docker compose run --rm app pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
```
