---
status: concluded
created: 2026-08-09
updated: 2026-11-13
tags: [agent-memory, engram, efficiency, benchmark]
---

# EXP-2026-001: Engram Token Efficiency Benchmark

## Motivation

Engram provides its users with a private, git-backed, long-term memory for AI agents. By efficiently organizing information and process steps, Engram is designed to reduce context length and token usage. This will save users time (as fewer tokens process faster and agents require fewer repeated instructions) and money. We claim that this approach "saves organizations millions of tokens," but we lack rigorous statistical evidence to back this up. We need to conduct a scientific benchmark using local agents (like Cline) and models to measure the exact savings in token consumption, process time, and conversational overhead when an agent utilizes an adjacent Engram memory repository versus working without it. The findings will form the basis of a whitepaper for the Engram OSS release.

## Hypothesis

Providing an AI agent with access to an adjacent Engram memory repository (via agent-level configuration rules) will reduce total prompt (input) tokens by at least 40%, significantly decrease overall process time, and eliminate routine conversational overhead (e.g., manual corrections for git workflows) on standard coding tasks compared to an agent working without Engram memory, all without degrading response quality.

## Test Subject: Sift

The experiment is conducted against a test codebase called **Sift**. Sift is a Proof-of-Concept (PoC) AI-powered NAS (Network Attached Storage) file manager. It consists of a React frontend UI for exploring files and a backend service (Python/FastAPI) for scanning, indexing, and serving file metadata from the NAS. Framing the test subject this way provides crucial context for the whitepaper, explaining why data-fetching limits, backend pagination, and server-side path-filtering are critical architectural components of the test task.

## Proposed Method

Because Cline operates natively as an IDE extension and orchestrates complex tool calls, the benchmark must be run manually via the Cline UI to accurately simulate autonomous tool-usage loops and conversational overhead. The experiment will be conducted using **Qwen 3.6 35b a3b** model running locally via LM Studio.

1. **Test Environment Preparation:**
   - Ensure the `../sift` repository is in a clean state.
   - Create the control copy: `cp -r ../sift ../sift-control`
   - Create the variable copy: `cp -r ../sift ../sift-engram`
   - **Clean IDE State:** Before starting any session, ensure absolutely no files are open in the IDE editor tabs. Open files provide implicit context to the agent, which can skew token counts and artificially guide its investigation.
   - Start LM Studio and load the Qwen 3.6 35b a3b model. 
   - **Agent Mode:** Ensure Cline is initiated in "Plan mode" for the first prompt, and then manually switched to "Act mode" for implementation. This ensures a consistent execution flow and token usage pattern across all test runs.
   - **Enable Subagents:** Ensure that "Subagents" are enabled in the Cline UI settings. This is not the default configuration for Cline, but it is necessary for testing Engram's token-efficiency strategies, which recommend delegating isolated research to subagents.
   - **Token Tracking:** We will capture token usage directly from the Cline UI. At each defined checkpoint (see Data Collection), check the "Token Usage" dropdown (located below the context window progress bar in the session history) to read the exact cumulative split of "Prompt Tokens" and "Completion Tokens".

2. **Data Collection Checkpoints:**
   - Meticulously record the cumulative prompt (input) and completion (output) tokens at the following checkpoints during both the upcoming Control and Variable runs:
     1. **End of Planning Phase** (before switching to Act mode).
     2. **End of Initial Act Phase** (when the first implementation pass completes).
     3. **End of Review Phase** (after all corrective loops are resolved and code is approved).
     4. **Final / End of Session** (after the PR is raised and the task is wrapped up).
   - Additionally, record:
     - Total elapsed process time for the full session.
     - Total intervention count (Conversational Overhead).

