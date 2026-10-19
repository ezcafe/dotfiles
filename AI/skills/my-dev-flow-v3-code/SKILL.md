---
name: my-dev-flow-v3-code
description: >-
  Builds with TDD after Gate B settled. Iron law: no production code without a
  failing test first. Verify gate max 3. Fix failures from test/review. Draft
  only — no merge. Use when run my-dev-flow-v3-code or after Gate B.
---

# my-dev-flow-v3-code

Adapted from [obra TDD](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md).

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
| clarity-check | [stages/clarity-check.md](stages/clarity-check.md) |

## Prerequisites (Build)

Design clean; Gate B settled for **current settle gen** (auto: `gate-b auto — gen:<N>` after Design clean — [../my-dev-flow-v3/gate-b.md](../my-dev-flow-v3/gate-b.md)). Absence → `blocked — Gate B auto not settled` / settle stale.
