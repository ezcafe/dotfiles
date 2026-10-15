---
name: my-dev-flow-code
description: >-
  Optionally reviews planned TDD test cases before Gate B when 04-tasks lists
  real tests to create; then builds approved design tasks with TDD after Gate B
  using a fast model. Build and Fix must pass a Verify gate (Verify commands;
  max 3 attempts; Result verify-pass first line). Build writes the Smoke section
  so the parent can skip the Smoke Task (Build-writes-Smoke). Also fixes failures from
  my-dev-flow-test when 06-test-log.md reports smoke-fail or failure. Produces a
  draft only — no merge or self-approval. Use when the user says run
  my-dev-flow-code, build from design, fix from test failures, TDD test-case
  review, or after my-dev-flow-design-review is clean / Gate B is approved.
---

# my-dev-flow-code

Build subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). First output is a **draft** — no merge or self-approval.

**Owned stages:** load **`stages/<stage-id>.md` only** (`tdd-review`, `build`, `fix-tests`) — index [stages.md](stages.md).

**Honor parent SoT** (do not restate Happy path / skip-review / veto mechanics here):

| Topic | File |
|-------|------|
| Runtime order | [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) |
| Verify / Smoke after Build (Build-writes-Smoke) / Fix | [`../my-dev-flow/verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) |
| Gate B veto / Build armed | [`../my-dev-flow/hitl.md`](../my-dev-flow/hitl.md) |
| skip-review legality | [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) |
| Design-backloop / max rounds | [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) |
| Result tokens | [`../my-dev-flow/results.md`](../my-dev-flow/results.md) |
| Handoffs / models | **Required** `scripts/handoff-for.py <stage-id>` · [`handoffs.md`](../my-dev-flow/handoffs.md) = edit SoT / debug only · [`models.md`](../my-dev-flow/models.md) |

## When to run

`run my-dev-flow-code`, build from design, TDD review, fix from test failures, or when parent reaches 4a / Build / Test↔Code.

## Principles (owned here)

- **TDD review before Gate B** only if `04-tasks` lists planned tests; else Notes skip.
- **Build after Gate B** (when parent is my-dev-flow). Re-read veto + Notes first — blocked tokens: [results.md](../my-dev-flow/results.md) / [hitl.md](../my-dev-flow/hitl.md).
- **Verify gate:** first line `Result: verify-pass | verify-fail`; max 3; on pass Build writes Smoke (Build-writes-Smoke).
- **Fix-from-tests:** repair from `06` Fix ask only; verify-pass before re-test.
- **Design-backloop** if `03`/`04` must change — never silently rewrite (invariants.md).
- TDD when tasks include tests. Has UI → match Design UI + chrome.
- Paste `scripts/handoff-for.py <stage-id>` output per Task; plain words.

## Models

[`models.md`](../my-dev-flow/models.md) — TDD = mechanical; Build/Fix = Fast.

## Prerequisites

| Mode | Need |
|------|------|
| **TDD review** | `03`+`04` with planned tests; Gate B not required yet |
| **Build** | Gate B checked; veto `none`; **Build armed** if async window open; Verify commands; prefer `04a` or Notes skip |
| **Fix-from-tests** | `06` smoke-fail/failure + Fix ask; Verify commands |

If not ready → **stop**.

## Pipeline

```
TDD (if planned) → Gate B → Build → Verify → Smoke (Build-writes-Smoke)
Fix-from-tests    → Fix → Verify → verify-pass → re-test
```

## Orchestrator rules

- Detect: no planned tests → skip 04a; `06` failure → fix-tests; else Build (require Gate B when parent is my-dev-flow).
- Advance only on **verify-pass**. Skip Smoke Task after Build-writes-Smoke unless Notes `smoke re-run`.
- After 3 verify-fail → Decision N (parent). Persist Last Verify on card.
- Post-Build routing (skip-review vs review): parent [stages.md](../my-dev-flow/stages.md) · [lenses.md](../my-dev-flow/lenses.md).

## Start checklist

1. Confirm mode + files + Verify commands.
2. Resolve models.
3. Run `stages/<id>.md` for TDD / Build / Fix.
