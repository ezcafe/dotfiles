---
name: my-dev-flow-v3-code
description: >-
  Builds with TDD after Gate B settled. Iron law: no production code without a
  failing test first. Verify gate max 3. Fix failures from test/review. Draft
  only — no merge. Use when run my-dev-flow-v3-code or after Gate B.
---

# my-dev-flow-v3-code

Adapted from [obra TDD](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md).

## Solo FIRST

1. Min card: Mode, profile, Has flags, Gate B settle gen on `00-run.md`.  
2. Design clean before Build; unpaid bans: no Build while ¬ Gate B settled / Grill open / ¬ **04a ok** / `design-stale` / `design-backloop` (Build FIRST list — [stages/build.md](stages/build.md)). Post-Build: **missing required api/db** → Prefer `finalize-lens-plan` first (before Smoke **and** before Adv — [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md)).  
3. Parent-only ([../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)): never write Gate B/C, settle, waiver Notes, provenance, **lifecycle Notes** (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), or **card Has** — Stages return `candidate …` / `proposed Has` only.  
4. Derive Next: Prefer first-match SoT = parent [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) + matching half ([../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) Pre-Build · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) Post-Build). Local [stages.md](stages.md) = **negative guards / Smoke-Fix cheat only** — not Prefer Next lookup.  
5. Solo entry checklist: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Iron law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Red → verify fail → Green minimal → verify pass → Refactor. Delete code written before tests.

## Stages

| Id | File |
|----|------|
| tdd-review | [stages/tdd-review.md](stages/tdd-review.md) |
| build | [stages/build.md](stages/build.md) |
| fix-tests | [stages/fix-tests.md](stages/fix-tests.md) |
| clarity-check | [stages/clarity-check.md](stages/clarity-check.md) (stub → [../my-dev-flow-v3/clarity-check.md](../my-dev-flow-v3/clarity-check.md)) |

## Prerequisites (Build)

Design clean; **Gate B settled** ([../my-dev-flow-v3/gate-b.md](../my-dev-flow-v3/gate-b.md)):

- **blocking:** `Gate B approved` + provenance `gate-b-approved`, gen == current settle gen  
- **auto:** matching Notes/Run-log `gate-b auto — gen:<N>` (Mode **simple** only when API=no ∧ DB=no ∧ auth/PII/schema=no — explicit `no` only; `unknown` ≠ `no` — [../my-dev-flow-v3/gate-b.md](../my-dev-flow-v3/gate-b.md); **not** implied by Design clean alone)  
- **async:** **Build armed: yes** + Run-log arm for current settle gen  

Mode **full** Gate B is always **blocking**. Absence of a matching settle → `Result: blocked — Gate B not settled` (+ subtype `blocking` / `auto` / `async` / `stale`).

Post-Build Prefer / Fix → Smoke: [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md).
