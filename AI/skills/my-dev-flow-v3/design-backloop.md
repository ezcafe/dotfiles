# Design-backloop (design invalid after Build)

When Build/review proves design wrong (contracts/IA) — parent **or** labeled solo (acting as orchestrator) set Notes (Stages return `candidate design-backloop` only — [hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)):

1. Notes `design-backloop`  
2. Bump Gate B settle gen; clear consent tokens  
3. Last Verify pending; clear verify-pass stamp + Last verify settle-gen  
4. Invalidate overall + isolated `03a*` clean → `pending`  
5. Keep `review-stale` / `test-stale` (parent **or** labeled solo ownership — [hitl.md](hitl.md) · [solo-entry.md](solo-entry.md))  
6. Selector: always **Pre-Build** while Notes set  
7. **backloop rewrite unpaid** until parent **or** labeled solo (acting as orchestrator) pays design-update (below)

## Prefer (Expected Next = [derive-next.md](derive-next.md))

1. **Entry:** Prefer **Grill open** → `grill` first; then Prefer unpaid `design-update` while **Grill closed** **and** **design-update unpaid** = any `03a*` **`needs update`** **or** **backloop rewrite unpaid**.  
2. **Pay rewrite:** when `design-update` Task completes, parent **or** labeled solo (acting as orchestrator) same-turn:  
   - appends Run-log `- **HH:MM** · design-update — settle-gen:<N>` (`<N>` = current Gate B settle gen) — pays **backloop rewrite**  
   - sets **ALL** `03a*` Results → **`pending`** (not only `needs update` — same as Amend invalidate on step 4)  
   Together that clears **design-update unpaid** — Prefer does **not** stick on `design-update` forever.  
3. After design-update paid (no `03a*` still **`needs update`**; all `03a*` **`pending`** or re-paid):  
   - Mode **full:** Prefer unpaid Isolated API/DB (even if files exist / `pending`) → else `design-review`  
   - Mode **simple:** Prefer `design-verify-phase` only (no isolated Prefer stages)  

**Blocked while Grill open:** `design-update` / Isolated / `design-review` / `design-verify-phase` — Prefer `grill` first.  
**Blocked while backloop rewrite unpaid / design-update unpaid:** Isolated / `design-review` / `design-verify-phase` ([derive-next.md](derive-next.md) unsafe jumps · [preflight.md](preflight.md) · [handoffs.md](handoffs.md)).

Do **not** Prefer `gate-b` / `build` on stale prior `clean`. Do **not** Prefer clear→`build` on a pre-Notes Gate B settle.

**Not design-stale:** Notes `design-stale` uses **design-stale unpaid** / **design unpaid under design-stale** — defs [derive-next-defs-pre.md](derive-next-defs-pre.md) · [step-0.md](step-0.md). Parent **or** labeled solo (acting as orchestrator) sets/clears `design-stale` ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)).

## Clear Notes

Same turn **only** when Design clean ∧ **04a ok** (¬ unpaid / dirty — incl. ¬ planned tests present) **and** **Gate B settled post-Notes**:

**Gate B settled post-Notes (checkable):** durable settle token for **current** settle gen **and** a Run-log line for that settle that appears **after** the Notes `design-backloop` line (or ISO stamp on Notes vs Run-log proves after) — [derive-next.md](derive-next.md) · [gate-b.md](gate-b.md) Prefer gate-b (blocking/auto/async arm must write that post-Notes Run-log line). Then parent **or** labeled solo (acting as orchestrator) clears Notes `design-backloop` → Prefer `build` ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)).

While Notes set without post-Notes settle → Prefer `gate-b` (do **not** Prefer `build` / clear Notes on a pre-Notes or uncleared settle that still matches gen). **Mode simple auto** must **not** Prefer `build` the same turn as writing `gate-b auto — gen:<N>` until Notes cleared under this predicate ([derive-next-pre.md](derive-next-pre.md) Prefer clear→build vs Prefer `gate-b` rows).

## Stale clear after rebuild

Lite/full and skip-review clear rules: [verify.md](verify.md) Stale — parent **or** labeled solo (acting as orchestrator) clears `review-stale` / `test-stale` when those predicates hold ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)).
