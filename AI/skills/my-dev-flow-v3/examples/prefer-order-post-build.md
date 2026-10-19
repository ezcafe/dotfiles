# Golden: Post-Build Prefer order (F3 / F4)

**SoT:** [../derive-next.md](../derive-next.md) + [../derive-next-post.md](../derive-next-post.md) Post-Build first-match.

## F3 — smoke-fail / test-fail → `fix-tests` first

**Setup:** Independent Smoke returned **smoke-fail** (or `06` test **fail**); Last stage ≠ post-`fix-tests` verify-pass.  
**Prefer:** `fix-tests` — **before** Prefer unpaid `smoke` / unpaid `test-*`.

**After** Last stage `fix-tests` + Last Verify = **verify-pass**: Prefer `smoke` if Smoke unpaid/**fail** (Prefer-re-smoke eligible) **or** unpaid `test-*` — do **not** stay on `fix-tests`; Smoke fail does **not** re-match `fix-tests` on that turn. **Gate:** Prefer-re-smoke / unpaid Smoke only when ¬ **missing required api/db** — else Prefer `finalize-lens-plan` first (before Smoke **and** before Adv — [../verify.md](../verify.md)).

See also [smoke-fail-fix-resmoke.md](smoke-fail-fix-resmoke.md).

## F4 — lens `needs fix` → `fix-review`

**Setup:** Review clean; planned lens or Merged Result = **`needs fix`**.  
**Prefer:** `fix-review` Mode `merged-lenses` / `plan-1-lens`.  
**Do not:** Prefer `merge-findings` while dirty; Prefer `test-*` / `gate-c` / `merge` while Lenses dirty or ¬ **Lenses clean** (unsafe-jump).

**After** Fix verify-pass (merged-lenses / plan-1): re-unpay planned lenses + Merged → Prefer re-lens → Prefer `merge-findings` only when planned lenses **clean** (plan 2+).

See also [fix-review-relens.md](fix-review-relens.md).

## F4b — Merged unpaid dual-false → `merge-findings`

**Setup:** Plan 2+; planned lenses **clean**; Merged unpaid/pending (clean=false ∧ dirty=false).  
**Prefer:** `merge-findings` — owns dual-false.  
**Do not:** Prefer `test-*` / `gate-c` / `merge` while ¬ **Lenses clean** (Tests success alone does **not** pay).

## F7 — `review-stale` before Lens plan unpaid

**Setup:** Notes `review-stale` (not skip-review); Adv+Quality still look `clean`; Lens plan unpaid.  
**Prefer:** unpaid review (clear duty) — **not** Prefer unpaid `lens-*` first ([../derive-next-post.md](../derive-next-post.md)).
