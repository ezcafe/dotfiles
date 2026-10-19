# Code Prefer cheat (solo)

**Negative guards / Smoke-Fix cheat only — first-match Prefer SoT is parent:** [derive-next.md](../my-dev-flow-v3/derive-next.md) + matching half ([derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) · [derive-next-post.md](../my-dev-flow-v3/derive-next-post.md)). Not Prefer Next lookup.

### Pre-Build

| When | Prefer |
|------|--------|
| Notes `design-stale` / `design-backloop` | **Ban** Prefer `build` — Pre-Build parent half only ([../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md)) |
| Notes `design-backloop` ∧ Design clean ∧ **04a ok** ∧ ¬ **Gate B settled post-Notes** | `gate-b` (parent) — not clear→`build` |
| Design clean ∧ **04a unpaid / dirty** | `tdd-review` |
| Design clean ∧ **04a ok** ∧ ¬ Gate B settled | `gate-b` (parent) |
| Notes `design-backloop` ∧ Design clean ∧ **04a ok** ∧ **Gate B settled post-Notes** | Parent clears Notes → then Prefer `build` |
| **Pre-Build** ∧ Design clean ∧ **04a ok** ∧ Gate B settled (Notes cleared) | `build` |

Do **not** Prefer `build` from Gate B settled alone after Build has started — Post-Build rows below own Smoke / Fix. Do **not** Prefer `build` while Notes `design-stale` / `design-backloop` (until clear rules — parent half SoT; Mode simple auto settle must not Prefer `build` until **Gate B settled post-Notes** clear — [../my-dev-flow-v3/gate-b.md](../my-dev-flow-v3/gate-b.md)).

### Post-Build (Smoke / Fix first)

| When | Prefer |
|------|--------|
| Smoke fail / test-fail Fix ask (**only when** Last stage ≠ `fix-tests` + verify-pass) | `fix-tests` |
| After Last stage `fix-tests` + verify-pass ∧ Smoke fail/unpaid ∧ ¬ **missing required api/db** | Prefer-re-smoke `smoke` |
| E1 / skip-review Smoke unpaid (**not** smoke-fail) ∧ ¬ **missing required api/db** | unpaid `smoke` |

Full Prefer / unpaid bans (Post-Build): [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md).
