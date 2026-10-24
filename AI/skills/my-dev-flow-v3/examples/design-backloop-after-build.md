# Golden: design-backloop after Build

**Trigger:** Build/Fix cannot stay aligned with `03`/`04` without contract or IA change.  
**Parent **or** labeled solo as orchestrator** ([../design-backloop.md](../design-backloop.md) · [../solo-entry.md](../solo-entry.md) · [../hitl.md](../hitl.md)):

1. Notes `design-backloop` (parent **or** labeled solo; Stages return `candidate design-backloop` only); bump settle gen; clear consent; Last Verify pending; invalidate overall + isolated `03a*` → `pending`.  
2. Keep `review-stale` / `test-stale` (parent **or** labeled solo ownership).  
3. **Pre-Build:** Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update` while **Grill closed** **and** (**backloop rewrite unpaid** **or** any `03a*` **`needs update`**).
4. Parent **or** labeled solo pays rewrite same turn: Run-log `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** (not only `needs update` — same as Amend invalidate) — Prefer does not stick forever.
5. Then by Mode: **full** unpaid Isolated → `design-review`; **simple** `design-verify-phase` only.
6. Fresh Design clean ∧ **04a ok** (¬ unpaid / dirty — incl. ¬ planned tests present) → Gate B re-settle **after** Notes set: blocking/auto/async arm writes Run-log settle line **after** the Notes `design-backloop` line (or ISO stamp proves after) = **Gate B settled post-Notes** → parent **or** labeled solo clears Notes **same turn** → Prefer `build`. Without post-Notes Run-log settle → Prefer `gate-b` (even if an old settle still matches). Mode simple **auto** must **not** Prefer `build` until Notes cleared under that predicate ([../gate-b.md](../gate-b.md)).

**Assert:** clear→`build` requires a Run-log settle line ordered after Notes `design-backloop` (not gen-match alone).

**Do not:** Prefer `design-update` while **Grill open**; Prefer Isolated / design-review while design-update unpaid (**backloop rewrite unpaid**); Prefer `gate-b` / `build` on stale prior `clean`; Prefer clear→`build` on pre-Notes settle; auto Prefer `build` while Notes still set; leave Notes after post-Notes re-settle; Task-write lifecycle Notes.

**Not design-stale:** Upgrade path uses **design-stale unpaid** (clear after Mode-full `design` + `03` rewrite) — no design-update Run-log required.
