---
applyTo: "src/**/*.py,tests/**/*.py"
---

## Python code instructions

- Use Python 3.11+ features (e.g., `X | None` union types).
- Keep functions small and testable.
- The output contract is enforced by `TriageOutput` in `src/triage_assistant/schema.py`.
- For CLI behavior:
  - `triage` prints JSON to stdout only
  - human-readable errors go to stderr
- Add or update tests when behavior changes.
