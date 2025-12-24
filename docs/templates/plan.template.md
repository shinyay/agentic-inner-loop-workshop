# Implementation Plan

> Copy this template into `docs/plan.md` and fill it in.
> The plan is allowed to change as you learn.

## 1. Milestones

Example:

- M0: Baseline CLI + schema + tests (deterministic)
- M1: Prompt/agent baseline evaluation (probabilistic)
- M2: Improve prompt/agent based on failures (loop)
- M3: Polish and documentation

## 2. Work breakdown

Break work into issues (0.5–2 hours each).

For each task, include:

- Problem statement
- Definition of Done (DoD)
- Validation command(s)
- Dependencies

## 3. Testing strategy

- Unit tests: `pytest -q`
- CLI tests: ensure JSON output is stable
- Contract tests: validate schema and error handling

## 4. Evaluation strategy

- AI Toolkit:
  - dataset: `datasets/triage_dataset.csv`
  - baseline version
  - metric(s): type/priority accuracy, label overlap
- Record outcomes in `reports/eval/`

## 5. Risks and mitigations

List the top 3–5 risks and how you will reduce them.

## 6. Timebox

What is “good enough” for the workshop duration?
