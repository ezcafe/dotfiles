# my-dev-flow-design-review stages (index)

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task.

Stage-scoped handoff: **required** `scripts/handoff-for.py <stage-id>` (`{my-dev-flow}/handoffs.md` = edit SoT / debug only). Paths: `{my-dev-flow}/skills-path.md`.  
Tiny tweak fold: `{my-dev-flow}/lenses.md`. Models: `{my-dev-flow}/models.md`.  
Parent Happy path: `{my-dev-flow}/stages.md`. Templates: `{my-dev-flow}/artifacts/INDEX.md`.  
Severity: `{my-dev-flow}/severity.md`.

## Happy-path pointers

| Mode | Order |
|------|-------|
| **full** | When both Has API+DB (not tiny): `api-contract-review` ∥ `db-design-review` (same turn) → `design-review` |
| **full** | API or DB only → that isolated stage → `design-review` |
| **simple** | `design-verify-phase` only |

## Per-stage prompts

| Stage id | File |
|----------|------|
| `design-verify-phase` | [stages/design-verify-phase.md](stages/design-verify-phase.md) |
| `api-contract-review` | [stages/api-contract-review.md](stages/api-contract-review.md) |
| `db-design-review` | [stages/db-design-review.md](stages/db-design-review.md) |
| `design-review` | [stages/design-review.md](stages/design-review.md) |
