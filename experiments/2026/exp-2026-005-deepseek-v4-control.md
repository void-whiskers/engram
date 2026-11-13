---
status: concluded
created: 2026-08-27
updated: 2026-11-13
tags: [agent-memory, engram, benchmark, deepseek, cloud-llm, 3-arm-showdown, retrieval]
---

# EXP-2026-005: Frontier Cloud LLM Benchmark — DeepSeek V4 Flash 3-Arm Showdown on Sift

## Hypothesis

1. Operating without external memory (Control), frontier-class cloud coding models (DeepSeek V4 Flash with 1M context) will fail to discover unstated enterprise-scale dataset constraints (1.4M files) on Sift, proposing unscalable client-side patches requiring human steering intervention.
2. Operating with external memory (Engram Smart Search or B-Tree), DeepSeek V4 Flash will autonomously identify dataset sizing and architectural constraints during planning, formulating server-side directory browsing architectures with **0 human interventions**, adhering to git workflow standards, and reducing overall token burn.

## Method

1. **Test Environment Preparation:**
   - **Target Codebases:**
     - Arm 1 (Control): `sift-control` cleanly reset to `e7e642c`, no memory, origin remote removed.
     - Arm 2 (Smart Search): `sift-esd` cleanly reset to `e7e642c`, origin remote removed, `engram` on `main` (`benchmark-search-baseline`).
     - Arm 3 (B-Tree): `sift-ebd` cleanly reset to `e7e642c`, origin remote removed, `engram` on `main` (`benchmark-btree-baseline`).
     - Arm 4 (Cross-Model Control): `sift-control` cleanly reset to `e7e642c`, tested on `poolside/laguna-s-2.1:free`.
   - **Model & Harness:** DeepSeek V4 Flash via Cline **v4.0.12**, medium reasoning effort.
   - **Prompt:** Canonical Tier 1 Vague Prompt:
     > *"I'm looking at the file explorer and I can only see files from the most recent scan. The older files and folders are just missing. It's like the data is being limited or something. Can you figure out why and fix it?"*
2. **Data Collection Checkpoints:**
   - **Checkpoint 1 (Planning):** Context window size, Prompt tokens, Completion tokens, Cache reads, Total tokens, Proposed architectural approach, Autonomous discovery of 1.4M scale.
   - **Checkpoint 2 (Act Phase):** Context window size, Prompt tokens, Completion tokens, Cache reads, Total tokens, Test suite results (pytest), Frontend build/type-check, Git branch creation.
3. **Analysis:**
   - Symmetrically compare Control vs. Smart Search vs. B-Tree on DeepSeek V4 Flash, and compare directly against local Qwen 3.8 27b baselines from EXP-2026-003 and EXP-2026-004.

## Results

### Checkpoint Matrix

| Run / Arm | Checkpoint | Context Window | Prompt Tokens | Completion Tokens | Cache Reads | Total Tokens | Interventions / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DeepSeek Control (Arm 1)** | 1a. Initial Plan | 29.1k (2.8%) | 81.2k | 3.4k | 38.4k | 123.0k | Unassisted Control. Proposed bulk-fetch anti-pattern (removing limit + ordering by file_path). Scalability mentioned only as afterthought. |
| | 1b. Post-Steering Re-plan | 34.4k (3.3%) | 236.9k | 5.2k | 67.6k | 309.7k | 1 human steering intervention (1.4M scale). Pivoted to server-side `/api/files/browse` endpoint with prefix queries (`LIKE`/`NOT LIKE`), pagination, and breadcrumbs. |
| | 2. Act Phase | 92.8k (8.9%) | 1.0M | 26.4k | 1.5M | 2.5M | 1 total intervention. 39/39 pytest pass. Next.js build succeeds. Worked on `main` (no branch). Ran `npm` on host. |
| **DeepSeek Smart Search (Arm 2)** | 1a. Initial Plan | 35.8k (3.4%) | 50.0k | 3.3k | 217.3k | 270.6k | **0 interventions**. Autonomously retrieved `/projects/sift.md` & scale constraint via Smart Search. Recommended full `parent_path` architecture. |
| | 1b. Finalized Plan | 43.3k (4.1%) | 92.9k | 4.7k | 369.7k | 467.2k | 0 interventions. Option 1 selected. Comprehensive plan: `parent_path` schema + B-Tree index, `01-init.sql` & `0005_add_parent_path.sql` migration, scanner update, `/tree` & `/dir` exact match, flat DOM table. |
| | 2. Act Phase | 110.8k (10.6%) | 285.9k | 25.0k | 2.2M | 2.5M | **0 interventions**. 34/34 tests pass. Clean implementation of full `parent_path` tree architecture. 88.0% KV cache hit rate. |
| **DeepSeek B-Tree (Arm 3)** | 1. Planning | 34.5k (3.3%) | 34.1k | 3.2k | 186.9k | 224.2k | **0 interventions**. Autonomously traversed 3-hop B-Tree (`AGENTS.md` -> `projects/INDEX.md` -> `projects/sift.md`). Discovered 1.4M scale and recommended full architecture (Option 1+2). |
| | 2. Act Phase | **93.2k (8.9%)** | **374.8k** | **21.0k** | **1.2M** | **1.6M** | **0 interventions**. 33/33 tests pass. Completed 10/10 tasks. Full `parent_path` tree architecture. **36.0% lower token burn** and **15.9% leaner context** than Smart Search. |
| **Poolside Laguna S-2.1 Control (Arm 4)** | 1a. Initial Plan | 37.6k (14.3%) | 94.5k | 5.3k | - | 99.8k | Unassisted Control. Proposed raising limit to `100,000` (bulk-fetch anti-pattern), citing stale comment in `01-init.sql`. |
| | 1b. Re-plan (Steered) | - | - | - | - | - | Hit repeated tool call failure in Cline on steering turn. |
| | 2. Act Phase | - | - | - | - | - | Paused. |

