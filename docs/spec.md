# Spec: Issue Triage Assistant (Workshop)

## Goal

Build a small CLI tool that turns a GitHub Issue (title + body) into a **stable, schema-valid JSON** triage result.
This repository is a workshop artifact to practice an agentic inner loop:

- Spec → Plan → Issues → Implement → Run/Evaluate → Feedback → repeat

In this workshop scenario, you will run **two iterations**:

- **v1 baseline**: establish a minimal prompt/agent and capture failure modes
- **v2 improved**: apply targeted fixes and show measurable improvement

## How you use it (high level)

Steps:

1. Run `triage-assistant triage --title ... --body ...` to get triage JSON.
2. In AI Toolkit (Agent Builder), create a minimal **v1** prompt/agent that outputs JSON-only.
3. Bulk run the repo dataset (`datasets/triage_dataset.csv`) and run an evaluation.
4. Write an evaluation report (`reports/eval/<timestamp>_v1.md`).
5. Turn failures into issues, apply targeted fixes (prompt-only or code+tests).
6. Re-run bulk run + evaluation for **v2**, compare with v1, and record `..._v2.md`.
7. Keep deterministic checks green with `pytest -q`.

Notes:

- This project reads configuration from environment variables (for example `TRIAGE_PROVIDER`).
- `.env` files are **not** auto-loaded by the CLI. If you use `.env`, load it in your shell (or use an env manager).
- If `triage-assistant` is not on your PATH, either activate the venv (`source .venv/bin/activate`) or run via `uv run triage-assistant ...`.

Expected outputs:

- `triage-assistant triage ...` prints **a single JSON object** to stdout.
- Errors are printed to stderr.
- JSON validates against `src/triage_assistant/schema.py`.
- Workshop evidence is recorded under `reports/eval/` (v1 + v2).

## 1. Problem statement

Maintainers (and workshop participants) spend time repeatedly classifying issues.
We want a fast, consistent triage output that is easy to:

- automate (JSON)
- test (schema + unit tests)
- evaluate (dataset + reports)

## 2. Goals

- Provide a CLI that triages issues into `type`, `priority`, `labels`, and `rationale`.
- Enforce a stable JSON output contract via `src/triage_assistant/schema.py`.
- Support both:

  - **offline** deterministic baseline (for repeatable tests)
  - **hosted-model** adapters (for realism and iteration)
- Enable prompt/agent iteration with evaluation using `datasets/triage_dataset.csv`.

## 3. Non-goals

- No GitHub API automation (no label writing back to GitHub).
- No web UI.
- No attempt to be “perfect triage”; the goal is a reliable loop for improvement.
- No secret management beyond environment variables (never commit secrets).

## 4. Users and use cases

- Maintainers: quickly classify new issues into buckets.
- Contributors: use the output to pick the next task (what matters most).
- Workshop participants: practice prompt/agent iteration with measurable feedback.

## 5. Functional requirements

- CLI command `triage-assistant triage --title ... --body ...` prints schema-valid JSON to stdout.
- CLI command `triage-assistant schema` prints JSON schema.
- CLI command `triage-assistant eval --dataset ... --adapter ...` runs a local, lightweight evaluation.
- Adapter selection:

  - explicit: `--adapter dummy|github|foundry|openai|auto`
  - implicit: `TRIAGE_PROVIDER` when using `--adapter auto`
- Output discipline:

  - JSON-only on stdout for `triage`
  - human-readable errors on stderr
- A deterministic baseline adapter exists (`DummyAdapter`).
- Hosted adapters validate model output against `TriageOutput`.

Provider configuration:

- Hosted adapters are enabled via environment variables only.
- Secrets (tokens/keys) must never be committed to git or pasted into issues/chat logs.

## 6. Output contract

The output must be a single JSON object with:

- `type`: `bug | feature | docs | question`
- `priority`: `p0 | p1 | p2`
- `labels`: string array
- `rationale`: short string

### Label taxonomy (used in this repo)

The workshop uses a small, stable label taxonomy so results are measurable and easy to reason about.

Required labels:

- Type label: one of `bug`, `feature`, `docs`, `question` (must match `type`)
- Priority label: one of `p0`, `p1`, `p2` (must match `priority`)

Optional labels (allowed, not always present):

- `needs-repro`: bug report missing clear reproduction steps
- `needs-env-info`: bug report missing environment/version info
- `needs-info`: question/issue is too vague (often short questions)
- `good-first-issue`: small docs fixes (typos, spelling, grammar)
- `enhancement`: non-urgent feature requests
- `security`: security-related bug reports (vulnerabilities, data loss, RCE signals, etc.)

Notes:

- Labels are normalized for stability (trim, remove empties, de-duplicate case-insensitively) by `TriageOutput`.
- Adapters may propose additional labels, but workshop evaluation should focus on the taxonomy above.

Source of truth:

- `src/triage_assistant/schema.py` (`TriageOutput`)

## 7. Acceptance criteria

All criteria must be testable with concrete commands.

- Unit tests pass:

	- `python3 -m pytest -q`
	- (if you are using `uv`) `uv run pytest -q`
- The `triage` command prints schema-valid JSON to stdout:

	- `triage-assistant triage --adapter dummy --title "Crash when saving" --body "Steps to reproduce:\n1. Open\n2. Save\nVersion: 1.0" --pretty`
	- (optional strict check) pipe the JSON into the schema validator:

		- `triage-assistant triage --adapter dummy --title "Crash" --body "..." | python3 -c "from triage_assistant.schema import validate_output_json; import sys; validate_output_json(sys.stdin.read())"`
- The `schema` command prints valid JSON:

	- `triage-assistant schema | python3 -c "import json,sys; json.loads(sys.stdin.read())"`
- For hosted adapters, missing env vars produce a clear CLI error on stderr and exit code != 0.

- Workshop artifacts exist (probabilistic loop recorded as repo memory):

	- `reports/eval/<YYYYMMDD-HHMM>_v1.md` committed
	- `reports/eval/<YYYYMMDD-HHMM>_v2.md` committed
	- v2 report includes (a) v1 vs v2 deltas and (b) at least one fixed failure case

Optional (hosted) acceptance check:

- `triage-assistant doctor` should report `Selected adapter: github` (or `foundry` / `openai`) when credentials are configured.

## 8. Evaluation plan

Deterministic gates:

- unit tests (`pytest -q`)
- schema validation (adapters return `TriageOutput`)

Probabilistic gates:

- AI Toolkit bulk runs using `datasets/triage_dataset.csv`
- evaluation jobs (built-in evaluators such as relevance/coherence, plus any custom checks you add)
- versioning + comparison between **v1** and **v2**
- record findings under `reports/eval/`

Expected outputs:

- A short report that highlights where the model failed (taxonomy mismatch, wrong priority, unstable labels, etc.).
- A follow-up report that shows what changed and what improved after fixes.

## 9. Risks and mitigations

- Model output is not valid JSON → enforce JSON extraction + schema validation.
- Rate limits / transient API failures → keep an offline baseline; treat hosted runs as best-effort.
- Secret leakage → keep secrets in environment variables; never paste tokens into issues/chat.
- UI drift (preview tooling) → document intent + fallback navigation rather than brittle click paths.

## 10. Open questions

- What counts as a “good enough” evaluation improvement within the workshop timebox?



