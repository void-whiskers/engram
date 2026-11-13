---
status: concluded
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
# supersedes: experiments/future/future-NNN-slug.md   # uncomment if this was a planned experiment
---

# EXP-YYYY-NNN: <Title>

<!-- Copy this template when creating a new experiment. Remove all HTML comments before saving. -->
<!-- File naming: exp-YYYY-NNN-<slug>.md  e.g. exp-2026-001-rag-vs-finetune-accuracy.md -->

## Hypothesis

What did we believe or expect before running this experiment? Be specific — a good hypothesis is falsifiable.

## Method

What did we do? How did we measure or test the hypothesis? This must follow a strict 5-step methodology:

1. **Test Environment Preparation:** Detail the exact setup (environments, models, repositories, branches).
2. **Data Collection Checkpoints:** Define exactly *what* data will be captured and *when* during the workflow it will be recorded.
3. **Control Run (Baseline):** Step-by-step execution details for the baseline run, including prompts used and where data is collected.
4. **Variable Run (Experiment):** Step-by-step execution details for the experimental run, highlighting the exact independent variables altered from the control.
5. **Analysis:** The statistical or comparative method used to evaluate the recorded data against the hypothesis.

## Results

Raw findings, data, and observations. Include numbers, outputs, and unexpected observations.

> If results are large (e.g. logs, datasets), reference external files or links here rather than embedding.

## Methodological Notes

<!-- Required by the experimentation standard. See standards/workflow/experimentation.md -->

Document acknowledged limitations, scope of claims, and discoveries made during execution:

- **Limitations:** Sample size, confounds, environmental constraints.
- **Mid-Experiment Discoveries:** Things that turned out to be findings rather than flaws.
- **Scope of Claims:** What the data supports vs. what it does not.

## Conclusions

What does this mean? Did the results confirm or deny the hypothesis?

- What changed in our mental model?
- What would we do differently?
- What follow-up questions does this raise?

## Impact

What did we change as a result of this experiment?

- [ ] Updated standards: *(link if applicable)*
- [ ] Added/updated knowledge: *(link if applicable)*
- [ ] Created follow-up future experiment: *(link if applicable)*
- [ ] No downstream changes required
