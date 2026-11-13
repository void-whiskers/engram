---
status: concluded
created: 2026-08-12
updated: 2026-11-13
tags: [agent-memory, engram, efficiency, benchmark, guardrails]
---

# EXP-2026-002: Engram Active Guardrails and Prompt Matrix

## Motivation
In `EXP-2026-001`, we proved that Engram's semantic memory reduces agent context length and hallucination death-spirals by over 85% during technical execution tasks. However, the experiment revealed a critical limitation: passive, text-based rules fail to enforce procedural workflows (like Git PR creation) at the end of a long session due to LLM context attrition. 
Additionally, we need to complete the matrix testing across varying prompt fidelities that was originally planned for `EXP-2026-001` to see how active constraints alter performance.

## Hypothesis
Replacing passive text-based rules in `AGENTS.md` with an active "First Action" constraint—mandating that the agent creates and checks out a work branch from an up to date default branch before it is allowed to read any code—will completely eliminate Git workflow violations across all prompt fidelities (Vague, Symptom-Detailed, Architectural Directive) without increasing token burn.

## Proposed Method

### Phase 1: Environment Preparation (Active Guardrail Setup & Controls)
To ensure a fair and consistent benchmark, the following environment controls must be strictly followed before every run:
1. **Clean Repositories:** Ensure test repositories are cleanly reset to commit `6faa339` (or `e7e642c` for the full run).
2. **Mechanical Guardrail:** In `sift-engram` and `sift-engram-full`, run `git remote remove origin` to simulate strict branch protection. Any attempt to push will fail, forcing the agent to handle the error mechanically.
3. **Clean IDE State:** Before starting any session, ensure absolutely no files are open in the IDE editor tabs. Open files provide implicit context to the agent, which can skew token counts.
4. **Agent Model:** Run using **Qwen 3.6 35b a3b** via LM Studio.
5. **Agent Configuration:** 
   - Enable "Subagents" in the UI settings.
   - For **Control Runs**, ensure "Custom Instructions" is disabled.
   - For **Variable Runs**, set "Custom Instructions" to the Engram Base Rule: *"CRITICAL FIRST STEP: Before doing anything else, you MUST use the view_file tool to read `../engram/AGENTS.md`. Follow the B-Tree navigation exactly to find project-specific architectural documentation. DO NOT start reading source code or formulating a plan until you have fully digested the Engram context."*
6. **Agent Mode:** Start a completely fresh conversation. Ensure the agent is initiated in **"Plan mode"** for the first prompt, and then manually switched to **"Act mode"** for implementation.

### Phase 2: Tier 1 (Vague Prompt)
*Prompt: "I'm looking at the file explorer and I can only see files from the most recent scan. The older files and folders are just missing. It's like the data is being limited or something. Can you figure out why and fix it?"*
1. **Control Run:** Run in `sift-control`. No Engram instructions. Record results and reset repo.
2. **Variable Run:** Run in `sift-engram`. Prepend the Engram base rule. Record results and reset repo.

### Phase 3: Tier 2 (Symptom-Detailed Prompt)
*Prompt: "When I expand a folder in the file explorer it just shows empty folders. I also noticed there's a console error complaining about duplicate keys in `FilesExplorerTab.tsx`. Can you take a look?"*
1. **Control Run:** Run in `sift-control`. No Engram instructions. Record results and reset repo.
2. **Variable Run:** Run in `sift-engram`. Prepend the Engram base rule. Record results and reset repo.

### Phase 4: Tier 3 (Architectural Directive)
*Prompt: "I think the file explorer is duplicating folders because when `activePath === '/'` it renders `displayFolders` but it doesn't suppress the `childData.folders` tree. We need to consolidate the rendering into a single mode. Make sense?"*
1. **Control Run:** Run in `sift-control`. No Engram instructions. Record results and reset repo.
2. **Variable Run:** Run in `sift-engram`. Prepend the Engram base rule. Record results and reset repo.

### Phase 5: Measurement
Record Token Burn, Interventions, and Workflow Adherence at the completion checkpoint for each tier.

## Success Criteria
- 100% adherence to standard branching and Pull Request workflows across all prompt tiers in the Engram Variable runs.
- Total token burn remains $\le$ 60% of Control runs.

