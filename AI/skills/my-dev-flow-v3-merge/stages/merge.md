# Merge

## Hard rules

0. Abort (`Result: aborted`) if ¬ Tests success (incl. unpaid stale Notes), **Lenses dirty**, **missing required api/db**, ¬ **Lenses clean**, or `merge` ∉ Gate C approved when performing merge — match parent Unsafe jumps ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).  
1. Only perform actions named in Gate C approved.  
2. Never force-push. Never invent approval.  
3. **Never write Status** (orchestrated Task — parent-only — [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md)). After actions: return `Result` + `candidate Status: done|paused` only.  
   - Merge success **and** `merge` ∈ approved → `Result: success` + `candidate Status: done`  
   - PR-only / remaining Gate C without merge complete → `Result: success` (or path-complete token) + `candidate Status: paused`  
   - Abort → `Result: aborted` (no Status candidate unless parent should pause — prefer parent Decision N / `stopped`)

## After (parent / labeled solo as orchestrator)

**Orchestrated:** parent stamps Status from `candidate Status` ([../../my-dev-flow-v3/step-0.md](../../my-dev-flow-v3/step-0.md) After Task · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §8). **Labeled solo:** stamps Status when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md)). Prefer must **not** re-Prefer `merge` when Last=`merge` ∧ Result=`success` (or Status `done`) — [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md).
