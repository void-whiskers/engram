---
name: update-standards
description: >-
  Create a new standard or revise an existing one with full supersession
  tracking. Handles coding, design, and workflow standards. Uses git history
  as the archive — superseded documents are deleted, not moved. Also manages
  the .editorconfig and the standards context document.
---

# update-standards

Create or revise standards documents with proper supersession tracking.

## When to Use

- Adding a new language-specific coding standard (e.g. adding `rust.md`)
- Revising an existing standard because practices have changed
- Updating the working context in `standards/coding/context.md`
- Updating formatting rules in `standards/coding/.editorconfig`
- Adding design or workflow standards

---

## Creating a New Standard

### 1. Identify the right location

| Type | Location |
|------|----------|
| Language-specific coding | `standards/coding/<language>.md` |
| General coding (language-agnostic) | `standards/coding/<topic>.md` (e.g. `naming.md`, `logging.md`) |
| Design | `standards/design/<topic>.md` |
| Workflow | `standards/workflow/<topic>.md` |

If a language has grown large enough to need multiple documents, create a subfolder:
`standards/coding/<language>/INDEX.md` + leaf docs.

### 2. Create the document

Use this frontmatter:

```yaml
---
status: current
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [standards, coding, <language>]
---
```

### 3. Update the parent INDEX.md

Add a row with the new document.

### 4. Sync

Run the `sync-memory` skill.

---

## Revising an Existing Standard

### Minor revision (wording, small additions)

Edit the document in place. Update `updated` in frontmatter. Run `sync-memory`.

### Major revision (significant rewrite, new direction)

Use the **supersession pattern** — git history is the archive:

1. Create the new document (e.g. `standards/coding/python-v2.md` temporarily, or rename in place)
2. In the **new** document's frontmatter: `supersedes: standards/coding/python.md`
3. In the **old** document's frontmatter: `superseded_by: standards/coding/python-v2.md`
4. **Delete the old document**:
   ```bash
   git rm standards/coding/python.md
   ```
5. Rename the new doc to the canonical name if needed:
   ```bash
   git mv standards/coding/python-v2.md standards/coding/python.md
   ```
6. Update the parent `INDEX.md` — no change needed if the filename stayed the same; update if it changed
7. Run `sync-memory`

### Recovering a superseded standard

```bash
# Find when it was last in the repo
git log -- standards/coding/old-name.md

# View the content at a specific commit
git show <hash>:standards/coding/old-name.md
```

---

## Updating the Editor Config

When formatting preferences change:

1. Edit `standards/coding/.editorconfig`
2. The file uses glob patterns — each language has its own `[*.ext]` section
3. Note: this file is the **baseline** for new projects. Projects may override values locally
4. Run `sync-memory`

---

## Updating the Context Document

When your working context changes (primary languages, kinds of project, deployment environments):

1. Edit `standards/coding/context.md`. Describe the change in general terms and never name an employer or a client: the Information Boundary in `standards/workflow/agent-strategies.md` applies.
2. Note the date of context change in the document
3. Consider whether existing language standards need updating to reflect the new context
4. Run `sync-memory`

---

## Standards Scope Note

Standards in this knowledge base reflect your **current working context** (languages, kinds of project, environments). They are not immutable. When that context changes, update `context.md` and revise language standards as needed using the supersession pattern above.
