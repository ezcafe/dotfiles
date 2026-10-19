# Golden: mid-run reclassify simple → full

**Start:** Mode simple (e.g. tiny copy tweak).  
**Flip:** Design discovers new public route + persistence → Has API=yes, Has DB=yes.  
**Parent actions:**

1. Pause; Decision N ([decisions.md](../decisions.md)): Stay simple · Upgrade to full · New slug/stop. Prefer **Upgrade to full**.
2. Set Mode **full**; Review profile **full** or **lite** (never keep skip-review). HITL Gate B → **blocking**.
3. Notes: `reclassify simple→full — API+DB appeared` **and** `design-stale` (Mode-simple `analyze`/`grill`/`03`/`03a*` unpaid until Mode-full rewrite). **Invalidate prior overall `03a` clean** **and** isolated `03a-api` / `03a-db` **clean** when present (set each Result **pending** or remove **clean** — same as Amend). **Mirror design-backloop Amend:** **Gate B approved: none**; **Build armed: none**; clear veto-window tokens (`Gate B veto: none`; drop Notes `async-gap-pending` if present); **clear** `gate-b auto — <HH:MM>` (or digest) if present; set **Last Verify: pending**; **Last verify-pass at: none**; keep `review-stale` / `test-stale` when set (skip-review: clear `review-stale` as N/A). Keep existing `01-idea` unless Decision N requires Ideation redo. Selector stays **Pre-Build** while Notes `design-stale`.
4. Run [derive-next.md](../derive-next.md) + [derive-next-pre.md](../derive-next-pre.md) Pre-Build (Mode full) **first-match** before Design-review / API∥DB: unpaid Gate A (`01a` ≠ `ok`) → `gate-a`; then unpaid skim → `skim`; then Notes `design-stale` Prefer first unpaid among `analyze` → `grill` → `design` (before Grill open / No `02-analysis` — do **not** treat Mode-simple Analyze/Grill/`03` as paid). **Parent clears** Notes `design-stale` only after Last stage `design` **and** `03-design.md` rewrite for Mode full; then Prefer re-run API∥DB when Has=yes **and** Isolated API/DB unpaid (**even if files exist**) → Mode-full `design-review` until overall **`clean`** (**Design clean** does not count on pre-upgrade / Mode-simple overall **or** isolated **`clean`**). Fail-closed: never past Gate A while `01a` ≠ `ok`; do **not** Build while Notes `design-stale` ([verify.md](../verify.md) · [preflight.md](../preflight.md)).
5. Gate B → **blocking** ([gate-b.md](../gate-b.md)).

**Do not:** Jump straight to Design-review / API∥DB / Build while Gate A / skim unpaid or Notes `design-stale`; treat leftover overall **or** isolated `03a*` **clean** as paid after Upgrade; keep Mode simple + skip-review after Has API/DB yes; invent Ideation redo unless Decision N requires it.
