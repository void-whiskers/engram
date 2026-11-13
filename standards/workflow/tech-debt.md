---
status: current
created: 2026-09-04
updated: 2026-11-11
tags: [standards, workflow, tech-debt]
---

# Tech Debt Management

Technical debt is an inevitable and sometimes necessary part of rapid software development. This standard defines how we categorize, avoid, introduce, and clean up technical debt without halting momentum.

## 1. The Two Faces of Debt

### Accidental / Toxic Debt
This includes orphaned files, obsolete comments, duplicated logic, and misleading naming conventions.
- **Impact:** It actively harms AI reasoning ("Context Pollution"). It burns tokens, distracts reasoning models, and forces agents to spend time analyzing code that isn't used.
- **Action:** We ruthlessly prune this opportunistically.

### Strategic / Intentional Debt
This includes hardcoding a configuration, skipping a database migration, or mocking a service to validate a feature faster.
- **Impact:** It buys us velocity today at the cost of refactoring tomorrow. It is debt taken on for the "greater good" of learning and validation.
- **Action:** It must be logged immediately upon creation and repaid when it blocks scaling or creates bugs.

---

## 2. How to Avoid Accidental Debt

- **Delete ruthlessly:** If code isn't called, remove it. Git history is forever; we do not need to keep commented-out code or unused files "just in case."
- **Avoid over-engineering:** Do not build complex abstractions before the pattern is proven. Build the simplest thing that works.
- **Review generated code:** Agents should actively review their own generated code for unused imports, leftover debug statements, and dead branches before opening a PR.

---

## 3. When to Introduce Strategic Debt

Introduce strategic debt when the cost of building the "perfect" architecture delays learning or feature validation.

**Rule:** Strategic debt MUST be logged in the local repository's `TECH_DEBT.md` (if one exists) immediately upon creation.
- Tag it as `Strategic`.
- Include the specific condition for repayment (e.g., *"Hardcoded fee tier for the one payment provider. Repay this when we support a second provider"*).

---

## 4. When (and How) to Clean it Up

Perfection is anti-ship. We do not drop everything to fix tech debt unless it meets specific criteria.

### The Opportunistic Path (The "Boy Scout" Rule)
If you are modifying a file or working in a specific feature area that has logged debt, clean it up as part of your current feature branch. Fix debt when you are already in the neighborhood.

### The Tipping Point (Formal Repayment)
If a piece of strategic debt is actively blocking a new feature or causing production bugs, it gets promoted to a formal, scoped task. It must be addressed before or alongside the feature that it blocks.

---

## 5. The "See It, Log It, Move On" Habit

If you stumble across dead code, duplicated logic, or severe context pollution while working on an **unrelated task**:
1. **Do not derail your task to fix it** (unless it takes less than 5 seconds).
2. Append a note to the local `TECH_DEBT.md` describing the debt, its location, and why it is problematic.
3. Move on. Maintain momentum on your primary goal.

---

## 6. Closing Out Resolved Debt

`TECH_DEBT.md` tracks what is still owed, not a history of what used to be owed. Once a logged item is fully fixed, it is no longer debt — it does not belong in the register at all, "resolved" or otherwise.

- **Delete the row, don't annotate it.** When a fix lands, remove the entry from `TECH_DEBT.md` in the same PR. The commit message and PR description are the permanent record of what was wrong and how it was fixed — git history is the archive, same as everywhere else in this knowledge base (see the Supersession Pattern). Do not leave a "**Resolved (date):** ..." paragraph appended to the row; that recreates the exact context-pollution problem Section 1 warns against, just inside the debt register instead of the codebase.
- **Partial fixes get trimmed, not narrated.** If a fix closes part of a logged item but a real gap remains, rewrite the row to describe only the remaining gap. Do not keep the resolved portion's backstory in the row — reference the PR that did the partial fix by number/branch if that context is genuinely needed to understand the remaining gap, and nothing more.
- **Rescoped debt moves, it doesn't duplicate.** If an item is deferred or folded into a different logged item's scope (rather than fixed), merge the note into the item it now belongs under and delete the original row — don't leave both a live row and a superseded one pointing at each other.
- **"Fully fixed" requires re-checking the original symptom, not just testing the implementation.** If a row was logged from an *observed* symptom — a live incident, a production bug, a reproduced failure — passing unit/integration tests against the new code is necessary but not sufficient to call it fixed. Tests verify the implementation does what you intended; they don't prove the real-world symptom is actually gone, and for whole classes of debt (capacity, concurrency, timing, load) the failure only appears under real conditions tests don't reproduce. Before deleting the row: reproduce or exercise that same class of real condition (a real running stack, real concurrent load, the actual failure trigger — not a mock of it) and confirm the symptom no longer occurs. Do this before the row is deleted and before the PR is considered done — not as a promised follow-up, and not before merge if merge is what makes the fix real. Debt logged from a code-smell or review finding, with no observed symptom to re-check, can still close on tests + review alone.
