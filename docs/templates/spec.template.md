# Spec: Issue Triage Assistant

> Copy this template into `docs/spec.md` and fill it in.
> Keep the spec short enough that it can be read in ~5 minutes.

## 1. Problem statement

Describe the problem this project solves and why it matters.

## 2. Goals

List the outcomes you want.

Example:

- Provide a CLI that triages GitHub issues into `type`, `priority`, `labels`, and `rationale`.
- Enforce a stable JSON output contract via `src/triage_assistant/schema.py`.
- Enable prompt/agent iteration with AI Toolkit evaluation using `datasets/triage_dataset.csv`.

## 3. Non-goals

Explicitly list what is out of scope.

Example:

- No GitHub API automation (no label writing back to GitHub).
- No web UI.
- No authentication or multi-tenant support.

## 4. Users and use cases

Who uses this and how?

Examples:

- Maintainers triage new issues into buckets quickly.
- Contributors use the output to pick the next task.

## 5. Functional requirements

Bullet list of requirements.

Examples:

- `triage-assistant triage --title ... --body ...` prints valid JSON on stdout.
- JSON must validate against `TriageOutput` schema.
- A deterministic baseline (rule-based adapter) must exist.
- Optional: an OpenAI-compatible adapter can be enabled via env vars.

## 6. Output contract

The output must be a single JSON object with:

- `type`: `bug | feature | docs | question`
- `priority`: `p0 | p1 | p2`
- `labels`: string array
- `rationale`: short string

Source of truth:

- `src/triage_assistant/schema.py`

## 7. Acceptance criteria

Write crisp, testable criteria (Definition of Done).

Examples:

- Running `pytest -q` passes.
- Running `triage-assistant triage ...` prints schema-valid JSON.
- `triage-assistant schema` prints valid JSON schema.

## 8. Evaluation plan

Define how you will measure improvement.

Deterministic gates:

- unit tests
- schema validation
- linting/formatting

Probabilistic gates:

- AI Toolkit bulk run using `datasets/triage_dataset.csv`
- evaluation metrics:
  - type accuracy
  - priority accuracy
  - label F1 / overlap
- record findings in `reports/eval/`

## 9. Risks and mitigations

List risks and how to reduce them.

Examples:

- Model output is not valid JSON → strict schema validation + JSON extraction + tests.
- Triage labels are subjective → focus on stable taxonomy and measurable metrics.

## 10. Open questions

List questions that are not yet decided.
