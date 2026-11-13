---
status: current
created: 2026-08-08
updated: 2026-08-08
tags: [standards, coding, naming, readability]
---

# Naming & API Contracts Standard

> **Names should be self-documenting — a good name makes a comment unnecessary.**

---

## Core Naming Principles

- **Descriptive Intent**: Variables, functions, and classes describe *what* they represent or *what* action they perform, not *how* they do it.
- **Boolean Prefixes**: Prefix boolean variables and functions with `is_`, `has_`, `can_`, `should_` (e.g. `is_valid`, `has_permission`).
- **Avoid Abbreviations**: Use full words unless the abbreviation is standard in context (e.g., `id`, `url`, `http`, `mime`).
- **Consistency**: Match existing conventions in the target codebase.
