---
status: current
created: 2026-08-08
updated: 2026-08-08
tags: [standards, coding, logging, observability]
---

# Logging Standard

> **The primary goal of logging is operational visibility without output noise.**
>
> Logs should provide actionable, contextual insight into system events, state transitions, and failures — allowing developers and AI agents to trace behavior cleanly without sifting through redundant boilerplate.

---

## Core Logging Principles

### 1. Shared Ownership & Authority

- These standards are co-owned and maintained in Engram to govern both human and AI agent code generation across all projects.

### 2. High Signal-to-Noise Ratio

- Log key operational milestones (file processing completed, AI categorization finished, dry-run actions executed, external API errors).
- **Avoid Routine Start Logs**: Prohibited for internal helper/module functions. Allowed *only* at major operational boundaries (e.g., incoming HTTP request start, queue job pick-up, or long-running CLI process start).
- Avoid logging inside tight loops for every single item; log batch summaries or aggregate metrics instead.

### 3. Contextual Metadata & Formatting

- **Format by Context**: Use human-readable key-value string formatting (`key=value` or pipe-delimited `|`) for CLI tools/scripts. Use single-line structured JSON for backend services/APIs.
- Always include relevant tracing identifiers (`file_id`, `file_path`, `status_code`, `category`, `duration_ms`).
- **No Heavy Data Dumps**: Never dump massive raw HTTP bodies, full directory trees, or complete database payloads into standard logs. Summarize or log relevant keys instead.

### 4. Severity Levels & Exception Handling

- **`DEBUG`**: Detailed diagnostic info for local development (query params, headers, sub-step transitions).
- **`INFO`**: Key application milestones and operational outcomes.
- **`WARNING`**: Recoverable issues or unexpected edge cases (API retries, cache misses, zero results). Keep context-focused without stack tracebacks.
- **`ERROR`**: Actionable failures requiring developer attention. Reserve full stack tracebacks (`exc_info=True`) strictly for `ERROR` level.

### 5. No Sensitive Information

- Never print API keys, user credentials, JWT tokens, or full private PII in log messages.

---

## Logging Example (Python)

```python
import logging

logger = logging.getLogger("sift.categorizer")

async def categorize_file(file_record):
    try:
        # Actionable result log with context metadata
        logger.info(
            "Categorization completed | file_id=%s category='%s' duration_ms=%d",
            file_record.id, category, elapsed_ms
        )
    except Exception as e:
        # Actionable failure with full stack traceback
        logger.error(
            "Categorization failed | file_id=%s path='%s' error='%s'",
            file_record.id, file_record.file_path, str(e), exc_info=True
        )
```
