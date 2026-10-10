---
name: my-dev-flow-test
description: >-
  Supports smoke mode (build + unit; usually skipped when Build already wrote
  smoke-pass via Verify gate Option B), full mode as one Task (coverage + missing
  e2e + build/unit/e2e), and lite mode (targeted e2e after lite review). Use when
  the user says run my-dev-flow-test, smoke tests, smoke re-run, verify before
  merge, after Build, or after my-dev-flow-review is clean before merge.
---

# my-dev-flow-test

Test subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Proves the draft
is worth reviewing (smoke) and matches requirements before merge (full/lite).

**Details:** [stages.md](stages.md) · Verify commands [`../my-dev-flow/verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) · handoffs [`../my-dev-flow/handoffs.md`](../my-dev-flow/handoffs.md)

## When to run

- **Smoke:** only when parent needs a **re-run** (Build did not write smoke-pass, mismatch, or Notes `smoke re-run`). Default after Build verify-pass: **skip** Smoke Task (Option B). Also Gate C bar for **skip-review** is Build verify-pass — no Smoke Task required.
- **Lite:** after lite review clean — targeted e2e; skip coverage / add-e2e unless `04-tasks` requires new e2e.
- **Full:** after full review clean, before Gate C — **one** `test-full` Task (not three).

## Principles

- **Honor Review profile** — full → `test-full` (one Task); lite → `test-lite`; skip-review → Gate C on Build verify-pass (no further test Tasks).
- **Use Verify commands** from `00-run.md` (same as Build/Fix). Do not invent a new test stack.
- **Fill e2e gaps** inside `test-full` only (lite: only if tasks require new e2e).
- **Generation ≠ verification.** Product fixes go to [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md). Full/lite re-run build+unit(+e2e) independently after review.
- Stage-scoped handoff (`smoke`, `test-full`, `test-lite`, `fix-tests`).
- Plain words in `06-test-log.md`.

## Models

Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models** (all test stages = Fast).

## Prerequisites

- Draft code exists (after Build / review fixes).
- Prefer Verify commands set on `00-run.md`.
- Prefer `03-design.md` / `04-tasks.md` for full mode success criteria.
- Create `06-test-log.md` from templates if missing.

If there is no code to test → **stop**.

## Pipeline

### Smoke mode (re-run only)

```
Use Verify commands → Run build + unit → write Smoke section
→ Result: smoke-pass | smoke-fail
```

### Lite / Full

- **lite** (`test-lite`): targeted e2e (+ unit if needed).
- **full** (`test-full`): **one** Task — coverage → add missing e2e → build+unit+e2e using Verify commands.

## Exit rule

| Result | Meaning | Next (parent my-dev-flow) |
|--------|---------|---------------------------|
| **smoke-pass** (from Build or Smoke Task) | Build + unit green | `my-dev-flow-review` (or Gate C if skip-review) |
| **smoke-fail** | Build or unit red | Fix-from-tests → verify-pass → re-smoke |
| **success** | Full or lite suite green | Gate C → `my-dev-flow-merge` |
| **failure** | Suite red or required e2e missing | Fix-from-tests → verify-pass → re-full/lite |

## Orchestrator rules

- Detect smoke vs full vs lite from parent ask / **Review profile**.
- Prefer **skip Smoke Task** when Build already wrote smoke-pass matching Verify commands.
- Cap: max **3** test↔fix rounds per mode, then pause.
- Do not merge, push, or open Gate C.

## Start checklist

1. Confirm draft exists; init `06-test-log.md` if needed; detect smoke vs full vs skip.
2. Resolve Fast model; use Verify commands from `00-run.md`.
3. Run mode → success/failure or smoke-pass/fail.
