# Scratch

Scratch is for unstructured working notes that don't have a clear home yet.

## Rules

- **Not indexed**: Scratch files are invisible to B-tree navigation. Don't rely on them for knowledge retrieval.
- **Ephemeral by design**: Notes here should either be promoted to the right domain or deleted.
- **No naming convention**: Use whatever filename makes sense in the moment.
- **Triaged by the `triage-scratch` skill**: Run this skill when scratch accumulates notes.

## When to Use Scratch

- Capturing notes mid-task when the right domain isn't clear yet
- Working notes during an experiment (before formalising results)
- Rough ideas for future experiments that need more thought before creating a `future/` doc
- Anything that doesn't fit neatly elsewhere right now

## When NOT to Use Scratch

- If you know it belongs in `knowledge/`, `experiments/`, `standards/`, etc. — put it there directly
- For permanent reference material — it will be invisible to other agents navigating the B-tree

## Triaging

Run the `triage-scratch` skill to process accumulated notes:
```
Read .agents/skills/triage-scratch/SKILL.md
```
