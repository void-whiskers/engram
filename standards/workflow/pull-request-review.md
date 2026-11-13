---
status: current
created: 2026-08-26
updated: 2026-11-11
tags: [standards, workflow, pull-requests, review]
---

# Pull Request Review Standard

## Objective

A review MUST establish whether a pull request safely fulfils its ticket. Passing CI is evidence that checks ran; it is not proof that the ticket outcome is correct. Review output MUST add decision-relevant information; it MUST NOT repeat the author’s description, ticket checklist, or already-agreed deployment plan.

## Review sequence

1. **Define the contract.** Read the ticket, pull request description, linked decisions, and environment scope. Identify the required outcome, exclusions, and completion evidence.
2. **Trace the change.** Follow trigger or input → validation → implementation → observable result. Check control flow, failure handling, and unintended behaviour.
3. **Assess operational safety.** Check environment guards, permissions, secret handling, destructive effects, idempotency, rollback, and configuration persistence.
4. **Verify evidence.** Confirm relevant tests cover the new execution path and failure cases. Review CI, static analysis, and targeted manual evidence proportionate to the declared delivery stage and risk.
5. **Record a decision.** State approve, request changes, or comment. Separate merge blockers from optional follow-ups.

## Required checks

| Area | Review question |
| --- | --- |
| Scope | Does the change fulfil the ticket without silently expanding to other environments, systems, or behaviour? |
| Correctness | Does each supported input take the intended path and produce the required result? |
| Safety | Can the change expose secrets, affect the wrong environment, leave partial state, or make recovery harder? |
| Domain Invariants | Does the diff preserve the project's domain invariants (for example numerical precision, parity between production and simulation or staging modes, safe behaviour when caches or tables are empty at boot) and use the project's canonical utilities? |
| Verification & Quality Gate | Do tests prove the changed path and error cases? Did the author run the universal check suite (`make check` / CI equivalent) with 0 errors and provide complete evidence in the PR template? |
| Maintainability | Is the diff focused, readable, and consistent with repository conventions? |

## Decision rules

- **Approve** only when ticket requirements, safety checks, and proportionate verification evidence are satisfied.
- **Request changes** for correctness, security, scope, or verification gaps.
- **Comment** only when there is a specific non-blocking finding the author needs to act on or consciously accept. Comments MUST NOT obscure a merge-blocking issue.

## Useful review comments

A PR comment MUST be anchored to a concrete diff location or directly linked evidence. It MUST state the observed issue, why it matters, and the specific outcome requested. Keep it short enough that the author can decide whether to change the PR without reconstructing the reviewer's reasoning.

Do not comment merely to:

- restate the PR description, ticket Definition of Done, or the author's stated test plan;
- list generic future checks such as "validate in Dev" or "add tests before production";
- announce that a deliberately staged change is not production-ready when its scope already makes that clear.

For an intentionally staged delivery, treat the declared next environment as part of the PR contract. Missing automated coverage is a merge blocker only when it is needed to establish the current stage's safety or is explicitly required before merge. Otherwise, record a follow-up only when it names a concrete untested behaviour and a destination for that work (an existing ticket or a newly requested one).

If a review finds no new actionable information beyond the agreed rollout plan, approve without adding a comment.

## Review record

A review SHOULD state:

- Decision and blockers, if any.
- The concrete finding that changes the decision, linked to the relevant code or evidence.
- Verification performed and its result, without replaying the PR description.
- Any deliberate exclusion only if it affects the current merge decision.

## Related standards

- [Git & Branching Workflow](./git-workflow.md)
- [Communication Standard](./communication.md)
