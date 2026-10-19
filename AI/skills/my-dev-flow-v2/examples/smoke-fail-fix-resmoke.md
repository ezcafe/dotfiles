# Golden: smoke-fail → fix-tests → re-smoke

**Setup:** Post-Build; independent Smoke (or re-run) returned **smoke-fail**; `06` has Fix ask.  
**Path:**

1. Derive Next → `fix-tests` (smoke-fail unpaid; Last stage not post-`fix-tests` verify-pass — [derive-next.md](../derive-next.md) Post-Build Smoke-fail row).
2. Fix-from-tests → Result **verify-pass**; may append `06` Round notes.
3. Parent derive again: Last stage `fix-tests` + Last Verify = **verify-pass** → Prefer **`smoke`** (Smoke still fail/unpaid or Notes re-smoke) — **not** stay on `fix-tests`.
4. Smoke Task → **smoke-pass** → continue (review / Prefer→Gate C / test-* per Mode × profile).

Same Prefer for unpaid **test-fail** after fix-tests verify-pass → Next = `test-full` / `test-lite` (not fix-tests again).

**Do not:** Re-match the smoke-fail → fix-tests row after fix-tests already returned verify-pass; re-smoke on verify-fail.

See [derive-next.md](../derive-next.md) Post-Build · [verify.md](../verify.md) Fix.
