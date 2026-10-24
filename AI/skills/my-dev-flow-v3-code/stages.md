# Code Prefer cheat (solo)

**Negative guards / Smoke-Fix cheat only — not Prefer Next lookup.** First-match Prefer SoT = parent [derive-next.md](../my-dev-flow-v3/derive-next.md) + matching half ([derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) Pre-Build · [derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) Post-Build · defs halves).

### Pre-Build

| Ban when | Do not Prefer |
|----------|---------------|
| Notes `design-stale` / `design-backloop` (until clear rules) | `build` — Pre-Build parent half ([../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) · [../my-dev-flow-v3/gate-b.md](../my-dev-flow-v3/gate-b.md)) |
| Notes `design-backloop` ∧ Design clean ∧ **04a ok** ∧ ¬ **Gate B settled post-Notes** | clear→`build` — Prefer `gate-b` (parent) |
| Design clean ∧ **04a unpaid / dirty** | `build` / `gate-b` — Prefer `tdd-review` (parent) |
| Design clean ∧ **04a ok** ∧ ¬ Gate B settled | `build` — Prefer `gate-b` (parent) |
| Gate B settled alone after Build started | re-`build` — Post-Build owns Smoke / Fix |

### Post-Build (Smoke / Fix)

| Ban when | Do not Prefer |
|----------|---------------|
| Smoke fail / test-fail Fix ask ∧ Last stage ≠ `fix-tests` + verify-pass | Prefer-re-smoke / unpaid `smoke` — Prefer `fix-tests` first (parent) |
| **missing required api/db** | Prefer-re-smoke / unpaid `smoke` / Adv — Prefer `finalize-lens-plan` (parent) |

Full Prefer / unpaid bans: [../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md).
