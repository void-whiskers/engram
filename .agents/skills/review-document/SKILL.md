---
name: review-document
description: >-
  Review and audit an existing or newly created memory document for factual sanity,
  information density, scientific objectivity, and structural integrity against
  the Communication Standard.
---

# review-document

Audit and review a document against the [Communication Standard](../../../standards/workflow/communication.md).

## When to Use

- Immediately after creating or updating any leaf document (experiments, knowledge, standards, projects, tools).
- When auditing existing documentation to prevent "documentation decay" and stale assumptions.
- Before committing significant additions to ensure high token efficiency for future agents.

---

## Review Workflow

### 1. Structural Validation

Run the automated validator to check frontmatter, status enums, broken links, and orphans:

```bash
bash .agents/skills/validate-memory/scripts/validate.sh
```

On Windows, or anywhere without Bash, run `python .agents/skills/validate-memory/scripts/validate.py` instead.

Fix any structural errors, missing tags, or broken relative links before proceeding.

### 2. Four-Pillar Quality Audit

Read the document and evaluate it against the four pillars of the Review Checklist in `standards/workflow/communication.md`:

| Pillar | Verification Question | Action if Failed |
| :--- | :--- | :--- |
| **1. Sense & Objectivity** | Does the text make logical sense? Are hypotheses falsifiable? Is the tone neutral and free of loaded/misleading phrasing? | Rephrase vague or biased assertions; define measurable criteria. |
| **2. Information Density** | Is the document concise? Are lists and tables used instead of narrative fluff? Are emojis omitted? | Cut filler words, convert sprawling paragraphs to tables, eliminate redundant explanations. |
| **3. Factual Sanity** | Do mentioned tech stacks, tools, schemas, and paths match the actual project reality? | Correct stale assumptions (e.g. Postgres vs SQLite) without running expensive full-codebase audits. |
| **4. Structural Hygiene** | Is YAML frontmatter complete and accurate? Is the document reachable within 3 hops? | Ensure `updated` date is current and valid tags are set. |

### 3. Parent Index Synchronization

1. Verify that the parent `INDEX.md` contains an entry pointing to this document.
2. Ensure the summary in `INDEX.md` is concise, accurate, and reflects the latest updates.

### 4. Sync

Once all checks pass, run the `sync-memory` skill to commit and sync changes.
