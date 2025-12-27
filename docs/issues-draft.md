# Issue drafts

Goal:

- Convert `docs/plan.md` into copy/paste-ready GitHub Issue drafts.

Steps:

1. Copy one issue draft into GitHub Issues.
2. Create a branch from the issue.
3. Implement → validate → open a PR.

Expected outputs:

- Each issue has a clear DoD and validation commands.
- Deterministic gates stay green: `python3 -m pytest -q`.

---

## Issue 1: Workshop docs prerequisites + UI drift guardrails

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- Participants get blocked by version/UI differences (VS Code checkpoints, AI Toolkit preview UI).

Definition of Done:

- [ ] Add a short “Versions & prerequisites” note to the relevant workshop doc(s) under `docs/workshop/`.
- [ ] Mention VS Code checkpoints requirement (VS Code 1.103+).
- [ ] Mention AI Toolkit is preview and include at least one fallback navigation path (Command Palette / alternate menu).
- [ ] Keep wording intent-based (avoid brittle click-by-click instructions).

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- None.

---

## Issue 2: Add `triage-assistant doctor` for configuration diagnosis

Labels (suggested):

- `feature`
- `p2`
- `enhancement`

Problem statement:

- Hosted adapters fail when env vars are missing; diagnosing “what is auto doing?” is slow.

Definition of Done:

- [ ] Add a `doctor` command that prints which adapter `--adapter auto` would choose.
- [ ] Show missing env vars for GitHub Models / Foundry / OpenAI-compatible (best-effort).
- [ ] Do not break `triage` JSON-only stdout contract.
- [ ] Add unit tests for the doctor output.

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- None.

---

## Issue 3: Improve hosted adapter error messages (actionable, safe)

Labels (suggested):

- `bug`
- `p1`

Problem statement:

- HTTP failures are not always actionable; users need “what to check next” without secrets leakage.

Definition of Done:

- [ ] Improve error messages for GitHub Models and Foundry adapters to include status code + safe hint.
- [ ] Ensure tokens/keys are never printed.
- [ ] Add at least one mocked failure test.

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- Independent of Issue 2.

---

## Issue 4: Strengthen CLI contract tests (stdout JSON-only)

Labels (suggested):

- `bug`
- `p1`

Problem statement:

- The most important contract is “`triage` prints JSON-only on stdout”. Regressions break pipelines.

Definition of Done:

- [ ] Add/extend tests that assert `triage` stdout is parseable JSON.
- [ ] Add/extend tests that assert errors go to stderr (not stdout).

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- This issue covers the deterministic baseline requirement: tests + schema + CLI stability.

---

## Issue 5: Improve `triage-assistant eval` Markdown report for fast iteration

Labels (suggested):

- `feature`
- `p2`
- `enhancement`

Problem statement:

- The local eval report is useful, but needs better “what failed” visibility for iteration.

Definition of Done:

- [ ] Improve report readability (expected vs predicted, rationale, failure examples).
- [ ] Add a small “top failure patterns” section (basic grouping is OK).
- [ ] Add a unit test that asserts key headings exist.

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- None.

---

## Issue 6: Document the evaluation loop (AI Toolkit) + where to record results

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- Participants run evals but don’t consistently record findings in a reusable way.

Definition of Done:

- [ ] Add a short “Run/Evaluate” checklist under `docs/workshop/`.
- [ ] Reference dataset: `datasets/triage_dataset.csv`.
- [ ] Specify where to record results: `reports/eval/`.

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- Issue 1 is recommended first (keeps docs consistent), but not required.
- This issue covers the probabilistic evaluation requirement: AI Toolkit dataset run + versioning notes.

---

## Issue 7: Close the loop (eval findings → new issues)

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- Without turning failures into issues, the loop stalls.

Definition of Done:

- [ ] Document how to create issue drafts from evaluation findings.
- [ ] (Optional) Document how to use `scripts/eval_report_to_issues.py` if appropriate.
- [ ] Ensure the flow produces copy/pasteable issue drafts.

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- Depends on Issue 6.
- This issue covers the feedback loop closure requirement.

---

## Issue 8: Hosted adapter smoke-test note (optional but practical)

Labels (suggested):

- `docs`
- `p2`

Problem statement:

- Participants want to confirm hosted adapters work end-to-end, but setup varies.

Definition of Done:

- [ ] Add a short doc note pointing to `docs/providers.md` and showing a minimal smoke-test command.
- [ ] Include a reminder that secrets live in env vars / `.env` and should not be pasted.

Validation command(s):

- `python3 -m pytest -q`

Notes / dependencies:

- None.



