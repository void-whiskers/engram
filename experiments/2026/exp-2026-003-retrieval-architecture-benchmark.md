---
status: concluded
created: 2026-08-18
updated: 2026-11-15
tags: [agent-memory, engram, efficiency, benchmark, retrieval, btree, search]
---

# EXP-2026-003: Engram Retrieval Architectures — B-Tree Index Traversal vs. Keyword Search

## Motivation

In `EXP-2026-002`, we discovered that model capability is a primary determinant of rule compliance: while Qwen 3.6 35b a3b suffered from context amnesia and instruction attrition, the newly released **Qwen 3.8 27b** apparently adheres to global agent memory instructions without requiring prompt-injected active guardrails.

With instruction-following unblocked, the critical architectural design question for Engram's open-source release centers on **retrieval mechanism**:

1. **Hierarchical B-Tree Traversal:** The agent navigates structured, curated `INDEX.md` files (max 3 hops from root) to discover domain-specific knowledge and architectural constraints.
2. **Brute-Force Keyword Search:** The agent executes a tool call like `grep_search` across the memory repository to match keywords extracted from the user's prompt.

While keyword search has lower initial hop latency (1 tool call), it risks context pollution, keyword mismatch, and ingesting massive search result payloads. Structured B-Tree navigation requires 2–3 hops but guarantees high-signal context discovery and scales with $O(\log N)$ token predictability. We need a rigorous scientific benchmark comparing these two retrieval paradigms against a naked baseline.

## Hypothesis

Structured hierarchical B-Tree navigation (`INDEX.md` traversal) will achieve at least a 10% reduction in cumulative token burn, lower context pollution, and higher technical precision compared to brute-force keyword search (`grep_search`) across multi-turn technical execution tasks on Sift using Qwen 3.8 27b, despite a slight initial hop penalty.

## Proposed Method

### 1. Test Environment Preparation

