## Parent loop hint (my-dev-flow)

Keys off **Review profile** (not Mode). Mode full + profile lite → lite row.

```
Review profile lite (any Mode):
  code-review-phase ⇄ Fix → api/db isolated if in plan (not tiny-tweak); 2+ → parallel + Merge → test-lite

Review profile full:
  Adversarial ⇄ Fix → Quality ⇄ Fix
  → Loop (max 3): only Lens plan lenses (must parallel when 2+) → Merge if 2+ → Fix → recheck
  → test-full (one Task)
```

Runtime order SoT: `{my-dev-flow}/stages.md` Mode × Review profile → post-Build path. Do not invent a parallel order here.
