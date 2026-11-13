---
name: add-experiment
description: >-
  Create a new experiment document — either a concluded/in-progress experiment
  in experiments/YYYY/ or a planned future experiment in experiments/future/.
  Updates all relevant indexes and links to goals if applicable. Use this skill
  whenever recording experimental work or capturing a hypothesis for future testing.
---

# add-experiment

Create an experiment document and keep all indexes consistent.

## When to Use

- Recording the results of a conducted experiment → **concluded/in-progress mode**
- Capturing a hypothesis you want to test later → **future mode**
- Promoting a future experiment to a real experiment (when work begins or concludes)

---

## Mode A: Concluded or In-Progress Experiment

### 1. Determine the next experiment ID

Check the current year's index:
```bash
cat <path/to/engram>/experiments/$(date +%Y)/INDEX.md
```

If the year folder doesn't exist yet, create it:
```bash
mkdir -p <path/to/engram>/experiments/$(date +%Y)
```

And create `experiments/YYYY/INDEX.md` (copy the structure of another year's `INDEX.md` and update the year; if no year directory is left, copy `experiments/future/INDEX.md` and adjust the title, description, and Navigation links).

The next ID is `EXP-YYYY-NNN` where NNN is the next sequential number (zero-padded to 3 digits).

### 2. Create the experiment file

Use the template at [`experiments/template.md`](../../../experiments/template.md).

File path: `experiments/YYYY/exp-YYYY-NNN-<slug>.md`

Example: `experiments/2026/exp-2026-001-rag-vs-finetune-accuracy.md`

Fill in all sections. At minimum, hypothesis and conclusions must be complete for `status: concluded`.

### 3. Update year INDEX.md

Add a row to `experiments/YYYY/INDEX.md`:

```markdown
| [exp-YYYY-NNN-slug.md](./exp-YYYY-NNN-slug.md) | Brief description | concluded | YYYY-MM-DD |
```

### 4. Update master experiments/INDEX.md

Add a row to the master table in `experiments/INDEX.md`.

### 5. Link to a future experiment goal (if applicable)

If this experiment was planned in `experiments/future/`, update that doc:
- Change its `status` to `undertaken`
- Add a link to the new experiment: `Experiment: [EXP-YYYY-NNN](../YYYY/exp-YYYY-NNN-slug.md)`

If a planned experiment can no longer be run as written (for example, a condition it depended on has changed), do not delete it:
- Change its `status` to `void`
- Under its **Experiment** heading, record the date and the reason it will not be run

### 6. Update impacted documents

If the experiment produced insights that change existing knowledge or standards:
- Update those documents (use `update-standards` or `add-knowledge` as appropriate)
- Link back from the experiment's **Impact** section

### 7. Sync

Run the `sync-memory` skill.

---

## Mode B: Future Experiment (Planned Hypothesis)

### 1. Determine the next future experiment number

Check `experiments/future/INDEX.md` for the current highest number.

### 2. Create the future experiment file

File path: `experiments/future/future-NNN-<slug>.md`

Use this template:

```markdown
---
status: future
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
---

# FUTURE-NNN: <Title>

## Motivation
Why do we want to run this experiment? What problem does it address?

## Hypothesis
What do we expect to find? Be specific enough that the experiment can confirm or deny it.

## Proposed Method
How would we test this? What would we measure?

## Success Criteria
What result would confirm or deny the hypothesis?

## Notes
Any relevant context, related experiments, or prior art.

## Experiment
<!-- Filled in when undertaken -->
```

### 3. Update experiments/future/INDEX.md

Add a row:
```markdown
| [future-NNN-slug.md](./future-NNN-slug.md) | Brief description | future | YYYY-MM-DD |
```

### 4. Sync

Run the `sync-memory` skill.

---

## Experiment ID Reference

- **Concluded/In-progress**: `EXP-YYYY-NNN` — scoped per calendar year, zero-padded
- **Future**: `FUTURE-NNN` — global sequence, zero-padded
