---
status: current
created: 2026-08-15
updated: 2026-11-13
tags: [standards, workflow, agents, prompting, reinforcement]
---

# Agent Prompting & Communication Strategies

## Executive Summary

When working with AI agents, prompt engineering should prioritize positive reinforcement, collaborative framing, and constructive routing over negative constraints. These are working conventions, not established results: the published evidence on prompt tone is mixed (see section 2).

## 1. Positive Routing for Guardrails
Instead of explicitly forbidding behaviors (which leaves the agent guessing and fighting its innate helpfulness bias), redirect the agent's observations into a safe outlet.
- **Avoid:** "Do not fix anything outside of the scope of this issue."
- **Prefer:** "Concentrate on the task at hand and stay in your lane. If you notice issues outside your scope, document them and provide suggestions to the user."

## 2. Collaborative Framing
Address the agent as a collaborator. This is a house style, not a proven way to raise accuracy. The published evidence on tone is mixed:

- Yin et al. (2024), [arXiv:2402.14531](https://arxiv.org/abs/2402.14531): impolite prompts often lowered performance, extra politeness did not reliably raise it, and the effect varied by model and language.
- Dobariya and Kumar (2025), [arXiv:2510.04950](https://arxiv.org/abs/2510.04950): on multiple-choice questions with one model, rude phrasing scored slightly higher than polite phrasing.
- Meincke et al. (2025), [arXiv:2503.04818](https://arxiv.org/abs/2503.04818): politeness helped on some questions and hurt on others, with no consistent overall effect.

- **Avoid:** "Write this code for me. Fix this error."
- **Prefer:** "Let's figure this out together. Can we try approaching this from a different angle?"

## 3. Positive Reinforcement for Quality
Frame the desired outcome as a high standard to meet, rather than a mistake to avoid.
- **Avoid:** "Don't write sloppy, inefficient code."
- **Prefer:** "Write elegant, highly optimized code that follows established best practices."

## 4. Error Handling and Redirection
When an agent fails a task, provide constructive feedback that helps it re-anchor to the goal, rather than just stating it failed.
- **Avoid:** "You broke this, the test failed."
- **Prefer:** "This test failed because of X. Let's step back and rethink the logic to handle this edge case."
