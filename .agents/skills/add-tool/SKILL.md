---
name: add-tool
description: >-
  Add a new tool knowledge document to the tools/ domain. Use when documenting
  how we use a specific tool, API, service, CLI, or framework — including
  gotchas, preferred configurations, and tips. Keeps tools/INDEX.md consistent.
---

# add-tool

Add a new tool knowledge document and keep the index consistent.

## When to Use

- Documenting how we use a specific tool, service, API, CLI, or framework
- Recording gotchas, workarounds, or preferred configurations for a named tool
- Promoting scratch notes about a tool into a permanent reference

## tools/ vs knowledge/ — Which to Use?

- **tools/**: Knowledge about our specific usage of a **named tool or service** (e.g. Redis, Docker, GitHub Actions). Answers: "how do we use X? what are the gotchas?"
- **knowledge/**: Broader domain knowledge that may reference tools but isn't about a specific one (e.g. caching patterns, distributed systems concepts). Answers: "what do we know about this domain?"

If in doubt: if you'd title the document with a product/tool name, it belongs in `tools/`. If you'd title it with a concept, it belongs in `knowledge/`.

---

## Steps

### 1. Read the tools index

```bash
cat <path/to/engram>/tools/INDEX.md
```

Check whether a document for this tool already exists. If it does, update it in place.

### 2. Create the tool document

File path: `tools/<tool-slug>.md`

**Naming**: use the tool's common name, lowercase and hyphenated. Examples:
`docker.md`, `github-actions.md`, `redis.md`, `postgresql.md`, `vscode.md`

Frontmatter:
```yaml
---
status: current
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tools, <tool-name>]
---
```

There is no required structure for tool docs — use whatever format best serves the content. Common sections include:

- **What it is** (one-liner)
- **How we use it** (our specific configuration, setup, or patterns)
- **Gotchas** (non-obvious behaviours, common mistakes)
- **Tips** (productivity tricks, useful commands)
- **Links** (official docs, useful references)

### 3. Update tools/INDEX.md

Add a row to the contents table:
```markdown
| [tool-slug.md](./tool-slug.md) | One-line description | current | YYYY-MM-DD |
```

### 4. Sync

Run the `sync-memory` skill.

---

## Updating Existing Tool Knowledge

### Minor update (adding a gotcha, new tip)
Edit in place. Update `updated` frontmatter. Run `sync-memory`.

### Tool replaced by another
Use the supersession pattern from `AGENTS.md`:
1. Create the new tool doc
2. Add `supersedes:` frontmatter pointing to the old doc
3. Add `superseded_by:` to the old doc
4. Delete the old doc
5. Update `tools/INDEX.md`
6. Run `sync-memory`
