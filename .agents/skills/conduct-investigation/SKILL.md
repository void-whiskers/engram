---
name: conduct-investigation
description: >-
  Conduct an architectural, root-cause, or exploratory investigation using a subagent
  to isolate context churn, and record the findings in investigations/. Updates year
  and master indexes and links to relevant projects.
---

# conduct-investigation

Conduct an investigation into an architectural question, bug root-cause, or technology trade-off, isolate exploratory context churn using a subagent, and record the findings in `investigations/`.

## When to Use

- Answering architectural questions or evaluating competing technology choices.
- Root-cause analysis of subtle bugs or system failures.
- Feasibility spikes or exploratory probing before committing to an approach.
- Whenever an inquiry requires extensive file reading, log searching, or tool runs that would pollute the main conversation's context window.

> **Investigation vs. Experiment**: If you are testing a falsifiable hypothesis with strict control vs. variable runs and numerical metrics, use `add-experiment`. If you are exploring an inquiry, finding facts, or diagnosing an issue triggered by a prompt or bug, use this skill.

---

## Why Use Subagents for Investigations?

Deep investigations frequently require inspecting dozens of source files, executing shell commands, grepping logs, and testing intermediate assumptions.

1. **Context Window Preservation**: Performing exploration directly in the parent agent burns **20,000 to 50,000 tokens** of disposable tool outputs and debugging iterations. That noise degrades model reasoning and inflates token cost for the remainder of the session.
2. **Context Isolation**: Spawning a subagent delegates the messy trial-and-error work to an isolated, disposable context.
3. **Structured Signal Return**: The subagent synthesizes its findings directly into the standardized Investigation Report format, returning ~300 tokens of pure signal to the parent.

---

## Workflow Steps

### 1. Determine the Next Investigation ID

Check the current year's index:
```bash
cat <path/to/engram>/investigations/$(date +%Y)/INDEX.md
```

If the year directory does not exist yet:
```bash
mkdir -p <path/to/engram>/investigations/$(date +%Y)
```
Create `investigations/YYYY/INDEX.md` with this content, and add a row for the year directory to the Contents table in `investigations/INDEX.md`:

```markdown
# YYYY Investigations Index

> Investigations undertaken in YYYY.

## Contents

| Path | Summary | Status | Date |
| --- | --- | --- | --- |

## Navigation

- Parent: [../INDEX.md](../INDEX.md)
- Root: [../../AGENTS.md](../../AGENTS.md)
```

The next ID format is `INV-YYYY-NNN` (e.g. `INV-2026-003`), where `NNN` is sequential and zero-padded.

### 2. Formulate the Investigation Scope

Extract:
- **Prompt**: The exact trigger prompt, user request, or incident report that prompted the investigation.
- **Goal**: 1–3 concrete questions or unknowns to resolve.
- **Project**: Associated project slug from `projects/` (or `general` if standalone).

### 3. Delegate to a Subagent

Invoke a subagent: a read-only one for codebase or web analysis where your harness offers it, or a general one if write or execution tools are required.

**Subagent Prompt Directive:**
```markdown
You are tasked with conducting an investigation on: <Topic>

CONTEXT / PROMPT:
<Verbatim prompt or error report>

GOAL:
<Bulleted list of specific questions to resolve>

CRITICAL RULES:
1. Conduct all necessary codebase exploration, tool executions, and file reads in your session.
2. Do NOT stream raw logs, large data dumps, or conversational filler back to the parent agent.
3. Format your final report STRICTLY using the Engram investigation format:
   - Frontmatter (status: concluded, created, updated, tags, project)
   - # INV-YYYY-NNN: <Subject / Title>
   - ## Prompt
   - ## Goal
   - ## Findings (structured comparisons, tables, bullet points)
   - ## Outcome & Recommendations (concrete action items and decisions)
4. Either save the completed file directly to `investigations/YYYY/inv-YYYY-NNN-<slug>.md` and return its path with an executive summary, or return the full markdown report in your final message.
```

### 4. Review and Save the Report

Ensure the report adheres to the template at [`investigations/template.md`](../../../investigations/template.md):
- File path: `investigations/YYYY/inv-YYYY-NNN-<slug>.md`
- Status set to `concluded` (or `in-progress` if further evaluation is pending).
- Remove any lingering raw debug dumps or conversational text to keep it token-dense.

### 5. Update Year Index

Add an entry to `investigations/YYYY/INDEX.md`:
```markdown
| [inv-YYYY-NNN-<slug>.md](./inv-YYYY-NNN-<slug>.md) | Concise 1-line summary | concluded | YYYY-MM-DD |
```

### 6. Update Master Investigations Index

Add a row to `investigations/INDEX.md` in the Master Status Table:
```markdown
| INV-YYYY-NNN | [<Title>](./YYYY/inv-YYYY-NNN-<slug>.md) | concluded | YYYY | [<project>](../projects/<project>.md) | Concise conclusion summary |
```
*(If no specific project, use `general` for the Project column).*

### 7. Link from Related Project (If Applicable)

If the investigation is tied to a project in `projects/`, open `projects/<project>.md` and add a reference under `## Related Investigations`:
```markdown
## Related Investigations
- [INV-YYYY-NNN: <Title>](../investigations/YYYY/inv-YYYY-NNN-<slug>.md) — <One-sentence summary of decision or finding>
```

If the investigation reached a definitive architectural choice, also note the key conclusion under `## Key Decisions` in `projects/<project>.md`.

### 8. Graduate Enduring Knowledge or Standards (If Applicable)

If the investigation discovered evergreen facts, system architecture, or new rules:
- Run `add-knowledge` to add persistent domain knowledge to `knowledge/`.
- Run `update-standards` if new workflow or coding standards were established.

### 9. Sync Memory

Run the `sync-memory` skill to commit all additions.
