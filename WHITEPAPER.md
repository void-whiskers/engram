---
status: current
created: 2026-08-28
updated: 2026-11-13
tags: [engram, whitepaper, pilot-study, agent-memory, benchmark]
---

# Engram: Reducing Context Churn and Token Burn with Hierarchical Agent Memory

> *A pilot study of Engram, a git-backed, hierarchical persistent memory for autonomous AI coding agents: its design, and what four exploratory experiments showed.*

---

## Abstract

Large Language Models (LLMs) operating as autonomous coding agents suffer from two compounding inefficiencies: **context churn** (repeated rediscovery of project constraints across sessions) and **token burn** (cumulative token consumption from trial-and-error debugging loops).

Engram is a zero-dependency, git-backed external memory that gives AI coding agents structured access to institutional knowledge: project constraints, architectural standards, domain expertise, and accumulated learnings. Knowledge is organized as a navigable index (the "B-Tree": at most 3 hops from the root to any leaf document), so an agent reaches the context it needs in a bounded number of reads, without scanning the repository.

This is a **pilot study**. It reports four exploratory experiments on one codebase and one bug, across four models (Qwen 3.6 35b, Qwen 3.8 27b, DeepSeek V4 Flash, Poolside Laguna S-2.1) and two compute tiers (local GPU and frontier cloud). It compares an agent that has Engram with the same agent without it. **Every arm was run once**, so the results show a direction and are not statistically tested (see section 8.1). In these runs we observed that:

1. **No agent without memory discovered the unstated scale constraint.** Every control run on the canonical prompt first proposed a client-side fix, and none reached a server-side design without human input.
2. **The agents with Engram read the project document before planning and designed the server-side solution.** In the two later experiments they needed no human steering; in the first they needed one intervention, for a UI bug.
3. **The runs with Engram used 36–83% fewer total tokens than their controls.**

The task was a favourable one for memory: the project document held the facts the bug turned on, and it had been written after earlier failed attempts at the same bug (section 3.7). The study does not compare Engram's index navigation with other ways of retrieving the same memory (section 1.3).

---

## 1. Introduction

### 1.1 The Problem

Modern AI coding agents operate within a fundamental constraint: every conversation starts from zero. The agent has no memory of previous sessions, no awareness of architectural decisions made last week, and no knowledge of dataset scale constraints that a human engineer would carry as institutional knowledge.

Without this context, agents propose solutions that violate established architectural decisions (context churn) and enter multi-million-token debugging spirals when those solutions fail at production scale (token burn).

### 1.2 Our Approach: Structured External Memory

Engram addresses both failure modes by providing agents with a persistent, structured, external knowledge base that lives alongside the project repository. It uses:

- **Plain Markdown files** organized in a hierarchical directory structure
- **Standard Git** for versioning, branching, and history
- **A B-Tree navigation protocol** (max 3 hops from root to leaf) for bounded, predictable knowledge retrieval

The agent reads Engram's root navigation file (`AGENTS.md`), follows index pointers to the relevant domain, and reads the specific leaf document containing the constraints it needs — all before writing a single line of code.

### 1.3 Scope of This Study

The study asks one question: does an agent with Engram do better on a task than the same agent without it, when the task turns on a fact that is not in the code?

It does not ask whether index navigation is the best way to retrieve that memory. EXP-2026-003 and EXP-2026-005 also ran an arm that retrieved the same memory by keyword search, and EXP-2026-004 screened a revised search protocol. Those results are left out of this paper because they are not a valid comparison: the first search protocol crawled a `node_modules` directory that should not have been in the memory repository, and for the later runs we cannot show that the agent issued a search query at all. The experiment documents record what was measured. A valid comparison of index navigation with keyword search is future work (section 8.2), and Engram's design will follow its result.

---

## 2. Architecture

### 2.1 Knowledge Organization

Engram organizes knowledge into domain directories, each containing an `INDEX.md` that maps subdocuments:

