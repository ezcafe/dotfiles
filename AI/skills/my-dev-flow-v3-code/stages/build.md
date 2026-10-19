# Build

Verify gate max 3 — [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/decisions.md](../../my-dev-flow-v3/decisions.md).

## FIRST

1. ¬ Design clean / Verify clean → `Result: blocked — Design not clean` ([../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Before Build · [../../my-dev-flow-v3/results.md](../../my-dev-flow-v3/results.md)).  
2. **Grill open** → `Result: blocked — Grill open` ([../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md)).  
3. ¬ **04a ok** → `Result: blocked — 04a unpaid/dirty` ([../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Before Build).  
4. Notes `design-stale` / `design-backloop` → `Result: blocked — …`  
5. ¬ **Gate B settled** → `Result: blocked — Gate B not settled` ([../../my-dev-flow-v3/gate-b.md](../../my-dev-flow-v3/gate-b.md) — missing blocking approval+provenance, missing matching `gate-b auto — gen:<current>`, missing **Build armed** on async, gen mismatch).  
6. Else proceed.

## Do

1. TDD per task in `04-tasks.md`.  
2. Verify commands → `verify-pass` or `verify-fail`.  
3. On verify-pass: set `Smoke source: Build-verify` on `06` when writing Smoke section.

## After

Return `Result: verify-pass` \| `verify-fail` only — **parent stamps** `Last Verify` / `Last verify-pass at` (ISO-8601 Run-log local wall time) / `Last verify settle-gen` ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §7). On rebuild when prior review/test Results look paid: return `candidate review-stale` / `candidate test-stale` only — parent alone sets Notes ([../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)).