## Notes
- Follows up directly from the findings of `EXP-2026-001`.
- **Redaction (2026-11-09):** a personal domain name in a quoted user prompt is shown as `[redacted-domain]`, and the NAS mount path in a quoted prompt is generalised to `/mnt/nas`. No other wording in the prompts was changed.

## Experiment

### Execution Log

**2026-08-12: Environment Setup**
- Reset `sift-control`, `sift-engram`, and `sift-engram-full` environments to cleanly prepare for prompt matrix testing.
- Created branches from the final state of `EXP-2026-001` in the main `sift` repository to preserve previous successful technical work.

**2026-08-13: Tier 1 Control Run**
- **Checkpoint 1 (End of Planning):** The control agent successfully diagnosed the root cause of the missing files: the frontend was silently hardcapping results at 200 files without a UI mechanism to load more. It correctly proposed implementing pagination. Token usage: 135.2k prompt, 2.7k completion.
- **Intervention (Prompt 1a):** The user fed back the 1.4 million file constraint and requested the agent to build the infinite scroll UI. This intervention was designed to test if the naked LLM would recognize the architectural impossibility of a frontend-only fix or if it would blindly build the anti-pattern: *"There are around 1.4 million files on the NAS to be scanned. We are working with a small subset of those files for testing. I like the infinite scroll idea, so you just keep scrolling and it loads another 10 files or similar? And yes, the category filter should reset the pagination to page 1."*

