# Fix-tests

Fix smoke-fail / test-fail. Prefer this stage **before** Prefer re-smoke / re-test ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)). Verify gate max 3 — [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/decisions.md](../../my-dev-flow-v3/decisions.md).

## After

Return `Result: verify-pass` \| `verify-fail` only — **parent stamps** `Last Verify` / `Last verify-pass at` / `Last verify settle-gen` ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §7). Never stage-clear lifecycle Notes — return `candidate clear review-stale` only when skip-review clear applies ([../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) Stale).

**After verify-pass** (align [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) Last stage `fix-tests` row):

1. **missing required api/db** → Prefer `finalize-lens-plan` first (before Smoke **and** before Adv — [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)).  
2. Else Prefer-re-smoke `smoke` when Smoke unpaid/**fail** (Prefer-re-smoke eligible — even if `Smoke source` already `Smoke-Task` — [../../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md](../../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md)). Do **not** Prefer unpaid `test-*` while Smoke fail unpaid.  
3. Else Prefer unpaid `test-*` **only** if test-fail unpaid.  
4. Else continue (do **not** stay on `fix-tests`). Skip-review ordered recovery otherwise ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)).
