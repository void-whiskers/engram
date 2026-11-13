---
name: sync-memory
description: >-
  Commit local changes to your Engram directly on its current branch and push
  them to its remote. Use this skill after contributing any new knowledge,
  standards, experiments, goals, or other content.
---

# sync-memory

Commit local changes in your Engram directly on its current branch and push them to its remote. Your Engram is the one repository where agents do not branch: see the exception in [git-workflow.md](../../../standards/workflow/git-workflow.md).

## When to Use

- After adding or editing any document in this knowledge base
- After running `triage-scratch`, `add-experiment`, `update-standards`, or `add-knowledge`
- Before handing off to another agent who may also contribute

## Steps

### 1. Check if pull is needed (before contributing)

Fetch and check if you are behind the remote:

```bash
git fetch origin
git status
```

If the status says you are behind `origin/main`, then pull to avoid conflicts:

```bash
git pull origin main
```

### 2. Review changes

```bash
git status
git diff --stat
```

### 3. Stage all changes

```bash
git add -A
```

### 4. Compose a commit message

Use this format:

```
<type>(<domain>): <brief description>
```

**Types:**
- `feat` — new content added
- `update` — existing content revised
- `supersede` — content replaced (old deleted, new created)
- `fix` — correction to existing content
- `meta` — changes to AGENTS.md, skills, or INDEX files only

**Domains:** `standards`, `experiments`, `goals`, `knowledge`, `tools`, `projects`, `investigations`, `personas`, `scratch`, `meta`

**Examples:**
```
feat(knowledge): add Redis caching patterns
update(standards): revise Python naming conventions
supersede(standards): replace old TS config with strict mode standard
feat(experiments): record results of RAG vs fine-tune comparison (EXP-2026-001)
feat(experiments): add future experiment hypothesis for vector DB benchmarks
```

For multiple domains in one commit, use the most significant one or `meta`.

### 5. Commit

Commit on the branch that is checked out. Do not create a branch.

```bash
git commit -m "<your message>"
```

### 6. Push

Push after every commit:

```bash
git push origin HEAD
```

### 7. Handle diverged history (if the push is rejected)

```bash
git pull --rebase origin main
git push origin main
```

If rebase produces conflicts, resolve them manually then:
```bash
git rebase --continue
git push origin main
```

If the push is rejected because the default branch is protected, this repository is not a personal Engram (for example, it is the public Engram template): move the commits to a work branch and open a pull request.
