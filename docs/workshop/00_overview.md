# 00 — Overview

## Workshop goal

By the end of this workshop, you should be able to **explain and execute** an agentic inner loop in VS Code:

1. **Spec** — define what “done” means
2. **Plan** — choose an implementation approach and slice work
3. **Tasks** — convert slices into GitHub Issues with DoD + validation commands
4. **Implement** — use Copilot Chat (Agent/Edit) to implement issue-scoped changes
5. **Run & Evaluate** — run deterministic gates (tests) and probabilistic gates (AI Toolkit evaluation)
6. **Feedback** — convert evaluation findings into new tasks and update spec/plan
7. Repeat

You will run the loop **at least twice**.

## The key mental model

An “agentic” workflow is not just “use AI to write code”.
It is a system that:

- **remembers** what you decided (spec, plan, issues)
- **checks** correctness (tests, schema)
- **measures** quality (evaluations, comparisons)
- **feeds back** failures into the next cycle

## Why GitHub Issues is part of the inner loop

Chat context is temporary. Issues are durable.

In this workshop, GitHub Issues acts as:
- an external task memory
- a lightweight requirements + acceptance criteria store
- the unit of iteration (branch/PR per issue)

## Why AI Toolkit is part of the inner loop

If you are using a model (prompt/agent) to triage, quality is probabilistic.
You need a structured way to:
- run a dataset
- track versions
- compare improvements

AI Toolkit provides that “prompt iteration loop” inside VS Code.

## What you will produce

- `docs/spec.md`
- `docs/plan.md`
- a set of GitHub Issues representing your plan
- working code + tests in `src/` and `tests/`
- evaluation notes in `reports/eval/`

## Recommended timeboxes

- Setup: 10 min
- Spec + plan: 20–30 min
- First implementation loop (1–2 issues): 30–45 min
- First evaluation loop: 20–30 min
- Second loop (improve + re-evaluate): 20–30 min
- Retro: 10 min

## Navigation

Next: `01_setup.md`
