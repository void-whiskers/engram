---
name: validate-memory
description: >-
  Run automated consistency checks on the Engram knowledge base: document and
  skill frontmatter, INDEX link validity, orphan detection, and navigation integrity.
  Run this after adding, moving, or superseding documents, and as a pre-commit check.
---

# validate-memory

Automated structural integrity checker for the Engram knowledge base.

## When to Use

- After creating a new document (verify frontmatter, check it appears in the relevant INDEX)
- After superseding or deleting a document (verify no broken links were left behind)
- Before committing and pushing via `sync-memory`
- Periodically as a health check

## How to Run

Both scripts run the same checks; use whichever interpreter you have.

### Linux / macOS / WSL / Git Bash:
```bash
bash .agents/skills/validate-memory/scripts/validate.sh
```

### Windows (PowerShell / Command Prompt) or Universal Python:
```bash
python .agents/skills/validate-memory/scripts/validate.py
```

## What it Checks

1. **Frontmatter compliance**: Every leaf document has valid `status`, `created`, `updated`, and `tags` fields with approved status values.
2. **Skill frontmatter**: Every `SKILL.md` under `.agents/skills/` has `name` and `description` fields.
3. **INDEX link consistency**: Every relative link in every `INDEX.md` resolves to a real file or directory.
4. **Orphan detection**: Every document that sits beside an `INDEX.md` is referenced in it. An orphan is an error.
5. **Navigation integrity**: Every `Parent:` and `Root:` link in every `INDEX.md` resolves correctly.

It does not check relative links inside leaf documents, or that the dates and summaries in an `INDEX.md` match the documents; check those when you review a document.

## Exit Codes

- `0`: All checks passed.
- `>0`: Errors found (number of errors equals the exit code).
