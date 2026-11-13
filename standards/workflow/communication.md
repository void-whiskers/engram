---
status: current
created: 2026-09-14
updated: 2026-11-11
tags: [standards, workflow, communication, documentation, review, quality, token-efficiency]
---

# Communication Standard

> **Every claim an agent makes is code for both humans and other agents to act on.**
>
> This applies to any surface — a chat response, a PR or code review comment, a
> commit message, or a document in your Engram. In each of them,
> a claim must be **factually truthful** (to prevent hallucination and decayed
> assumptions) and **dense** (to avoid wasting the reader's — human or agent's —
> time and, for written documents, future context-window tokens).

---

## Core Principles

1. **High Signal-to-Noise Ratio:** Every sentence must carry semantic weight. Prefer structured tables, bullet points, and code snippets over sprawling narrative prose.
2. **Scientific Objectivity:** Claims must be measurable and falsifiable where possible. Execution logs, summaries, and status updates must record what *actually happened* without presupposition or loaded language (e.g., "observed a React loop" rather than "planned to introduce a bug").
3. **Precision in Claimed Relationships:** Don't describe two values, settings, or facts as "matching," "aligned with," "derived from," or "consistent with" unless that relationship is actually exact or derivable. If the real reasoning is looser or merely directional (e.g. "comfortably above a default, with headroom under an unrelated limit"), state that plainly instead. This is a specific, checkable form of the Scientific Objectivity principle above — reaching for a word that implies more rigor than the reasoning has is itself a form of loaded language, even when nothing else about the claim is false.
4. **Factual Sanity (Anti-Decay):** Never state an architectural assumption, tool, or fact without checking ground truth (e.g., confirming `PostgreSQL` is actually in use before documenting it, not carrying forward a stale `SQLite` assumption).

### Additionally, for written documents (your Engram, or similar)

5. **Structural Hygiene:** Every leaf document must have valid YAML frontmatter, be reachable within 3 hops from `AGENTS.md`, and pass automated structural validation.

---

## Quality Signals

Mainly relevant to written documents, but the underlying habits (dense, falsifiable, accurate, non-redundant) apply just as well to a long PR description or a chat response.

### Green Flags (Communication that earns its keep)

- **Dense & Scannable:** Key points can be extracted in seconds by a human or in a single tool call by an agent.
- **Falsifiable Claims:** Experiments and status claims define concrete metrics (e.g., "10% token reduction", "0% Git violations") rather than vague assertions.
- **Accurate Ground Truth:** Paths, schemas, config flags, and tools match the actual codebase reality.
- **Canonical Linking:** References existing standards or tool docs rather than copy-pasting duplicate definitions.
- **Indexed:** The parent `INDEX.md` contains an accurate, concise one-line summary (documents only).

### Red Flags (Communication that wastes time and misleads)

- **Narrative Fluff:** Conversational storytelling, filler introductions, and redundant summary sections.
- **Stale Assumptions:** Outdated tech stacks, incorrect ports, or phantom filenames left over from earlier drafts.
- **Unverifiable or Overclaimed Relationships:** Vague goals like "make the UI much better," or precise-sounding but unverified claims like "this matches the existing timeout" when it doesn't.
- **Emoji & Formatting Bloat:** Heavy emoji usage (which burns 2–4 tokens per character) and broken markdown formatting.
- **Orphans & Dead Links:** Documents not listed in any `INDEX.md` or containing broken relative links (documents only).

---

## The Review Checklist

When authoring or reviewing a chat response, a PR/code review comment, a commit message, or a document in your Engram, apply this check (pillar 4 applies to documents only):

| Pillar | What to Check |
| :--- | :--- |
| **1. Sense & Objectivity** | Does the logic hold? Are claims measurable, falsifiable, and stated at the precision the underlying reasoning actually supports? Is the tone neutral, factual, and free of loaded or overclaiming phrasing? |
| **2. Information Density** | Can anything be removed without losing meaning? Are concepts formatted as tables/lists instead of long paragraphs? |
| **3. Factual Sanity** | Do mentioned tech stacks, schemas, branch names, and commands reflect the actual project reality? |
| **4. Structure & Links** (documents only) | Does it pass the `validate-memory` checks? Is the YAML frontmatter complete? Is it linked in the parent `INDEX.md`? |
