# Fix-review

Fix review / lens findings. Preserve behavior when simplifying. Verify gate max 3 — [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/decisions.md](../../my-dev-flow-v3/decisions.md).

Modes: Adv/Quality dirty; `merged-lenses` / `plan-1-lens` when lens Result = `needs fix`.

**After:** return `Result: verify-pass` \| `verify-fail` only — **parent stamps** `Last Verify` / `Last verify-pass at` / `Last verify settle-gen` ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §7). On verify-pass: Prefer re-run dirty verifier; Mode `merged-lenses`\|`plan-1-lens` → re-unpay planned lenses + Merged → Prefer re-lens ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).
