# Agentic Inner Loop Workshop

This repository is a **hands-on workshop** that teaches how to run an **agentic inner loop** inside Visual Studio Code by connecting:

- **GitHub Copilot Chat** (Ask / Edit / Agent / Plan)
- **AI Toolkit for VS Code** (prompt/agent iteration, bulk run, evaluation, version comparison)
- **GitHub Issues** (task decomposition, progress tracking, feedback loop closure)

You will repeatedly run a deep loop:

**Spec → Plan → Tasks → Implement → Run/Evaluate → Feedback → (back to Spec/Plan)**

The deliverable is a tiny but realistic “Issue Triage Assistant” CLI and a set of reusable workflows
(prompt files, templates, issue templates) that make the loop repeatable.

---

## What you will build

A small Python CLI that takes a GitHub Issue `title` and `body` and produces a **schema-validated JSON** response:

```json
{
  "type": "bug | feature | docs | question",
  "priority": "p0 | p1 | p2",
  "labels": ["..."],
  "rationale": "short explanation"
}
```

The CLI ships with:
- a **rule-based adapter** (offline baseline, deterministic)
- a **GitHub Models adapter** (hosted models via your GitHub token)
- a **Microsoft Foundry adapter** (hosted models via Azure AI inference endpoints)
- an optional **OpenAI-compatible adapter** (fallback for existing OpenAI-style endpoints)
- tests and CI so you can keep “deterministic correctness” while iterating on “probabilistic quality”.

---

## Repository tour

- `docs/workshop/` — step-by-step workshop modules
- `docs/templates/` — templates for spec/plan/eval reports
- `docs/providers.md` — how to configure GitHub Models / Foundry for hosted-model runs
- `.github/prompts/` — Copilot prompt files invoked via `/` in the Chat view
- `.github/ISSUE_TEMPLATE/` — standardized issue templates for tasks, bugs, and evaluation regressions
- `src/triage_assistant/` — the CLI + schema + adapters
- `datasets/` — a small evaluation dataset for AI Toolkit and local evaluation
- `reports/eval/` — where you save evaluation notes so feedback becomes actionable work

---

## Prerequisites

- VS Code (latest stable recommended)
- Extensions:
  - GitHub Copilot
  - GitHub Copilot Chat
  - AI Toolkit for VS Code
  - GitHub Pull Requests and Issues
  - Python (and Pylance)
- Python 3.11+ installed locally

---

## Quickstart

Create and activate a virtual environment, then install:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Run the CLI:

```bash
triage-assistant triage --title "Crash on startup" --body "Steps to reproduce: ..."
```

Run tests:

```bash
pytest -q
```

---

## Using a hosted model

By default, `triage-assistant` uses the deterministic `dummy` adapter so the workshop can run
without any external credentials.

If you want to call a hosted model from the CLI, configure a provider and then run with
`--adapter ...` (or set `TRIAGE_PROVIDER`).

For full details (including environment variables), see:

- `docs/providers.md`

### Option A: GitHub Models

1) Create a token that can access GitHub Models.

2) Set environment variables:

```bash
export TRIAGE_GITHUB_TOKEN="..."
export TRIAGE_GITHUB_MODEL="openai/gpt-4.1"  # optional; default shown
```

3) Run:

```bash
triage-assistant triage --adapter github --title "Crash on startup" --body "Steps to reproduce: ..." --pretty
```

### Option B: Microsoft Foundry

1) Deploy a model in Microsoft Foundry and copy the Azure AI inference endpoint and key.

2) Set environment variables:

```bash
export TRIAGE_FOUNDRY_ENDPOINT="https://<resource-name>.services.ai.azure.com/models"
export TRIAGE_FOUNDRY_API_KEY="..."  # or AZURE_INFERENCE_CREDENTIAL
export TRIAGE_FOUNDRY_MODEL="<deployment-name>"
```

3) Run:

```bash
triage-assistant triage --adapter foundry --title "Crash on startup" --body "Steps to reproduce: ..." --pretty
```

---

## Workshop flow

Start here:

- `docs/workshop/00_overview.md`

Then follow modules in order:

1. Setup (`01_setup.md`)
2. Spec (`02_spec.md`)
3. Plan (`03_plan.md`)
4. Tasks (`04_issues.md`)
5. Implement (`05_implement.md`)
6. Run & Evaluate (`06_run_and_evaluate.md`)
7. Feedback loop closure (`07_feedback.md`)
8. Retro and mental model (`08_retro.md`)

---

## Conventions

- Keep changes **small** and **issue-scoped**.
- Every task has a **Definition of Done** (DoD) and a **validation command**.
- Deterministic gates: tests, schema validation, linting.
- Probabilistic gates: AI Toolkit evaluation runs and version comparisons.

---

## License

MIT. See `LICENSE`.
