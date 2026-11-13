---
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [<project>, roadmap, priorities]
---

# <Project>: roadmap

<!-- Copy to projects/<project>-roadmap.md and add it to projects/INDEX.md; for a project shared with other people, copy it to the project's own repository instead. -->
<!-- Standard: standards/workflow/planning-and-roadmapping.md. Remove all HTML comments before saving. -->

The one ordered list of what happens next for <Project>. Context and standing decisions are in the project document, `<project>.md`.

**Objective:** <one sentence: what this roadmap is trying to reach>

**Scope:** in: <what is covered>. Out: <what is explicitly not>.

## Rules

1. **Start of session:** read this file. The top of **Now** is the work. A request that is not the Now item gets one line first: what it displaces.
2. **End of session:** update this file. Finished → one line in **Changes**, then removed. Found during the work → inserted where it belongs, with the reason. A **Waiting** item whose date or condition has come moves into **Next**.
3. **Change of direction:** allowed at any time, logged in **Changes** with what it pushed down.
4. **Jumps the queue without asking:** <the one or two classes of event that do>. Nothing else.
5. **Backlog:** <in Later below | in the issue tracker; Later is a pointer>.

## Assumptions

<!-- Omit this section if there are none. -->

Checked YYYY-MM-DD; re-check any that a step depends on.

- <a fact the plan relies on>

## Now

1. **<Item>.** <What it is and where the work lives: branch, pull request, issue.>
   - Done = <an observable condition>.

## Next

2. **<Item>.** <Detail that belongs to this item only.>

## Waiting

| When | Item | Source |
| --- | --- | --- |
| <date or condition> | <item> | <why it waits: an issue, a decision, an external limit> |

## Decisions waiting on <owner>

<!-- Omit this section if there are none. -->

- **<Decision>** (blocks <item>): <option A> (recommended: <reason>), or <option B>.

## Later

- <an unordered backlog item, or a pointer to the issue tracker>

## Changes

| Date | Change | Pushed down |
| --- | --- | --- |
| YYYY-MM-DD | Roadmap created | — |
