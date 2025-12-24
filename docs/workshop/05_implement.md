# 05 — Implement

## Goal

Complete at least one GitHub Issue using an issue-scoped inner loop:

1. Read issue + DoD
2. Implement the smallest change that satisfies DoD
3. Run validation command(s)
4. Commit (and optionally open a PR)

## Steps

### Step 1 — Bring the issue into context

In Copilot Chat:

- switch to **Agent** (or Edit for smaller diffs)
- paste the GitHub Issue text (title, DoD, validation commands)
- add relevant files as context (for example: `src/triage_assistant/schema.py`)

### Step 2 — Run the implementation prompt

Run:

- `/implement-issue`

When asked, provide:
- the issue title
- acceptance criteria
- what to validate (tests, CLI command)

### Step 3 — Keep the diff small

If the agent proposes a large refactor, constrain it:

- “Do the minimal change to satisfy the acceptance criteria.”
- “Do not rename public APIs unless required.”

### Step 4 — Run deterministic gates

At minimum:

```bash
pytest -q
```

Optionally:

```bash
ruff check .
ruff format --check .
```

### Step 5 — Commit

```bash
git status
git add -A
git commit -m "feat: <short summary>"
```

### Step 6 — Close the loop in the issue

In the issue description or a comment, record:
- what you changed
- how you validated it

## Outputs for this module

- One completed issue (code + tests)
- Deterministic gates passing

Next: `06_run_and_evaluate.md`