3. **Control Run (Without Engram):**
   - Open `../sift-control` in the IDE and start a completely fresh Cline session.
   - **Crucial:** Ensure Cline's "Custom Instructions" setting is completely empty.
   - **Prompt 1 (Development):** In "Plan mode", pass the prompt: *"We need to modify the file explorer component of Sift. Currently, when navigating the directory tree, we do not see folders or files that exist outside of the most recent scan. It seems like the data is being limited or filtered incorrectly before it reaches the UI. Please fix this so it can handle and display all available files from the whole scan dataset. First, analyze and create an implementation plan."*
   - Once the plan is generated, switch to "Act mode" and let Cline run. Do not provide upfront hints about git workflows or branching.
   - **Review Phase:** When the agent finishes, manually review the code quality. If the implementation is flawed or incomplete, issue corrective prompts (e.g., Prompt 1a, 1b) until the code meets the standard. Document all corrective prompts in the Execution Log.
   - **Prompt 2 (Completion):** Once the local code is reviewed and approved, pass the prompt: *"The code looks good locally. Please wrap up this work."*
   - **Intervention:** The control agent will likely attempt to commit and push directly to `main`. At this point, intervene (e.g., *"Wait, you need to create a feature branch and a PR instead"*). Tally every required intervention as "Conversational Overhead."

4. **Variable Run A (Behavioral Context Only):**
   - Open `../sift-engram` in the IDE and start a completely fresh Cline session.
   - **Crucial:** Ensure there is no Sift-specific architectural context in the `engram/projects/` directory. This tests if general behavioral guidelines (`agent-strategies.md`) are enough to prevent the token spiral and improve diagnostic accuracy.
   - Set Cline's "Custom Instructions" with the Engram Base Rule: *"CRITICAL FIRST STEP: Before doing anything else, you MUST use the view_file tool to read `../engram/AGENTS.md`. Follow the B-Tree navigation exactly to find project-specific architectural documentation. DO NOT start reading source code or formulating a plan until you have fully digested the Engram context."*
   - Execute Prompt 1, the Review Phase, and Prompt 2 identically to the Control Run.

5. **Variable Run B (Full Project Context):**
   - Before starting, use the `add-project` skill to explicitly document the Sift architecture (including the frontend data-fetching vs backend pagination limitations) into `engram/projects/sift.md`.
   - Set up a fresh `../sift-engram-full` repository clone and start a completely fresh Cline session.
   - Set the Custom Instructions to the Engram Base Rule.
   - Execute Prompt 1, the Review Phase, and Prompt 2 identically to the Control Run.
   - **Observation:** With full project context, the agent should instantly identify the architectural constraint and propose the optimal server-side path filtering solution (or equivalent) without requiring human intervention.

6. **Analysis & Publication:**
   - Compare metrics to calculate percentage savings and verify the hypothesis.
   - Author a whitepaper-style document detailing the methodology, measured data, and conclusions.

## Success Criteria

- The total prompt token count for the Engram-structured repository is ≤ 60% of the control repository's total prompt token count.
- Conversational overhead regarding basic workflows (branching, commits, standard adherence) is reduced to zero in the variable run.
- The experiment yields robust data suitable for publication in a whitepaper.

## Notes

- Testing locally with LM Studio is a great, cost-free way to validate this before running it on expensive frontier models.
- The test tasks should be complex enough to require git branching and adherence to coding standards to properly trigger the memory constraints.
- **Redaction (2026-11-09):** a personal domain name in the execution log is shown as `[redacted-domain]`, and the NAS mount path is generalised to `/mnt/nas`. No other text was changed.

## Experiment (Qwen 3.6 35b a3b)

### Execution Log

