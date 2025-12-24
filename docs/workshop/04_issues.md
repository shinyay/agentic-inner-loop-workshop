# 04 — Tasks with GitHub Issues

## Goal

Convert the plan into **GitHub Issues** that act as the durable “task memory” for the loop.

Primary artifacts:

- GitHub Issues in this repo
- optional: a local draft file (for workshop record keeping)

## Steps

### Step 1 — Generate issue drafts from the plan

In Copilot Chat, run:

- `/split-to-issues`

This prompt writes a draft list into `docs/issues-draft.md`.

Open `docs/issues-draft.md` and review:
- Are issues small enough?
- Does each issue have checkboxes (DoD)?
- Is there a clear validation command?

### Step 2 — Create GitHub Issues using templates

Use `.github/ISSUE_TEMPLATE/` templates:

- Task
- Bug
- Eval regression

Create issues in GitHub (web or VS Code GitHub view).

Suggested labels:
- `workshop:spec`
- `workshop:plan`
- `workshop:impl`
- `workshop:eval`
- `workshop:prompt`

(You can create labels manually in GitHub if they don't exist yet.)

### Step 3 — Start work on an issue (branch per issue)

Using the GitHub Pull Requests and Issues extension:

1. Open the issue in VS Code.
2. Choose **Start working on issue** (creates a branch).
3. Confirm your branch naming convention (example: `issue/12-add-eval-command`).

### Step 4 — Define “done” in the issue itself

Before writing code, ensure each issue contains:

- [ ] Acceptance criteria (checkboxes)
- [ ] Validation command(s) (example: `pytest -q`)
- [ ] Notes about what files to touch (optional)

This reduces ambiguity for both humans and agents.

## Outputs for this module

- A small backlog of GitHub Issues with DoD
- A branch created from at least one issue

Next: `05_implement.md`
