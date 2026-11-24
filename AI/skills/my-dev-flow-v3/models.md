# Models

Model selection guidelines for spawning subtasks in [`my-dev-flow-v3`](SKILL.md).
**Priority:** Explicit user choice > Stage designated model (never inherit from orchestrator) > Same-tier provider fallback.
**Task allowlist wins.** Routing SoT: [SKILL.md](SKILL.md) Routing table · [step-0.md](step-0.md) Load budget — models never override Prefer / Open 1–2 / [spawn-contract.md](spawn-contract.md) skill map.

## Core Rule: Independent Subagent Model Assignment

**Subagents must always use their own designated models and NEVER inherit from the orchestrator.**
Even if the parent orchestrator runs on a different model (e.g. `opus`, `pro`, or default session model), each subagent Task must be explicitly spawned with its dedicated stage model.

## Stage Model Guidelines

When spawning a Task for a skill, resolve and pass the designated model based on the entry stage (Expected Next):

| Tier | Used by Stages | Selection Guidance |
|------|----------------|--------------------|
| **Stronger** | `grill`, `adversarial` (`adv`), `design-review` (overall & isolated API/DB), `gate-a` (ideation / scope alignment), `design` | High-tier reasoning model. Prefer **`sonnet`** (or `pro`) for low/medium complexity tasks. Only select **`opus`** for high/critical complexity tasks (e.g. mission-critical architectural shifts, complex distributed security, intricate migrations). |
| **Faster** | `build` (TDD code generation), standard test runs (`test-full`, `test-lite`), `smoke`, `merge`, `skim`, `fix-tests`, `fix-review`, and any stage where tier requirements are uncertain | Fast/lightweight model from the allowlist (**`flash`**, **`haiku`**, **`flash_lite`**, **`mini`**). Subagent must run on this tier regardless of orchestrator model. |

## Resolution Rules on Spawn

1. **User Override**: If the user explicitly named or requested a model for the subagent, that choice wins unconditionally.
2. **Dedicated Stage Selection (Mandatory)**: Always assign and explicitly pass the stage's designed model tier:
   - Use **Stronger** for architecture, grilling, and deep reviews (`grill`, `adv`, `design-review`, `gate-a`, `design`). Prefer `sonnet` for low/medium complexity; only select `opus` for high/critical complexity.
   - Use **Faster** for `build` (TDD code generation), standard test runs, `merge`, `smoke`, mechanical fixes, and any unassigned/uncertain stages.
3. **No Orchestrator Inheritance**: Do **not** omit the model parameter or set `inherit`. The subagent must run on its own designated model tier, not the orchestrator's model.
4. **Fallback on Quota/Error**: If a designated model hits usage limits or quota errors, switch to an alternative model within the same tier (e.g., `flash` → `haiku` or `mini`; `sonnet` → `pro`), rather than falling back to the orchestrator model.

