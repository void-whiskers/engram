---
status: current
created: 2026-08-05
updated: 2026-11-15
tags: [standards, workflow, planning, roadmapping]
---

# Planning and Roadmapping Standard

A roadmap is the one ordered list of what happens next for a project. It answers "what do I work on now?" without a conversation, and it records each change of direction. Context, architecture and standing decisions stay in the project document, which links to the roadmap.

- **Location:** `projects/<project>-roadmap.md`, listed in `projects/INDEX.md`. For a project you share with other people, put the roadmap in the project's own repository instead, where they can read it, and link to it from the project document.
- **Template:** [roadmap-template.md](../../projects/roadmap-template.md).
- **When to create one:** the project has more queued work than one session finishes, or its priorities have changed more than once. A project with a single next step does not need one.

## Requirements

1. **One ordered list.** Position is priority. The top of Now is the work; nothing is ranked by labels or dates.
2. **Objective and scope.** One sentence for what the roadmap is trying to reach, then what is in scope and what is explicitly out.
3. **Dated assumptions.** Each fact the plan relies on, with the date it was checked. Re-check an assumption before a step that depends on it.
4. **Open decisions are separate from work.** A decision that belongs to the owner is listed with its options, a recommendation, and the item it blocks. An item is never silently blocked.
5. **Item-scoped detail.** Detail sits under the item it belongs to. An item states its done condition unless that is obvious.
6. **Current.** Read at the start of a session and updated at the end. Agents act on what the roadmap says, so a stale roadmap misdirects work.
7. **Short.** Finished items are removed, not ticked and kept. Git history is the archive.

## Sections

In this order.

| Section | Holds | Notes |
| --- | --- | --- |
| Header | Objective, scope, link to the project document | |
| Rules | How the roadmap is used (see below) | |
| Assumptions | Facts relied on, with check dates | Omit if none |
| Now | The item in progress | Ordered if more than one |
| Next | Queued items, in order | About 10 at most |
| Waiting | Items that cannot start until a date or condition | Table: When, Item, Source |
| Decisions waiting on the owner | Open decisions, each with options and a recommendation | Omit if none |
| Later | Unordered backlog | Or a pointer to the issue tracker |
| Changes | Dated log of finished items and changes of direction | Table: Date, Change, Pushed down |

## Rules

Every roadmap carries these rules in its own Rules section, so an agent that reads only the roadmap follows them.

1. **Start of session:** read the roadmap. The top of Now is the work. A request that is not the Now item gets one line first: what it displaces.
2. **End of session:** update the roadmap. Finished → one line in Changes, then removed. Found during the work → inserted where it belongs, with the reason. A Waiting item whose date or condition has come moves into Next.
3. **Change of direction:** allowed at any time, logged in Changes with what it pushed down.
4. **Jumps the queue without asking:** the roadmap names the one or two classes of event that do (for example a credential exposure or a production safety fault). Nothing else does.
5. **Backlog:** it lives in Later or in the issue tracker, not both. If it is in the tracker, Later is a pointer.

A project MAY add rules of its own, for example how work is delivered (one pull request per item).
