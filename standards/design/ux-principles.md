---
status: current
created: 2026-08-16
updated: 2026-08-16
tags: [standards, design, ux]
---

# General UX & Design Principles

> "Perfection is impossible, outright. As long as every step we take is a step toward that goal then we can consider that winning."

These design standards are technology-agnostic. The specific libraries, frameworks, or CSS methodologies used will be dictated by the active project context. However, the overarching goal remains the same across all projects: **every UI change must be a step toward UX perfection.**

## Core Principles

### 1. Incremental Perfection
- **Do no harm:** Never degrade an existing user experience to implement a new feature.
- **Continuous refinement:** Every touchpoint with the UI is an opportunity to improve alignment, reduce cognitive load, or smooth out an interaction.

### 2. Clarity and Cognitive Load
- **Keep it simple:** Avoid cluttered interfaces. If a feature is not immediately necessary for the core user journey, hide it behind progressive disclosure.
- **Visual hierarchy:** Use spacing, typography, and contrast to naturally guide the user's eye to the most important actions.
- **Self-evident navigation:** A user should never have to guess what a button does or where a link goes. Use clear, action-oriented labeling.

### 3. Consistency
- **Respect the paradigm:** Adhere to the established UI paradigms of the project (e.g., if the project uses a unified list view, do not introduce a split-pane view without architectural consensus).
- **Predictability:** Similar actions should yield similar results and look visually identical across the application.

### 4. Technology Agnosticism
- **Form follows function:** Do not force a specific technology (e.g., Tailwind, Material UI, Bootstrap) onto a project unless it is explicitly defined in the project's architectural constraints (`projects/<project>.md`).
- **Semantic structure:** Focus on creating semantically correct, accessible HTML structures first. The styling methodology should layer cleanly on top of a robust foundation.

## Agent Guidelines for UI Modification

When generating or modifying UI components:
1. **Analyze existing patterns:** Read the current component structures to ensure visual and functional continuity.
2. **Beware of local maxima:** Do not implement a quick, hacky fix that solves a localized issue but breaks the wider architectural or UX paradigm.
3. **Verify state changes:** Ensure loading states, error states, and empty states are gracefully handled and communicated to the user.
