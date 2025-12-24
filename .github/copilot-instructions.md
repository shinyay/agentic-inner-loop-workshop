# Repository instructions for GitHub Copilot

These instructions apply when using Copilot Chat, Copilot code review, or Copilot coding agent in this repository.

## Context

This repository is a workshop about an **agentic inner loop**. The goal is to practice:

Spec → Plan → Issues → Implement → Run/Evaluate → Feedback → repeat

The codebase is intentionally small. Optimize for **clarity** and **repeatability**, not cleverness.

## Output contract is strict

The triage output must conform to the `TriageOutput` schema:

- `src/triage_assistant/schema.py`

When implementing changes that affect output:
- update or add tests
- keep CLI output JSON-only on stdout for the `triage` command

## Preferred workflow

1. Read `docs/spec.md` and `docs/plan.md`
2. Work issue-by-issue (one issue → one PR)
3. Keep diffs small and focused
4. Run validation (`pytest -q`) before finishing

## Coding guidelines

- Python 3.11+
- Type hints required
- Prefer small pure functions
- Avoid unnecessary dependencies
- Errors should be human-readable on stderr and machine-readable output should remain on stdout

## Don’t do these

- Don’t introduce GitHub API automation unless explicitly requested in the spec/plan.
- Don’t change the schema contract without updating documentation and tests.
- Don’t print logs before JSON on stdout for `triage`.