```
AGENTS.md                          ← Navigation root
├── standards/INDEX.md             ← Coding, design, workflow standards
├── projects/INDEX.md              ← Project-specific architectural constraints
│   └── sift.md                    ← E.g., "1.4M files, B-Tree index on parent_path"
├── knowledge/INDEX.md             ← Domain expertise and learnings
├── tools/INDEX.md                 ← Tool/service-specific knowledge
├── experiments/INDEX.md           ← Experimental results and methodology
└── scratch/                       ← Ephemeral working notes
```

### 2.2 The B-Tree Navigation Protocol

The protocol enforces a maximum traversal depth of 3 hops. The path used in these experiments was:

1. Agent reads `AGENTS.md` (the navigation root), which contains the domain map
2. Agent reads the relevant domain's `INDEX.md` (e.g., `projects/INDEX.md`)
3. Agent reads the specific leaf document (e.g., `projects/sift.md`)

This bounds a lookup however large the knowledge base grows. The path above is three reads; a leaf inside a subdomain (for example `knowledge/physics/`) adds one more index, which is the three-hop limit as `AGENTS.md` counts it. The token cost of a lookup is the size of the root, one or two indexes, and one leaf document, not the size of the repository. With the depth fixed at three, each index grows as documents are added, and we have not measured how cost changes with repository size.

### 2.3 Design Principles

| Principle | Implementation |
|:---|:---|
| **Zero heavy runtime dependencies** | Pure Markdown + Git. No databases, no embeddings, no cloud services. |
| **Bounded retrieval cost** | Index traversal with a fixed maximum hop count. |
| **Git-native versioning** | Full history, branching, diffing, and rollback via standard Git. |
| **Human-readable and auditable** | Every document is plain Markdown that you can read, check, and correct yourself. |
| **Agent-writable** | Agents can contribute knowledge back via structured skills (`add-knowledge`, `sync-memory`). |

---

## 3. Experimental Methodology

### 3.1 Test Subject: Sift

All experiments were conducted against **Sift**, a NAS file manager consisting of a React (TypeScript) frontend and a FastAPI (Python) backend. Sift is a vibe-coded proof of concept: it was written by prompting AI agents, not engineered as a production system. The bug used as the test task was not planted. The agents that built Sift introduced it, the author found it afterwards, and it was then left unfixed so that Sift could be used for these experiments. It is an architectural trap: the file explorer fetches a hardcoded limit of 200 files (ordered by `updated_at DESC`), performing all directory navigation client-side. This works for small datasets but fails at the scale of the real NAS (1.4M+ files).

The critical constraint — that the NAS contains 1.4 million files — is documented in Engram's `projects/sift.md` but is **never mentioned in the user's prompt**. This tests whether an agent discovers an unstated scale constraint from memory.

### 3.2 Prompts

EXP-2026-002, EXP-2026-003 and EXP-2026-005 used the same "Vague Symptom" prompt, designed to simulate a real user reporting a bug without providing architectural guidance:

> *"I'm looking at the file explorer and I can only see files from the most recent scan. The older files and folders are just missing. It's like the data is being limited or something. Can you figure out why and fix it?"*

EXP-2026-001 used an earlier, more detailed prompt that named the file explorer component and asked for an implementation plan. It is quoted in the experiment document.

### 3.3 Experimental Arms

| Arm | Memory Access | What the agent has |
|:---|:---|:---|
| **Control** | None | Only the codebase and its training knowledge |
| **Engram** | Full | An instruction to read `AGENTS.md` and navigate the indexes to the relevant leaf documents before planning |

EXP-2026-001 had a third condition between these two: Engram with behavioural standards only and no project document. EXP-2026-002 ran a control to completion; its memory arm was cut short and is not used in the comparisons.

### 3.4 Models and Compute Tiers Tested

| Model | Class | Compute Tier | Context Window | Arms Run |
|:---|:---|:---|:---|:---|
| Qwen 3.6 35b a3b | Open weights | Local GPU (LM Studio) | ≥200k | Control, Engram |
| Qwen 3.8 27b | Open weights | Local GPU (LM Studio) | 262k | Control, Engram |
| DeepSeek V4 Flash | Frontier cloud | OpenRouter API | 1M | Control, Engram |
| Poolside Laguna S-2.1 | Specialized code model | OpenRouter API | 262k | Control only (initial plan) |

### 3.5 Harness and Configuration

