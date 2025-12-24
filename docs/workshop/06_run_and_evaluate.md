# 06 — Run and Evaluate

## Goal

Run evaluation on two lanes:

- **Deterministic lane**: tests, schema validation
- **Probabilistic lane**: AI Toolkit bulk runs + evaluation + version comparison

The workshop aims to make you feel the difference between:
- “the code works”
- “the model is getting better”

## Lane A: Deterministic gates

Run:

```bash
pytest -q
```

Optional:

```bash
ruff check .
ruff format --check .
```

## Lane B: Probabilistic evaluation with AI Toolkit

### Step 1 — Open AI Toolkit

Open the AI Toolkit view in VS Code.
You should see features like Prompt Builder / Agent Builder, Bulk Run, Evaluation, etc.

### Step 2 — Create a baseline prompt

Create a prompt that takes two variables:
- `title`
- `body`

And returns **only JSON** matching the schema in `src/triage_assistant/schema.py`.

Tip: include the exact allowed values for `type` and `priority`.

### Step 3 — Run a bulk run on the dataset

Use `datasets/triage_dataset.csv` as the dataset.

Map columns:
- input variables: `title`, `body`
- expected: `expected_type`, `expected_priority`, `expected_labels` (depending on evaluator)

### Step 4 — Evaluate

Run an evaluation that gives you a number you can compare between versions.
Examples:
- accuracy for type/priority
- overlap/F1 for labels (if supported)

### Step 5 — Save version + compare

Save your prompt/agent as a version:
- v1: baseline

After improvements later, create:
- v2, v3, ...

Compare results to confirm you improved the metric.

### Step 6 — Write down findings

Create a Markdown note under `reports/eval/` using:
- `docs/templates/eval-report.template.md`

At minimum record:
- what changed
- what improved / regressed
- 3 failure cases
- next actions (to become issues)

## Outputs for this module

- A recorded evaluation report under `reports/eval/`
- At least one baseline evaluation in AI Toolkit (v1)

Next: `07_feedback.md`
