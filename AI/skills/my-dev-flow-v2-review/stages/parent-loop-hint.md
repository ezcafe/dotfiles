## Parent loop hint (my-dev-flow-v2)

Keys off **Review profile** (not Mode). Mode full + profile lite → lite row.

```
Review profile lite (any Mode):
  code-review-phase ⇄ Fix
  → lenses per Lens plan (parent launches lens-*; never paid in-band; parallel when 2+)
  → merge-findings if 2+ → Fix → Prefer: mark lenses unpaid → re-lens → merge-findings if 2+
  → test-lite only when lenses clean

Review profile full:
  independent Smoke (Smoke source: Smoke-Task) → Adversarial ⇄ Fix → Quality ⇄ Fix
  → After fix-review verify-pass: Prefer re-run dirty section
    (Adv/Quality Fix ask → that section; both dirty/unclear → Adv then Quality;
     Mode merged-lenses | plan-1-lens → mark planned 05-lens-* + Merged unpaid → re-lens → merge if 2+)
  → Loop (max 3): only Lens plan lenses (must parallel when 2+) → Merge if 2+ → Fix → Prefer re-lens
  → test-full only when lenses clean (one Task)
```

Prefer dirty / [derive-next.md](../../my-dev-flow-v2/derive-next.md) is Expected-Next SoT. `tests/behavior changed` is informational only — not a Prefer override.

Runtime order SoT: `{my-dev-flow-v2}/stages.md` Mode × Review profile → post-Build path. Do not invent a parallel order here.
