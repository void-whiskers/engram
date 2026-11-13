---
name: add-project
description: >-
  Add a new project document to the projects/ domain. Guides agents through
  creating a project doc from the template, setting correct frontmatter, and
  updating projects/INDEX.md. Use when recording high-level context about an
  active or past project.
---

# add-project

Add a new project document and keep the index consistent.

## When to Use

- Recording context about a new project (why it exists, key decisions, current status)
- Promoting scratch notes that describe a project into a permanent project doc
- Documenting a project that agents are working on across multiple sessions

---

## Steps

### 1. Read the projects index

```bash
cat <path/to/engram>/projects/INDEX.md
```

Check whether a document for this project already exists. If it does, update it in place rather than creating a duplicate.

### 2. Check the information boundary

Project documents are default-deny: see "Project documentation" under the Information Boundary in [agent-strategies.md](../../../standards/workflow/agent-strategies.md). Create one only for a project you own or a public open-source project, and include only facts that could be published as they stand. If the project fails that test, stop and tell the user why; do not write a partial document.

### 3. Create the project document

File path: `projects/<project-slug>.md`

Use the template at [`projects/template.md`](../../../projects/template.md).

Frontmatter:
```yaml
---
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [project, <domain>]
---
```

**Status values for projects**: `active`, `paused`, `completed`, `abandoned`

Fill in all sections. At minimum, the Summary and Current Status must be complete. **Architectural Constraints** is the section agents rely on most. For a project you own, include the facts about how you run it that the code does not state, such as the scale of its data. For a public project you do not own, record only the constraints a reader could verify in its public source.

### 4. Update projects/INDEX.md

Add a row to the contents table:
```markdown
| [project-slug.md](./project-slug.md) | One-line description | active | YYYY-MM-DD |
```

### 5. Link to related knowledge and experiments

If this project has related documents elsewhere in the knowledge base:
- Add links in the project doc's **Related Knowledge** and **Related Experiments** sections
- Optionally add a backlink from those documents to this project

### 6. Sync

Run the `sync-memory` skill.

---

## Updating an Existing Project

### Status change (e.g. active → paused)
Edit the document's frontmatter `status` and `updated` fields. Update the status column in `projects/INDEX.md`. Run `sync-memory`.

### Adding context
Edit in place. Update `updated` frontmatter. Run `sync-memory`.
