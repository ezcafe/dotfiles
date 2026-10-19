# Clarity-check

Parent habit before heavy stages (wired from [preflight.md](preflight.md) · [parent-next.md](parent-next.md) · [step-0.md](step-0.md) Load budget §4).

**Budget:** open this file **in addition to** parent-next Open 1–2 — it does **not** compete for the two-file slot.

**When Next ∈ this set**, open this file (or use the inline checklist below) **before** launching the stage; confirm the ask, Mode, and Next are unambiguous; log `clarity-check ok — <Next>`:

`design-phase` \| `analyze` \| `grill` \| `design` \| `design-update` \| `design-review` \| `design-verify-phase` \| `api-contract-review` \| `db-design-review` \| `api\|db` \| `tdd-review` \| `build` \| `adversarial` \| `quality` \| `code-review-phase` \| `fix-review` \| `fix-tests` \| `merge`

When Next = `api|db` (both Isolated unpaid → same-turn parallel), clarity-check applies to **each** launched Isolated id (`api-contract-review` / `db-design-review`).

**Out of scope** (no clarity-check required): `ideation` / `gate-a` / `skim` / `smoke` / `lens-*` / `merge-findings` / `test-full` / `test-lite` / `gate-b` / `gate-c` / `finalize-lens-plan` — unless parent chooses to log anyway.

## Merge

Confirm before Prefer/launch `merge`:

1. Tests success ≡ Gate C bar (incl. unpaid stale Notes cleared).  
2. **Lenses clean** (ban while **Lenses dirty**, **missing required api/db**, or Merged unpaid when plan 2+ — [derive-next.md](derive-next.md) · [derive-next-post.md](derive-next-post.md)).  
3. Independent Smoke for skip-review (`Smoke source: Smoke-Task`) + escape Notes↔provenance when profile is skip-review.  
4. Build-writes-Smoke alone fails closed for skip-review.  
5. `merge` ∈ Gate C approved (+ provenance).
