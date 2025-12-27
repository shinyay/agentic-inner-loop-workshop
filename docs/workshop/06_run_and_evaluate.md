# 06 — Run and Evaluate

## Goal

Run evaluation on two lanes:

- **Deterministic lane**: tests, schema validation
- **Probabilistic lane**: AI Toolkit bulk runs + evaluation + version comparison

The workshop aims to make you feel the difference between:
- “the code works”
- “the model is getting better”

## Run/Evaluate checklist

Use this as a quick, reproducible checklist before you move on.

- [ ] Run deterministic gates:
	- [ ] `pytest -q`
	- [ ] (optional) `ruff check .`
	- [ ] (optional) `ruff format --check .`
- [ ] Run a dataset evaluation:
	- [ ] Use the workshop dataset: `datasets/triage_dataset.csv`
	- [ ] Run either:
		- [ ] AI Toolkit bulk run + evaluation (preferred for iteration)
		- [ ] local eval: `triage-assistant eval --adapter dummy --dataset datasets/triage_dataset.csv`
- [ ] Record findings in this repo (don’t leave them only in the UI):
	- [ ] Create a Markdown report under `reports/eval/`
	- [ ] Start from `docs/templates/eval-report.template.md`
	- [ ] Note what changed, what improved/regressed, and 3 concrete failure cases

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

> AI Toolkit is in **preview**, so the exact UI and feature names can drift across VS Code / extension versions.
>
> If you can’t find a panel or button mentioned below, use the **Command Palette** (`Ctrl/Cmd+Shift+P`) and search for:
> “AI Toolkit”, “Model Catalog”, “Bulk Run”, or “Evaluation”.
>
> The intent of this lane is stable:
> 1) pick a model/provider, 2) run your prompt/agent on a dataset, 3) evaluate, 4) save a version you can compare.

### Step 1 — Open AI Toolkit

Open the AI Toolkit view in VS Code.
You should see features like Prompt Builder / Agent Builder, Bulk Run, Evaluation, etc.

### Step 1.5 — Select a hosted model (GitHub Models or Foundry)

In AI Toolkit's **Model Catalog**, select a model to run your prompt/agent.

Recommended options for the workshop:

- **GitHub Models** — quickest start if you have a GitHub account + token
- **Microsoft Foundry** — best if you already have an Azure / Foundry environment

If you cannot access a hosted provider, you can still run the deterministic lane and
continue the workshop using the rule-based baseline.

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

