# Contributing

This repository is primarily a workshop. Contributions that improve clarity and repeatability are welcome.

## How to contribute

1. Create or pick an existing GitHub Issue.
2. Work on a branch scoped to that issue.
3. Keep changes small and focused.
4. Ensure deterministic gates pass:

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
ruff format --check .
```

5. Open a PR and link the issue.

## Style and conventions

- Python 3.11+
- Type hints required
- Output contract is enforced by `src/triage_assistant/schema.py`
- `triage` command must output JSON on stdout

## Workshop note

If you are using this repo as part of a workshop, prefer to keep changes aligned with the teaching goals:
Spec → Plan → Issues → Implement → Run/Evaluate → Feedback.
