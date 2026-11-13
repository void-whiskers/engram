---
status: current
created: 2026-08-08
updated: 2026-11-13
tags: [standards, workflow, git, branching, code-review]
---

# Git & Branching Workflow Standard

This document defines the core strategy for code versioning, commit hygiene, and branching workflows across repositories and projects.

## Core Strategy: Commit Often & Push Small

Smaller, focused changes are significantly easier to review, test, understand, and debug. Unusually large pull requests or monolithic commits increase review cognitive load, hide subtle bugs, and complicate git bisect operations.

### Key Principles

1. **Smaller Changes Are Easier to Review:**
   - Keep commits and pull requests scoped to a single logical change or concern.
   - Break large features or multi-part refactors into small, incremental, reviewable steps.

2. **Commit Often:**
   - Commit logical units of work as you complete them rather than holding all changes locally.
   - Frequent commits create clear checkpoints, make reverting or cherry-picking straightforward, and preserve git history context.

3. **Push Small & Incrementally:**
   - Push commits to the remote frequently.
   - Pushing small, incremental changes prevents data loss, enables early review or feedback, and keeps remote branches up to date.
   - Maintain shared branch integrity. When rebasing or rewriting history on personal feature branches, enforce safe updates using `git push --force-with-lease`.

4. **Branch-Based Development:**
   - **MANDATORY First Action:** Creating and checking out a work branch from an up to date default branch must be the absolute first action taken in any new session, before reading any project code or making modifications.
   - **Avoid pushing directly to `main`** (or default production branches) in any repository.
   - Always create dedicated work branches for ongoing changes conforming to the **Branch Naming Standard** below.
   - Integrate changes into `main` via reviewed pull requests or merge requests.

### Exception: your own Engram

Your Engram is a single-maintainer personal knowledge base, not a code repository. Agents SHOULD work directly on its current branch and MUST NOT create a branch or pull request there unless you explicitly ask. The `sync-memory` skill does the commit and the push.

This exception does not apply to any other repository. In a code repository: branch, commit, push, and raise a pull request. A change to the public Engram template is a change to a code repository, so it goes through a branch and a pull request as well.

---

## Branch Naming Standard

Branch names must describe the **domain feature or technical fix**, never process meta-actions.

### Schema & Types

- **Pattern**: `[<type>/]<ticket>-<slug>` or `<type>/<slug>` (2–4 words, kebab-case)
- **Types**: `feature/`, `fix/`, `refactor/`, `chore/`, `docs/`, `test/`, `exp/`

### Core Rules

1. **Strict Lowercase**: All characters must be `[a-z0-9-/]`. Never keep uppercase ticket keys (use `issue-123`, **never** `ISSUE-123`).
2. **Domain Focus (No Meta-Actions)**: Name what code/system is changing, not what workflow step you are doing.
   - **Anti-patterns (Forbidden)**: `prepare-draft-pr`, `agent-work`, `implement-fixes`, `temp-branch`, `wip`.
   - **Domain patterns (Correct)**: `issue-123-user-session-caching`, `fix/issue-102-auth-header-parsing`, `refactor/btree-traversal`.

### Quick Reference

| Prompt Context | Anti-Pattern | Correct Branch |
| :--- | :--- | :--- |
| "ISSUE-123: Prepare draft PR for user session caching" | `ISSUE-123-prepare-draft-pr` | `issue-123-user-session-caching` |
| "Fix auth header parsing in ISSUE-102" | `ISSUE-102-fix-bug` | `fix/issue-102-auth-header-parsing` |
| "Refactor Engram btree traversal" | `refactor-code-changes` | `refactor/btree-traversal` |

---

## Author Pre-PR Quality Gate & Self-Audit Checklist

Before pushing a branch to open a Pull Request, or declaring a task complete, the author agent MUST execute and pass the Pre-PR Quality Gate. Passing localized unit tests alone is necessary but not sufficient.

### Gate 1: Automated Verification (Linters, Types, Tests)

1. **Run Universal Repository Checks**:
   Execute the repository's CI-equivalent verification command (e.g. `make check`, `make lint`, or `npm run check`).
2. **Zero Errors Policy**:
   All linters, static analysis tools (e.g. `mypy`, `ruff`, `hadolint`, `yamllint`, `eslint`), and test suites must pass with 0 errors. Never push or open a PR expecting CI to catch syntax, type, or formatting issues.

### Gate 2: Pull Request Template Adherence

1. **Inspect PR Template**:
   Check whether the repository has a pull request template (commonly `.github/PULL_REQUEST_TEMPLATE.md`).
2. **Populate Every Mandatory Section**:
   Do not replace the template with an ad-hoc summary. Complete every section it defines. Where the template has no section for it, add concrete verification evidence: the actual commands run and their results.

### Gate 3: Author Diff Self-Interrogation

Run `git diff <default-branch>...HEAD` and check the diff against the project's domain invariants. Each project SHOULD list its own in its project document or repository `AGENTS.md`. Common ones:

- **Precision / Formatting**: Did I introduce arbitrary fixed-decimal rounding (`round(val, 2)`) that breaks small or high-precision values?
- **Environment Parity**: Did I inadvertently exclude simulation, test, or staging modes from monitoring, watchers, or queries?
- **Cold-Boot & Nil Safety**: Can any consumer, API route, or background loop crash on an unhandled missing key or return a `500` if caches or database tables are empty at boot?
- **Canonical Utilities**: Did I use the project's established helpers, or did I invent redundant or non-existent ones?

---

## Project-Level Specialization

While individual projects or repositories may define specialized workflow rules (such as specific branch naming patterns, pull request templates, approval rules, or CI pipeline triggers), the core strategy of **branching, committing often, pushing small changes, and passing the Pre-PR Quality Gate** applies universally across all codebases.
