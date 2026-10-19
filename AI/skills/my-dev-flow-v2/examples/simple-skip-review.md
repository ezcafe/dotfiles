# Golden: simple skip-review

**Ask:** Docs/token-only change.  
**Classify:** Mode simple, profile skip-review (Has API/DB/auth = no).  
**Path:** design-phase → design-verify clean → Gate B auto (parent writes design-scoped `gate-b auto — <HH:MM>` same turn → Prefer `build` — [gate-b.md](../gate-b.md)) → Build verify-pass → **ordered recovery** ([verify.md](../verify.md) Skip-review + Smoke):

1. Prefer unpaid Notes `smoke re-run` once → independent Smoke when Smoke unpaid/fail **or** Notes `test-stale` (even if an escape pair already exists — do not softlock). Build-writes-Smoke does **not** pay ([derive-next.md](../derive-next.md) **Smoke unpaid**). Clear `test-stale` when `Smoke source: Smoke-Task` is fresh after **Last verify-pass at**. `review-stale` is N/A under skip-review — clear.
2. Prefer paid when bar met (stale cleared + verify-pass + independent smoke-pass + escape) → `merge` \| `gate-c` ([verify.md](../verify.md) Prefer paid).
3. Else **Decision N** ([decisions.md](../decisions.md) Skip-review else) — Prefer stay skip-review + ask escape **or run Smoke** vs drop → lite; drop → lite only as Option 2 after named yes; do **not** drop profile or write escape Notes without named user yes. Escape alone is **not** enough.

Do not launch `test-lite` while profile stays skip-review.