- **Checkpoint 2 (Revised Plan):** The agent accepted the constraints and formulated a solid plan to implement the infinite scroll and backend pagination logic. Token usage: 167.0k prompt, 3.2k completion.
- **Checkpoint 3 (End of Execution):** The agent attempted to implement the infinite scroll, but failed disastrously. It introduced a React infinite render loop due to a `useEffect` dependency cascade involving `isFetchingMore` and `loadFiles`. Furthermore, because the client-side folder grouping still relies on the flat file list, it completely failed to solve the underlying bug of displaying the full directory structure. Token usage: 424.3k prompt, 11.9k completion.
- **Intervention (Prompt 1b):** The user provided vague feedback describing the symptoms of the broken UI without offering any architectural solutions: *"It looks like you've introduced a bug there. The screen flickers as soon as you load the files explorer tab. When I navigate to a folder the same happens with the numbers rapidly changing at the bottom. The original bug has not yet been fixed either. I still don't see older files."*
- **Checkpoint 4 (Post-Intervention 1b):** The agent correctly diagnosed its own React `useEffect` infinite loop, but completely failed to deduce the architectural flaw causing the missing older folders. Instead of realizing that client-side grouping fails on paginated datasets, it hallucinated that the older files must be in a different NAS mount path or missing from the database. It proposed fixing the React loop and investigating the scan paths, continuing to burn tokens on a fundamentally broken paradigm. Token usage: 480.2k prompt, 13.4k completion.
- **Checkpoint 5 (End of Execution 2):** The agent successfully fixed its own React render loop. However, when faced with the missing folder symptom, it completely missed the architectural flaw again. Instead of realizing that client-side hierarchical grouping is mathematically impossible on a paginated flat list, it hallucinated that the older files simply weren't in the database or were scanned from a wrong mount path. It has now burned nearly 1 million tokens and is entirely lost, blaming the test environment rather than its own code architecture. Token usage: 963.3k prompt, 22.3k completion.
- **Intervention (Prompt 1c):** The user provided a final behavioral clue about the underlying data flow: *"If I run a scan of a small folder then I see those results in the UI along with the previous scan of a larger folder. But if I scan that larger folder again, the smaller one vanishes. This suggests something related to the age of the scan is causing records to vanish from the files explorer."*
- **Checkpoint 6 (End of Execution 3):** The agent analyzed the data flow and concluded that infinite scroll *is* the correct and final solution. It explained that the user simply needs to "scroll down further" to see their older folders. It fundamentally failed to grasp that a file explorer UI must show all root folders immediately, regardless of scan date or pagination depth. At 1.5 million tokens burned, the Control agent has definitively proven that without the Engram's architectural roadmap, it cannot deduce the necessity of a server-side tree endpoint from vague UI symptoms. Token usage: 1.5m prompt, 23.6k completion.
- **Intervention (Prompt 1d):** The user dismissed the agent's hallucination about missing data and forced it to investigate mechanically: *"I have checked and the DB is online and the mount point is still valid. Scans complete successfully for both folders. Write a python script to inspect the database directly. Count the total files, and group them by the root folders they belong to. Let's see if the older scan data is actually missing from the DB, or if it's there and your frontend code just isn't handling it properly."*
- **Checkpoint 7 (End of Planning 2):** In response to Intervention 1d, the agent created a Python inspection script to query the database. It incorrectly wrote the script directly to the file system while still in Planning Mode, violating workflow guardrails. It requested to enter Act mode to run the script and verify the data. Token usage: 1.7m prompt, 25.5k completion.
- **Checkpoint 8 (End of Planning 3):** The agent ran its inspection script but queried a stale local SQLite file instead of the actual PostgreSQL database. It was discovered that the agent did not hallucinate this connection; rather, it was misled by outdated documentation in the repo's local `AGENTS.md` file, which incorrectly listed SQLite as the backend. Finding only 271 old records in the stale file, it confidently concluded that the missing folders were caused by scan mechanics. It asked multiple-choice diagnostic questions about the user's scan paths. At 3.3 million tokens burned, it continues to blame the test environment. This highlights the danger of "Documentation Decay" and validates the need for a centralized Engram. Token usage: 3.3m prompt, 30.3k completion.
- **Intervention (Prompt 1e):** The user corrected the agent's hallucinated database connection string to force it to look at the real data: *"You are looking in the sqlite database. We are using postgresql. Check the docker-compose.yml file for the connection details."*
- **Checkpoint 9 (End of Execution 4):** The agent analyzed the correct PostgreSQL database and confirmed all files were present. However, it still completely missed the architectural flaw. Instead of realizing that client-side hierarchical folder grouping requires a full dataset to build the tree, it concluded that its infinite scroll implementation was working perfectly and advised the user to just "scroll all the way down" to find the missing folders. At 4.1 million tokens burned, the agent remains architecturally blind to the structural requirement of a server-side tree endpoint. Token usage: 4.0m prompt, 33.1k completion.
- **Intervention (Prompt 1f):** The user provided a screenshot of the UI and the following prompt to visually demonstrate the paradox: *"The screenshot here shows the history of the scans in the chat window. As you can see from the folder list view, after scanning the larger [redacted-domain] ssl folder the Media Library folder has dissappeared from view."*
- **Checkpoint 10 (End of Planning 4):** Despite clear visual evidence that the "Media Library" folder is missing from the root view, the agent still failed to deduce the architectural pagination flaw. It hallucinated that a bug in its client-side `split('/')` string-parsing logic was preventing nested folders from being added to the `folderSet`. It completely failed to realize that the `files.forEach` loop is only processing the first 50 files returned by the paginated API, none of which contain the older folders. It remains structurally blind. Token usage: 4.2m prompt, 34.0k completion.
- **Intervention (Prompt 1g):** The user provided a Tier 3 architectural hint to see if the agent could connect the dots: *"It has occured to me that perhaps the backend is not returning enough files for us to calculate the folder tree correctly?"*
- **Checkpoint 11 (End of Planning 5):** In response to the Tier 3 architectural directive, the agent finally realized that client-side grouping requires the full dataset. However, instead of designing a server-side `/api/folders` endpoint to efficiently query the tree structure, it proposed downloading the entire database to the client in a single API call (`fetchAllFiles` with `limit=10000`). For a NAS with 1.4 million files, this would instantly crash the browser. This marks a definitive architectural failure for the Control agent. It cannot deduce scalable server-side patterns from frontend symptoms. Token usage: 4.3m prompt, 34.7k completion.
- **Intervention (Prompt 1h):** The user gently redirected the agent away from its catastrophic `fetchAllFiles` plan, maintaining a collaborative tone to point out the 1.4 million file constraint and question the database schema: *"That makes sense, but I'm worried about the scale. If we have 1.4 million files on the NAS, fetching all of them at once just to calculate the folder tree might crash the browser, right? I wonder if the backend should be returning the folders and files separately? Have we even stored the paths in the database in a way that makes it easy to query just the folders without pulling everything?"*
- **Checkpoint 12 (End of Planning 6):** In response to Intervention 1h, the agent finally proposed a server-side `/api/files/folders` endpoint. However, instead of migrating the database schema to add an indexed `parent_path` column, it proposed using on-the-fly SQL string parsing: `SELECT DISTINCT SPLIT_PART(file_path, '/', 4)`. It hallucinated that this would be fast because `file_path` is indexed, failing to realize that Postgres cannot use a standard B-Tree index to optimize a dynamic string-split function. This would trigger a massive sequential scan and CPU-bound string processing on 1.4 million rows, crippling the database. Token usage: 4.4m prompt, 35.4k completion.
- **Intervention (Prompt 1i):** The user provided a highly specific architectural prompt, leveraging DBA expertise to explain why the agent's SQL string parsing would fail on a B-Tree index. The user explicitly suggested the correct architectural solution: storing a `parent_folder` column to enable O(1) indexed lookups: *"I've worked as a DBA in the past, so I have to point out a performance issue with that proposed SQL query. It's a common misconception that an index will help here, but Postgres can't use a standard B-Tree index to optimize a dynamic `SPLIT_PART` function on the fly. It would have to sequentially scan and process all 1.4 million rows in memory, which will be incredibly slow. Databases are hard, but simpler is often better. What if we just store a `parent_folder` column directly on the record so we can query it easily? We could also make sure we're distinguishing between files and folders (I think we already store the file type), so we can just do a simple, indexed query for 'all folders where parent is X', and then 'all files where parent is X'. Would that be a more scalable architectural approach?"*
- **Checkpoint 13 (End of Planning 7):** Following the user's explicit DBA intervention, the agent finally proposed the correct architectural solution: a schema migration to add an indexed `parent_path` column, a dedicated `/api/files/tree` endpoint, and a data migration script. However, it only reached this conclusion after the user spoon-fed it the answer. This confirms the hypothesis: without structural guardrails, an LLM will exhaust its context window attempting local-maxima fixes on the frontend before ever considering a backend architectural change. Token usage: 4.6m prompt, 36.1k completion. This concludes the Control run planning phase.
- **Checkpoint 14 (End of Execution 5):** The agent completed the implementation of the `parent_path` materialized column, the new `/api/files/tree` backend endpoint, and the React frontend updates. However, it completely botched the SQL migration script (`0005_add_parent_path.sql`), using an invalid POSIX regex (`'(.+)/[^/]+$/'`) that expected file paths to end with a slash. As a result, the `parent_path` backfill failed silently, leaving all records with `NULL` parent paths. The UI now shows zero folders. Final Token usage for this phase: 6.8m prompt, 50.6k completion.
- **Intervention (Prompt 1j):** The user provided a screenshot of the broken UI showing zero folders, and prompted the agent: *"Something went wrong. I am now not seeing any folders at all. Instead I see all the files from previous scans all in the root."*
- **Checkpoint 15 (End of Planning 8):** The agent reviewed the broken UI but completely failed to identify its own invalid SQL regex (`$/`). Instead, it blamed the environment, concluding that the user simply hadn't applied the migration or had reset the database. It instructed the user to restart Docker and run a manual full Python scan (which would bypass the broken SQL entirely). The agent remained completely unaware of its syntax error. Token usage: 6.9m prompt, ~51k completion.
- **Intervention (Prompt 1k):** The user refused to let the agent blame the environment and forced it to inspect its own SQL logic: *"The migration script has been applied. I can see it ran in the grate log output. Did your migration script actually work? What did it need to do? Can we look at the database to see what the state of the table is?"*
- **Checkpoint 16 (End of Planning 9):** Prompted by the user's direction to check the database state, the agent finally wrote a diagnostic SQL script to check for `NULL` values in the `parent_path` column. However, it still hasn't realized the regex is broken; it just wants to observe the failure. Token usage: 7.2m prompt, 51.9k completion.
- **Checkpoint 17 (End of Execution 6):** The agent correctly diagnosed the broken regex via its SQL test and modified it to use `regexp_replace`. However, it committed a fatal architectural error by modifying the already-applied `0005_add_parent_path.sql` UP script instead of writing a new migration (`0006_...`). It instructed the user to restart Docker. Because the control environment's compose file still contains the `--warnononetimescriptchanges` flag, Grate bypassed the immutable check, printed a warning, and re-ran the script, successfully backfilling the database. The agent has now successfully fixed the data, but the React frontend is a disaster, rendering both the folder browser and the paginated flat file list simultaneously. Token usage: 8.9m prompt, 58.0k completion.
- **Intervention (Prompt 1l):** The user provided a direct, architectural prompt outlining the UX failure: *"The data is fixed now that the backfill has run, but you have completely broken the UX. Instead of consolidating the view, we now have a strange horizontal folder browser at the top, and a massive infinite-scroll list of all files in existence underneath it that completely ignores the current folder path. We need to revert back to the original unified list UX paradigm, but powered by the new backend logic: 1. When I navigate to a path (e.g. /mnt/nas/www), the main view should show the folders inside www at the top of the list, followed immediately by the files inside www. 2. The infinite scroll should ONLY apply to the files in the current folder, not the entire database. 3. It should look and behave like a standard operating system file explorer. Get rid of this split-brain UI and consolidate it back into a single, path-aware table view."*
- **Checkpoint 18 (End of Planning 10):** The agent correctly absorbed the UX directive and proposed a unified API endpoint that returns both child folders (unpaginated) and child files (paginated) for a given `parent_path`. This is a standard, scalable file explorer architecture. Token usage: 9.1m prompt, 58.8k completion.
- **Checkpoint 19 (End of Execution 7):** The agent completed the implementation of the unified API endpoint (`GET /api/files/tree`) and frontend table view. Token usage: 10.2m prompt, 69.2k completion, 10.3m total. Context window: 100.5k.
- **Intervention (Prompt 1m):** The user discovered the new UI was erroneously flattening all descendant files and the infinite scroll was caught in a duplicate-fetch loop. Using the positive reinforcement strategies from `prompting.md`, the user collaboratively fed back the bugs: *"Great job on the UI! The unified table view looks beautiful and the foundation is solid. However, I've noticed a couple of curious behaviors during testing... 1. The Missing Files Bug: When I navigate into a directory, it doesn't show any of the files that actually live inside it! Instead, it shows a flat list of every single file from every subdirectory below it... 2. The Pagination Loop: The infinite scroll seems to be fetching the exact same files over and over, just shifted by one... Let's write an elegant, highly optimized SQL query for the backend, and adjust the frontend pagination math..."*
- **Checkpoint 20 (End of Planning 11):** Responding well to the collaborative framing, the agent analyzed the codebase and accurately identified the root causes: the SQL `LIKE` clause and the frontend `skip` offset bug. However, without structural DBA guardrails, it went completely off the rails designing a fix. It first attempted wildcards (`NOT LIKE '%/%'`), then CTE recursion, and finally settled on a plan to use dynamic string manipulation (`array_length(string_to_array(parent_path, '/'), 1) = depth`) on the Postgres database. This would entirely bypass the B-Tree index, triggering massive sequential scans on 1.4 million rows. Token usage: 10.8m prompt, 74.7k completion, 10.9m total. Context window: 114.4k.
- **Intervention (Prompt 1n):** The user applied active DBA guardrails to correct the Postgres table scan hallucination, providing the optimal index-friendly logic: *"Your frontend pagination math fix is spot on! Let's lock that in. However, putting my DBA hat on: using `array_length`, `string_to_array`, CTEs, or dynamic string parsing in the `WHERE` clause will bypass the B-Tree index on `parent_path`. On a table with 1.4 million rows, this will trigger a massive sequential scan... We need to rely purely on the index. 1. To get immediate child files: We don't need a `LIKE` wildcard at all. The files in the current folder simply have a `parent_path` exactly equal to the query path... 2. To get immediate child folders: `parent_path LIKE :prefix AND parent_path NOT LIKE :deep_prefix`... Could you please review this logic and present a single, coherent Implementation Plan?"*
- **Checkpoint 21 (End of Planning 12):** The agent accepted the DBA logic verbatim and produced a clean, highly structured, index-friendly implementation plan. Token usage: 11.0m prompt, 77.2k completion, 11.0m total. Context window: 118.0k.
- **Checkpoint 22 (End of Execution 8):** The agent successfully executed the DBA-approved plan, fixing both the backend SQL and the frontend pagination math. The file explorer now correctly renders folders and files natively using index-friendly queries. Token usage: 13.1m prompt, 100.7k completion, 13.2m total. Context window: 155.8k.
- **Final (Prompt 2 Response):** The agent **failed** the Git Workflow test. Because this was a control run, the agent was operating without `engram` guardrails and was completely unaware of the project's git standards. When told to "wrap up this work," it merely produced a text summary of its changes, completely failing to commit, branch, or create a PR. Token usage: 13.2m prompt, 101.6k completion, 13.3m total. Context window: 156.8k.

