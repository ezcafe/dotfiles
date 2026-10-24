# Isolated subflows (Option B) — overview / narrative

**Goal:** Parent keeps a thin routing + HITL context. Heavy work runs in a **fresh** Cursor `Task` (`generalPurpose`, local) per **subflow skill**, so stage noise does not accumulate in the parent.

**Does not change:** Prefer / Unsafe jumps / Gate B·C / parent-only fields ([hitl.md](hitl.md)). Isolation is **how** stages run, not **which** Next wins. **Load-budget SoT** for map / Hard stop / Return = [spawn-contract.md](spawn-contract.md); After Task = [step-0.md](step-0.md) After Task (+ Always §8). This file is optional narrative — do **not** open it every turn to spawn.

## Parent vs Task

| Actor | Owns |
|-------|------|
| **Parent** | Step 0; routing pack; card `00-run.md`; Gate B / Gate C / `finalize-lens-plan`; all parent-only writes; **user-facing HITL** (Parent-relay — present Task questions, named yes); spawn/reap Tasks; After apply ([preflight.md](preflight.md) Always §4·§8) |
| **Task (subflow)** | Unpaid stages **inside one skill only**; artifact writes per [handoffs.md](handoffs.md); After **signals** only — never parent-only fields; **never AskQuestion** for HITL |

**Ban:** Parent executing a skill-mapped stage inline when orchestrating (except Decision N / failure recovery the user names). **Solo** subflow entry ([solo-entry.md](solo-entry.md)): the solo agent *is* the skill runner — no nested Task required; solo may AskQuestion / settle same turn.

## Skill map (Expected Next → skill)

**Full map SoT only:** [spawn-contract.md](spawn-contract.md) Skill map. **Parent-inline only:** Step 0, `gate-b`, `gate-c`, `finalize-lens-plan`. `api|db` both unpaid → two design-review Tasks same turn.

## Hard stop (Task must return)

**Paste SoT:** [spawn-contract.md](spawn-contract.md) Hard stop list (verbatim in every Task prompt). Index only — do **not** restate the body here:

1. Parent-only Next  
2. Skill boundary  
3. HITL / consent  
4. Candidate-apply  
5. Verify / failure cap  
6. Skill unpaid empty  

Do **not** cross skills, write parent-only fields, or AskQuestion for HITL ([spawn-contract.md](spawn-contract.md) · [hitl.md](hitl.md)).

**Example:** [examples/isolation-spawn-hardstop.md](examples/isolation-spawn-hardstop.md).

## Spawn contract (parent → Task)

**SoT:** [spawn-contract.md](spawn-contract.md) — Load budget §5 opens that file only (Hard stop list inlined there). Do not restate the full prompt contract here.

## After Task (parent)

**Checklist SoT:** [step-0.md](step-0.md) After Task (6 steps) + [preflight.md](preflight.md) Always §8. This section is optional narrative — do **not** open this file every turn for After apply.

**HITL re-entry:** [spawn-contract.md](spawn-contract.md) checklist — present Qs → stamp Notes → fresh Task same skill.

**Context rule:** Parent keeps signals + card + ≤5-line Run-log. Do **not** re-read Task tool transcripts as stage input on later turns.

## Models

Soft hints stay in [models.md](models.md). Parent may pass a stronger/faster model on spawn when the user asked for a specific model; otherwise omit (inherit).