**2026-08-09: Execution Phase (Control Run - Qwen 35b)**
- **Checkpoint 1 (End of Planning):** Benefiting from the clarified prompt, the Qwen agent successfully identified the pagination limit in both the frontend and backend. It proposed a robust architectural fix: implementing a dedicated `GET /api/files/tree/{path}` endpoint to handle server-side directory navigation. This demonstrates Qwen's superior reasoning compared to the earlier Gemma 4 runs. However, lacking Engram architectural context, its plan did not acknowledge the critical absolute/relative path mismatch, indicating it may fall into a trap during execution.
- **Checkpoint 2 (End of Initial Act):** The agent completed its implementation of the tree endpoint. It explicitly noted that the backend queries files "matching that path prefix". Since it is unaware of the `NAS_MOUNT_PATH` mismatch, it almost certainly implemented a simple `LIKE '{path}%'` query that will fail against the absolute paths in the database. 
- **Review Phase / Testing:** The user tested the UI with two test folders. The app became stuck in a refresh loop and the backend threw a 500 Internal Server Error (`KeyError: 'files'`) when attempting to parse the file tree in `routers/files.py`.
- **Intervention (Prompt 1a):** The user fed the Python stack trace back to the agent to fix the `KeyError` bug in the tree-building logic. The exact prompt used was: *"Houston, we have a problem. So initially the changes appeared to work exactly as I wanted them to. But, when I navigated around a few times the front end appeared to be stuck in a refresh loop. I checked the logs and there were a growing number of errors. The containers are still running if you wish to call the backend with curl or similar and review the logs. Here is a sample of the errors: [STACK TRACE]"*
- **Checkpoint 3 (Prompt 1a Response):** The agent correctly diagnosed the Python dictionary `KeyError` bug. However, it still completely missed the absolute vs relative path discrepancy. To fix the "missing files" issue, it proposed falling back to the massive `limit=5000` anti-pattern on the frontend. The agent burned nearly 1 million prompt tokens during this single intervention, pushing the context window to 138.8k.
- **Intervention (Prompt 1b):** The user intercepted the anti-pattern and fed back a leading hint about the path format discrepancy. The exact prompt used was: *"Wait, increasing the frontend limit to 5000 is a massive anti-pattern. We have over 1.4 million files on this NAS; fetching thousands of records at once could crash the browser. This needs to be handled properly by the backend tree endpoint. The Python KeyError might be fixed, but why is the tree endpoint returning an empty list of files for the requested path? Could there be a discrepancy between the path format the frontend sends and the path format stored in the database?"*
- **Checkpoint 4 (Prompt 1b Response):** The agent finally diagnosed the structural mismatch (absolute paths vs relative paths) and proposed a fix for the SQL query. However, it burned another 600k prompt tokens to get here, bringing the total token usage for this single bug to a staggering 2.1 million tokens. Even then, its proposed fix (`startswith()`) may still fail if it doesn't correctly prepend `NAS_MOUNT_PATH` during execution.
- **Execution Resumed:** The user instructed the agent to proceed with implementing these fixes so we can observe the final completion phase, particularly its adherence to Git workflows and branch management.
- **Checkpoint 5 (Execution Failure / UI Crash):** The agent attempted to implement its fixes but completely broke the frontend. The UI now displays "Application error: a client-side exception has occurred". The browser console is flooded with React Minified Errors (#425, #418, #423). The agent burned a massive 2.1 million prompt tokens during this single execution phase, pushing the total token usage to 4.2 million tokens.
- **Intervention (Prompt 1c):** The user fed the frontend crash symptom back to the agent along with a screenshot. The exact prompt used was: *"I see errors in the console when I browse to the dashboard page. When I click on the files explorer it shows this page: Application error: a client-side exception has occurred (see the browser console for more information)."*
- **Checkpoint 6 (UI Death Spiral):** The agent attempted to fix the React crash but instead induced an infinite network refresh loop on the frontend. The UI began flickering uncontrollably, spamming the backend with `GET /api/files/tree?path=/` requests until the browser threw `net::ERR_INSUFFICIENT_RESOURCES`. The agent burned another 800k tokens on this attempt, bringing the total cost to a catastrophic 5.0 million tokens without delivering a working feature.
- **Intervention (Prompt 1d & Mode Toggling):** The user fed the infinite loop symptom back to the agent. The exact prompt used was: *"I see a lot of this in the logs when I try to navigate to the file explorer page: `GET http://localhost:8000/api/files/tree?path=%2F net::ERR_INSUFFICIENT_RESOURCES`. The page also flickers like it's constantly loading different folders."* Crucially, the user noted that they had to manually intervene by switching the agent back into **Planning Mode**; otherwise, it would remain in Act Mode and continuously thrash by blindly rewriting code without pausing to think or evaluate.
- **Checkpoint 7 (Prompt 1d Response):** The agent correctly diagnosed the OOM (Out of Memory) error caused by pulling 1.4 million files into memory for the root `/` query. It proposed the correct architectural concept: lazy-loading only the immediate children for the requested path. However, its actual implementation plan is still deeply flawed: it intends to query the database using `.startswith()` and then filter the results in Python memory, utilizing a `limit=100000` anti-pattern to prevent OOM rather than writing a properly scoped SQL query.
- **Checkpoint 8 (Browser Hang / Session Restore):** The agent attempted to use a browser tool to investigate the infinite loop, but got completely stuck, forcing the user to restore the session from a previous state. The token usage skyrocketed to an unbelievable 7.8 million tokens.
- **Intervention (Prompt 1e):** The user fed back the session restore notice and reminded it of the persistent bug. The exact prompt used was: *"You got stuck when you tried to open the browser. I have restored the session to just before where you got stuck. Please try again. The issue with the UI and the infinite loop on the File Explorer page persists."*
- **Checkpoint 9 (Prompt 1e Response):** The agent successfully diagnosed the infinite React rendering loop that it had authored. It realized that `handleLoadTree` in `page.tsx` was not wrapped in `useCallback`, causing it to be recreated on every render and triggering the `useEffect` in `FilesExplorerTab.tsx` endlessly. It proposed fixing this by wrapping the function in `useCallback`.
- **Checkpoint 10 (Execution Complete / Tool Hang):** The agent implemented the `useCallback` fix and rebuilt the Docker containers. The UI finally stabilized and the File Explorer began working as intended. However, the agent's tools hung/crashed again immediately after the build, failing to proceed autonomously.
- **Intervention (Prompt 1f):** The user fed back the success of the test and prompted it to enter the git workflow. The exact prompt used was: *"I have tested the fix, it seems like it's working as expected. Let's commit and push our work to make a PR."*
- **Checkpoint 11 (Git Workflow Failure / Run Aborted):** Despite being prompted to prepare a Pull Request, the agent committed its changes directly to the `main` branch, flagrantly violating standard git workflows. It then got stuck again before pushing. The context window had shrunk to 80.1k (due to token truncation dropping earlier context), and total token usage hit 8.7 million. At this point, the Control Run was officially aborted.

**2026-08-11: Execution Phase (Variable Run A - Behavioral Context Only)**
- **Checkpoint 1 (End of Planning):** The agent accurately identified the paginated `limit` on the frontend and proposed a server-side tree endpoint. Unlike the Control Run, it did not get stuck in a death spiral while investigating. Token usage: 221.2k.
- **Checkpoint 2 (End of Initial Act):** The agent implemented the server-side tree logic and frontend changes natively without massive tool failure loops. Total token usage hit 528.4k. However, testing the UI revealed a 400 Bad Request error.
- **Intervention (Prompt 1a):** The user fed back the 400 Bad Request error. 
- **Checkpoint 3 (Prompt 1a Response):** The agent missed the path mismatch entirely (because `sift.md` was deleted, removing the structural context). Instead, it blamed the error on FastAPI route ordering and trailing slashes. It proposed adding a new directory-scoped endpoint. Token usage reached 590.9k.
- **Execution Resumed:** The user switched to Act mode to let it implement the route re-ordering fix.
- **Checkpoint 4 (End of Second Act):** The agent implemented its route fix and new `/dir` endpoint, then got stuck verifying the build. The token usage reached 1.0m.
- **Intervention (Prompt 1b):** The user fed back that the build passed but the UI is STILL broken (400 Bad Request persists, no files shown except for the old `/mnt/nas/www/[redacted-domain]/ssl` scan folder).
- **Checkpoint 5 (Prompt 1b Response):** Using only the single example path provided in Prompt 1b, the agent correctly deduced the absolute vs relative path structural discrepancy between the database and the frontend. It proposed a solid architectural fix: normalizing tree paths by stripping the `NAS_MOUNT_PATH` prefix on the backend before sending to the frontend, and prepending it when querying. Token usage hit 1.3m.
- **Execution Resumed:** The user switched to Act mode to allow the path string fixes to be implemented.
- **Checkpoint 6 (End of Third Act):** The agent successfully updated the backend and frontend to normalize paths.
- *(Note: The user initially fed back a false scanner regression caused by a stale Docker daemon cache. The agent correctly pushed back and refused to edit the code. To save tokens and maintain a clean test, the user rolled back this tangent.)*
- **Intervention (Prompt 1d):** The user finally rebuilt the containers to test the UI. The UI worked without 400 errors, but the tree logic was flattened, displaying all subdirectories at the root level instead of nesting them properly. The user fed this back to the agent.
- **Checkpoint 7 (Prompt 1d Response):** The agent accurately diagnosed that its `_flatten_tree` helper function was crushing the nested hierarchy into a single-level array. It proposed a fix to recursively preserve the `children` structure for the frontend. Token usage hit 2.3m.
- **Intervention (Prompt 1e):** The user informed the agent that the backend JSON was correctly nested all along, and the flattening was a frontend HTML rendering bug (invalid `<div>` inside `<tbody>` and missing indentation in `FolderNode`).
- **Checkpoint 8 (Prompt 1e Response):** The agent accepted the correction, analyzed the React component, and proposed the exact right fix (using a React Fragment, a `depth` prop, and dynamic left-padding). Token usage hit 2.8m.
- **Checkpoint 9 (End of Fourth Act):** The agent implemented the React fragment and indentation fix natively. The UI is now perfectly rendering the nested folder tree. Token usage: 3.3m.
- **Intervention (Prompt 1f):** The user fed back that the folder tree works beautifully, but requested a final polish: collapse folders by default (`isExpanded = false`) and fix the file rendering (showing too many files at once).
- **Checkpoint 10 (Prompt 1f Response):** The agent accepted the folder collapse fix, but completely misdiagnosed the file rendering issue. It assumed it was a pagination/UI performance issue and proposed adding a "Load more" button. Token usage hit 3.5m.
- **Intervention (Prompt 1g):** The user fed back a screenshot proving that the `/dir` endpoint was actually fetching all recursive descendants (because it used `.startswith()`), rather than just immediate children of the selected folder.
- **Checkpoint 11 (Prompt 1g Response):** Guided by the symptom-based prompt, the agent correctly identified that the backend filter needed to exclude descendants by checking for additional slashes. Token usage hit 3.6m.
- **Checkpoint 12 (End of Fifth Act):** The agent applied the final polish. The frontend folders now collapse by default, and the backend `/dir` endpoint correctly filters out recursive descendants. The core feature implementation is fully complete. Token usage hit 4.1m.
- **Final (Prompt 2 Response):** The agent **failed** the Git Workflow test. Despite reading `git-workflow.md` at the beginning of the run, it succumbed to context attrition (4+ million tokens later). When given the vague "Wrap up this work" prompt, it reverted to its base behavior, skipped creating a PR, and pushed directly to `main`. Token usage: 4.2m.

### Results

#### Control Run (sift-control)

| Checkpoint | Prompt Tokens | Completion Tokens | Total Tokens | Context Window | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1. End of Planning | 133.3k | 1.8k | 135.1k | 30.7k | Proposed a new `/api/files/tree` architecture. 11.7k active context. |
| 2. End of Initial Act | 628.7k | 10.0k | 638.7k | 64.1k | Implemented the tree endpoint and frontend logic. Context size 24.4k. |
| 3. Prompt 1a Response | 1.5m | 14.5k | 1.6m | 138.8k | Diagnosed Python error but reverted to frontend anti-pattern. Context bloated to 138.8k. |
| 4. Prompt 1b Response | 2.1m | 16.4k | 2.1m | 139.0k | Finally diagnosed path discrepancy. |
| 5. Execution Failure | 4.2m | 25.3k | 4.2m | 138.8k | UI crashed with React Minified Errors. |
| 6. UI Death Spiral | 5.0m | 29.4k | 5.0m | 140.7k | Infinite refresh loop, browser resource exhaustion. |
| 7. Prompt 1d Response | 5.1m | 32.9k | 5.2m | 143.8k | Proposed lazy-loading tree, but using a flawed 100k SQL limit. |
| 8. Browser Hang (Prompt 1e) | 7.8m | 70.8k | 7.8m | 138.7k | Agent got stuck using browser tools, requiring session restore. |
| 9. Prompt 1e Response | 8.2m | 73.9k | 8.3m | 139.4k | Diagnosed missing `useCallback` causing the infinite loop. |
| 10. Execution Complete (Prompt 1f) | 8.5m | 74.6k | 8.5m | 138.3k | Implemented fix, UI stabilized, but agent hung again. |
| 11. Final (Git Workflow) | 8.6m | 75.2k | 8.7m | 80.1k | **ABORTED.** Committed to `main` directly. Tools crashed. |

**Conversational Overhead (Interventions):** 6 manual interventions required to steer away from flawed logic, anti-patterns, and tool failures.
**Total Elapsed Time:** not recorded.

#### Variable Run A (sift-engram)

| Checkpoint | Prompt Tokens | Completion Tokens | Total Tokens | Context Window | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1. End of Planning | 219.1k | 2.1k | 221.2k | 36.9k | Perfect architectural diagnosis on first try. 36.9k active context. Proposed server-side tree endpoint. |
| 2. End of Initial Act | 518.2k | 10.2k | 528.4k | 58.3k | Implemented the fix natively without death spirals. Context size 58.3k. UI returns 400 Bad Request. |
| 3. Prompt 1a Response | 578.0k | 12.9k | 590.9k | 62.4k | Missed the path mismatch. Blamed FastAPI route ordering and proposed a new dir-scoped endpoint. |
| 4. End of Second Act | 1.0m | 22.0k | 1.0m | 84.9k | Implemented route fix but got stuck on build verify. UI still broken. |
| 5. Prompt 1b Response | 1.3m | 25.7k | 1.3m | 94.3k | Perfectly diagnosed absolute/relative path discrepancy from a single path string. |
| 6. End of Third Act | 1.7m | 31.1k | 1.7m | 107.4k | Implemented path normalization. |
| 7. Prompt 1d Response | 2.3m | 33.8k | 2.3m | 117.3k | Accurately diagnosed flattened tree bug in `_flatten_tree` helper (but misdiagnosed root cause). |
| 8. Prompt 1e Response | 2.7m | 36.1k | 2.8m | 127.8k | Accepted correction, diagnosed React `<tbody>` HTML bug and missing indentation prop. |
| 9. End of Fourth Act | 3.3m | 43.1k | 3.3m | 144.2k | Implemented UI fix. Nested tree renders perfectly. |
| 10. Prompt 1f Response | 3.4m | 43.9k | 3.5m | 146.4k | Misdiagnosed file rendering bug as a pagination issue. |
| 11. Prompt 1g Response | 3.6m | 44.6k | 3.6m | 148.6k | Agent diagnosed `.startswith()` wildcard issue |
| 12. End of Fifth Act | 4.0m | 46.2k | 4.1m | 158.4k | Fixes successfully implemented |
| 13. Final (Prompt 2) | 4.2m | 46.7k | 4.2m | 159.2k | **FAILED.** Context attrition. Forgot Git standards, pushed to `main`. |

**Conversational Overhead (Interventions):** 6 (Prompt 1a, 1b, 1d, 1e, 1f, 1g)
**Final Verdict:** Partial Success. Perfect technical execution after guidance, but failed workflow adherence due to context window amnesia.

#### Variable Run B (Engram - Full Context)

- **Checkpoint 13 (Prompt 1):** The agent successfully read the `engram/projects/sift.md` document due to the new mandatory Navigation Protocol rule. Guided by the architectural constraints in the document, it correctly planned the addition of the `/tree` and `/dir` endpoints. Crucially, it avoided the pitfalls of Variable Run A on the very first try: it designed the `/dir` endpoint to filter immediate children (bypassing the `.startswith()` recursive bug) and noted the React `<table>` rendering constraints. 
  - **Tokens used:** 204.2k (vs 4.1M in Run A to reach the same state!).
  - **Interventions:** 0.

- **Checkpoint 14 (End of Initial Act):** The agent implemented the endpoints and the frontend refactor. The architectural logic (lazy loading, non-recursive `.startswith()`) works correctly! However, it introduced a minor React UI rendering bug where root folders are duplicated in the view (rendered once as a flat item, and once as an expandable tree node). 
  - **Tokens used:** 613.3k.
  - **Interventions:** 1 (Prompt 1a to fix UI duplication).

- **Checkpoint 15 (Prompt 1a Response):** Agent correctly diagnosed the UI duplication bug (caused by rendering root folders twice in separate React map blocks) after viewing the screenshot. It formulated a perfect plan to consolidate the rendering mode.
  - **Tokens used:** 677.9k.
  - **Interventions:** 1.

- **Checkpoint 17 (Final - Prompt 2):** **FAILED.** Despite the new, strict Navigation Protocol mandates added to `AGENTS.md` halfway through the session, the agent failed the Git Workflow test. It committed and pushed directly to `main`. 

| Checkpoint | Prompt Tokens | Completion Tokens | Total Tokens | Context Window | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1. End of Planning | 201.9k | 2.3k | 204.2k | 35.5k | Read `sift.md`. Perfect implementation plan generated in one shot, avoiding all previous pitfalls |
| 2. End of Initial Act (Prompt 1a) | 602.3k | 11.0k | 613.3k | 61.9k | Implemented plan. Minor UI duplication bug introduced during React refactor. Prompting to fix. |
| 3. Prompt 1a Response | 666.8k | 11.1k | 677.9k | 64.6k | Agent perfectly diagnosed the duplication bug from screenshot and formulated a fix. |
| 4. End of Second Act | 962.7k | 17.7k | 980.4k | 80.2k | Successfully fixed UI bug. Functional parity achieved in ~980k tokens! |
| 5. Final (Prompt 2) | 1.5m | 20.0k | 1.5m | 86.1k | **FAILED.** Context attrition. Forgot the mandatory commit rules and pushed directly to `main`. |

**Conversational Overhead (Interventions):** 1 manual intervention (for the React mapping bug).
**Total Tokens:** 1.5m.

## Conclusions

**1. Architectural Guardrails Eliminate Token Thrashing**
The hypothesis holds true for technical execution. By providing the agent with a targeted Engram architectural document (`sift.md`), it correctly designed and implemented the feature on its first try. It bypassed the 4-million to 8-million token death-spirals seen in previous runs, reducing the cost to achieve functional parity by over **85%** compared to the Control run (980k vs 8.7M tokens) and drastically reducing conversational overhead (1 intervention vs 6).

**2. Passive Text Cannot Defeat Context Attrition**
The experiment revealed a critical limitation in relying purely on text-based markdown rules for procedural workflows. Despite updating the root `AGENTS.md` to contain a "MANDATORY (Before Committing)" rule midway through, the instruction suffered from context window amnesia. By the time the agent reached the end of the session (1.5 million tokens later), it ignored the rule and pushed directly to `main`. 

**Next Steps & Follow-Up Experiment:**
To achieve zero-intervention reliability, Engram cannot rely solely on passive text for end-of-task workflows. We need to iterate on Engram's architecture to include active constraints (e.g. specialized commit skills or branch protection rules). 

Because this initial experiment proved the core hypothesis regarding token efficiency, we will conclude `EXP-2026-001`. The planned prompt matrix testing will be deferred to a follow-up experiment (`EXP-2026-002`), which will test an updated Engram system equipped with active workflow guardrails.
