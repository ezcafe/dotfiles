# Merge Prefer cheat (solo)

**Negative guards only — not Prefer Next lookup.** First-match Prefer SoT = parent [derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) (+ [derive-next.md](../my-dev-flow-v3/derive-next.md) Definitions / Unsafe jumps).

| Ban when | Do not Prefer |
|----------|---------------|
| **Lenses dirty** / **missing required api/db** / ¬ **Lenses clean** | `merge` / `gate-c` — parent Prefer `finalize-lens-plan` / `merge-findings` / re-lens per [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) |
| Unpaid stale Notes / ¬ Tests success | `merge` / `gate-c` |
| Tests unpaid (lite/full only; **vacuous** for skip-review) | `merge` on lite/full while unpaid — Gate C bar = **Tests success** ([../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md)), not `06` success alone |
| `merge` ∉ Gate C approved | `merge` — Prefer `gate-c` or stay `paused` |
| Approved subset without `merge` | stay `paused` / Prefer `gate-c` for remaining (parent) |

Full bar: [../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md) · [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md).