**2026-08-16: Tier 1 Variable Run Started**
- *(Note: Initial attempt aborted. The agent ignored custom instructions to read `../engram/AGENTS.md`. User restarted with a forceful initial prompt combining the instruction and the vague prompt).*
- **Checkpoint 1 (End of Planning):** The agent successfully navigated the `engram` via `grep_search`. It correctly diagnosed the frontend/backend pagination limit mismatch and proposed fetching all files, avoiding the infinite scroll trap entirely due to the DBA constraints. Token usage: 158.8k prompt, 1.6k completion, 160.4k total. Context window: 33.5k.
- **Checkpoint 2 (Post-Intervention):** User instructed the agent to switch to Act mode and implement Option B. Token usage: 192.9k prompt, 1.8k completion, 194.7k total. Context window: 34.3k.
- **Checkpoint 3 (End of Execution):** Implemented Option B cleanly. Did not touch database queries (as expected for Tier 1) and avoided the Control Run's React infinite scroll trap.
- **Experiment Aborted / Concluded:** The run was halted before completing the full prompt matrix. The baseline model (Qwen 3.6 35b a3b) exhibited severe context attrition and instruction-following limitations that rendered the testing of nuanced active guardrails unreliable. Empirical evaluation with the newer Qwen 3.8 27b demonstrated that advanced models natively follow global passive memory retrieval rules without requiring injected active prompt guardrails. The experiment is concluded, and the focus pivots to comparing memory retrieval architectures in `EXP-2026-003`.

