# Golden: design-backloop after Build

**Trigger:** Build/Fix cannot stay aligned with `03`/`04` without contract or IA change.  
**Parent actions** ([design-backloop.md](../design-backloop.md)):

1. Decision N: Amend design · Fix-only · Stop. Prefer Amend when contracts/IA must change.
2. Notes `design-backloop`; **Gate B approved: none**; **Build armed: none**; clear veto-window tokens; **clear** `gate-b auto — <HH:MM>` (or digest) if present; set **Last Verify: pending**; **Last verify-pass at: none**; invalidate prior overall `03a` **clean** **and** isolated `03a-api` / `03a-db` **clean** when present (pending / unpaid); Next `design-update`.
3. Prior `05`/`06` Results → Notes `review-stale` / `test-stale` ([verify.md](../verify.md) Stale) — keep stale Notes when resetting Last Verify; under **skip-review**: clear `review-stale` (N/A); keep `test-stale` until fresh `Smoke source: Smoke-Task` after a **new** **Last verify-pass at**. **lite/full:** keep until Lite/full clear (Run-log Adv+Quality / `code-review-phase` after **Last verify-pass at**; `06` **Updated** or Run-log `test-*` after that + success + matching path).
4. Resume: **Pre-Build** Prefer unpaid `design-update` (entry; leftover verify-pass is not fresh for current settle). Then Prefer by Mode ([design-backloop.md](../design-backloop.md) · [derive-next-pre.md](../derive-next-pre.md)):
   - **Mode full:** Prefer re-run API∥DB while Isolated API/DB unpaid (**even if files exist**) → `design-review` until fresh clean.
   - **Mode simple:** Prefer `design-verify-phase` only (no API∥DB Prefer) until fresh clean.
   Then Gate B again (auto: rewrite design-scoped `gate-b auto` token same turn → Prefer `build`) → clear Notes **same turn** as re-settle → Fix/Build.
5. Clear `design-backloop` only after design re-clean **and** Gate B re-settled (**same turn**); keep `review-stale` / `test-stale` until Lite/full clear ([verify.md](../verify.md) Stale) (skip-review: Prefer paid only after stale Notes cleared).

**Do not:** Prefer `gate-b` / `build` on a stale prior overall **or** isolated `03a*` **clean** while Notes still say `design-backloop`; leave Notes set after Gate B re-settle; launch Build before Notes clear; silently rewrite `03`/`04` inside Build/Fix; go to Gate C with a known design mismatch; Prefer paid under skip-review while `test-stale` remains.
