# my-dev-flow-v2-design-review stages (index)

**Owned stage ids:** `api-contract-review`, `db-design-review`, `design-review`, `design-verify-phase`.

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task.

Stage-scoped handoff: compose from `{my-dev-flow-v2}/handoffs.md` (base block + R/W + Description). Paths: `{my-dev-flow-v2}/skills-path.md`.
Tiny tweak fold: `{my-dev-flow-v2}/lenses.md`. Models: `{my-dev-flow-v2}/models.md`.  
Parent Happy path: `{my-dev-flow-v2}/stages.md`. Templates: `{my-dev-flow-v2}/artifacts/INDEX.md`.  
Severity: `{my-dev-flow-v2}/severity.md`.

## Happy-path pointers

| Mode | Order |
|------|-------|
| **full** | Has API **and** Has DB (not tiny): both `03a-*` missing → `api-contract-review` ∥ `db-design-review` (**same-turn** parallel); one `03a-*` exists → launch **missing only** (resume serialize) → `design-review` |
| **full** | API or DB only → that isolated stage → `design-review` |
| **simple** | `design-verify-phase` only |

## Per-stage prompts

| Stage id | File |
|----------|------|
| `design-verify-phase` | [stages/design-verify-phase.md](stages/design-verify-phase.md) |
| `api-contract-review` | [stages/api-contract-review.md](stages/api-contract-review.md) |
| `db-design-review` | [stages/db-design-review.md](stages/db-design-review.md) |
| `design-review` | [stages/design-review.md](stages/design-review.md) |
