# Design-update

Rewrite design from review findings. Parent Prefer this stage when **Grill closed** **and** **design-update unpaid** (any `03a*` **`needs update`** **or** **backloop rewrite unpaid**) — before Isolated / design-review / design-verify. While **Grill open** → Prefer `grill` first ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/design-backloop.md](../../my-dev-flow-v3/design-backloop.md)).

## FIRST

1. Notes `design-stale` → `Result: blocked — design-stale` (unsafe-jump — Prefer **Grill open** → `grill` first, then Mode-full `design` + `03` rewrite — [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).  
2. **Grill open** → `Result: blocked — Grill open` (Prefer `grill` first — before `design-update` under Notes `design-backloop` / `needs update` — [../../my-dev-flow-v3/grill.md](../../my-dev-flow-v3/grill.md) · [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md)).  
3. Else proceed.

**After (parent):**  
1. Same-turn Run-log `design-update — settle-gen:<N>` (pays **backloop rewrite** for current Gate B settle gen).  
2. Same turn: set **ALL** `03a*` Results → **`pending`** (not only `needs update` — same as backloop / Amend invalidate).  
3. Mode **full:** Prefer unpaid Isolated API/DB (even if files exist / `pending`) → else `design-review`.  
4. Mode **simple:** Prefer `design-verify-phase` only.  

Return `proposed Has: …` / `Has flip detected` / `candidate tiny-contract-tweak` to parent — parent writes card Has + Notes via Always §4 ([../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/preflight.md](../../my-dev-flow-v3/preflight.md)).
