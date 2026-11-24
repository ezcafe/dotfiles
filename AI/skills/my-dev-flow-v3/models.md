# Models

Model selection guidelines for spawning subtasks in [`my-dev-flow-v3`](SKILL.md).
**Priority:** Explicit user choice > Stage soft guidelines > `inherit`.
**Task allowlist wins.** Routing SoT: [SKILL.md](SKILL.md) Routing table · [step-0.md](step-0.md) Load budget — models never override Prefer / Open 1–2 / [spawn-contract.md](spawn-contract.md) skill map.

## Stage Model Guidelines

When spawning a Task for a skill, select the model based on the entry stage (Expected Next):

| Tier | Used by Stages | Selection Guidance |
|------|----------------|--------------------|
| **Stronger** | `grill`, `adversarial` (`adv`), `design-review` (overall & isolated API/DB), `gate-a` (ideation / scope alignment), `design` | Pick a high-tier / deep-reasoning model from the available allowlist (e.g. `pro`, `sonnet`, `opus`, thinking models). |
| **Faster** | `skim`, `smoke`, `test-lite`, mechanical `fix-tests` / `fix-review` (when diff/scope is tiny) | Pick a fast/lightweight model from the allowlist (e.g. `flash`, `haiku`, `flash_lite`, `mini`). |
| **Default / Inherit** | `build` (TDD implementation), standard `fix-tests`, full test runs, `merge`, or when uncertain | Inherit the active parent model (`inherit` / omit model parameter). |

## Resolution Rules on Spawn

1. **User Override**: If the user explicitly named or requested a model, that choice wins unconditionally.
2. **Auto-Select by Stage**: If no model was specified by the user, select the model matching the entry stage's tier from the available environment allowlist.
3. **Fallback**: If a specific model tier hits usage limits, quota errors, or is unavailable, fall back to `inherit` (parent session model).

