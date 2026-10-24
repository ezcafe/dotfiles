# Fix-review

Fix review / lens findings. Preserve behavior when simplifying. Verify gate max 3 — [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/decisions.md](../../my-dev-flow-v3/decisions.md).

Modes: Adv/Quality dirty; `merged-lenses` / `plan-1-lens` when lens Result = `needs fix`.

## After

Return `Result: verify-pass` \| `verify-fail` only — **Hard stop** — do **not** Prefer Next / write card fields. **Orchestrated:** parent stamps `Last Verify` / `Last verify-pass at` / `Last verify settle-gen` from Result. **Labeled solo:** stamps verify fields when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §8). Parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md)).

### Ban-when (Task / solo cheat — not Prefer Next lookup)

| Ban when | Do not Prefer |
|----------|---------------|
| planned lens Result = `needs fix` (pre-fix) | `merge-findings` / `test-*` / `gate-c` / `merge` — Prefer `fix-review` (**parent**) |
| verify-pass ∧ Mode `merged-lenses`\|`plan-1-lens` | invent paid lenses — parent re-unpays + re-derives |
