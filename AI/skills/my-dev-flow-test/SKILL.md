---
name: my-dev-flow-test
description: >-
  Supports smoke mode (build + unit; Mode full + profile full requires independent
  Smoke / re-run before Adv; Mode simple / Mode full + profile lite usually skip
  when Build already wrote smoke-pass via Build-writes-Smoke), full mode as one
  Task (coverage + missing e2e + build/unit/e2e), and lite mode (targeted e2e
  after lite review). Use when the user says run my-dev-flow-test, smoke tests,
  smoke re-run, verify before merge, after Build, or after my-dev-flow-review is
  clean before merge.
---

# my-dev-flow-test

Test subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Proves the draft is
worth reviewing (smoke) and matches requirements before merge (full/lite).

**Owned stages:** [stages.md](stages.md) index — load **`stages/<stage-id>.md` only** via parent-next / handoff (`smoke`, `test-full`, `test-lite`)

**Shared SoT (do not restate Happy path):**

| Concern | File |
|---------|------|
| Pipeline order / Status | [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) |
| Verify commands + Smoke after Build (Build-writes-Smoke) | [`../my-dev-flow/verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) |
| Gate C test bar | [`../my-dev-flow/hitl-gate-c.md`](../my-dev-flow/hitl-gate-c.md) |
| skip-review legality | [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) |
| Stage handoffs | **Required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` · [handoffs.md](../my-dev-flow/handoffs.md) = edit SoT / debug only |
| Models (all test = Fast) | [`../my-dev-flow/models.md`](../my-dev-flow/models.md) |
| Max rounds / Decision N | [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) |
| Test log template | [`../my-dev-flow/artifacts/06-test-log.md`](../my-dev-flow/artifacts/06-test-log.md) |

## When to run

`run my-dev-flow-test`, smoke re-run, or when parent reaches smoke / test after Build or review clean.

## Principles (owned here)

- Route by Review profile / skip-review legality: parent [`stages.md`](../my-dev-flow/stages.md) · [`lenses.md`](../my-dev-flow/lenses.md) · [`hitl-gate-c.md`](../my-dev-flow/hitl-gate-c.md).
- **Smoke Task:** Mode **full** + profile **full** → required independent re-run before Adv (E1). Mode simple / Mode full + profile **lite** → skip when Build-writes-Smoke smoke-pass — [`verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) · [`stages.md`](../my-dev-flow/stages.md) Mode×profile table.
- **Use Verify commands** from `00-run.md`. Do **not** invent a test stack.
- **test-full = one Task** (coverage → missing e2e → suite).
- Product fixes → [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md). Do **not** open Gate C from this skill.
- Result tokens: [`results.md`](../my-dev-flow/results.md). Max 3 test↔Fix rounds → Decision N ([`invariants.md`](../my-dev-flow/invariants.md)).

## Models

[`models.md`](../my-dev-flow/models.md) — all test stages = Fast.

## Prerequisites

- Draft code exists (after Build / review fixes).
- Prefer Verify commands set on `00-run.md`.
- Prefer `03-design.md` / `04-tasks.md` for full-mode success criteria.
- Create `06-test-log.md` from template if missing.

If there is no code to test → **stop**.

## Pipeline

```
smoke (E1 / re-run):  Verify commands → build + unit → Smoke section → smoke-pass | smoke-fail
test-lite:            targeted e2e (+ unit if needed) → success | failure
test-full (one Task): coverage → add missing e2e → build+unit+e2e → success | failure
```

Parent routes next steps (review / Gate C / Fix / merge) — see Happy path in [`stages.md`](../my-dev-flow/stages.md).

## Orchestrator rules

- Detect smoke vs full vs lite from parent ask / **Review profile**.
- Prefer **skip Smoke Task** when Build already wrote smoke-pass (Build-writes-Smoke) **except** Mode **full** + profile **full** (E1 requires independent Smoke / re-run).
- Legal skip-review ([lenses.md](../my-dev-flow/lenses.md)) → do **not** launch `test-full` / `test-lite`. Allow **`smoke` only** when Notes `smoke re-run` (or parent ordered recovery in [verify-and-fix.md](../my-dev-flow/verify-and-fix.md)); otherwise parent → Gate C when fail-closed escape **+ provenance** met ([hitl-gate-c.md](../my-dev-flow/hitl-gate-c.md) · [hitl.md](../my-dev-flow/hitl.md)). Build-writes-Smoke alone is not enough.
- Fresh Task per stage; prompt from `stages/<stage-id>.md` only (index: [stages.md](stages.md)).
- On failure / smoke-fail → Fix-from-tests (code); re-run same mode only after verify-pass.
- Do not merge, push, or open Gate C.
- Skip-review + Smoke gap: ordered recovery in [verify-and-fix.md](../my-dev-flow/verify-and-fix.md).

## Start checklist

1. Confirm draft exists; init `06-test-log.md` if needed; detect smoke vs full vs lite vs skip.
2. Resolve Fast model; use Verify commands from `00-run.md`.
3. Run mode per `stages/<stage-id>.md` (see [stages.md](stages.md)) → write Result; return path.
