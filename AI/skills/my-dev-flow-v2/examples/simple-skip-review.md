# Golden: simple skip-review

**Ask:** Docs/token-only change.  
**Classify:** Mode simple, profile skip-review (Has API/DB/auth = no).  
**Path:** design-phase → design-verify clean → Gate B auto → Build verify-pass → **ordered recovery** ([verify.md](../verify.md) Skip-review + Smoke):

1. Prefer unpaid Notes `smoke re-run` once → independent Smoke.
2. Prefer paid Notes `smoke-pass (re-run)` ↔ provenance `smoke-pass-rerun` → Gate C.
3. Else peer alternatives — drop skip-review → lite (`code-review-phase` → lenses → `merge-findings` if 2+ → `test-lite`) → Gate C, **or** Gate C with escape+provenance (`docs-only` / `smoke-waive` / `gate-c-test-override`).

Build-writes-Smoke alone is **not** enough. Do not launch `test-lite` while profile stays skip-review.
