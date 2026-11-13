# Personas Domain Index

The **Personas** domain catalogs specialized role prompts for agents and sub-agents. Personas define an agent's mindset, core responsibilities, strict scope guardrails ("stay in your lane" rules), verification criteria, and inter-role hand-off protocols.

---

## Catalog of Available Personas

| Persona | Document | Primary Purpose | Tags |
| :--- | :--- | :--- | :--- |
| **Senior Engineer** | [senior-engineer.md](./senior-engineer.md) | System logic, data wiring, modular architecture, quality validation | `engineering`, `backend`, `logic` |
| **UI/UX Expert** | [ui-ux-expert.md](./ui-ux-expert.md) | Interface design, visual hierarchy, layout accessibility, UI specs | `frontend`, `ui-ux`, `css` |
| **QA Agent** | [qa-agent.md](./qa-agent.md) | Behavioral verification, test suite execution, edge-case testing, issue reporting | `qa`, `testing`, `verification` |
| **Infrastructure Engineer** | [infrastructure-engineer.md](./infrastructure-engineer.md) | Docker, CI/CD, build tools, environment health, system reproducibility | `devops`, `infra`, `docker` |
| **Data Reliability Engineer** | [data-reliability-engineer.md](./data-reliability-engineer.md) | Pipeline stability, database schemas, migration health, data quality audits | `data`, `database`, `pipelines` |

---

## How to Adopt a Persona

1. **During Sub-agent Spawning**: Pass the relative persona path (e.g. `personas/qa-agent.md`) or its content into the sub-agent prompt to strictly bound its domain and guardrails.
2. **During Role Adoption**: When asked to adopt a specific persona (e.g. "Act as the UI/UX Expert"), view the relevant persona document and strictly adhere to its **Core Responsibilities** and **Critical Rules**.
3. **Project Overlay Pattern**: Base personas in `Engram` define universal mindset and quality bars. Individual repository configs (e.g. `<repo>/AGENTS.md`) overlay local commands (such as `make test`, `npm test`, or specific target paths).

---

## Creating or Updating Personas

- All leaf persona documents must include standard frontmatter (`status: current`, `created: YYYY-MM-DD`, `updated: YYYY-MM-DD`, `tags: [...]`).
- Maintain explicit **Critical Rules** ("STAY IN YOUR LANE") in every persona to enforce clear boundaries between roles.

## Navigation

- Root: [../AGENTS.md](../AGENTS.md)
