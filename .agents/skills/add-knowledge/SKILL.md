---
name: add-knowledge
description: >-
  Add a new knowledge document to the knowledge/ domain. Creates subdomains
  as needed and keeps all INDEX.md files consistent. Use for accumulated
  learnings, domain expertise, reference material, and any reusable knowledge
  that doesn't fit into standards, experiments, tools, or projects.
---

# add-knowledge

Add a new leaf document to the knowledge domain and keep all indexes consistent.

## When to Use

- Capturing a learning or insight that is general and reusable
- Documenting domain expertise (e.g. how a technology works, trade-offs, patterns)
- Promoting a scratch note that contains reference-quality knowledge
- Recording how a public external system or data source behaves

Every entry must meet the Information Boundary in [agent-strategies.md](../../../standards/workflow/agent-strategies.md): nothing personal, and nothing learned through employer or client work.

---

## Steps

### 1. Read the knowledge index

```bash
cat <path/to/engram>/knowledge/INDEX.md
```

Identify whether an appropriate subdomain already exists.

### 2. Choose or create a subdomain

**Using an existing subdomain**: proceed to step 3.

**Creating a new subdomain**:

1. Create `knowledge/<new-subdomain>/INDEX.md`:

```markdown
# <Subdomain> Knowledge Index

> <One-sentence description of what lives here.>

## Contents

| Path | Summary | Status | Last Updated |
|------|---------|--------|-------------|
| *(empty — add documents below)* | | | |

## Navigation
- Parent: [../INDEX.md](../INDEX.md)
- Root: [../../AGENTS.md](../../AGENTS.md)
```

2. Add the new subdomain to `knowledge/INDEX.md`.

**Subdomain naming**: lowercase, hyphenated. Examples:
`ai-ml`, `databases`, `infrastructure`, `web-apis`, `security`, `distributed-systems`, `compilers`, `networking`

### 3. Create the knowledge document

File path: `knowledge/<subdomain>/<topic-slug>.md`, or `knowledge/<topic-slug>.md` for a document that fits no subdomain yet

Frontmatter:
```yaml
---
status: current
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
---
```

Then write the content. There is no required structure for knowledge docs — use whatever format best serves the content (prose, tables, lists, code blocks, etc.).

**If this knowledge was informed by an experiment**, add a reference:
```markdown
## Source
Informed by [EXP-2026-NNN](../../experiments/2026/exp-2026-NNN-slug.md).
```

### 4. Update the parent INDEX.md

Add a row to the contents table of the subdomain's `INDEX.md` (or of `knowledge/INDEX.md` for a top-level document):
```markdown
| [topic-slug.md](./topic-slug.md) | One-line description | current | YYYY-MM-DD |
```

### 5. Sync

Run the `sync-memory` skill.

---

## Revising Existing Knowledge

### Minor update (adding detail, correcting facts)
Edit in place. Update `updated` frontmatter. Run `sync-memory`.

### Major revision (knowledge has fundamentally changed)
Use the supersession pattern from `AGENTS.md`:
1. Edit the document to reflect new understanding
2. If replacing a fundamentally wrong belief with a new one, note in frontmatter: `supersedes: path/to/old-belief.md` (if it was a separate doc)
3. Run `sync-memory`

Git history will show what was believed before.
