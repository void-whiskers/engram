# Engram Maintenance Skills

This directory contains specialized skills and automated scripts for maintaining the Engram knowledge base.

## Available Skills

| Skill | Purpose |
| :--- | :--- |
| [`sync-memory`](./sync-memory/SKILL.md) | Commit changes and push to GitHub |
| [`triage-scratch`](./triage-scratch/SKILL.md) | Review ephemeral scratch notes and promote or delete them |
| [`add-experiment`](./add-experiment/SKILL.md) | Create a new experiment doc and update relevant indexes |
| [`update-standards`](./update-standards/SKILL.md) | Revise a standard with supersession tracking |
| [`add-knowledge`](./add-knowledge/SKILL.md) | Add a new domain knowledge leaf |
| [`add-tool`](./add-tool/SKILL.md) | Add tool/service knowledge to `tools/` |
| [`add-project`](./add-project/SKILL.md) | Add project architectural constraints |
| [`conduct-investigation`](./conduct-investigation/SKILL.md) | Conduct an investigation in a subagent and record the findings in `investigations/` |
| [`validate-memory`](./validate-memory/SKILL.md) | Run automated consistency checks on the knowledge base |
| [`review-document`](./review-document/SKILL.md) | Audit a document against the Communication Standard |
| [`skill-review`](./skill-review/SKILL.md) | Review a new or changed skill for coherence, safe authority boundaries, and evidence |

---

## Cross-Platform Execution

The two validation scripts run the same checks, so use whichever interpreter you have:

- **Linux / macOS / WSL / Git Bash**: Run `bash .agents/skills/validate-memory/scripts/validate.sh`
- **Windows (PowerShell / Command Prompt)**: Run `python .agents/skills/validate-memory/scripts/validate.py`

No external dependencies or package installations are required (Bash with the standard POSIX tools, or the Python standard library).
