# Golden paths

| Example | Covers |
|---------|--------|
| [simple-bugfix.md](simple-bugfix.md) | Mode simple + lite |
| [simple-skip-review.md](simple-skip-review.md) | Design clean → Prefer `tdd-review` if unpaid/dirty else `gate-b` when **04a ok**; Prefer unpaid → Prefer paid → merge\|gate-c |
| [full-api-db.md](full-api-db.md) | Mode full + API∥DB; Prefer checkpoints incl. 04a/`tdd-review`; finalize-lens-plan if needed; E1 Smoke before Adv |
| [prefer-order-pre-build.md](prefer-order-pre-build.md) | F1 Grill open (unpaid/`pending` ∧ ¬Notes grill-skip) before ¬Design present→design; Notes grill-skip closes even if `02b` pending; Result `skipped` does not close; F1b Design present=`03`+`done`; Mode simple ¬Design present → `design-phase` (cold start Grill unpaid **or** Grill closed / grill-skip; not design-verify); mid-open ≡ Grill open ∧ ¬carve (incl. `skipped`); F2 design-update only when Grill closed (else Prefer `grill`); F5 ideation unpaid / Notes `ideation-confirmed`\|`ideation-skip`; F6 Prefer `tdd-review` only unpaid/dirty; Prefer `gate-b` when **04a ok** (incl. ¬ planned tests); F10 Gate A/skim/Analyze unpaid (`done`); F11 happy Upgrade writes Mode=full + design-stale (Grill closed → Analyze unpaid → design unpaid under design-stale); F12 design-stale+Grill open → `grill` first (then Analyze→design) |
| [prefer-order-post-build.md](prefer-order-post-build.md) | F3 fix-tests before re-smoke; F4 lens needs-fix → fix-review; F7 review-stale before Lens plan unpaid |
| [smoke-fail-fix-resmoke.md](smoke-fail-fix-resmoke.md) | smoke-fail → fix-tests verify-pass → re-smoke |
| [design-backloop-after-build.md](design-backloop-after-build.md) | Amend → Prefer Grill open→`grill` first → design-update (Grill closed) → re-review → Gate B settled post-Notes (Run-log after Notes) |
| [drop-skip-review-api-flip.md](drop-skip-review-api-flip.md) | Has flip §1–5 (Always §4 full apply): drop skip-review; Gate B blocking when API/DB/auth→yes (UI alone ≠ deny auto); settle bump any flip; overall `03a`→`pending`; Mode simple Prefer design-verify; Mode full Prefer Isolated when required → design-review |
| [fix-review-relens.md](fix-review-relens.md) | Fix Mode merged-lenses → re-unpay → re-lens |
| [anti-patterns.md](anti-patterns.md) | Fail-closed Wrong→Right; grill Result `skipped` invent-waive; Mode simple mid-open ≡ full Grill open; Prefer design-update while Grill open; bare ideation ≠ Done; lifecycle Notes parent-only; Gate B settled post-Notes / auto Prefer build while Notes; Mid-run Upgrade Mode=full; `06` Result alone ≠ escape; clarity-check vs Open 1–2; paused-wait; design-stale+Grill open→grill; finalize before Smoke **and** Adv — [../lenses.md](../lenses.md) |

Do **not** use v2 `derive-next` / `gate-b` / settle-clock examples as runtime SoT — v3 settle gen + Prefer order above win.
