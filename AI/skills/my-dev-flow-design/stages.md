# my-dev-flow-design stages (index)

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task (do not load this whole package of prompts).

Stage-scoped handoff: **required** `scripts/handoff-for.py <stage-id>` (`{my-dev-flow}/handoffs.md` = edit SoT / debug only).  
Paths: `{my-dev-flow}/skills-path.md`. Models: `{my-dev-flow}/models.md`.  
Grill HITL: `{my-dev-flow}/hitl.md` + `{my-dev-flow}/grill.md`. Parent Happy path: `{my-dev-flow}/stages.md`.

Parent uses the **resolved** model for that stage’s tier (see `00-run.md`).

## Happy-path pointers

| Mode | Order (stage ids) |
|------|-------------------|
| **full** | `ideation` → `gate-a` → (`ideation-update` if needed) → `skim` → `analyze` → `grill` → `design` → (parent) design-review… |
| **simple** | `design-phase` only → (parent) design-verify-phase… |
| **update** | `design-update` → (parent) re-review |

Clarity: before Analyze / Grill / Design (full) or **design-phase entry** (simple) — [stages/clarity-check.md](stages/clarity-check.md).

## Per-stage prompts

| Stage id | File |
|----------|------|
| `ideation` | [stages/ideation.md](stages/ideation.md) |
| `gate-a` | [stages/gate-a.md](stages/gate-a.md) |
| `ideation-update` | [stages/ideation-update.md](stages/ideation-update.md) |
| `skim` | [stages/skim.md](stages/skim.md) |
| `design-phase` | [stages/design-phase.md](stages/design-phase.md) |
| `analyze` | [stages/analyze.md](stages/analyze.md) |
| `grill` | [stages/grill.md](stages/grill.md) |
| `design` | [stages/design.md](stages/design.md) |
| `design-update` | [stages/design-update.md](stages/design-update.md) |
| clarity (parent) | [stages/clarity-check.md](stages/clarity-check.md) |
