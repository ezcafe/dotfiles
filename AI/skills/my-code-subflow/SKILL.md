---
name: my-code-subflow
description: >-
  Optionally reviews planned TDD test cases before Gate B when 04-tasks lists
  real tests to create; then builds approved design tasks with TDD after Gate B
  using a fast model. Also fixes failures from my-test-subflow when
  06-test-log.md reports smoke-fail or failure. Produces a draft only — no merge
  or self-approval. Use when the user says run my-code-subflow, build from
  design, fix from test failures, TDD test-case review, or after
  my-design-review-subflow is clean / Gate B is approved.
---

# my-code-subflow

Build subflow of [`my-plan-flow`](../my-plan-flow/SKILL.md).

- **TDD test-case review** runs **before Gate B** only when `04-tasks.md` has planned test cases.
- **Build** runs **after Gate B** and produces a **draft** (then Smoke → review).
- **Fix-from-tests** repairs [`my-test-subflow`](../my-test-subflow/SKILL.md) smoke or full failures.

**Details:** [stages.md](stages.md) · templates [`../my-plan-flow/templates.md`](../my-plan-flow/templates.md)

## When to run

`run my-code-subflow`, build from design, TDD test-case review, fix from test failures, or when
`my-plan-flow` reaches Step 4a (before Gate B), Step 4 Build (after Gate B), or Test↔Code loop.

## Principles

- First Build output is a draft, not a deliverable.
- **TDD test-case review before Gate B (conditional):** Run only if `04-tasks.md` creates planned tests (non-empty TDD case lists). Otherwise skip — note `04a skipped — no planned test cases` in `00-run.md`; do not invent `04a`.
- **Build after Gate B only** (when parent is `my-plan-flow`). Gate B may be HITL **auto**.
- TDD: Red → Green → Refactor → Verify (when tasks include tests).
- **Build when Has UI:** match Design UI specs + existing app chrome. Do not invent a conflicting layout.
- When fixing from tests: **only** address `06-test-log.md` fix ask + stay aligned with design/tasks (+ Design UI when Has UI).
- Each Task has a **fresh context** and **stage-scoped handoff** (`tdd-review`, `build`, `fix-tests`).
- Plain words in comments.

## Models

| Tier | Stages | Preferred slug |
|------|--------|----------------|
| **Medium** | TDD test-case review when run (→ Fast if Medium unavailable) | `gpt-5.6-sol-medium` |
| **Fast** | Build; Fix from tests | `composer-2.5-fast` |

### Model availability

Follow [`my-plan-flow`](../my-plan-flow/SKILL.md) → **Model availability (auto fallback)**.

## Prerequisites

**TDD test-case review** (before Gate B) — only when tests are planned:

- `03-design.md` and `04-tasks.md` present
- `04-tasks.md` has concrete planned test cases (not N/A / empty)
- Prefer `03a` Result **clean** (when present; skip in simple if absent and starting mid-pipeline)
- Full: Gate A checked; Simple: prefer those already checked from earlier framing
- Gate B is **not** required yet

**Build mode** (after Gate B):

- Gate B checked in `00-run.md` (human or HITL auto)
- Prefer `04a-tdd-test-review.md` present **or** Notes say 04a skipped
- `03-design.md` and `04-tasks.md` present

**Fix-from-tests mode:**

- `06-test-log.md` with **Result: smoke-fail** or **failure** and Fix ask
- Prefer Gate B already checked

If the requested mode’s files are not ready → **stop**.

## Pipeline

```
TDD review (Step 4a, if planned tests):  TDD test-case review (Medium) → Gate B (parent HITL) → Build
No planned tests:                        skip 04a → Gate B (parent HITL) → Build
Build mode:                              Build TDD (Fast) → draft → parent runs Smoke then review
Fix-from-tests mode:                     Fix from 06-test-log (Fast, TDD) → re-run smoke or full test
```

When parent runs `my-plan-flow`, it calls this skill for TDD review only when needed, then again for Build after Gate B.

## TDD (required when tests exist)

**Before Gate B — TDD test-case review (conditional):**

1. If `04-tasks.md` has **no** planned test cases → skip; parent notes skip; go to Gate B.
2. Else collect planned tests from `04-tasks.md`.
3. Launch TDD review Task → `04a-tdd-test-review.md`.
4. If **needs more tests**: fold Fix ask into `04-tasks.md` when practical.
5. Hand off to parent for **Gate B** — do **not** Build yet.

**After Gate B — per task / fix:**

1. Red → Green → Refactor → Verify (include 04a Fix ask when 04a ran)

## Orchestrator rules

- Detect mode: no planned tests → skip TDD review; TDD review only / Step 4a → stop before Build; `06-test-log` failure → fix-from-tests; else Build (require Gate B when parent is my-plan-flow).
- Fresh Task per stage.
- After **TDD review or skip**: next is **Gate B** (parent HITL).
- After **Build**: next is Smoke (`my-test-subflow` smoke), then `my-review-subflow` (unless parent orchestrates).
- After **Fix-from-tests**: re-run the same test mode (smoke or full).

## Start checklist

1. Confirm mode + required files. Check whether planned tests exist before launching 04a.
2. Resolve Medium + Fast models.
3. TDD review (or skip) → Gate B. Build → draft. Fix → repair from log.
