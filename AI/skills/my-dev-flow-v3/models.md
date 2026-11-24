# Models

Model selection guidelines for spawning subtasks in [`my-dev-flow-v3`](SKILL.md).
**Priority:** Explicit user choice > Stage soft guidelines > Faster tier default > `inherit` fallback.
**Task allowlist wins.** Routing SoT: [SKILL.md](SKILL.md) Routing table · [step-0.md](step-0.md) Load budget — models never override Prefer / Open 1–2 / [spawn-contract.md](spawn-contract.md) skill map.

## Stage Model Guidelines

When spawning a Task for a skill, select the model based on the entry stage (Expected Next):

| Tier | Used by Stages | Selection Guidance |
|------|----------------|--------------------|
| **Stronger** | `grill`, `adversarial` (`adv`), `design-review` (overall & isolated API/DB), `gate-a` (ideation / scope alignment), `design` | Pick a high-tier / deep-reasoning model from the available allowlist. Prefer `sonnet` (or `pro`) for low/medium complexity tasks. Only select `opus` for high/critical complexity tasks (e.g. mission-critical architectural shifts, complex distributed security, intricate migrations). |
| **Faster** | `build` (TDD code generation), standard test runs (`test-full`, `test-lite`), `smoke`, `merge`, `skim`, `fix-tests`, `fix-review`, and any stage where tier requirements are uncertain | Pick a fast/lightweight model from the allowlist (e.g. `flash`, `haiku`, `flash_lite`, `mini`). Default choice for implementation, test loops, and unassigned stages. |
| **Default / Inherit** | Explicit user request, or fallback when Faster hits quota / rate limits | Inherit the active parent model (`inherit` / omit model parameter). |

## Resolution Rules on Spawn

1. **User Override**: If the user explicitly named or requested a model, that choice wins unconditionally.
2. **Auto-Select by Stage**: If no model was specified by the user, select the model matching the entry stage's tier:
   - Use **Stronger** for architecture, grilling, and deep reviews (`grill`, `adv`, `design-review`, `gate-a`, `design`). Prefer `sonnet` for low/medium complexity tasks; only select `opus` for high/critical complexity tasks.
   - Use **Faster** for `build` (TDD code generation), standard test runs, `merge`, `smoke`, mechanical fixes, and any stage where tier requirements are uncertain.
3. **Fallback**: If a specific model tier hits usage limits, quota errors, or is unavailable, fall back to `inherit` (parent session model).

