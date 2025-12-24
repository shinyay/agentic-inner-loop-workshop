# Evaluation dataset

This folder contains a small, human-authored dataset that can be used for:

- **AI Toolkit** bulk runs and evaluations
- local quick checks via `triage-assistant eval`

File(s):

- `triage_dataset.csv`

## CSV schema

Columns:

- `id` — stable identifier
- `title` — GitHub Issue title
- `body` — GitHub Issue body (plain text)
- `expected_type` — `bug | feature | docs | question`
- `expected_priority` — `p0 | p1 | p2`
- `expected_labels` — JSON array string (for example: `["bug","p1","needs-repro"]`)

## Notes on evaluation

- Treat `expected_labels` as a *suggestion* (labels are often subjective).
- For probabilistic evaluation, focus on:
  - type accuracy
  - priority accuracy
  - label overlap / F1
- For deterministic evaluation, rely on tests (`pytest`) and schema validation.