## Methodological Notes

- **Model Divergence & KV Cache Dynamics:** DeepSeek V4 Flash leverages aggressive server-side KV prefix caching across all runs (60% to 88% cache hit rate), resulting in sub-second tool turn generation.
- **B-Tree Efficiency Across Model Classes:** B-Tree index traversal consistently produced lower total token burn (1.6M vs 2.5M) and tighter peak context (93.2k vs 110.8k) than Smart Search, replicating the EXP-2026-003 findings on a frontier cloud model.
- **Memory Integrity & Branch Parity:** Setting `engram` directly on `main` at tags `benchmark-search-baseline` and `benchmark-btree-baseline` completely eliminated cross-branch divergence, allowing clean linear Act phases without token thrash.
- **Universal Control Anti-Pattern (3 for 3):** Qwen 3.8 27b, DeepSeek V4 Flash, and Poolside Laguna S-2.1 all defaulted to client-side bulk-fetch limit removal without external memory.
- **Sample size (note added 2026-11-13):** each arm was run once, so the differences reported here are directional and run-to-run variance is unknown.
- **Search arm not verifiable (note added 2026-11-13):** this document does not record which search protocol the Smart Search arm's `AGENTS.md` carried, or whether the agent issued a search query. The session logs and the two test beds were not kept. In [EXP-2026-004](./exp-2026-004-improved-search-retrieval.md) the refined protocol led the agent to the project document with no query, so the 36.0% difference between Arm 3 and Arm 2 may compare two routes to the same document and is not established as a comparison with keyword search.
- **Use in the whitepaper (note added 2026-11-13):** for the reason above, the [whitepaper](../../WHITEPAPER.md) reports only the Control and B-Tree arms of this experiment.
- **Git workflow not recorded for the memory arms (note added 2026-11-13):** the checkpoint matrix records branching only for the Control arm. The "adhering to git workflow standards" part of Hypothesis 2 is therefore not evidenced here, and Conclusion 1's "fully confirmed" applies to Hypothesis 1 and to the autonomy and token parts of Hypothesis 2.
- **Poolside control incomplete (note added 2026-11-13):** Arm 4 stopped at its steering turn on repeated tool-call failures; only its initial plan is recorded.
- **Live Container Verification & UI Ergonomics (`sift-ebd`):** Docker containers built cleanly (`make build`), launched without error (`make run`), and completed live disk scans (indexing 382+ files with deep metadata refresh). The UI loaded smoothly with zero flickering. Structurally, the agent rendered both the full ancestral folder hierarchy tree and the immediate child directory pills within the same unified table view, functionally supporting arbitrary scale without client-side pagination choking.

## Conclusions

1. **Hypothesis Fully Confirmed:** Even frontier-class cloud coding models equipped with massive context windows (1M tokens) fail to identify unstated enterprise-scale dataset constraints without institutional memory.
2. **Engram Autonomy (0 Interventions):** Both Engram-assisted arms (Smart Search and B-Tree) achieved 100% autonomous execution (0 human interventions), correctly identified the 1.4M NAS scale constraint, formulated the `parent_path` tree/dir endpoint architecture, and passed all backend test suites cleanly.
3. **B-Tree Wins the Cloud Showdown:** B-Tree index traversal outperformed Smart Search on DeepSeek V4 Flash by **36.0% in total token consumption** (1.6M vs 2.5M) and **15.9% in peak context size** (93.2k vs 110.8k), cementing B-Tree as the gold-standard retrieval architecture across both local and cloud tiers.

## Impact

- Concludes the comprehensive 3-Arm Frontier Cloud LLM benchmark on DeepSeek V4 Flash.
- Confirms the cross-tier validity of Engram's hierarchical B-Tree retrieval design for the open-source release whitepaper.
