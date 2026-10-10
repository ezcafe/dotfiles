---
name: my-dev-flow-code
description: >-
  Optionally reviews planned TDD test cases before Gate B when 04-tasks lists
  real tests to create; then builds approved design tasks with TDD after Gate B
  using a fast model. Build and Fix must pass a Verify gate (Verify commands;
  max 3 attempts; Result verify-pass first line). Build writes the Smoke section
  so the parent can skip the Smoke Task (Option B). Also fixes failures from
  my-dev-flow-test when 06-test-log.md reports smoke-fail or failure. Produces a
  draft only — no merge or self-approval. Use when the user says run
  my-dev-flow-code, build from design, fix from test failures, TDD test-case
  review, or after my-dev-flow-design-review is clean / Gate B is approved.
---

# my-dev-flow-code

Build subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md).

- **TDD test-case review** runs **before Gate B** only when `04-tasks.md` has planned test cases.
- **Build** runs **after Gate B**, passes **Verify gate**, writes Smoke section (Option B).
- **Fix-from-tests** repairs [`my-dev-flow-test`](../my-dev-flow-test/SKILL.md) failures and must **verify-pass** before re-test.

**Details:** [stages.md](stages.md) · shared [`../my-dev-flow/verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) · handoffs [`../my-dev-flow/handoffs.md`](../my-dev-flow/handoffs.md)

## When to run

`run my-dev-flow-code`, build from design, TDD test-case review, fix from test failures, or when
`my-dev-flow` reaches Step 4a (before Gate B), Step 4 Build (after Gate B), or Test↔Code loop.

## Principles

- First Build output is a draft, not a deliverable.
- **TDD test-case review before Gate B (conditional):** Run only if `04-tasks.md` creates planned tests. Otherwise skip — note `04a skipped — no planned test cases` in `00-run.md`.
- **Build after Gate B only** (when parent is `my-dev-flow`). Gate B may be HITL **auto**.
- TDD: Red → Green → Refactor → Verify (when tasks include tests).
- **Verify gate:** Follow [`verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) — Verify commands on `00-run.md`, max 3 attempts, first return line `Result: verify-pass | verify-fail`.
- **Smoke Option B:** On verify-pass, write `06-test-log.md` Smoke section; parent skips Smoke Task by default.
- **Build when Has UI:** match Design UI specs + existing app chrome.
- Fix-from-tests: only `06-test-log.md` fix ask + design/tasks; then Verify gate.
- Stage-scoped handoffs (`tdd-review`, `build`, `fix-tests`). Plain words.

## Models

Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models** (TDD review = mechanical; Build/Fix = Fast).

## Prerequisites

**TDD test-case review** (before Gate B) — only when tests are planned:

- `03-design.md` and `04-tasks.md` present with concrete planned test cases
- Prefer `03a` Result **clean** when present
- Gate B is **not** required yet

**Build mode** (after Gate B):

- Gate B checked in `00-run.md`
- Prefer `04a` present **or** Notes say 04a skipped
- `03-design.md` and `04-tasks.md` present
- **Verify commands** set on `00-run.md` (not empty)

**Fix-from-tests mode:**

- `06-test-log.md` with **Result: smoke-fail** or **failure** and Fix ask
- Prefer Gate B already checked; Verify commands set

If the requested mode’s files are not ready → **stop**.

## Pipeline

```
TDD review (if planned):  TDD review → Gate B → Build
No planned tests:         skip 04a → Gate B → Build
Build:                    TDD → Verify gate → write Smoke → verify-pass → parent skips Smoke (Option B)
Fix-from-tests:           Fix → Verify gate → verify-pass → re-run smoke or full/lite
```

## Orchestrator rules

- Detect mode: no planned tests → skip 04a; `06-test-log` failure → fix-from-tests; else Build (require Gate B when parent is my-dev-flow).
- Fresh Task per stage.
- After Build **verify-pass**: skip Smoke Task unless Notes `smoke re-run` or Smoke section incomplete.
- After Fix **verify-pass**: re-run the same test mode. After 3 verify-fail attempts → Decision N.
- Persist Last Verify + attempts on Orchestrator card.

## Start checklist

1. Confirm mode + required files + Verify commands (for Build/Fix).
2. Resolve Medium + Fast models from allowlist.
3. TDD review (or skip) → Gate B → Build/Fix per stages.md.