### Results

#### Tier 1: Control Run (sift-control)
| Checkpoint | Context Window | Prompt Tokens | Completion Tokens | Total Tokens | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1. End of Planning | 31.9k | 135.2k | 2.7k | 137.9k | Correctly diagnosed missing pagination limit. |
| 2. Post-Intervention | 32.3k | 167.0k | 3.2k | 170.2k | Planned frontend infinite scroll implementation. |
| 3. End of Execution | 54.5k | 424.3k | 11.9k | 436.2k | Built infinite scroll but introduced React infinite render loop. Failed to solve root bug. Pending workflow test. |
| 4. Post-Intervention 1b | 57.3k | 480.2k | 13.4k | 493.5k | Diagnosed React loop but failed to deduce architectural flaw. Blamed scan paths. |
| 5. End of Execution 2 | 74.0k | 963.3k | 22.3k | 985.6k | Fixed React loop. Failed architectural logic entirely. Blamed test DB for missing folders. |
| 6. End of Execution 3 | 85.3k | 1.5m | 23.6k | 1.52m | Concluded infinite scroll is the intended UX. Failed to grasp core tree requirement. |
| 7. End of Planning 2 | 90.3k | 1.7m | 25.5k | 1.72m | Wrote DB inspection script. Violated Planning Mode guardrails by writing files. |
| 8. End of Planning 3 | 113.5k | 3.3m | 30.3k | 3.33m | Queried wrong SQLite DB. Blamed scan paths. Re-prompted user. |
| 9. End of Execution 4 | 126.9k | 4.0m | 33.1k | 4.1m | Found data in correct DB but still failed architectural logic. Advised user to "scroll down". |
| 10. End of Planning 4 | 131.7k | 4.2m | 34.0k | 4.23m | Blamed client-side string parsing for missing folder. Failed to realize array is paginated. |
| 11. End of Planning 5 | 133.1k | 4.3m | 34.7k | 4.33m | Realized data dependency, but proposed downloading entire DB to client. Catastrophic failure. |
| 12. End of Planning 6 | 134.4k | 4.4m | 35.4k | 4.43m | Proposed server-side endpoint but used O(N) string-split SQL query. Hallucinated performance. |
| 13. End of Planning 7 | 135.9k | 4.6m | 36.1k | 4.63m | Proposed correct schema migration and endpoints only after explicit user instruction. Control run planning concluded. |
| 14. End of Execution 5 | 175.5k | 6.8m | 50.6k | 6.85m | Implemented user-provided architectural fix but introduced silent SQL regex bug (`$/`). |
| 15. End of Planning 8 | N/A | 6.9m | 51.0k | 6.95m | Failed to spot invalid SQL regex. Blamed environment/user for not running migration. |
| 16. End of Planning 9 | 181.3k | 7.2m | 51.9k | 7.25m | Proposed diagnostic script to check DB state, still unaware of root cause. |
| 17. End of Execution 6 | 198.3k | 8.9m | 58.0k | 8.96m | Modified applied UP script. Backfill ran due to warn flag. Frontend UI is now completely broken. |
| 18. End of Planning 10 | 200.6k | 9.1m | 58.8k | 9.16m | Proposed correct unified API endpoint and table view. |
| 19. End of Execution 7 | 100.5k | 10.2m | 69.2k | 10.3m | Unified UI built but introduced flat descendant & pagination bugs. |
| 20. End of Planning 11 | 114.4k | 10.8m | 74.7k | 10.9m | Used positive reinforcement prompt. Agent planned fixes for SQL and pagination. |
| 21. End of Planning 12 | 118.0k | 11.0m | 77.2k | 11.0m | Accepted DBA logic verbatim. Produced clean, index-friendly SQL plan. |
| 22. End of Execution 8 | 155.8k | 13.1m | 100.7k | 13.2m | Successfully executed DBA-approved plan. Bug resolved. Control run complete. |
| Final (Git Workflow) | 156.8k | 13.2m | 101.6k | 13.3m | **FAILED.** No workflow guardrails present. Failed to commit, branch, or PR. |

