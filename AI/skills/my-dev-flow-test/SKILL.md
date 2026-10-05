---
name: my-dev-flow-test
description: >-
  Supports smoke mode (build + unit before code review), full mode (coverage,
  missing e2e, build, unit, e2e), and lite mode (targeted e2e after lite review).
  Use when the user says run my-dev-flow-test, smoke tests, verify before merge,
  after Build (smoke), or after my-dev-flow-review is clean before merge.
---

# my-dev-flow-test

Test subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Proves the draft
is worth reviewing (smoke) and matches requirements before merge (full).

**Details:** [stages.md](stages.md) · handoffs [`../my-dev-flow/handoffs.md`](../my-dev-flow/handoffs.md) · templates [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md)

## When to run

- **Smoke:** after Build, **before** review (`run my-dev-flow-test smoke`, or parent Step 4s). Also last gate before Gate C when Review profile is **skip-review**.
- **Lite:** after lite review clean (`run my-dev-flow-test lite`) — targeted e2e only; skip coverage Task and “add missing e2e” unless `04-tasks` requires new e2e.
- **Full:** after full review clean, before Gate C (`run my-dev-flow-test`, verify before merge)

## Principles

- **Smoke before review** — do not burn review cycles on a draft that fails build/unit.
- **Honor Review profile** — full → full suite; lite → targeted e2e; skip-review → smoke then Gate C (no further test Tasks).
- **Full before merge** (profile full) — coverage + e2e + runs; do not skip to Gate C while red.
- **Use the repo’s commands.** Do not invent a new test stack.
- **Fill e2e gaps** in full mode only (lite: only if tasks require new e2e).
- **Generation ≠ verification.** Product fixes go to [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md).
- Stage-scoped handoff (`smoke`, `test-full`, `test-lite`, `fix-tests`).
- Plain words in `06-test-log.md`.

## Models

Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models** (all test stages = Fast).

## Prerequisites

- Draft code exists (after Build / review fixes).
- Prefer `03-design.md` / `04-tasks.md` for full mode success criteria.
- Prefer Gate B checked when parent is `my-dev-flow`.
- Full mode: prefer review lenses clean (`05-review-log.md`) when parent runs full pipeline.
- Create `06-test-log.md` from templates if missing.

If there is no code to test → **stop**.

## Pipeline

### Smoke mode

```
Run build + unit (Fast) → write Smoke section in 06-test-log.md
→ Result: smoke-pass | smoke-fail
```

Do **not** require e2e or coverage in smoke mode.

### Lite mode

```
Run targeted e2e (and unit if not already smoke-pass) (Fast)
→ Skip coverage Task and “add missing e2e” unless 04-tasks requires new e2e
→ Result: success | failure
```

### Full mode

```
Coverage check (Fast)
→ Add missing e2e (Fast) if gaps
→ Run build + unit + e2e (Fast)
→ Result: success | failure
```

## Exit rule

| Result | Meaning | Next (parent my-dev-flow) |
|--------|---------|---------------------------|
| **smoke-pass** | Build + unit green | `my-dev-flow-review` (or Gate C if skip-review) |
| **smoke-fail** | Build or unit red | Fix-from-tests → re-smoke |
| **success** | Full or lite suite green; no open requirement gaps | Gate C → `my-dev-flow-merge` |
| **failure** | Full suite red or required e2e missing/blocked | Fix-from-tests → re-full |

## Failure handoff (required)

On **smoke-fail** or **failure**, `06-test-log.md` must include commands, failing tests, short excerpts, and Fix ask for `my-dev-flow-code`.

## Orchestrator rules

- Detect smoke vs full vs lite from parent ask / **Review profile**.
- One stage at a time; Task **`description`**: `Smoke build and unit` | `Test coverage check` | `Add missing e2e` | `Run build and tests` (lite: skip coverage/add-e2e unless required).
- Do not merge, push, or open Gate C.
- Product/unit fixes belong in `my-dev-flow-code` (except adding missing e2e in full mode).
- Cap: max **3** test↔fix rounds per mode, then pause.

## Start checklist

1. Confirm draft exists; init `06-test-log.md` if needed; detect smoke vs full.
2. Resolve Fast model.
3. Smoke: build+unit → smoke-pass/fail. Lite: targeted e2e. Full: coverage → e2e → suite → success/failure.
