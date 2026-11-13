---
status: current
created: 2026-08-08
updated: 2026-11-11
tags: [standards, coding, error-handling, quality, fallbacks]
---

# Error Handling Standard

> **Errors should be surfaced early, handled explicitly, and rendered actionably.**
> 
> A robust codebase distinguishes between expected domain failures (e.g. invalid user input, missing file) and unexpected infrastructure faults (e.g. DB connection dropped, service offline).

---

## Core Error Handling Rules

### 1. Fail Loudly & Validate Boundaries
- Validate inputs at system boundaries (API endpoints, file paths, external service responses).
- Surface errors immediately where they occur rather than letting corrupted state flow downstream.

### 2. Handle Specific Exceptions
- Catch specific, typed exceptions that you can recover from actionably.
- If you must catch a broad exception at a system boundary (e.g., a top-level job runner), ensure it is explicitly logged and the application gracefully degrades or restarts.

### 3. Actionable Messages
- Error messages must explain **what broke** and, when possible, **how to fix it**.
- Avoid generic errors like `"Something went wrong"`.

### 4. Preserve System Contracts
- Never fix test or runtime failures by returning dummy fallback data (e.g. empty 0-byte arrays) or commenting out assertions. Fix the root cause.

---

## Fallbacks: Substitute, Push On, or Fail

A fallback replaces a missing input with another value, or a failed path with another way of
working. Some keep the system faithful to reality; others let it carry on blind. Decide each one
with two questions.

### 5. Is the substitute the same fact?

- **Acceptable**: another source for the same quantity whose age is known and checked, e.g. a REST
  read of a value a stream normally supplies, or the upstream system's own record before a local
  estimate.
- **Not acceptable**: a different quantity (the quantity requested standing in for the quantity delivered), a
  value of unknown age, or a default that looks like data (`0`, `0.0`, `1.0`, `[]`, `{}`,
  `"neutral"`). Unknown is `None`/`null`, and stays distinguishable from every real value through to
  where it is used or shown.

### 6. Which way does the action move risk?

Risk is the harm if the action is wrong: money, data, safety. With an input unknown:

| The action                                                         | Then                                                                                                            |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| Adds risk (spending, sending, writing, deleting, loosening a guard) | **Fail**: refuse, naming the missing input.                                                                     |
| Removes risk or is owed (cancelling, refunding, a safety stop)     | **Push on** with the best substitute, and record it and its source. Never block a risk-reducing action on a missing input.     |
| An optional check                                                  | **Skip and record**, only if a later check fails closed on the same risk. Otherwise fail.                      |
| A display, report or telemetry value                               | **Show unknown**: null, "—", a stale banner. Never a substitute.                                                |
| Hit a transient fault (timeout, connection drop)                   | **Retry**, bounded, then one of the rows above.                                                                 |

### 7. Every fallback is visible afterwards

- Where it fires, it logs at WARNING or above with what was missing and what was used.
- If the result is persisted, the row says so: the substitute's source, or the rule that was skipped
  and why. A fallback nobody can see after the fact is a silent bug.

### 8. What "fail loudly" means

- Raise a typed error that names what is missing and why it matters. The caller decides whether it
  can recover.
- Where no caller can recover, log at ERROR or alert; a human must be able to find out.
- Never swallow: no `except Exception: pass`, no `except` that returns a default.

### 9. Anti-patterns

- `a or b or c` chains across different quantities or freshness, ordered by habit rather than by
  fidelity.
- `x or 0` with a later `if x == 0` as the "unknown" test: the sentinel can collide with a real zero.
- `.get(key, default)` where the default is a plausible value.
- A gate whose input is missing silently passing the action it was meant to guard.
