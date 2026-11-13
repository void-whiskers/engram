---
status: concluded
created: 2026-08-27
updated: 2026-11-13
tags: [agent-memory, engram, efficiency, benchmark, retrieval, search, refined-search]
supersedes: experiments/future/future-007-improved-search-retrieval.md
---

# EXP-2026-004: Engram Retrieval Architectures — Refined Smart Search Screening Benchmark

## Hypothesis

A refined, domain-scoped keyword search implementation (`grep_search` targeted at `projects/` and `standards/` with match filtering) will reduce cumulative token consumption by $\ge 40\%$ compared to the naive search in `EXP-2026-003` (6.90M tokens) on Sift using Qwen 3.8 27b (seed: `524287`), keeping total token burn within $1.5\text{x}$ of the B-Tree baseline ($\le 3.8\text{M}$ tokens) and planning context $<60\text{k}$ tokens.

## Method

1. **Test Environment Preparation:**
   - **Target Codebase:** `sift-engram-search` cleanly reset to baseline commit `e7e642c` with origin remote stripped.
   - **Memory Repository:** `engram` checked out on branch `feature/benchmark-search` with `node_modules` purged and `.gitignore` active. The branch existed only in the local test bed and was not preserved (see the note in [EXP-2026-003](./exp-2026-003-retrieval-architecture-benchmark.md)).
   - **Model & Sampling:** Qwen 3.8 27b via LM Studio, temperature `1.0`, Mersenne prime seed `524287` (identical to `EXP-2026-003` for baseline alignment).
   - **Search Protocol:** Redesigned Smart Search protocol in `engram/AGENTS.md` enforcing targeted project lookup, scoped keyword queries, and selective match reading. The Navigation Protocol as the agent read it at the start of the run (recovered from the harness session log on 2026-11-12):

     > To find relevant context for a task using Smart Search:
     >
     > 1. **MANDATORY PROJECT ROUTING (First Action)**: Before planning or executing any task, check `projects/<current_repo_name>.md` using `view_file` (or `grep_search` scoped exclusively to `projects/`). This document contains essential project-specific architectural constraints and database schemas. You MUST read it before writing code. If it does not exist, suggest creating one using the `add-project` skill.
     > 2. **FOCUSED TECHNICAL QUERIES (Only as Needed)**: If you need specific coding, design, or workflow standards, execute a tightly-targeted `grep_search` scoped specifically to `standards/coding/` or `standards/design/` (e.g. searching for a specific library, database rule, or git workflow).
     > 3. **SELECTIVE FILE READING**: Review match snippets first. Do NOT bulk-read all matching files. Open only the 1-2 most relevant matching markdown documents to avoid context bloat.
     > 4. **DOMAIN BOUNDARIES**: Search exclusively within Markdown documentation files (`*.md`) inside `projects/`, `standards/`, `knowledge/`, and `tools/`. Never search across external directories or unindexed assets.

2. **Data Collection Checkpoints:**
   - **Checkpoint 1 (Planning):** Context window size, Prompt tokens, Completion tokens, Total tokens, Proposed architectural plan.
   - **Checkpoint 2 (Act Phase):** Context window size, Peak context, Prompt tokens, Completion tokens, Total tokens, Test suite results (pytest), Frontend build/type-check, Git branch creation.
3. **Control Run (Baseline from EXP-2026-003):**
   - **Control (Naked + Steered):** 562.0k Planning / 5.61M Act Total (1 human intervention).
   - **Variable A (B-Tree):** 567.3k Planning / 2.55M Act Total (0 human interventions).
   - **Variable B (Naive Search):** 1.41M Planning / 6.90M Act Total (0 human interventions, peak context 221.4k / 84.5%).
4. **Variable Run (Experiment):**
   - Single experimental arm (`sift-engram-search`) tested against the Tier 1 Vague Prompt using the refined Smart Search protocol.
5. **Analysis:**
   - Compare planning context, token burn, and code quality against EXP-2026-003 baselines.

## Results

### Checkpoint Matrix