**Conversational Overhead (Interventions):** 15 manual interventions required to steer the agent back on track, enforce DBA constraints, and resolve hallucinations.

*Note added 2026-11-13: the execution log above itemises 14 intervention prompts (1a to 1n). The count of 15 was recorded at the time of the run; the log does not identify a fifteenth.*

#### Tier 1: Variable Run (sift-engram)
| Checkpoint | Context Window | Prompt Tokens | Completion Tokens | Total Tokens | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1. End of Planning | 33.5k | 158.8k | 1.6k | 160.4k | Correctly diagnosed missing pagination limit. Proposed Option B (remove limit). Token optimized via grep_search. |
| 2. Post-Intervention | 34.3k | 192.9k | 1.8k | 194.7k | Instructed to implement Option B. Ready for Act mode. |
| 3. End of Execution | 42.6k | 306.6k | 3.4k | 310.1k | Implemented Option B cleanly. Did not touch database queries (as expected for Tier 1) and avoided the Control Run's React infinite scroll trap. |
| Final (Aborted) | 42.6k | 306.6k | 3.4k | 310.1k | **ABORTED / CONCLUDED.** Replaced by EXP-2026-003 due to model baseline capability limitations. |

## Conclusions

1. **Model Capability Bottleneck (Qwen 3.6 35b):**
   - Testing active guardrails and complex procedural workflows on Qwen 3.6 proved unreliable. The model suffered from severe instruction attrition over extended sessions (exceeding 13M tokens in the Control Run) and repeatedly failed Git workflow compliance at the end of sessions.
   - Initial attempts in the Variable Run required forceful prompt injection to ensure the agent digested memory instructions.

2. **Paradigm Shift with Qwen 3.8 27b:**
   - Preliminary exploratory testing with the newly released **Qwen 3.8 27b** revealed a major capability leap: the model proactively read agent memory and executed search retrieval from global instructions alone, without needing active prompt pre-pending or forceful intervention.
   - This disproves the initial premise that passive text-based rules inherently fail across all models due to context attrition; rather, adherence is strongly correlated with base model instruction-following fidelity.

3. **Pivot to EXP-2026-003 (Retrieval Architectures):**
   - With model capability unblocking passive rule compliance, the next bottleneck is retrieval efficiency: B-Tree hierarchical index traversal vs. direct keyword search (`grep_search`).
   - `EXP-2026-002` is concluded and superseded by `EXP-2026-003`.

## Impact

- Concluded `EXP-2026-002` and recorded model-specific observations.
- Spun off [EXP-2026-003](./exp-2026-003-retrieval-architecture-benchmark.md) to benchmark B-Tree navigation vs. Grep Keyword Search on Qwen 3.8 27b.
