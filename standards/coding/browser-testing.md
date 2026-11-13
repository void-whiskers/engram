---
status: current
created: 2026-09-11
updated: 2026-11-11
tags: [standards, coding, testing, browser, playwright, e2e]
---

# Browser & E2E Testing Standard

> **"Test what you want, not what you have."**
>
> End-to-end and browser tests verify the user-facing contract of the application. They are not merely regression catches—they serve as executable specifications for layout confirmation, navigation flow, error resilience, and business invariants.

---

## 1. Core Principles

1. **Appropriate over Passing**: A test is only valuable if it fails when something genuinely breaks. Assert domain rules and visual invariants (e.g. data precision, status indicators, error banners), not fragile static snapshots or trivial container renders.
2. **Hermetic by Default in CI**: Continuous integration browser tests must **never** depend on external third-party services (e.g. payment gateways, partner APIs, LLM endpoints) or volatile shared database states. All network interactions must be intercepted and fulfilled deterministically at the boundary.
3. **Auto-Waiting over Arbitrary Delays**: Never use `page.waitForTimeout()`, `time.sleep()`, or arbitrary delay loops. Rely exclusively on web-first auto-waiting assertions (`toBeVisible()`, `toHaveCount()`, `toHaveText()`). Tests must execute as fast as the DOM can render.
4. **Accessible, User-Centric Locators**: Query elements the way a human or assistive technology interacts with them:
   - Prefer: `page.getByRole('button', { name: /save/i })`, `page.getByPlaceholder(...)`, `page.getByText(...)`.
   - Avoid: Brittle CSS selectors (`div > div.col-span-2 > p.text-xs`), dynamic test IDs, or framework-generated class chains.
5. **Cold-Boot & Defensive Hydration Testing**: APIs may boot empty or experience network hiccups. Every suite must assert that the frontend handles unpopulated telemetry or HTTP 500 responses gracefully (displaying clear error banners or empty states rather than crashing or flashing `NaN`).

---

## 2. Test Suite Architecture (Dual-Track Model)

Browser testing is split into two distinct tracks:

| Track | Scope | Network Layer | Frequency | CI Target |
| :--- | :--- | :--- | :--- | :--- |
| **Track 1: Hermetic UI Specs** | Layout, routing, domain formatting, error handling | Mocked via `page.route` / fixtures | Every PR (`make check`) | Yes |
| **Track 2: Live Integration / Smoke** | Full-stack auth, live third-party APIs, DB transactions | Real backend & third-party sandboxes | Staging / Pre-deployment | Gated / Manual |

Track 1 tests provide fast feedback (< 30 seconds for full suites) and 100% determinism with zero external API key requirements.

---

## 3. Fixture & Network Interception Patterns

### Centralized Mock Fixtures
Store synthetic domain fixtures in dedicated mock modules (e.g. `fixtures/mockData.js`). Fixtures should represent realistic domain states:
- Boundary conditions (empty lists, maximum balances, extreme values).
- Realistic entity models (open orders, flagged items, telemetry stats).

### Base Test Interceptor
Create a customized base test fixture (e.g. `baseTest.js` extending Playwright's `test`) that automatically sets up network routes before each test runs:

```javascript
import { test as base, expect } from '@playwright/test';
import { mockBalances, mockOrders } from './mockData.js';

export const test = base.extend({
  page: async ({ page }, use) => {
    // Intercept API routes at the network boundary
    await page.route('**/api/v1/balance', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockBalances),
      });
    });

    await page.route('**/api/v1/orders', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockOrders),
      });
    });

    await use(page);
  },
});

export { expect };
```

Individual tests can override specific routes to simulate errors or alternative scenarios:

```javascript
test('displays error banner when balance endpoint fails', async ({ page }) => {
  await page.route('**/api/v1/balance', route => route.fulfill({ status: 500 }));
  await page.goto('/');
  await expect(page.getByText(/Failed to fetch balance/i)).toBeVisible();
});
```

---

## 4. Domain Invariant Assertions

Browser tests must actively verify domain rules rather than superficial renders:

1. **Sub-Penny & Numeric Precision**:
   - Financial and scientific systems handle numbers spanning orders of magnitude (from \$100,000 to \$0.00001234).
   - Assert that formatted values do not truncate decimals to `$0.00` or introduce floating-point artifacts (`0.000012340000001`).
2. **Business Rule Transparency**:
   - Verify that conditional domain badges (e.g. `SANDBOX`, `FLAGGED`, `PENDING`) render with accurate context.
   - For flagged or filtered items, assert that opening the detail drawer surfaces the specific reason the item was flagged.
3. **Responsive Viewport Invariants**:
   - Verify that primary navigation and triage controls adapt cleanly without overlapping or hiding critical actions across standard viewports (Desktop 1440x900, Tablet, Mobile).

---

## 5. Containerization & Security

All browser test suites must be fully runnable inside Docker containers to ensure identical behavior between local developer environments and CI runners:

- **Non-Root Execution**: Container images must specify a non-root user (e.g. `USER pwuser` in Playwright Docker images) to satisfy container security scans (Checkov, Trivy).
- **Filesystem Permissions**: When bind-mounting artifact directories (test reports, screenshots, videos) on host Linux systems, configure user mappings (`user: "0:0"` in Docker Compose runner profiles if needed) so the container can write artifacts without permission denials.
- **Universal Task Integration**: Wrap test runs in repository task runners (e.g. `make test-e2e` and `make test-e2e-report`) so that developers and CI agents do not need to memorize ad-hoc flags.
