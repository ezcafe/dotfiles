# Test Prefer cheat (solo)

**Negative guards only — not Prefer Next lookup.** First-match Prefer SoT = parent [derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) (+ [derive-next-defs-post.md](../my-dev-flow-v3/derive-next-defs-post.md) · [derive-next.md](../my-dev-flow-v3/derive-next.md) Unsafe jumps).

Split Smoke **fail** vs **unpaid** (F3 / [../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md](../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md) — never conflate).

| Ban when | Do not Prefer |
|----------|---------------|
| **missing required api/db** | Prefer-re-smoke / unpaid `smoke` / `test-*` / `gate-c` / `merge` — Hard stop; parent re-derives ([../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md)) |
| Smoke fail ∧ Last stage ≠ `fix-tests` + verify-pass | Prefer-re-smoke / unpaid `smoke` — Hard stop; parent re-derives |
| Lenses dirty / ¬ **Lenses clean** / ¬ Review clean | unpaid `test-*` / `gate-c` / `merge` |
| ¬ Tests success | `gate-c` / `merge` |
| Tests unpaid (lite/full) ∨ (`merge` ∉ Gate C approved) | `merge` |

Full Prefer: [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md).
