# Contributing to Engram

First off, thank you for considering contributing to Engram! It's people like you that make open source such a great community.

## How to Contribute

This repository serves as a template for agent memory frameworks. While the `AGENTS.md` file defines how *agents* contribute to the memory repository itself, human contributors can help improve the base template.

### Reporting Bugs
If you find a bug or a typo, please use the Bug Report issue template to submit it. Include as much detail as possible to help us reproduce the issue.

### Suggesting Enhancements
Have an idea for a new agent skill, or a better way to structure the B-tree navigation? 
- Open an issue using the Feature Request template to discuss your idea before writing code.
- This ensures your time is well spent and aligns with the project's direction.

### Pull Requests
1. Fork the repository and create your branch from `main`. The rule in `AGENTS.md` that agents commit directly applies to a personal Engram, not to this template: a change here is always a branch and a pull request, whether a person or an agent makes it.
2. Make sure your code or markdown adheres to the existing style.
3. Update any relevant documentation, including the parent `INDEX.md` of any document you add, move, or change.
4. Run the validator and make sure it passes: `bash .agents/skills/validate-memory/scripts/validate.sh` (or `python .agents/skills/validate-memory/scripts/validate.py`). CI runs both.
5. Issue that PR!

## Community
Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
