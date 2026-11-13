---
status: current
created: 2026-08-15
updated: 2026-08-15
tags: [standards, workflow, debugging]
---

# Debugging & Verification Standards

## Executive Summary

Debugging is an empirical science. Our process for investigating, isolating, and resolving defects prioritizes hard data over assumptions, and explicit verification over implicit trust.

---

## Core Tenets

### 1. Empirical Evidence over Assumption
Never assume a bug is caused by an environmental issue (e.g., "the database must have been reset", "the cache must be stale", "the dependency must be broken") without verifying it. You must query the raw state of the system to prove your hypothesis before declaring it the root cause.

### 2. A/B State Verification
When fixing a logic flaw—particularly in data transformations, regex matching, or SQL string parsing—explicitly output the "broken" transformation and the "fixed" transformation side-by-side using real data.

For example, when correcting a broken SQL regex, write a diagnostic query that selects both the broken regex result and the new regex result on the same rows to conclusively verify the logic fix before applying it globally.

### 3. Verify the Raw State (Bottom-Up Traversal)
If a symptom appears at the top level of the stack, traverse down to the absolute source of truth to isolate the failure point:
- If a UI is not displaying data, check the API response.
- If the API response is empty, check the database query logs.
- If the query returns nothing, check the raw database tables.

Always verify the raw state at the lowest possible level before assuming the failure lies in the middleware or presentation layer.
