# AGENTS.md

This file defines **agent operating guidelines** for this repository.

It is intended for:
- GitHub Copilot coding agent
- GitHub Copilot CLI agent sessions
- Humans using Copilot Chat in Agent mode

The goal is to make changes that are **repeatable, reviewable, and easy to revert**.

---

## Repository purpose

This repository is a workshop to practice an **agentic inner loop**:

1. Write / refine a **spec**
2. Convert spec into a **plan**
3. Split plan into **GitHub Issues**
4. Implement each issue with tests and validation commands
5. Run deterministic + probabilistic evaluations
6. Turn evaluation findings into new issues and update spec/plan
7. Repeat

---

## Non-negotiables

1. **Schema is the contract**
   - The output contract is enforced by `src/triage_assistant/schema.py`.
   - Any change that affects output must update tests.

2. **Small, issue-scoped changes**
   - Prefer one issue → one branch → one PR.
   - If a change touches many files, justify it in the PR description.

3. **Always keep deterministic gates green**
   - Run `pytest -q` before finalizing work.
   - If you change lint rules or formatting, ensure CI still passes.

4. **No silent behavior changes**
   - CLI output must remain JSON on stdout for `triage` command.
   - Use stderr for human-readable errors.

5. **Prefer edit-in-place over rewrites**
   - Avoid rewriting modules wholesale unless the issue explicitly asks for it.
   - Keep interfaces stable unless the spec/plan says otherwise.

---

## Working agreement

When starting work on a task:

1. Read:
   - `docs/spec.md`
   - `docs/plan.md`
   - the relevant GitHub Issue (acceptance criteria + validation command)

2. Propose:
   - a short approach summary
   - files you will touch
   - the validation command you will run

3. Implement:
   - update / add tests first when it clarifies behavior
   - keep commits small

4. Validate:
   - `pytest -q`
   - optionally: `ruff check .` and `ruff format --check .`

---

## Suggested Definition of Done

A task is “done” when:

- [ ] Acceptance criteria in the issue are met
- [ ] Tests cover the new behavior (or the task documents why tests are not needed)
- [ ] `pytest -q` passes locally
- [ ] Any new configuration has documentation
- [ ] Any evaluation changes are recorded in `reports/eval/`

---

## Style and tooling

- Python 3.11+
- Use type hints
- Prefer pure functions and small modules
- Use `typer` for CLI commands
- Use `pydantic` models for schema enforcement
- Use `ruff` for linting/formatting

---

## What to do when uncertain

If requirements are ambiguous:
- Ask at most **3 clarifying questions**
- Otherwise, pick the smallest reasonable interpretation and document assumptions.

If a change might be risky:
- Add a test that locks the old behavior before modifying it.

---

## Security

- Never commit secrets.
- Model adapters read credentials from environment variables.
  - GitHub Models: PAT / token (`TRIAGE_GITHUB_TOKEN`)
  - Microsoft Foundry: API key (`TRIAGE_FOUNDRY_API_KEY` or `AZURE_INFERENCE_CREDENTIAL`)
  - OpenAI-compatible: API key (`TRIAGE_OPENAI_API_KEY`)
