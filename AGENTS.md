# Engram — Navigation Root

## Core Philosophy
Perfection is impossible, outright. As long as every step we take is a step toward that goal then we can consider that winning.

> ### Opportunistic Tech Debt Management
>
> 1. **Check Local Debt:** When beginning work in a specific component, briefly check the local repository's `TECH_DEBT.md`. If a logged item is in your immediate workspace and simple to resolve alongside your feature, clean it up.
> 2. **Log, Don't Stop:** If you stumble across dead code, duplicated logic, or severe context pollution while working on an unrelated task, **do not derail your task to fix it**. Instead, append a note to `TECH_DEBT.md` describing the debt and its location, then move on.

> ### Thought Partner, Not Sycophant
>
> The agent's job is to solve the real problem, not to make the user feel good about it. Sycophancy — quietly agreeing, hedging, or over-praising to avoid friction — is a failure mode to actively resist, whether the subject is a technical claim or the user's own conduct. If the user's framing, assumptions, diagnosis, or behavior look wrong, say so plainly and explain why. Agreement should track correctness, not the path of least resistance.

## Domain Map

| Domain | Path | Purpose |
|--------|------|---------|
| Standards | [standards/](./standards/INDEX.md) | How we write code, design systems, and run workflows |
| Experiments | [experiments/](./experiments/INDEX.md) | Undertaken experiments + planned future experiments |
| Goals | [goals/](./goals/INDEX.md) | Milestones and objectives we want to achieve |
| Knowledge | [knowledge/](./knowledge/INDEX.md) | Accumulated learnings, domain expertise, reference material |
| Tools | [tools/](./tools/INDEX.md) | How we use specific named tools, APIs, services, frameworks |
| Projects | [projects/](./projects/INDEX.md) | High-level context about active and past projects |
| Investigations | [investigations/](./investigations/INDEX.md) | Exploratory spikes, diagnostic root-cause analyses, tool evaluations |
| Personas | [personas/](./personas/INDEX.md) | Specialized agent roles, responsibilities, scope guardrails, and hand-offs |
| Scratch | [scratch/](./scratch/README.md) | Ephemeral working notes; triaged periodically |

