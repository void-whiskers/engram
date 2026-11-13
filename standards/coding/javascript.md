---
status: current
created: 2026-09-03
updated: 2026-11-11
tags: [standards, coding, javascript, react, frontend, quality]
---

# JavaScript & Web Frontend Standard

> **"Simple is better."**
>
> Frontend complexity grows exponentially when code is tangled across deeply nested components, unnecessary abstractions, and redundant state. Clean web architecture favors explicit data flow, small focused components, and native platform features over heavy frameworks or premature indirection.

---

## 1. Core Principles

1. **Keep It Simple (KISS & YAGNI)**: Do not introduce global state stores (Redux, Zustand) or complex context providers when standard React hooks (`useState`, `useReducer`, custom hooks) suffice.
2. **Declare Components at Module Scope**: **Never declare a React component inside another component's render function**. Inner components are re-created on every render, resetting internal state, breaking reconciliation, and causing input focus loss.
3. **Derived State Over Synchronized State**: Compute values directly during render or with `useMemo`. Never duplicate props or state into a second `useState` with `useEffect` sync.
4. **Defensive Data Hydration**: Always safely deserialize API data. JSON payloads can arrive as strings, pre-parsed objects, or `null`. Never call `JSON.parse` raw without fallback handling.
5. **Accessibility & Semantic HTML**: Use real semantic elements (`<button>`, `<input>`, `<dialog>`, `<nav>`) with clear `aria-label` or `title` attributes instead of un-styled clickable `<div>` elements.

---

## 2. Component Design & Architecture

### Focused Component Size

- Keep component files focused and concise (aim for under 350–400 lines).
- When a component grows beyond this threshold, extract cohesive sub-components (e.g. drawers, cards, header controls, metric decks) into dedicated files.

### Clean Separation of Concerns

- **Page Container / Smart View**: Orchestrates custom hooks, manages routing params, handles top-level actions.
- **Custom Hook**: Encapsulates data fetching, polling, websocket events, and filter/search business logic.
- **Presentational Component**: Receives typed props, renders UI, emits user events via callbacks (`onApprove`, `onSelect`).

```javascript
// Good: Clear separation
export const ReviewQueue = () => {
  const { filteredItems, activeTab, setActiveTab, handleApprove } = useReviewQueue();

  return (
    <div className="space-y-6">
      <StatusTabBar activeTab={activeTab} onSelectTab={setActiveTab} />
      <TriageTable items={filteredItems} onApprove={handleApprove} />
    </div>
  );
};
```

---

## 3. React Hooks & State Management

### Rule of State Co-location

Keep state as close as possible to the component that consumes it. Only lift state up to the nearest common ancestor when multiple sibling components need coordinated access.

### Avoiding Stale Closures & Dependency Lying

- Always include all reactive values (props, state) referenced inside `useEffect`, `useMemo`, and `useCallback` in the dependency array.
- To prevent unnecessary re-renders or effect re-triggers, use functional state updates:

```javascript
// Good: Does not depend on the previous count value in scope
setCount(prev => prev + 1);
```

### Safe Custom Hooks

Group related async operations, web event listeners, or intervals inside custom hooks. Always ensure cleanup functions are returned:

```javascript
export const useWebSocketFeed = (url) => {
  useEffect(() => {
    const ws = new WebSocket(url);
    ws.onmessage = (event) => { /* handle message */ };
    return () => ws.close(); // Cleanup is mandatory
  }, [url]);
};
```

---

## 4. Defensive Data Hydration & Parsing

APIs (especially with caching layers or serialization layers) can return heterogeneous data shapes. All string parsing must be resilient:

```javascript
// Good: Defensive parser that never throws and handles both objects and strings
export const safelyParseJSON = (raw, fallback = null) => {
  if (!raw) return fallback;
  if (typeof raw === 'object') return raw;
  try {
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
};
```

---

## 5. UI/UX, Styling & Density

- **Design System Consistency**: Use the project's standardized design tokens (e.g. Tailwind theme values) for colors, spacing, and panels rather than one-off values. See the aesthetic profiles in [`standards/design/`](../design/INDEX.md).
- **Dual-Mode Visual Density**: For complex dashboards (operations, telemetry, monitoring), offer a **Compact Triage Mode** (high information density for rapid scanning) alongside a **Deep Dive Card Mode** (rich visual cards with expandable details).
- **Zero Layout Shifts**: Use fixed height placeholders or skeleton loaders (`SkeletonLoader`) during async fetches to prevent visual jarring.

---

## 6. Testing & Quality Standards

- **Behavior Over Implementation**: Test what the user sees and interacts with. Use React Testing Library with accessible queries:

```javascript
// Good: Accessible queries
expect(screen.getByRole('button', { name: /approve/i })).toBeInTheDocument();
```

- **Async State Wrap (`act` & `waitFor`)**: Wrap custom events and async mutations in `act(...)` or assert within `await waitFor(...)` to prevent React state update warnings.
- **Strict Zero-Warning Linting**: All frontend code must pass ESLint with **0 errors and 0 warnings** (`npm run lint`).
