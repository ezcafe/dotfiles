# Test-full

## FIRST

1. **missing required api/db** → `Result: blocked — missing required api/db` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md)).
2. **Lenses dirty** **or** ¬ **Lenses clean** → `Result: blocked — Lenses dirty` / `blocked — ¬ Lenses clean` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) — covers Merged-unpaid dual-false).
3. ¬ **Review clean** → `Result: blocked — Review not clean` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/results.md](../../my-dev-flow-v3/results.md)).

Coverage + e2e + suite as project defines. Set Test path `full`.  
**After:** return `candidate clear test-stale` when Lite/full clear met — **Hard stop**; do **not** Prefer Next / write parent-only fields (orchestrated Task). **Orchestrated:** parent clears Notes + re-derives. **Labeled solo:** clears Notes when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/gate-c.md](../../my-dev-flow-v3/gate-c.md)).
