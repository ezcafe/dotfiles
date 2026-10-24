# Grill (Task)

Follow [../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md). Write rounds into `02b-grill.md`.

**HITL (orchestrated Task):** Parent-relay — never AskQuestion. Write the whole frontier into `02b` + Return `Blocked / questions for user`; hard-stop (`hitl:grill-frontier` or `hitl:grill-skip`). Parent presents answers / skip; re-spawns until Grill closed ([../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/spawn-contract.md](../../my-dev-flow-v3/spawn-contract.md)). **Solo:** settle frontier in chat same turn OK.

**Done when:** Grill closed — Definitions: [../../my-dev-flow-v3/derive-next-defs-pre.md](../../my-dev-flow-v3/derive-next-defs-pre.md) (**Grill closed**). Card Next stays `grill` until closed when artifacts present.  
**After:** **Orchestrated Task:** return `candidate grill-skip` only + Parent-relay — never write Notes or invent Result `skipped` as a waive. **Labeled solo:** stamps Notes `grill-skip` / preferred `grill skipped — <reason>` + provenance after AskQuestion ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md)).
