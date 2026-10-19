---
name: my-dev-flow-v3-design-review
description: >-
  Reviews design artifacts. Mode full: isolated API∥DB when unpaid (missing or
  Result unpaid/pending — Prefer re-run even if files exist; both unpaid →
  same-turn parallel) then general design-review. Mode simple: design-verify-phase.
  Use when run my-dev-flow-v3-design-review or after design before Build.
---

# my-dev-flow-v3-design-review

**Orchestrator SoT:** Isolated unpaid, Design clean — `../my-dev-flow-v3/derive-next.md` · `results.md`.

## Stages

| Id | File |
|----|------|
| api-contract-review | [stages/api-contract-review.md](stages/api-contract-review.md) |
| db-design-review | [stages/db-design-review.md](stages/db-design-review.md) |
| design-review | [stages/design-review.md](stages/design-review.md) |
| design-verify-phase | [stages/design-verify-phase.md](stages/design-verify-phase.md) |

## Principles

1. Unpaid = missing **or** Result ≠ `clean` (incl. `pending`). Prefer re-run even if files exist.  
2. Both unpaid → same-turn parallel; resume Prefer only unpaid sibling.  
3. Do not deep-re-review paid isolated Results.  
4. Never write Gate B consent.
