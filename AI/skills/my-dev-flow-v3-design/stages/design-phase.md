# Design-phase (Mode simple)

## FIRST

1. **ideation unpaid** → `Result: blocked — ideation unpaid` (Definition: [../../my-dev-flow-v3/derive-next-defs-pre.md](../../my-dev-flow-v3/derive-next-defs-pre.md)).  
2. **Grill open ∧ ¬ cold-start carve (mid-open)** → `Result: blocked — Grill open (mid-open)` — fail-closed for full **Grill open** when ¬carve; do **not** re-enter. Carve SoT: [../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md) cold-start carve · [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps · align [design.md](design.md) / [../../my-dev-flow-v3-design-review/stages/design-verify-phase.md](../../my-dev-flow-v3-design-review/stages/design-verify-phase.md).  
3. Else proceed.

Bundle Analyze + Grill + Design into `02`/`02b`/`03`/`04`.

**HITL (orchestrated Task):** Parent-relay for grill / Prefer-grill mid-open only inside the bundle — never AskQuestion. Write Qs into artifacts + Return `Blocked / questions for user`; hard-stop; parent re-spawns (Prefer `grill` mid-open, or continue `design-phase` when carve allows) after answers ([../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/spawn-contract.md](../../my-dev-flow-v3/spawn-contract.md)). Ideation must already be paid before this stage (FIRST). Do **not** invent Grill closed to finish in one Task. **Solo:** may settle grill in chat same turn.

Stamp `03` Result **`done`** only when Grill closed; while Grill open keep `03` Result **`pending`** / unset — do **not** stamp `done` from Design body alone ([../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md) · [../../my-dev-flow-v3/results.md](../../my-dev-flow-v3/results.md)).

**Done when:** design artifacts present (`02-analysis` + `03` + `04`) **and** Grill closed — Definitions: [../../my-dev-flow-v3/derive-next-defs-pre.md](../../my-dev-flow-v3/derive-next-defs-pre.md). Align [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md).

**After:** if **Grill open** ∧ ¬ cold-start carve → signal Prefer `grill` / mid-open (do not Prefer re-design-phase; keep `03` Result `pending`/unset) — **card Next** parent-written (orchestrated) or labeled solo when acting as orchestrator ([../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §2). **Orchestrated Task:** return `proposed Has: …` / `Has flip detected` / `candidate tiny-contract-tweak` / `candidate grill-skip` only + Parent-relay — parent writes card Has + Notes. **Labeled solo:** stamps Notes+provenance (e.g. `grill-skip`) after AskQuestion; applies Has / Next when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §4). Cold start carve — [../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md).
