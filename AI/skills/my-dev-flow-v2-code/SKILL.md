---
name: my-dev-flow-v2-code
description: >-
  Optionally reviews planned TDD test cases before Gate B; then builds design
  tasks with TDD after Gate B is settled. Build and Fix must pass a Verify gate
  (max 3 attempts; Result verify-pass first line). Build writes Smoke so the
  parent can skip the Smoke Task (Build-writes-Smoke). Also fixes failures from
  my-dev-flow-v2-test. Draft only — no merge. Use when the user says run
  my-dev-flow-v2-code, build from design, or fix from test failures.
---

# my-dev-flow-v2-code

Build subflow of [`my-dev-flow-v2`](../my-dev-flow-v2/SKILL.md). Draft only — no merge or self-approval.

**Owned stages:** `tdd-review`, `build`, `fix-tests` — load `stages/<id>.md` only.

| Topic | File |
|-------|------|
| Verify / Smoke / Fix | [`../my-dev-flow-v2/verify.md`](../my-dev-flow-v2/verify.md) |
| Gate B | [`../my-dev-flow-v2/gate-b.md`](../my-dev-flow-v2/gate-b.md) |
| Consent | [`../my-dev-flow-v2/hitl.md`](../my-dev-flow-v2/hitl.md) |
| Handoffs | compose from [`../my-dev-flow-v2/handoffs.md`](../my-dev-flow-v2/handoffs.md) |
| Models | [`../my-dev-flow-v2/models.md`](../my-dev-flow-v2/models.md) — Build/Fix = Fast |

## Principles

- TDD review only if `04-tasks` lists planned tests; else Notes skip.
- Build after Gate B settled. Re-read veto / approved / Build armed first.
- Advance only on **verify-pass**. Design-backloop if `03`/`04` must change.
- Build-writes-Smoke: parent may skip the Smoke Task **except** Mode **full** + profile **full** (E1 independent Smoke required — [verify.md](../my-dev-flow-v2/verify.md)).

## Prerequisites

| Mode | Need |
|------|------|
| TDD | `03`+`04` with planned tests |
| Build | Gate B settled; veto `none`; Verify commands; design clean |
| Fix-from-tests | `06` smoke-fail/failure + Fix ask |

## Start

1. Confirm mode + Verify commands.
2. Clarity-check ([stages/clarity-check.md](stages/clarity-check.md)); parent logs token.
3. Compose handoff; run `stages/<id>.md`.
