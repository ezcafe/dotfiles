# Design review (general)

**Stage id:** `design-review`  
**When:** Mode **full** after Isolated API/DB paid when required. Mode **simple** uses `design-verify-phase`.  
**Skills:** project AGENTS / architecture docs; useful bits from myplan, planning-and-task-breakdown, documentation-and-adrs, security-and-hardening; when Has API/DB already paid via Isolated, do **not** deep-re-review those surfaces — flag cross-cutting gaps only. Point API/DB deep review at `{api-and-interface-design}` / `{database-and-data-model}` via Isolated stages.

**Allowed Results** (FIRST LINE of overall `03a-design-review-log.md`):

| Token | Meaning |
|-------|---------|
| `clean` | Zero Critical/Major **and** required Isolated paid (`clean`\|`skipped`) — parent may advance |
| `needs update` | Critical/Major open — Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)); **allowed to write** — do not force `clean` |
| `pending` | Unpaid / invalidated (Amend / Upgrade) |

**Advance-on-clean / Done when:** parent Prefer next pipeline stage only when overall Result is **`clean`** (and Design clean). Writing **`needs update`** is **allowed** ≠ Done — Prefer Grill-open → `grill` first else `design-update`, not invent clean.

## FIRST

1. ¬ **Design present** → `Result: blocked — Design not present` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md)).  
2. **Grill open** → `Result: blocked — Grill open` ([../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md) · [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps).  
3. Notes `design-stale` → `Result: blocked — design-stale` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) unsafe jumps).  
4. **design-update unpaid** → `Result: blocked — design-update unpaid` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/handoffs.md](../../my-dev-flow-v3/handoffs.md)).  
5. Else proceed.

Write overall `03a-design-review-log.md`. Respect Design clean (isolated paid when required). Never write Gate B consent.

**After:** `needs update` → Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update` (parent pays Run-log only after Task complete — [../../my-dev-flow-v3/design-backloop.md](../../my-dev-flow-v3/design-backloop.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md) Always §7). If **clean:** re-derive ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).
