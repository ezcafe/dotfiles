# Fix-tests

Fix smoke-fail / test-fail. Prefer this stage **before** Prefer re-smoke / re-test ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)). Verify gate max 3 — [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/decisions.md](../../my-dev-flow-v3/decisions.md).

## After

Return `Result: verify-pass` \| `verify-fail` only — **Hard stop** — do **not** Prefer Next / cross skill / write card fields. Never stage-clear lifecycle Notes — return `candidate clear review-stale` only when skip-review clear applies. **Orchestrated:** parent stamps `Last Verify` / `Last verify-pass at` / `Last verify settle-gen` from Result; parent clears lifecycle Notes from candidates. **Labeled solo:** stamps verify fields / clears lifecycle when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §8). Parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md)).

### Ban-when (Task / solo cheat — not Prefer Next lookup)

| Ban when | Do not Prefer |
|----------|---------------|
| verify-pass ∧ **missing required api/db** | Prefer-re-smoke / unpaid `smoke` / Adv — Prefer `finalize-lens-plan` (**parent**) |
| Smoke fail unpaid ∧ Last ≠ `fix-tests` + verify-pass | Prefer-re-smoke / unpaid `test-*` — Prefer `fix-tests` first (**parent**) |
| stay on `fix-tests` after verify-pass | continue — parent re-derives |
