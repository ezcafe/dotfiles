# Golden: smoke-fail → fix-tests → re-smoke

**Setup:** Post-Build; Smoke returned **smoke-fail**; `06` has Fix ask.  
**Path:**

1. Derive Next → `fix-tests` (Smoke fail — [../derive-next.md](../derive-next.md) + [../derive-next-post.md](../derive-next-post.md); wins before Prefer unpaid Smoke).  
2. Fix-from-tests → Result **verify-pass**.  
3. Derive again: Last stage `fix-tests` + verify-pass ∧ ¬ **missing required api/db** → Prefer **`smoke`** because Smoke unpaid/**fail** is Prefer-re-smoke eligible — not stay on `fix-tests`; do **not** re-match Smoke fail → `fix-tests`. If missing required api/db → Prefer `finalize-lens-plan` first ([../verify.md](../verify.md)).  
4. Smoke Task → **smoke-pass** (Notes `smoke-pass` + provenance after parent; alias `smoke-pass (re-run)` only) → continue per Mode × profile.

Same Prefer for unpaid **test-fail** after fix-tests verify-pass → Next = `test-full` / `test-lite`.

**Do not:** Re-match smoke-fail → fix-tests after fix-tests already verify-pass; Prefer re-smoke on verify-fail.