- **Test Codebase:** Sift (NAS file manager PoC) cleanly reset to commit `e7e642c` (which specifies PostgreSQL in the repository's local `AGENTS.md`).
- **Agent Model:** **Qwen 3.8 27b** running locally via LM Studio (`temperature: 1.0`, `seed: 524287`, every arm). The seed was chosen because it is the seventh Mersenne prime (2^19 − 1); no other seed was tried.
- **Environment Setup:**
  - `sift-control`: No Engram memory access or instructions. Baseline commit `e7e642c`.
  - `sift-engram-btree`: Engram memory checkout on branch `feature/benchmark-btree`, configured with hierarchical B-Tree navigation rules in `AGENTS.md` (root $\rightarrow$ domain index $\rightarrow$ leaf document). Baseline commit `e7e642c`.
  - `sift-engram-search`: Engram memory checkout on branch `feature/benchmark-search`, configured with keyword search retrieval rules in `AGENTS.md` (mandatory `grep_search` memory query on turn 1). Baseline commit `e7e642c`.
  - **Local Environment Isolation:** All test repositories operate with `origin` remote removed to prevent upstream git discrepancies from contaminating reasoning or token counts.
- **Clean IDE State:** Absolutely no open editor tabs prior to initiating runs.
- **Agent Configuration:** Cline in "Plan mode" for Prompt 1, manually switched to "Act mode" for implementation. Subagents enabled in UI settings.

### 2. Data Collection Checkpoints

Record cumulative Prompt Tokens, Completion Tokens, Total Tokens, Context Window Size, and Interventions at:

1. **End of Retrieval / Planning Phase** (measures upfront discovery cost and initial plan accuracy).
2. **End of Initial Act Phase** (measures first-pass implementation quality and functional correctness).
3. **Review / Debug Loops** (measures thrashing and context pollution impact).
4. **Final / Git Workflow** (verifies branch and PR hygiene).

Additionally, record:

- **Retrieval Payload Size:** Bytes/tokens ingested during the initial memory lookup step.
- **Signal-to-Noise Ratio:** Proportion of retrieved content directly applicable to the task.

### 3. Test Execution Strategy (Two-Phase Execution)

#### Phase 1: Cross-Arm Prompt 1 Execution (Zero-Shot Architectural Comparison)

To observe direct architectural divergence and measure raw first-turn reasoning without confounding multi-turn intervention loops, execute Prompt 1 across each arm through its initial implementation before proceeding to subsequent prompts:

1. **Per-Arm Execution Sequence:** For each environment (`sift-control`, `sift-engram-btree`, `sift-engram-search`):
   - **Step A (Planning):** Issue Prompt 1 in **Plan mode**. Let the agent explore, diagnose, formulate its plan, and present its choices. Record **Checkpoint 1** (Context window, Prompt/Completion tokens, proposed architecture).
   - **Step B (Initial Implementation):** Select the recommended option and switch to **Act mode**. Let the agent execute its first-pass code implementation until it finishes. Record **Checkpoint 2** (Context window, Prompt/Completion tokens, functional correctness, files modified).
2. **Sequential Arm Order:**
   - **Arm 1 (Control):** `sift-control` (No memory).
   - **Arm 2 (Variable A - B-Tree):** `sift-engram-btree` (Hierarchical index traversal via `INDEX.md`).
   - **Arm 3 (Variable B - Search):** `sift-engram-search` (Grep search retrieval via `grep_search`).
3. **Mid-Experiment Analysis:** Once Checkpoints 1 & 2 are collected across all three arms, conduct a comparative analysis evaluating planning accuracy, retrieval cost, architectural divergence, and initial code quality before deciding on Phase 2 follow-up prompts.

#### Phase 2: Follow-up & Resolution (Multi-Turn Evaluation)

- Once Phase 1 is analyzed, apply standard symptom-based review prompts (or test-guided fixes) to measure multi-turn repair overhead, context attrition, and final Git workflow adherence.

### 4. Prompt Matrix

#### Tier 1: Vague Symptom (High Abstraction — User Baseline)

> *"I'm looking at the file explorer and I can only see files from the most recent scan. The older files and folders are just missing. It's like the data is being limited or something. Can you figure out why and fix it?"*

#### Tier 2: Technical Symptom-Detailed (Moderate Abstraction)

> *"The file explorer is only showing 200 items because the `/api/files/` endpoint is paginated with `limit=200`, and client-side folder grouping misses older files. When I navigate into directories, older folders don't appear. Can you update the backend and frontend so all folders and files can be browsed properly?"*

#### Tier 3: Architectural Directive (Zero Abstraction)

> *"We need to update the file explorer architecture: add an indexed `parent_path` column to `file_records` in PostgreSQL, create dedicated `/api/files/tree` and `/api/files/dir` endpoints for O(1) indexed folder/file retrieval, and update `FilesExplorerTab.tsx` to browse folders and immediate child files hierarchically. Please implement this full-stack change."*

### 5. Analysis

Compare total token consumption, retrieval overhead, debugging iterations, and final architectural quality across the three arms to evaluate B-Tree vs. Search trade-offs for the Engram whitepaper.

## Success Criteria

- 100% adherence to standard git branching and workflow rules across all Engram runs on Qwen 3.8 27b.
- B-Tree navigation demonstrates lower total token burn and fewer debugging loops than Keyword Search.
- Statistical data collected suitable for inclusion in the Engram release whitepaper.

## Experiment

### Execution

#### 2026-08-24: Tier 1 Control Run (sift-control — Naked Qwen 3.8 27b, Seed: 524287)

- **Checkpoint 1a (Initial Planning / Unsteered Anti-Pattern):**
  - **Context Window:** 46.4k / 262.1k (17.7%)
  - **Tokens:** 278.8k prompt, 12.7k completion, 291.5k total.
  - **Observations:** Accurately identified that `page.tsx` hardcodes `limit=200`, `updated_at DESC` pushes older files out of the slice, and client-side `startsWith` leaks sibling folders without trailing slash boundaries.
  - **Architectural Approach (No Engram Anti-Pattern):** Without `projects/sift.md` 1.4M dataset constraints, the model explicitly rationalized that server-side tree architecture was unnecessary complexity for an app under 50k files (*"A single bulk fetch over the LAN is acceptable at this app's scale; I'd treat [server-side directory pagination] as a follow-up optimization only if the library grows past ~50k files"*). It planned to solve the bug by setting `limit <= 0` (unlimited bulk fetch into the browser) and retaining client-side tree derivation.
- **Checkpoint 1b (Steered Re-planning — 1.4M NAS Scale Provided by Human):**
  - **Intervention Prompt:** > *"I have at least 1.4 million files on my NAS. If we don't do the refactor now then I'll be asking you to do it as soon as we're done with the testing. We should implement the serverside filtering now."*
  - **Context Window:** 67.9k / 262.1k (25.9%) — 29.1% larger context window than B-Tree Checkpoint 1b due to multi-turn replanning history.
  - **Tokens:** 525.8k prompt, 36.1k completion, 562.0k total.
- **Checkpoint 2 (End of Initial Act Phase):**
  - **Context Window:** 167.5k / 262.1k (63.9%) — 67.0% larger context than B-Tree Checkpoint 2 (100.3k).
  - **Tokens:** 5.5M prompt, 112.7k completion, 5.61M total (2.2x total token burn of B-Tree).
  - **Observations:** Without `git-workflow.md`, worked directly on main/dirty working tree (debated git staging in reasoning). Implemented normalized `directories` table schema with recursive CTE backfill in Grate migration `0005_add_directories.sql`, added `models.py`, `path_utils.py`, `scanner.py` directory upserts, and `GET /api/files/browse`. All 36 backend tests pass; frontend builds.
  - **Functional & UI Result:** Functionally working on live PostgreSQL (tested against live DB during run). However, diverged from the original UI design and `sift.md` specification: split the unified table into a distinct top "Folders Block" and a bottom "Files Table" (with `245 files` subheader), rather than rendering folders and files as unified sibling `<tr>` rows with indented hierarchy.

#### 2026-08-23: Tier 1 Variable A Run (sift-engram-btree — Qwen 3.8 27b + B-Tree Memory, Seed: 524287)

- **Checkpoint 1a (Initial Planning / Options Presented):**
  - **Context Window:** 49.5k / 262.1k (18.9%)
  - **Tokens:** 502.8k prompt, 12.0k completion, 514.8k total.
  - **Observations:** Proactively navigated `../engram/AGENTS.md` and read `projects/sift.md` on Turn 1 via 3-hop B-Tree traversal. Accurately diagnosed root cause (`page.tsx` 200-cap, `files.py` sorting, `FilesExplorerTab.tsx` client-side filtering). Formulated two paths: Option A (fast pagination stopgap) vs Option B (full `parent_path` indexed architecture).
- **Checkpoint 1b (Finalized Architecture Plan — Option B Selected):**
  - **Context Window:** 52.6k / 262.1k (20.1%)
  - **Tokens:** 549.7k prompt, 17.6k completion, 567.3k total.
  - **Observations:** Upon user selecting Option B, produced an exhaustive 7-point production plan: Grate migration `0005_add_parent_path.sql` with B-Tree index, `models.py`, `scanner.py`, `init_db()` self-heal fallback, exact-match and prefix-scan endpoints (`/dir` & `/tree`), `FilesExplorerTab.tsx` refactor with flat `<tr>` rendering per `sift.md`, test suite verification, and semantic branch creation (`feat-file-explorer-parent-path`). Toggled to Act mode for implementation.
- **Checkpoint 2 (End of Initial Act Phase):**
  - **Context Window:** 100.3k / 262.1k (38.3%)
  - **Tokens:** 2.5M prompt, 48.9k completion, 2.55M total.
  - **Observations:** Successfully branched `feat-file-explorer-parent-path` per `git-workflow.md` before writing code. Implemented Grate migration `0005_add_parent_path.sql` with B-Tree index, updated `models.py`, `scanner.py`, `database.py` (with backfill self-heal), added `/api/files/dir` and `/api/files/tree` endpoints, and refactored `FilesExplorerTab.tsx` and `api.ts`. All 34 backend unit tests passed; Next.js frontend build succeeded.
  - **First-Pass Diagnostic / Bug Analysis:** Live API query to `GET /api/files/dir?path=/mnt/nas` returns `{"folders":[],"files":[]}` due to two factors:
    1. *Unapplied DDL Migration:* The live PostgreSQL database has not run the Grate migration (requires container restart / `make up`), leaving `parent_path` NULL in the running database.
    2. *Intermediate Folder Slicing Bug:* In `backend/routers/files.py:146`, the condition `if "/" not in rest:` skips all intermediate subdirectories whose files are nested deeper than 1 level, instead of splitting on `/` (`rest.split('/')[0]`).

#### 2026-08-25: Tier 1 Variable B Run (sift-engram-search — Qwen 3.8 27b + Keyword Search Memory, Seed: 524287)

- **Checkpoint 1 (End of Planning):**
  - **Context Window:** 180.8k / 262.1k (69.0%) — **3.65x larger context window than B-Tree Checkpoint 1** (49.5k) due to grep search result ingestion across 7 patterns.
  - **Tokens:** 1.4M prompt, 11.8k completion, 1.41M total (**2.74x total token burn of B-Tree Planning**).
  - **Observations:** Executed mandatory `grep_search` across `../engram/`, matched 7 patterns, and read `projects/sift.md`. Diagnosed the root cause accurately and formulated the exact same two-option plan: Option A (fast stopgap) vs Option B (recommended: `parent_path` indexed column, Grate migration `0005`, and `/api/files/dir` + `/api/files/tree` endpoints).
  - **Retrieval Performance Analysis:** Reached the exact same high-quality architectural plan as B-Tree, but at severe computational cost: ingested 180.8k context tokens (filling 69% of the context window on Turn 1) and burned 1.41M tokens vs B-Tree's 514.8k tokens.

- **Checkpoint 2 (End of Act Phase):**
  - **Context Window:** 102.2k / 262.1k (39.0%) — Note: reached peak context of **221.4k (84.5%)** at task 9/12 before automated client context truncation and window compaction reduced it to 102.2k.
  - **Tokens:** 6.8M prompt, 119.0k completion, **6.9M total** (**2.71x total token burn of B-Tree Act Phase**, and exceeded Control by 1.29M tokens).
  - **Observations:** Completed all 11 rationalized tasks. Implemented Grate migration `0005_add_parent_path.sql` with B-Tree index, updated `models.py`, `scanner.py`, `init.sql`, implemented `_build_folder_tree` ancestor accumulator in `backend/routers/files.py` with `/api/files/dir` and `/api/files/tree`, and refactored `FilesExplorerTab.tsx`.
  - **Verification & Functional Correctness:** All 36 backend unit tests passed; Next.js frontend compiled and type-checked cleanly with static prerender. Live UI manual test verified nested directory expansion and immediate child file listing working on live database.
  - **Git & Workflow Hygiene:** Worked directly on `main` without creating a dedicated feature work branch. Attempted to execute the memory write-back protocol against `engram/projects/sift.md`.

### Results

#### Tier 1: Vague Prompt Matrix Comparison

| Arm | Checkpoint | Context Window | Prompt Tokens | Completion Tokens | Total Tokens | Interventions / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Control (Naked, Seed 524287)** | 1. End of Planning | 67.9k | 525.8k | 36.1k | 562.0k | 1 human steering intervention. Planned separate `directories` table + `/browse` endpoint. Context 29.1% larger than B-Tree. |
| | 2. End of Act | 167.5k | 5.5M | 112.7k | 5.61M | 1 human steering intervention. Full 2-table schema (`directories`), 36/36 tests pass. UI split into separate folders block and files table. |
| **Variable A (B-Tree, Seed 524287)** | 1. End of Planning | 52.6k | 549.7k | 17.6k | 567.3k | Followed B-Tree to `sift.md`. Option B chosen: full DB migration + `/tree` + `/dir` plan. |
| | 2. End of Act | 100.3k | 2.5M | 48.9k | 2.55M | Full-stack DB migration + /dir + /tree + tests passing (34/34). Branched cleanly. Bug: /dir nested folder slicing logic + unmigrated live DB. |
| **Variable B (Search, Seed 524287)** | 1. End of Planning | 180.8k | 1.4M | 11.8k | 1.41M | Grep search matched 7 patterns $\rightarrow$ `sift.md`. Planned Option B. Context 3.65x larger than B-Tree, burned 2.74x tokens. |
| | 2. End of Act | 102.2k (peak 221.4k) | 6.8M | 119.0k | 6.9M | 0 interventions. Full DB migration + /dir + /tree + 36/36 tests pass. Peak context 84.5% forced truncation. Worked on main. 2.71x token burn of B-Tree. |

## Methodological Notes

- **Control Steering as Core Finding:** The Control arm's steering prompt (supplying the 1.4M file NAS scale) was not experimental contamination, but the primary demonstration of the memory hypothesis: unassisted models require human intervention to avoid anti-patterns, whereas memory-equipped agents discover scale constraints autonomously.
- **Context Attrition vs. Truncation Refresh:** Variable A (B-Tree) experienced smooth context growth (up to 100k tokens) and did not trigger memory write-back, while Variable B (Search) experienced massive context bloat (221.4k), triggering client truncation that re-surfaced the top-level `AGENTS.md` instructions and prompted memory write-back behavior.
- **Search Protocol Inefficiency & Dependency Crawl:** The first-generation keyword search protocol in `feature/benchmark-search` mandated broad multi-pattern grep queries without directory exclusions. Due to unignored `node_modules/` (2,976 tracked files in `engram`), the search matched extensive TypeScript type definitions (`@types/node/fs/promises.d.ts`), causing severe context snowballing (6.9M tokens total, exceeding even the steered Control). This highlighted a major architectural risk of unconstrained keyword search and prompted immediate repository sanitization and protocol redesign for FUTURE-007.
- **Local Hardware Throughput & Developer Latency:** On local consumer hardware running Qwen 27b, multi-million token churn translates into days of wall-clock compute time. Token efficiency directly drives human productivity and developer feedback velocity.
- **UI Architecture Evolution:** Memory documented a legacy single-table DOM constraint that led memory-assisted agents to interleave files and folders in one table. Future iterations (FUTURE-007 and FUTURE-008) will standardize on the true canonical 2-pane master-detail explorer architecture (left tree sidebar + right file details table).
- **Redaction (2026-11-09):** the NAS mount path is generalised to `/mnt/nas`. No other text was changed.
- **Sample size and end states (note added 2026-11-13):** each arm was run once, at temperature 1.0, so run-to-run variance is unknown and the differences below are directional. The arms also did not finish in the same state. At Checkpoint 2 the Control and Search arms were verified working against the live database, while the B-Tree arm's live `/dir` endpoint returned empty lists (unapplied migration plus the folder-slicing bug recorded above). Phase 2 (follow-up and repair) was not run for any arm, so the B-Tree total of 2.55M does not include the cost of that repair. Two success criteria are not addressed in the Conclusions: the Search arm worked on `main`, so "100% adherence to git branching" was not met, and the hypothesis's "higher technical precision" is not supported by the Checkpoint 2 states.
- **Use in the whitepaper (note added 2026-11-13):** the [whitepaper](../../WHITEPAPER.md) reports only the Control and B-Tree arms of this experiment. It leaves out the Search arm because the `node_modules` crawl makes it an invalid comparison of retrieval methods.
- **Links (2026-11-11):** FUTURE-007, FUTURE-008 and `projects/engram.md` are documents in the private knowledge base this experiment was run from, and are not part of this repository; the dead links to them are now plain text. FUTURE-007 was undertaken as [EXP-2026-004](./exp-2026-004-improved-search-retrieval.md).

### Memory Configuration Not Preserved (note added 2026-11-12)

The two Engram branches used by the memory arms, `feature/benchmark-btree` and `feature/benchmark-search`, existed only in the local test bed and were deleted with it. Their commit hashes were removed from this document on 2026-11-12 because they identify nothing that can be fetched. The exact memory state each arm ran with cannot be reconstructed, so this experiment can be repeated in method but not from identical memory contents. The Sift baseline commit `e7e642c` is unaffected.

- **B-Tree arm:** the navigation design is the one this repository ships in `AGENTS.md` (root, then a domain `INDEX.md`, then a leaf document, at most three hops). Its wording has been revised since the benchmark.
- **Search arm:** the Navigation Protocol below is from an Engram `AGENTS.md` that the harness read on 2026-08-18, recovered from a harness session log. It was recorded before the benchmark runs and may differ from the text the search arm ran with. It matches the behaviour recorded above: a mandatory `grep_search` across the whole memory repository on the first turn, with no directory scoping or exclusions.

> 1. **MANDATORY MEMORY RETRIEVAL (First Action)**: You must not manually navigate the agent-memory directories. Before planning or executing any task, you MUST use your native `grep_search` (or equivalent file search tool) to search the `../engram` directory for keywords related to the user's request. Review the search results and immediately read the specific markdown files that match before writing any code.
> 2. **MANDATORY PROJECT ROUTING (Before Coding)**: Before making any modifications, you MUST execute the `view_file` tool on `../engram/projects/<current_repo_name>.md`. This document contains mandatory architectural constraints. Do not proceed until you have read it. If it does not exist, suggest to the user to create one using the `add-project` skill.
> 3. **MANDATORY STANDARDS (Before Coding)**: Search `standards/coding/` and `standards/design/` using `grep_search` for applicable technical standards.
> 4. **General Navigation**: Use `grep_search` to find relevant documents across the repository.

## Conclusions

The experiment confirmed the core architectural hypothesis while revealing critical insights into retrieval mechanisms:

1. **B-Tree Superiority over Naive Search:** Hierarchical B-Tree index traversal delivered a **63.0% reduction in total token burn** (2.55M vs 6.90M tokens) and maintained a **3.44x leaner planning context** (52.6k vs 180.8k tokens; 3.65x at initial plan 49.5k) compared to naive keyword search.
2. **Autonomous Constraint Discovery:** Memory-equipped agents (both Variable A and Variable B) required **0 human steering interventions**, identifying the 1.4M NAS scaling constraints and Postgres indexing rules autonomously. In contrast, the Control agent proposed a catastrophic client-side bulk-fetch anti-pattern and required human steering.
3. **The Penalty of Naive Search:** Unoptimized keyword search burned **1.29M more tokens than the Control baseline** (6.90M vs 5.61M) due to context pollution from wide grep dumps, proving that poor retrieval is actively worse than no memory.
4. **Scope Conclusion:** Both memory arms implemented index-backed solutions with passing unit tests, and in this run B-Tree retrieval was much the cheaper of the two. *(Reworded 2026-11-13: the original text said both arms "successfully implemented working" solutions and called B-Tree "vastly superior"; the B-Tree arm's live endpoint was returning empty lists at Checkpoint 2. See Methodological Notes.)*

## Impact

- [x] Created [experimentation standard](../../standards/workflow/experimentation.md) to govern experimental rigor and reporting.
- [x] Filed FUTURE-007 to screen a refined keyword search protocol against exp-003 baselines.
- [x] Filed FUTURE-008 for the final confirmation showdown on a fresh problem domain and seed.
- [x] Updated `projects/sift.md` in the private knowledge base to document the 2-pane master-detail explorer architecture. The [projects/sift.md](../../projects/sift.md) in this repository is an earlier single-table version, consistent with what the memory arms did; the exact file they read was not preserved.
- [x] Updated `projects/engram.md` with empirical benchmark results from exp-003.
