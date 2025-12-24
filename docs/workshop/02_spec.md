# 02 — Spec

## Goal

Create a **written spec** that is concrete enough to generate tasks with acceptance criteria.

Primary artifact:

- `docs/spec.md`

## Why this matters

The inner loop only works if “done” is explicit.
If the spec is vague, the plan and issues will be vague, and the loop collapses into “random edits”.

## Steps

### Step 1 — Switch Copilot Chat to Plan mode

In the Chat view, switch the agent/mode to **Plan** (or use Ask mode but explicitly request a plan).
Plan mode is useful because it tends to:
- ask clarifying questions
- produce structured output
- avoid premature code edits

### Step 2 — Run the spec prompt file

In Chat, run:

- `/draft-spec`

If asked, answer clarifying questions. Keep answers short and specific.

### Step 3 — Review `docs/spec.md`

Open the generated file and check:

- Does it define the output contract (type/priority/labels/rationale)?
- Does it reference `src/triage_assistant/schema.py` as source of truth?
- Are acceptance criteria testable?
- Does it include an evaluation plan (AI Toolkit + dataset)?

### Step 4 — Make the spec “taskable”

A good rule:
> If you cannot write a DoD and a validation command, the spec is still too vague.

If needed, ask Copilot:

- “Rewrite acceptance criteria as checkboxes with validation commands.”

### Step 5 — Commit the spec

Commit the spec so the rest of the loop has a stable anchor.

Example:

```bash
git add docs/spec.md
git commit -m "docs: add initial spec"
```

## Outputs for this module

- `docs/spec.md` exists and is usable as an anchor for tasks

Next: `03_plan.md`