All experiments used **Cline** as the agent harness with Plan/Act mode separation. EXP-2026-003 and EXP-2026-005 were pinned to **Cline v4.0.12**; EXP-2026-001 and EXP-2026-002 used the contemporary stable release. Data was recorded at two checkpoints:

- **Checkpoint 1 (Planning)**: Agent diagnoses the problem and proposes an architecture
- **Checkpoint 2 (Act Phase)**: Agent implements the solution, runs tests, and verifies

### 3.6 Sample Size

Every arm in every experiment was run once (N=1). The local Qwen 3.8 27b runs used temperature 1.0 with a fixed seed, 524287. The seed was chosen by the author, who likes prime numbers, because it is the seventh Mersenne prime (2^19 − 1); the value has no connection to the task. No other seed was tried. No run was repeated, so run-to-run variance is unknown and none of the differences reported below has been tested statistically. Engram's own [experimentation standard](standards/workflow/experimentation.md) classes single-run results as exploratory: they show a direction, not a confirmed effect size.

### 3.7 How the Memory Was Written

The project document used by the Engram arms was written for the third condition of EXP-2026-001, after the first two runs had struggled with this bug. It records the specific pitfalls the second run hit: a prefix filter that returns every descendant of a folder instead of its immediate children, and invalid table markup that flattens the tree. Its database indexing rule names the same query constructs that the EXP-2026-002 control had tried. The later experiments reused the document on the same bug.

This is the mechanism Engram is meant to provide: a lesson recorded once is available to every later session. It is also the most favourable test there is, because the memory held the answer to this particular problem. The results below show what an agent does when its memory contains what the task needs. They do not show how often that is the case in ordinary work, or what memory costs on tasks it does not help with.

The exact memory contents that the EXP-2026-003 arm read were not preserved (section 8.1). The `projects/sift.md` in this repository is consistent with the behaviour recorded for that arm.

---

## 4. Results

### 4.1 EXP-2026-001: Initial Token Efficiency Discovery

**Model**: Qwen 3.6 35b a3b (local)

| Condition | Total Tokens | Interventions | Outcome |
|:---|:---|:---|:---|
| Control (no memory) | **8.7M** | 6 | Aborted after UI death spirals, infinite render loops, and git workflow failure |
| Engram, behavioural context only | **4.2M** | 6 | Functional but required extensive human steering; git workflow failed |
| Engram, full project context (`sift.md`) | **1.5M** | 1 | Achieved functional parity in ~980k tokens; git workflow failed due to context attrition |

**Key Finding**: With the project document, the agent used **82.8%** fewer tokens over the complete session than the control (1.5M vs 8.7M; 88.7% fewer to reach functional parity, 980k vs 8.7M), with 1 human intervention against 6. The control was aborted before it finished, so its total is a lower bound.

**Secondary Finding**: Passive text-based rules for git workflows suffered from context attrition. By the end of their multi-million-token sessions, both agents with Engram ignored its git rules and pushed directly to `main`.

### 4.2 EXP-2026-002: Model Capability as Confound

**Model**: Qwen 3.6 35b a3b → Qwen 3.8 27b (local)

This experiment set out to test active guardrails for git workflows. It was cut short when the base model (Qwen 3.6) proved to be the bottleneck. The control run consumed **13.3M tokens** and a recorded 15 human interventions (the execution log itemises 14) before producing a working implementation. It was given the 1.4M scale constraint in its first intervention and still needed explicit architectural direction to reach a server-side design.

**Key Finding**: On its first attempt the Qwen 3.6 memory arm ignored the instruction to read Engram. The newly released Qwen 3.8 27b read agent memory from global instructions alone, without prompt injection. Whether passive instructions work depends on how well the base model follows instructions.

### 4.3 EXP-2026-003: Engram vs. Control (Local Tier)

**Model**: Qwen 3.8 27b (local, seed: 524287)

One run per arm. Token counts are cumulative:

| Arm | Planning Context | Tokens at End of Planning | Total Tokens at End of Act | Interventions | State at End of Act |
|:---|:---|:---|:---|:---|:---|
| **Control** | 67.9k | 562.0k | **5.61M** | 1 (steering) | 36/36 tests pass; verified against the live database; worked on `main` |
| **Engram** | 52.6k | 567.3k | **2.55M** | **0** | 34/34 tests pass; created a work branch; live `/dir` endpoint returned empty lists |

