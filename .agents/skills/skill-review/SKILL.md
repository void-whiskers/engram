---
name: skill-review
description: Review a new or changed agent skill for instruction coherence, safe authority boundaries, and evidence that it produces the intended behaviour. Use when developing or reviewing skills.
---

# Skill Review

Review a skill as executable guidance, not merely as Markdown. Apply this workflow to a new or changed `SKILL.md`, its templates, references, examples, scripts, and UI metadata.

Use the general [Pull Request Review Standard](../../../standards/workflow/pull-request-review.md) and [Communication Standard](../../../standards/workflow/communication.md) as the baseline. This skill adds checks specific to agent behaviour.

## Establish the contract

1. Read the whole `SKILL.md` and every changed or directly referenced resource needed by the skill's active workflow.
2. Identify the intended trigger, supported inputs, observable outcome, deliberate exclusions, and required completion evidence.
3. Identify the skill's authority boundary: read-only work, local edits, tracker/API writes, credential use, destructive actions, cost-bearing actions, and stopping conditions.

Do not infer requirements from an example. Treat examples as evidence only when the instructions make them normative.

## Review checks

### Discovery and scope

- The name and description MUST be concise and distinguish this skill from adjacent skills.
- The description MUST state when the skill applies and SHOULD name important exclusions that prevent false activation.
- The skill MUST preserve the user's requested product, scope, and authorisation boundaries.
- Generic advice already enforced by system or repository instructions SHOULD NOT be duplicated.

### Instruction and output contract

- Instructions, templates, examples, references, and scripts MUST agree on required versus optional fields, ordering, terminology, and output format.
- A supported request MUST have one deterministic valid path. Clarification rules MUST not conflict with output-only rules.
- Templates MUST mark optional sections as optional; examples that deliberately omit sections MUST agree with the template and guidance.
- The completion signal and any validation requirement MUST be observable. Do not require tautological statements or placeholder ceremony.
- References MUST be reachable from the active instructions and read only when relevant.

### Safety and authority

- The skill MUST require explicit current-request authorisation before tracker writes, external messages, deployments, destructive actions, or other material state changes.
- Credential and secret handling MUST prevent values from entering chat, command output, patches, or tracked files.
- Failure handling MUST leave the user with a truthful status and a safe next action; the skill MUST NOT silently continue after an unexpected failure.
- Retry, rollback, idempotency, and cost controls MUST be explicit when the workflow needs them.

### Evidence and maintainability

- Added or changed scripts MUST be executed against a meaningful input or invariant.
- Run the available structural validator. For Codex skills, use `quick_validate.py` from the `skill-creator` package when it is available.
- Verify links, paths, commands, tool names, and referenced schemas against the actual target environment.
- Use realistic scenario tests for changes that affect decisions, output shape, permissions, or external actions. Do not rely only on wording, heading, or regex checks.
- For complex or high-risk skills, use an independent forward-test when delegation is available and the evaluation is authorised. Give the evaluator a realistic request and the minimum needed artefacts, not the expected answer or suspected defect.

## Decision

Approve only when the skill fulfils its contract, has no contradictory instructions, respects authority boundaries, and has proportionate evidence for the changed behaviour.

Request changes for incorrect routing, conflicting instructions, unsafe or implicit authority, untestable completion claims, stale references, or missing validation evidence. Use comments only for improvements that do not change correctness, safety, or deterministic behaviour.

Record:

- Decision and blockers.
- Contract and deliberate exclusions checked.
- Validation performed and its result, including checks that were unavailable.
- Remaining non-blocking follow-up work.

## Suggested changes

When reviewing a pull request, make suggestions directly applicable where practical. A suggestion MUST preserve the skill's contract and SHOULD update every coupled template, example, or reference needed to keep the instructions coherent.
