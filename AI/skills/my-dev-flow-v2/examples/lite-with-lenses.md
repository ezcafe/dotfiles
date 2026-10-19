# Golden: lite + lenses

**Ask:** Small feature; Lens plan includes `api` (or `api|db`).  
**Classify:** Mode simple or full; profile **lite**; Lens plan not `none`.  
**Path:** … → Build verify-pass (Build-writes-Smoke; skip independent Smoke) → `code-review-phase` clean → lenses per plan (isolated api/db; parallel when 2+) → `merge-findings` if 2+ → `test-lite` → Gate C → merge → `done`.

**Do not:** Jump to `test-lite` while Lens plan unpaid; fold any lens (api/db/security/perf/memory) into `code-review-phase` as a paid `05-lens-*` write — parent always launches `lens-*` Tasks. Tiny-tweak: light contract checks in Quality prose only (no forced api/db lens).