**Key Findings**:

1. The Engram arm used **54.5% fewer total tokens** than the steered control (2.55M vs 5.61M)
2. The Engram arm needed **0 human interventions**: it read `projects/sift.md` on its first turn and planned the indexed `parent_path` architecture
3. The control reasoned explicitly that a server-side design was unnecessary below ~50k files, planned an unlimited bulk fetch, and re-planned only when told the NAS held 1.4M files

**Caveat**: the arms did not finish in the same state. The Engram arm's unit tests and build passed, but its live `/dir` endpoint returned empty folder and file lists: the migration had not been applied to the running database, and the endpoint had a folder-slicing bug. The control was verified working against the live database. The follow-up repair phase planned for this experiment was not run, so the 2.55M figure does not include the cost of fixing that bug. The token comparison is between first-pass implementations, not between equally verified ones.

### 4.4 EXP-2026-005: Engram vs. Control (Frontier Cloud Tier)

**Model**: DeepSeek V4 Flash (1M context, via OpenRouter)

A check of whether the direction seen on a local 27b model also appears on a frontier cloud model with a roughly 4x larger context window. One run per arm:

| Arm | Planning Context | Act Phase Context | Total Tokens | Interventions | Tests Passing |
|:---|:---|:---|:---|:---|:---|
| **Control** | 29.1k → 34.4k (steered) | 92.8k | **2.5M** | 1 (steering) | 39/39 |
| **Engram** | 34.5k | 93.2k | **1.6M** | **0** | 33/33 |

**Key Findings**:

1. The Engram arm used **36% fewer total tokens** than the steered control (1.6M vs 2.5M)
2. The Engram arm needed **0 human interventions**, and its build was verified in live containers
3. The control proposed removing the limit and fetching everything, with 1M tokens of context available

**Cross-Model Control**: a control run on Poolside Laguna S-2.1 (a specialized code model) showed the same behaviour: it proposed raising the fetch limit to 100,000, citing a stale code comment about "tens of thousands of files." Its steering turn then failed on repeated tool-call errors, so no re-plan was recorded.

### 4.5 Summary

Each row is one run per arm.

| Experiment | Model | Control Tokens | Control Interventions | Engram Tokens | Engram Interventions | Fewer Tokens with Engram |
|:---|:---|:---|:---|:---|:---|:---|
| EXP-2026-001 | Qwen 3.6 35b | 8.7M (aborted) | 6 | 1.5M | 1 | 82.8% |
| EXP-2026-003 | Qwen 3.8 27b | 5.61M | 1 | 2.55M | 0 | 54.5% |
| EXP-2026-005 | DeepSeek V4 Flash | 2.5M | 1 | 1.6M | 0 | 36% |

The saving was smaller in each later experiment, and each later experiment used a more capable model. Three single runs cannot show whether that is a trend.

### 4.6 What the Memory Cost

Reading the memory is not free. In all three experiments the Engram arm had spent more tokens than the control by the time each produced its first plan:

| Experiment | Control, First Plan | Engram, First Plan | Ratio |
|:---|:---|:---|:---|
| EXP-2026-001 | 135.1k | 204.2k | 1.5x |
| EXP-2026-003 | 291.5k | 514.8k | 1.8x |
| EXP-2026-005 | 123.0k | 224.2k | 1.8x |

The saving came afterwards: the control's first plan either was the wrong architecture or failed in implementation, and had to be redone or repaired. On a task where the memory holds nothing relevant, this up-front cost would be paid with no saving to offset it. That case was not tested.

---

## 5. Control Behaviour Without Memory

On the canonical prompt, no unassisted model discovered the scale constraint, and each first proposed a client-side fix:

| Model | Experiment | Class | Context Window | First Control Proposal |
|:---|:---|:---|:---|:---|
| Qwen 3.6 35b | EXP-2026-002 | Local open weights | ≥200k | Client-side pagination; after further steering, a bulk fetch with `limit=10000` |
| Qwen 3.8 27b | EXP-2026-003 | Local open weights | 262k | Set `limit <= 0` (unlimited bulk fetch) |
| DeepSeek V4 Flash | EXP-2026-005 | Frontier cloud | 1M | Remove limit, order by `file_path` |
| Poolside Laguna S-2.1 | EXP-2026-005 | Specialized code | 262k | Raise limit to 100,000 |

