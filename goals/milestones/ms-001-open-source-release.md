---
status: active
created: 2026-08-28
updated: 2026-11-13
tags: [goals, milestone, release, open-source, engram]
---

# MS-001: Engram Open Source Release

**Target Date**: Not set (the original target, August 2026, passed before release)  
**Status**: Active (Final Pre-Launch Verification)

---

## Objective

Prepare, benchmark, and release Engram as an open-source, zero-dependency, hierarchical persistent memory architecture for autonomous AI coding agents.

---

## Pre-Launch Checklist

### 1. Research & Empirical Validation
- [x] Run 5 exploratory experiments on Sift (`EXP-2026-001` through `EXP-2026-005`).
- [x] Check the direction of the findings across local (Qwen 3.6 35b, Qwen 3.8 27b) and frontier cloud models (DeepSeek V4 Flash, Poolside Laguna S-2.1).
- [x] Author the whitepaper as a pilot study (`WHITEPAPER.md`).
- [x] Review whitepaper against the four-pillar checklist of the Communication Standard (`review-document`).

### 2. Repository Hygiene & Structure
- [x] Clean, navigable B-Tree navigation root in `AGENTS.md` (≤ 3 hops).
- [x] Synchronized master and domain indexes (`experiments/INDEX.md`, `standards/INDEX.md`, etc.).
- [x] Include historical example experiments (`1801/`, `1971/`) and sample future experiments.
- [x] Exclude private and proprietary project data.
- [x] Provide standard coding, testing, and automation guidelines (`standards/coding/automation.md`).

### 3. Open Source & Community Standards
- [x] `LICENSE` (MIT).
- [x] `CODE_OF_CONDUCT.md` & `CONTRIBUTING.md`.
- [x] `.github/` pull request and issue templates.
- [x] Generalize all skill instructions and scripts (remove machine-specific absolute paths).

### 4. Tooling & Integrity
- [x] Zero validation errors from automated integrity validator (`validate.sh`).
- [x] All internal relative links resolve.
- [x] Frontmatter compliance across all leaf documents.

---

## Success Criteria

1. `validate.sh` passes with 0 errors and 0 warnings.
2. `WHITEPAPER.md` reports the pilot results (36–83% fewer tokens with Engram than without, from single runs) and states the limits of the evidence.
3. Clean repository clone ready for public distribution and mirroring.