| Arm / Run | Checkpoint | Context Window | Prompt Tokens | Completion Tokens | Total Tokens | Interventions / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B-Tree Baseline (EXP-2026-003)** | 1. Planning | 52.6k | 549.7k | 17.6k | 567.3k | 3-hop B-Tree traversal. Option B chosen. |
| | 2. Act Phase | 100.3k | 2.5M | 48.9k | 2.55M | 0 interventions. 34/34 tests pass. Branched. |
| **Control Baseline (EXP-2026-003)** | 1. Planning | 67.9k | 525.8k | 36.1k | 562.0k | 1 human steering intervention (1.4M scale). |
| | 2. Act Phase | 167.5k | 5.5M | 112.7k | 5.61M | 1 human intervention. 36/36 tests pass. Worked on main. |
| **Naive Search (EXP-2026-003)** | 1. Planning | 180.8k | 1.4M | 11.8k | 1.41M | Unconstrained grep + node_modules crawl. |
| | 2. Act Phase | 102.2k (peak 221.4k) | 6.8M | 119.0k | 6.90M | 0 interventions. 36/36 tests pass. Truncated. |
| **Refined Smart Search (EXP-2026-004)** | 1a. Initial Plan | 43.0k | 309.5k | 8.9k | 318.4k | Scoped search + clean repo. Context 76.2% leaner than naive search; 77.4% token reduction vs exp-003 search planning. |
| | 1b. Finalized Plan | 56.6k | 685.2k | 23.5k | 708.7k | Option 1 selected. Detailed schema + endpoint + frontend plan. Context 56.6k (comparable to B-Tree Checkpoint 1b at 52.6k). |
| | 2. Act Phase | - | - | - | - | Not completed; no valid data (see Methodological Notes). |

## Methodological Notes

- **Screening Design:** EXP-2026-004 is an isolated screening test testing a single independent variable (search protocol refinement) against established EXP-2026-003 baselines under identical prompt, seed, model, and codebase conditions.
- **Dependency Isolation:** Following the discovery of `node_modules` grep pollution in EXP-2026-003, all dependency directories have been purged and `.gitignore` enforced across `engram`.
- **Harness Stability & Extension Version Pinning:** To eliminate prompt-injection drift and harness confounds observed during subsequent minor updates, the Cline extension version is strictly pinned to **v4.0.12** matching the EXP-2026-003 testbed configuration.
- **No keyword search ran in the planning phase (note added 2026-11-13):** The harness session log of the run shows the agent read `AGENTS.md`, tried `projects/sift-engram-search.md` (not found), listed `projects/`, and read `projects/sift.md`. It called no search tool. The refined protocol's first step routes straight to the project document, so the planning figures measure direct project-document lookup, which reaches the same document as the B-Tree arm's index traversal. They are not a measurement of keyword search.
- **Act phase abandoned (note added 2026-11-13):** The session log was migrated to harness version 4.1.16 before act mode began (the log marks it a legacy conversation whose tool names had changed), so the act phase did not run under the pinned version. The agent made nine file edits, and the session was then cancelled with 907,948 input and 27,825 output tokens recorded. Seven further sessions were started in the same test bed that evening (six on Qwen 3.8 27b, one on Poolside Laguna S-2.1, under harness versions 4.1.16 and 4.1.9); none read the Engram `AGENTS.md`, and all ended failed or cancelled. No act-phase result is reported.

## Conclusions

Concluded on 2026-11-13 as a planning-phase screening. The act phase was not completed, and it cannot be resumed from the same memory state because the memory branch was not preserved.

1. **Planning context criterion met:** 56.6k at the finalized plan, under the 60k limit and 1.08x the B-Tree planning context (52.6k).
2. **Planning tokens:** 708.7k, which is 49.7% below the naive search planning phase (1.41M) and 24.9% above the B-Tree planning phase (567.3k).
3. **Hypothesis not tested:** the hypothesis concerns cumulative token consumption ($\ge 40\%$ below 6.90M and $\le 3.8\text{M}$ in total). There is no act-phase data, so it is neither supported nor refuted.
4. **Not a search result:** the agent ran no keyword query (see Methodological Notes). What the planning data shows is that routing to the project document first avoids the context cost of the naive protocol's mandatory repository-wide search.

## Impact

- This experiment is not used in the [whitepaper](../../WHITEPAPER.md), which compares Engram with no memory and makes no claim about keyword search.
- Full-lifecycle Smart Search figures exist only in EXP-2026-003 (naive protocol) and [EXP-2026-005](./exp-2026-005-deepseek-v4-control.md), and neither is a valid test of keyword search.
- A test of keyword search itself needs a task whose answer is not in the project document, so that the agent must run at least one query.