In these four control runs, the model:

1. Correctly identified the 200-file limit as the proximate cause
2. Proposed a client-side fix: removing or raising the limit (three models) or paginating in the browser (Qwen 3.6)
3. Did not consider that the dataset might contain millions of records
4. Did not reach a server-side architecture unaided. Qwen 3.8 and DeepSeek re-planned once a human supplied the scale constraint. Qwen 3.6 was given the constraint in its first intervention and still needed explicit architectural direction. The Poolside run stopped at its steering turn

EXP-2026-001 is a different case. With its more detailed prompt, the Qwen 3.6 control proposed a server-side tree endpoint at planning, then failed during implementation.

We read this as a failure of **information access** rather than of reasoning: the models reasoned correctly about the code they could see, and the scale constraint is not in the code. Four single runs on one codebase support that reading; they do not establish it for agents or codebases in general.

---

## 6. Observations

### 6.1 A Fact That Is Not in the Code Cannot Be Recovered from the Code

The control runs suggest why external memory helped here: the constraint that decided the right architecture was a fact about the deployment, not about the source. No model inferred it, and the Qwen 3.8 control reasoned explicitly from a wrong assumption about scale. The agents in these runs proposed solutions that work on small datasets and fail at production scale.

### 6.2 Context Window Size Did Not Help

DeepSeek V4 Flash has a 1M token context window, roughly 4x larger than Qwen 3.8's 262k. Its control run still did not discover the 1.4M file constraint. A larger context window does not supply information that is absent from the code.

### 6.3 Memory Instructions Depend on the Model Following Them

In EXP-2026-002, Qwen 3.6 ignored the instruction to read Engram on its first attempt and needed a forceful prompt. Qwen 3.8 read it from global instructions alone. A memory the agent does not read is worth nothing, so the benefit reported here depends on a model that follows the navigation instruction.

### 6.4 Passive Git Rules Did Not Survive Long Sessions

In EXP-2026-001, both agents with Engram ended their sessions by pushing directly to `main`, although Engram's git rules were available to them. Memory removed the architectural mistakes in these runs; it did not make an agent keep a procedural rule across millions of tokens. In EXP-2026-003, with a more capable model and a shorter session, the Engram arm did create a work branch before writing code.

### 6.5 Stale Documentation Misleads

In the EXP-2026-002 control, the agent queried a stale SQLite file because the test repository's own `AGENTS.md` still named SQLite as the database, and it drew a wrong conclusion from what it found there. Written context is followed whether or not it is true. A memory that is not kept current can cost more than no memory.

---

## 7. What These Results Do Not Show

- **That memory helps on most tasks.** The task was chosen because its answer was a fact absent from the code, and the memory held that fact (section 3.7).
- **That the index is the best way to retrieve the memory.** No valid comparison with keyword search or any other retrieval method is reported (section 1.3).
- **An effect size.** The percentages are differences between single runs.
- **The cost of keeping a memory.** Writing the project document, and keeping it true, took human and agent effort that is not counted in the token figures.

---

## 8. Limitations and Future Work

### 8.1 Current Limitations

