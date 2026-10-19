# Test-lite

## FIRST

1. **missing required api/db** → `Result: blocked — missing required api/db` (Prefer `finalize-lens-plan` — [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md)).
2. **Lenses dirty** **or** ¬ **Lenses clean** → `Result: blocked — Lenses dirty` / `blocked — ¬ Lenses clean` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) — covers Merged-unpaid dual-false).
3. ¬ **Review clean** → `Result: blocked — Review not clean` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/results.md](../../my-dev-flow-v3/results.md)).

Targeted e2e / suite. Set Test path `lite`.  
**After:** return `candidate clear test-stale` when Lite/full clear met — parent alone clears ([../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md)); Prefer merge|gate-c only when Tests success **and** **Lenses clean**.
