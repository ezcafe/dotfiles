# API contract review

**Stage id:** `api-contract-review`  
**When:** Mode **full**, Has API ∈ {yes, unknown} (not tiny / ¬Notes `tiny-contract-tweak`).  
**Skills:** `{api-and-interface-design}/SKILL.md` (+ `reference.md` when useful).

**Allowed Results** (FIRST LINE of `03a-api-contract-review.md`):

| Token | Meaning |
|-------|---------|
| `clean` | Zero Critical/Major — paid |
| `needs update` | Critical/Major open — Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update`; **allowed to write** |
| `skipped` | Has API = no or Notes `tiny-contract-tweak` — never invent empty file to skip (`unknown` ≠ skip) |
| `pending` | Unpaid / invalidated |

Prefer unpaid sibling `db-design-review` if parallel; then `design-review` when both paid.

**After:** `needs update` → Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update` (parent pays Run-log only after Task complete — [../../my-dev-flow-v3/design-backloop.md](../../my-dev-flow-v3/design-backloop.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §7).

## FIRST

1. ¬ **Design present** → `Result: blocked — Design not present` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md)).  
2. **Grill open** → `Result: blocked — Grill open` ([../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md) · [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps).  
3. Notes `design-stale` → `Result: blocked — design-stale` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps).  
4. **design-update unpaid** → `Result: blocked — design-update unpaid` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md)).  
5. Else proceed.
