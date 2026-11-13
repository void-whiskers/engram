---
status: current
created: 2026-08-04
updated: 2026-11-11
tags: [standards, coding, testing, quality]
---

# Testing Standard

> **The definition of done includes two conditions, in order of importance:**
>
> 1. The tests are appropriate.
> 2. The tests pass.
>
> A suite of passing but meaningless tests is worse than no tests — it creates false confidence while hiding real problems. Appropriate tests that fail are honest and actionable.

---

## What Makes a Test "Appropriate"

A test is appropriate if:

- It would **catch a real bug** if the implementation were wrong in a plausible way
- It tests **behaviour, not implementation** — it survives a correct refactor without modification
- It is **readable as a specification** — someone unfamiliar with the code can understand what it's asserting and why
- It **fails for the right reason** — the failure message points to the actual problem
- It tests **one logical thing** — a failure tells you precisely what broke

A test is *not* appropriate if:

- It would pass even if the implementation were **completely wrong**
- It tests that mocks return what you told them to return (testing your test doubles, not your code)
- It is tightly coupled to implementation details and **breaks on refactors that preserve behaviour**
- It only exercises the **happy path** for code that has meaningful error conditions
- It is a **snapshot/golden file test** applied to volatile output without deliberate intent
- It passes because the assertion is **too weak** (e.g. asserting a list is non-empty rather than asserting its contents)

---

## Test Quality Signals

### Green flags — tests that are earning their keep

- The test would fail if you deleted the code under test
- The test would fail if you introduced a specific, realistic bug
- The test name reads as a statement of behaviour: *"returns empty list when no items match the filter"*
- The test exercises a **boundary condition** (empty input, max value, concurrent access, network failure)
- The test is short enough to read in one sitting and requires no knowledge of the implementation

### Red flags — tests that are lying to you

- The test asserts `assert result is not None` for a function that always returns something
- The test mocks every collaborator and only checks that methods were called in a specific order
- Changing the test requires reading the implementation to understand what changed
- The test passes when you comment out the core logic
- The test name says *"test_create_user"* rather than *"raises ValueError when email is already registered"*
- 100% line coverage with 0% confidence anything actually works

---

## The Coverage Trap

Code coverage measures which lines were **executed**, not which behaviours were **verified**. It is a useful tool for finding untested code paths, but it is not a quality metric.

A codebase can have:

- 100% coverage with no meaningful assertions — every line runs, nothing is checked
- 60% coverage with highly valuable tests — the critical paths are thoroughly exercised

**Do not use coverage targets as a proxy for test quality.** Use coverage as a signal of *where to look*, not as a measure of *how good the tests are*.

---

## What to Test

### Always test

- **Boundary conditions**: empty collections, zero values, maximum values, null/None inputs
- **Error paths**: what happens when a dependency fails, input is invalid, or a constraint is violated
- **Business rules**: the logic that makes the software correct for its purpose
- **Integration points**: how components behave when wired together (not just in isolation)

### Test with care

- **Happy paths**: necessary but not sufficient; don't let them crowd out edge cases
- **Internal helpers**: sometimes worth testing directly if complex; otherwise covered by higher-level tests

### Generally avoid

- **Implementation details**: private methods, internal data structures, specific call sequences on mocks
- **Framework and library behaviour**: test your code, not third-party code
- **Trivial getters/setters** with no logic
- **Generated code** that you don't own

---

## Test Structure

Use **Arrange / Act / Assert** (or **Given / When / Then**). Each section should be visually distinct.

```python
def test_returns_error_when_balance_insufficient():
    # Arrange
    account = Account(balance=10.00)

    # Act
    result = account.withdraw(amount=50.00)

    # Assert
    assert result.is_err()
    assert result.error == InsufficientFundsError(available=10.00, requested=50.00)
```

- One logical assertion per test (multiple `assert` statements are fine if they test the same thing)
- Test name describes the **scenario and expected outcome**, not the method name
- No logic in tests (no `if`, `for`, `while`) — if you need logic, write more tests

---

## Test Independence

- Tests must be **order-independent**: each test sets up and tears down its own state
- Tests must be **deterministic**: no reliance on system time, random values, or external services without explicit control
- Tests must be **isolated**: a failure in one test must not cause another to fail
- Synchronize asynchronous state transitions using **explicit polling or condition waits** (e.g., waiting for a database record to appear) to ensure tests run as fast as the system allows.
- Shared fixtures are fine; shared mutable state is not

---

## When Tests and Code Disagree

If a test fails after a code change, there are two possibilities:

1. **The code is wrong** — fix the code
2. **The test is wrong** — fix the test

Before changing a failing test, ask: *"Does this test describe correct behaviour?"* If yes, the code is wrong. If the behaviour genuinely changed intentionally, update the test — but treat this as a deliberate decision, not a reflex.

**Never delete a failing test to make the build pass.** If a test is wrong, understand why and fix it properly.