> **tools/ vs knowledge/**: If you'd title the document with a product/tool name (Redis, Docker, GitHub Actions), it belongs in `tools/`. If you'd title it with a concept (caching patterns, distributed systems), it belongs in `knowledge/`.

---

## Navigation Protocol (Read)

To find relevant context for a task:

1. **MANDATORY (First Action)**: In any repository other than this Engram, check out a new work branch from an up-to-date default branch before exploring the codebase, reading any code, or making any changes. Use clean semantic branch naming: strict lowercase kebab-case for the domain feature or fix (e.g. `issue-123-session-caching`), never meta-actions like `prepare-draft-pr`. This Engram is a single-maintainer personal knowledge base: work directly on its current branch unless the user explicitly asks for a branch. (A change to the public Engram template is not a change to your Engram: there, branch and raise a pull request.) Review `standards/workflow/git-workflow.md` for the full conventions.
2. **MANDATORY (Before Coding)**: Check whether a project document exists in the `projects/` directory. If it exists, you MUST read it to understand the project's constraints. If it does not exist, suggest that the user create one with the `add-project` skill.
3. **MANDATORY (Before Coding)**: Check `standards/coding/INDEX.md`, `standards/design/INDEX.md`, and `standards/workflow/INDEX.md` for applicable standards. `workflow/` gets the same treatment as `coding/`, not a lighter one: debugging, PR review, tech-debt, and communication standards apply as directly to a task as coding conventions do. [agent-strategies.md](./standards/workflow/agent-strategies.md) applies to every task regardless of domain (its session-boundary and handoff protocol governs how the task is wrapped up, not just how it starts) and must be read in full each time.
4. Identify which other domain(s) are relevant from the Domain Map above.
5. Read the domain's `INDEX.md` to identify the relevant subdomain or leaf document.
6. Read at most one more `INDEX.md` before reaching a leaf document (**max 3 hops** from this file to any document).
7. If no relevant document exists, check `scratch/` before concluding there is none.

**Before relying on memory whose freshness is material**, run:
```bash
git fetch origin
git status
```
If the checkout is behind `origin/main`, pull before proceeding:
```bash
git pull origin main
```

---

## Core Strategies

- **Token Efficiency & Sub-agents:** To maximize token efficiency and isolate context, prefer using sub-agents for specialized or isolated tasks (e.g. web browsing, deep debugging). See [standards/workflow/agent-strategies.md](./standards/workflow/agent-strategies.md) for details.
- **Session Boundaries & Clean Handoffs:** At natural phase boundaries (post-investigation, plan approval, milestone completion, post-deadlock recovery), proactively suggest starting a fresh conversation with a pre-crafted kickoff prompt rather than accumulating context inertia. See [standards/workflow/agent-strategies.md](./standards/workflow/agent-strategies.md) for details.
- **Commit Often & Push Small:** Keep changes small, incremental, and easy to review. Work on feature/topic branches and avoid pushing directly to main across all repositories. See [standards/workflow/git-workflow.md](./standards/workflow/git-workflow.md) for details.

---

## Contribution Protocol (Write)

When adding or updating knowledge, use the appropriate skill:

| What you're doing | Use this skill |
|-------------------|---------------|
| Adding/revising coding, design, or workflow standards | `update-standards` |
| Recording a completed experiment | `add-experiment` |
| Adding a planned future experiment | `add-experiment` (future mode) |
| Adding general knowledge | `add-knowledge` |
| Adding tool/service knowledge | `add-tool` |
| Adding project context | `add-project` |
| Conducting or recording an investigation | `conduct-investigation` |
| Unstructured notes that don't fit yet | Drop in `scratch/`, run `triage-scratch` later |
| Syncing to GitHub | `sync-memory` |
| Checking structural integrity | `validate-memory` |
| Auditing / reviewing documentation | `review-document` |
| Reviewing a new or changed skill | `skill-review` |

**After contributing**, always run the `sync-memory` skill to commit and push.

**Always update the relevant `INDEX.md`** files after adding or modifying any content.

---

## Frontmatter Schema

All leaf documents (not `INDEX.md` files) must include YAML frontmatter:

```yaml
---
status: <see table below>
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
supersedes: relative/path/to/older-doc.md    # optional: if this replaces another doc
superseded_by: relative/path/to/newer-doc.md # set when this doc is retired before deletion
---
```

**Approved status values by domain:**

| Domain | Statuses |
|--------|----------|
| Standards, Knowledge, Tools, Personas | `current`, `draft`, `superseded` |
| Experiments (concluded) | `in-progress`, `concluded`, `superseded` |
| Experiments (future) | `future`, `undertaken`, `void` |
| Investigations | `in-progress`, `concluded`, `abandoned`, `superseded` |
| Goals / Milestones | `planned`, `active`, `achieved`, `abandoned` |
| Projects | `active`, `paused`, `completed`, `abandoned` |

---

## Supersession Pattern

This is a **git-backed knowledge base**. Git history is the archive — there are no archive folders.

When knowledge becomes outdated:

1. Create the new document with `supersedes: path/to/old-doc.md` in its frontmatter.
2. Add `superseded_by: path/to/new-doc.md` to the **old** document's frontmatter (final edit before deletion).
3. **Delete the old document** — git history preserves it permanently.
4. Update the parent `INDEX.md` to point to the new document.

To recover a superseded document:
```bash
git log -- standards/coding/old-standard.md   # find the last commit hash
git show <hash>:standards/coding/old-standard.md  # view the content
```

### Investigations Are Immutable Snapshots

Investigations are a partial exception to "delete the old document, create a new one." Once concluded, an investigation is a record of what was known and decided at that point in time: its findings and open questions must not be rewritten or corrected in place. `git show` at its concluding commit should always show the same conclusions that session actually reached; a "living" investigation makes that history lie.

- **Allowed edit, resolution**: a minimal back-link when an open question gets resolved. Tick its checkbox and add `Resolved: <PR/plan link> (date)`. The solution lives in the PR or plan; do not restate it in the investigation.
- **Allowed edit, redaction**: removing content the Information Boundary forbids. Replace it with a neutral description that keeps the finding readable, and add `Redacted <date>: <what was removed>` at the end of the document.
- **Nothing else** may change in a concluded investigation.
- **A substantive correction to a finding** (the original analysis was wrong, not merely "now resolved") gets a new investigation with `supersedes`/`superseded_by`, exactly like any other domain document. Never rewrite the concluded one in place.

---

## Sync Protocol

- **Before relying on memory whose freshness is material**: run `git fetch origin` and `git status`. Pull only if behind.
- **After contributing**: Use the `sync-memory` skill to commit and push. It pushes after every commit.
- **Remote**: Private GitHub repository (already configured)

---

## Available Skills

Skills are defined in [.agents/skills/](./.agents/skills/). Read the relevant `SKILL.md` before executing.

| Skill | Purpose |
|-------|---------|
| [`sync-memory`](./.agents/skills/sync-memory/SKILL.md) | Commit all changes and push to GitHub |
| [`triage-scratch`](./.agents/skills/triage-scratch/SKILL.md) | Review scratch notes and promote or delete them |
| [`add-experiment`](./.agents/skills/add-experiment/SKILL.md) | Create a new experiment doc (concluded or future), update indexes |
| [`update-standards`](./.agents/skills/update-standards/SKILL.md) | Revise a standard with supersession tracking |
| [`add-knowledge`](./.agents/skills/add-knowledge/SKILL.md) | Add a new knowledge leaf, create subdomain if needed, update indexes |
| [`add-tool`](./.agents/skills/add-tool/SKILL.md) | Add tool/service knowledge to tools/ |
| [`add-project`](./.agents/skills/add-project/SKILL.md) | Add project context to projects/ |
| [`conduct-investigation`](./.agents/skills/conduct-investigation/SKILL.md) | Conduct an investigation using a subagent to isolate context churn and record findings |
| [`validate-memory`](./.agents/skills/validate-memory/SKILL.md) | Run automated consistency checks on the knowledge base |
| [`review-document`](./.agents/skills/review-document/SKILL.md) | Audit and review documents against the Communication Standard |
| [`skill-review`](./.agents/skills/skill-review/SKILL.md) | Review new or changed agent skills for coherence, safety, and behavioural evidence |

---

## Naming Conventions

- **Experiments**: `exp-YYYY-NNN-<slug>.md` (e.g. `exp-2026-001-llm-context-window-limits.md`)
- **Future experiments**: `future-NNN-<slug>.md` (e.g. `future-001-rag-vs-finetune.md`)
- **Investigations**: `inv-YYYY-NNN-<slug>.md` (e.g. `inv-2026-001-session-cache-eviction.md`)
- **Milestones**: `ms-NNN-<slug>.md` (e.g. `ms-001-launch-engram.md`)
- **Knowledge/Standards**: `<topic-slug>.md` (e.g. `python.md`, `redis-caching.md`)
- **Slugs**: lowercase, hyphenated, descriptive
- **Dates**: ISO 8601 (`YYYY-MM-DD`)
- **IDs**: NNN is zero-padded, scoped per year for experiments and investigations, global for milestones
