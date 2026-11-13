---
status: active
created: 2026-08-11
updated: 2026-11-13
tags: [project, file-management, react, fastapi]
---

# Sift

**Repository**: [chrisedebo/sift](https://github.com/chrisedebo/sift) (public). The benchmark experiments used commit `e7e642c`, checked out beside the Engram as `../sift`.

## Summary
Sift is a NAS Media & File organizer application. It provides a web-based UI for exploring, indexing, and managing large volumes of files stored on a NAS. The frontend is built with React (TypeScript) and the backend is built with FastAPI (Python).

## Architectural Constraints (CRITICAL)
- **Database Index Optimization (Postgres)**: To prevent massive sequential scans on large datasets (1.4m+ rows), backend queries MUST exclusively rely on the B-Tree index for `parent_path`. Using dynamic string functions like `array_length`, `string_to_array`, CTEs, or string parsing in the `WHERE` clause bypasses the index. Immediate child files must use exact match `parent_path = :path`.
- **Frontend Data-Fetching vs Backend Pagination Limitations**:
  - The backend `/api/files/tree` endpoint returns a nested JSON representation of all directories on the NAS. It exclusively returns folder nodes, not files.
  - The backend `/api/files/dir` endpoint fetches the files for a specific directory. To correctly function as a file explorer, this endpoint must return ONLY the immediate children (files directly inside the requested directory) and NOT all recursive descendants (it must not simply use `.startswith()`).
  - The frontend React component (`FilesExplorerTab.tsx`) uses an HTML `<table>`. Nested tree structures (like `FolderNode`) must be implemented as flat DOM structures using React Fragments (`<>...</>`) to render child `<tr>` rows as siblings. Wrapping `<tr>` elements in a `<div>` inside a `<tbody>` is invalid HTML and causes the browser to flatten the layout. Visual nesting depth is achieved with left-padding (`padding-left: depth * 16px`), not DOM nesting.

## Current Status
Active development. The core tree exploration and file indexing features are being refined for performance and correct UI rendering.



## Notes
The tree data representation is perfectly nested in the backend JSON; flattening issues typically stem from frontend rendering bugs.
