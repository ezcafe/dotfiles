# Golden: Fix → Prefer re-verify (dirty Adv/Quality / lite)

**Setup:** Profile **full**; Quality (or Adversarial) wrote Fix ask → `fix-review` Mode `quality` / `adversarial-tests` returned **verify-pass**.  
**Path:**

1. Derive Next: Last stage `fix-review` + Last Verify = **verify-pass** → Prefer re-run the **dirty** verifier section that produced the Fix ask (here Quality) — **not** “next unpaid” Adv if Adv is already clean.
2. Quality re-check → clean (or needs fix → Fix again).
3. If both Adv and Quality dirty/unclear after Fix → Prefer `adversarial` then `quality`.
4. If 05 already clean after Fix → Prefer else continue table (lenses / test-full / …) — **not** stay on `fix-review`.

**Lite:** Prefer always re-runs `code-review-phase` (not Adv/Quality).

**Lens / merged Fix ask:** use twin [fix-review-relens.md](fix-review-relens.md) — do **not** Prefer “already clean → test-*” while Merged / plan-1 still `needs fix`.

**Do not:** After fix-review verify-pass, re-match the “Review needs fix → fix-review” row; pick next unpaid Adv while Quality is the dirty section.

See [derive-next.md](../derive-next.md) Post-Build · [verify.md](../verify.md) Fix · [fix-review.md](../../my-dev-flow-v2-review/stages/fix-review.md).
