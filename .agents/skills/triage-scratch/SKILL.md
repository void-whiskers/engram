---
name: triage-scratch
description: >-
  Review notes in scratch/ and decide their fate: promote to the appropriate
  knowledge domain, link to an experiment, or delete if ephemeral. Use this
  skill periodically when scratch has accumulated notes.
---

# triage-scratch

Review scratch notes and route them to their permanent home, or delete them.

## When to Use

- When `scratch/` contains files beyond `README.md`
- After a period of active work where unstructured notes were dropped there
- As a regular maintenance task

## Steps

### 1. List scratch contents

```bash
ls <path/to/engram>/scratch/
```

Ignore `README.md` — only process other files.

### 2. For each file, read and classify

Read the content and decide:

| Content type | Action |
|-------------|--------|
| Reusable learning, domain knowledge | → Promote to `knowledge/` using `add-knowledge` skill |
| Experiment result or observation | → Promote using `add-experiment` skill |
| Coding/design/workflow insight | → Use `update-standards` skill |
| Future experiment idea / hypothesis | → Create in `experiments/future/` using `add-experiment` (future mode) |
| Project context | → Add to `projects/` |
| Tool knowledge | → Add to `tools/` |
| Truly ephemeral (already captured elsewhere, or no lasting value) | → Delete |

### 3. Execute the promotion

Follow the relevant skill's instructions for the destination domain.

For simple promotions (no dedicated skill needed), create the leaf document manually:
1. Write the document with correct frontmatter
2. Update the parent `INDEX.md`
3. Delete the scratch file

### 4. Delete the scratch file after promotion

```bash
git rm scratch/<filename>
```

Or if it was never staged:
```bash
rm <path/to/engram>/scratch/<filename>
```

### 5. Sync

Run the `sync-memory` skill after all scratch files have been triaged.

## Notes

- Don't force content into an ill-fitting category — it's fine to leave a scratch file if the right home isn't clear yet
- If multiple scratch notes are related, consider consolidating them into a single document before promoting
- Scratch is not indexed, so notes left there are invisible to B-tree navigation