- **One run per arm**: Every arm was run once (section 3.6). Run-to-run variance is unknown, and the percentage differences reported here are observations from single runs, not tested effect sizes.
- **A favourable task**: The memory held the answer to the bug under test, and it was written after earlier failed attempts at that bug (section 3.7).
- **Uneven end states**: In EXP-2026-003 the Engram arm finished with a live endpoint bug that the control did not have, and the planned repair phase was not run (section 4.3).
- **Experimenter not blind**: The runs were set up, steered and assessed by Engram's author, who knew which arm was which. Steering prompts were written during the runs, not fixed in advance.
- **Single test domain**: All experiments used the Sift codebase and one bug. Sift is a vibe-coded proof of concept whose bug was left unfixed for the experiments (section 3.1), not a maintained production codebase, and the experimenter knew the bug before any run.
- **Single prompt tier**: The comparisons used only the "Vague Symptom" prompt (and, in EXP-2026-001, one more detailed prompt).
- **Git workflow compliance**: Adherence to branching and pull-request rules depended on the model and the session length rather than on memory (section 6.4).
- **Memory state not preserved**: The Engram branch that the memory arm ran on in EXP-2026-003 was not kept, and neither were the session logs of EXP-2026-005. The experiments can be repeated in method, using the public [Sift](https://github.com/chrisedebo/sift) baseline commit `e7e642c` and the prompts and model settings recorded in the experiment documents, but not from identical memory contents.

### 8.2 Future Work

- **Replication**: Repeat the Engram-versus-control comparison with several seeds per arm (random or otherwise), complete the repair phase for every arm, fix the steering prompts in advance, and keep the session logs and memory state.
- **Index navigation versus keyword search**: Compare the two on tasks whose answer is not in the project document, so that a search arm must issue a query, and on a memory large enough for the difference to matter. If search proves cheaper, with results as good and no more human intervention, Engram's design will change to follow it.
- **Tasks where memory does not help**: Measure the overhead of reading the memory on tasks whose answer is in the code.
- **Cross-domain validation**: Test on codebases and problems other than Sift.
- **Long-horizon use**: Measure what a memory is worth, and what it costs to maintain, over weeks and months of real development.
- **Multi-agent memory sharing**: Test Engram's contribution protocol across concurrent agent sessions.

---

## 9. Conclusion

In this pilot study, coding agents given a structured external memory avoided an architectural mistake that every agent without it made, needed little or no human steering, and used 36–83% fewer tokens. The mistake came from a fact that was not in the code, and the memory supplied it.

That is a narrow result, from single runs on one bug that the memory had been written to cover. It is enough to say the approach is worth testing properly, and section 8.2 lists what a proper test needs. It is not enough to say how much a memory like this is worth in general. The design itself is simple to adopt: it is human-readable, and it needs no infrastructure beyond a Git repository and plain Markdown files.

---

## Appendix A: Experiment Cross-Reference

| Experiment | Model | Focus | Result as Used in This Paper |
|:---|:---|:---|:---|
| [EXP-2026-001](experiments/2026/exp-2026-001-engram-token-efficiency.md) | Qwen 3.6 35b | Engram vs control, three conditions | 82.8% fewer tokens over the session with the project document (88.7% to parity) |
| [EXP-2026-002](experiments/2026/exp-2026-002-engram-active-guardrails.md) | Qwen 3.6 → 3.8 | Git guardrails; cut short | Control behaviour only; model capability decides whether memory is read |
| [EXP-2026-003](experiments/2026/exp-2026-003-retrieval-architecture-benchmark.md) | Qwen 3.8 27b | Engram vs control, local tier | 54.5% fewer tokens, 0 interventions; Engram arm ended with an unfixed endpoint bug |
| [EXP-2026-004](experiments/2026/exp-2026-004-improved-search-retrieval.md) | Qwen 3.8 27b | Keyword search screening | Not used in this paper (section 1.3) |
| [EXP-2026-005](experiments/2026/exp-2026-005-deepseek-v4-control.md) | DeepSeek V4 Flash | Engram vs control, cloud tier | 36% fewer tokens, 0 interventions |

The experiment documents for EXP-2026-003 and EXP-2026-005 also record a keyword search arm, which this paper does not use (section 1.3).

## Appendix B: Glossary

| Term | Definition |
|:---|:---|
| **Context churn** | Repeated rediscovery of project constraints across agent sessions |
| **Token burn** | Cumulative token consumption from trial-and-error debugging loops |
| **B-Tree navigation** | Hierarchical index traversal through `INDEX.md` files (max 3 hops) |
| **Control arm** | Agent operating without any external memory access |
| **Engram arm** | Agent instructed to navigate Engram's indexes before planning |
| **Anti-pattern (bulk-fetch)** | Removing API limits to fetch entire datasets into the browser |
| **Context attrition** | Loss of instruction compliance as the context window fills over long sessions |
| **Steering intervention** | Human-provided prompt to redirect the agent away from a flawed approach |
