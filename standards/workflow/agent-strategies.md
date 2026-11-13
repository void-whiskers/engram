---
status: current
created: 2026-08-05
updated: 2026-11-15
tags: [standards, workflow, agents, token-efficiency, documentation, privacy]
---

# Agent Strategies

This document outlines core strategies for AI agents working within this environment, focusing on token efficiency, context management, delegation, and documentation structure.

## Sub-Agents and Delegation

To maximize token efficiency and prevent context bloat, complex or isolated tasks should be delegated to sub-agents.

### Why Use Sub-Agents?

- **Token Efficiency:** A sub-agent can be spawned with a very narrow context, preventing large log outputs or irrelevant intermediate steps from cluttering the main session's context window.
- **Isolation:** Operations like web browsing, running extensive tests, or deep-diving into specific, isolated file structures are perfect for sub-agents.
- **Parallelism:** Sub-agents can sometimes work asynchronously while the main agent handles other coordination tasks.

### When to Delegate

- **Research & Browsing:** Use a `browser_subagent` to research documentation, navigate web pages, and return only the final summarized findings.
- **Deep Investigations:** When a bug or feature requires reading many files and following long chains of logic that aren't relevant to the high-level task.
- **Sandbox Execution:** When running code that might fail repeatedly, a sub-agent can handle the error-recovery loop and report back when successful.

### Best Practices for Spawning Sub-Agents

1. **Provide Clear Instructions:** The prompt to the sub-agent must be highly detailed, containing a comprehensive task description and a strict condition for when to stop.
2. **Limit Provided Context:** Only pass the exact files or URLs the sub-agent needs.
3. **Require a Summary:** Explicitly instruct the sub-agent to return a concise summary of its findings and actions, rather than a massive log dump.

### The Subagent Investigation Hand-off Pattern

Deep investigations (debugging, architectural evaluations, root cause analysis) carry extreme risk of parent session context exhaustion. Exploration often requires reading tens of files, running test scripts, and inspecting logs—generating 20,000 to 50,000 tokens of intermediate churn.

To isolate this churn:

1. **Delegate to a Subagent**: The parent agent spawns a subagent (read-only where the harness offers one) with the verbatim user prompt, 1–3 concrete target questions, and the strict requirement to report back using the standard Investigation Template (`Prompt`, `Goal`, `Findings`, `Outcome & Recommendations`).
2. **Exploration in Isolation**: The subagent carries out all exploratory reads, searches, and trial-and-error checks exclusively within its disposable context window.
3. **Structured Signal Return**: The subagent delivers only the synthesized report (~300 tokens) back to the parent agent (or commits the file to `investigations/YYYY/inv-YYYY-NNN-<slug>.md`).
4. **Parent Context Preservation**: The parent conversation remains completely unpolluted by the noisy investigation churn, retaining full reasoning capacity to implement solutions or engage with the user.

---

## Session Boundaries and Context Handoffs

Just as subagents isolate intermediate exploration within a session, **session boundaries isolate lifecycle phases across sessions**. Agents must actively resist conversational inertia — continuing in a bloated context window when a task has reached a natural resting point.

### The "Clean Desk" Principle

A session boundary should feel like finishing early with everything working and state committed. Before suggesting a handoff:

- The current phase, spike, or diagnostic loop is completely concluded.
- Tests are passing and the working tree is clean or committed to a feature branch.
- Findings and decisions are externalized into durable files (`investigations/`, `projects/`, or plan artifacts), not trapped in chat history.

### The 4 Semantic Phase Boundaries

Suggest a handoff at lifecycle transitions where prior context has become dead scaffolding:

1. **Investigation → Implementation:** A spike or root-cause audit is concluded and findings are committed to an investigation document. The next step is design or code changes.
2. **Plan Consensus → Execution:** A design discussion or implementation plan has been approved. The debate over discarded alternatives is obsolete; the approved plan is the single source of truth.
3. **Milestone / Roadmap Phase Completed:** A discrete sub-phase has passed verification and been committed.
4. **Post-Deadlock Recovery:** A difficult error or churn-heavy debugging loop has finally been diagnosed and resolved with a verified fix.

### The Handoff Bundle Contract

An agent must never give a vague suggestion to start a new chat. It must deliver a frictionless **Handoff Bundle**:

1. **State Anchor:** Confirm where state is saved (branch name, commit, investigation or plan link).
2. **Kickoff Prompt:** Provide an exact, pre-written prompt in a copyable code block that gives the next agent immediate orientation without needing conversation history.
3. **Non-Blocking Fork:** Always offer the option to continue immediately in the current session if the user prefers to keep momentum.

#### Standard Handoff Format

> **Phase Complete:** [Brief summary of accomplishment]
> **State Anchor:** Committed to `[branch]` ([link to doc/commit])
>
> *This is a natural resting point to start a fresh conversation with a clean context window. If you'd like to start fresh, paste this into the next session:*
> ```text
> On branch <branch>. Read <path-to-anchor-doc>. Proceed with <next concrete phase/task>.
> ```
> *(Or, reply here if you prefer to continue in this session.)*

---

## Documentation Formatting for Agent Consumption

Knowledge base files, standards, and memory documents are primarily read and processed by AI agents. To maximize semantic precision and token efficiency:

- **Maximize Information Density & Eliminate Redundancy:** Write concise, high-signal documentation. Avoid repeating definitions across multiple sections, verbose narrative explanations, or boilerplate. Favor compact schemas, focused rule sets, and single quick-reference tables.
- **Avoid Emojis in Agent Documentation:** Unicode emojis decompose into 2–4 tokens each in BPE tokenizers and carry weaker syntactic anchoring than explicit markdown tokens.
- **Use Explicit Lexical Markers:** Use standard markdown emphasis and clear tags (e.g. `**Anti-Pattern:**`, `**Correct:**`, `**Warning:**`, `**Required:**`).
- **Scope Guardrail:** This rule applies specifically to stored memory documents, standards, and guidelines intended for agent parsing. It does not dictate or restrict conversational tone when agents interact with human users.

---

## Information Boundary

Your Engram is a personal, cross-context knowledge base: agents read it from every repository you work in. Every entry MUST be safe to disclose outside the context in which it was learned.

- **Public-safe requirement:** Agents MUST store only information that could be published without edits and without exposing confidential, employer, client, customer, security, or personal information.
- **Work-information prohibition:** Agents MUST NOT store information learned through employment, client, contractor, or other confidential work. This includes information that has been partially sanitised when the source, combination of details, or context could still reveal non-public information.
- **Default to omission:** When the confidentiality or identifying nature of information is uncertain, agents MUST omit it.
- **Safe examples:** Agents MUST use fictional examples such as `example.com`, `ISSUE-123`, and `organisation/repository` rather than real work identifiers.
- **Prohibited content, from any source:** Agents MUST NOT store credentials, security findings, customer data, employer or client names, or the fully qualified domain names and IP addresses of private infrastructure.
- **Prohibited content, except where it concerns a project you own:** Agents MUST NOT store internal repository names or links, ticket or pull-request identifiers, internal domains, internal paths, account or resource identifiers, commercial information, non-public roadmaps, or operational procedures.
- **Approved location for work context:** Work-specific knowledge MUST remain in the relevant work repository, issue tracker, approved documentation system, or another storage location authorised for that work.

### Project documentation

Project documents are default-deny. Agents MAY create one only for a project you own or a public open-source project, and only when every included fact meets the public-safe requirement. A project you own is one you control, alone or with co-owners, that is not done for, or owned by, an employer or client; its repository may be public or private.

- **Any permitted project:** the document MAY include a public repository or homepage, a high-level purpose, public technology choices, and stable non-sensitive decisions.
- **A project you own:** the document MAY also record architectural constraints and facts about how you run it that the code does not state (for example the scale of the data it must handle, an indexing rule, or an API contract). These are what an agent most needs from the document. You decide whether they can be published; for a jointly owned project, record only what every owner would publish.
- **A public project you do not own:** the document MAY also record architectural constraints, but only those a reader could verify in its public source. It MUST NOT include architecture that is not visible there, deployment topology, unreleased work, incidents, performance data, schedules, or references to issues that are not public.
- **Never, for any project,** in addition to the prohibited content above: absolute host paths, people other than you, customers, vendor or partner relationships, contracts, or costs.
- A work-project exception does not exist. If a lesson cannot be stated independently of confidential work context, it MUST NOT be stored here.
