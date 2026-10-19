# Merge

## Hard rules

0. Abort (`Result: aborted`) if ¬ Tests success (incl. unpaid stale Notes), **Lenses dirty**, **missing required api/db**, ¬ **Lenses clean**, or `merge` ∉ Gate C approved when performing merge — match parent Unsafe jumps ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).  
1. Only perform actions named in Gate C approved.  
2. Never force-push. Never invent approval.  
3. Status `done` only after merge success **and** `merge` ∈ approved. PR-only → stay `paused`.
