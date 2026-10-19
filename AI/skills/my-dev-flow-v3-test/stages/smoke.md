# Smoke

## FIRST

1. **missing required api/db** → `Result: blocked — missing required api/db` (Prefer `finalize-lens-plan` — [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) Prefer order vs finalize-lens-plan).  
2. Smoke fail ∧ Last stage ≠ (`fix-tests` + verify-pass) → `Result: blocked — Prefer fix-tests first` ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) Skip-review ordered recovery · [../../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md](../../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md)).  
3. ¬ (E1|skip-review Smoke unpaid ∨ (Smoke unpaid∨fail ∧ Prefer-re-smoke eligible)) → `Result: blocked — Smoke not Prefer unpaid` (Prefer unpaid = E1 or skip-review Smoke unpaid; Prefer-re-smoke eligible = Last stage `fix-tests` + verify-pass; Prefer-re-smoke proceed **only** when Smoke unpaid∨fail ∧ Prefer-re-smoke eligible — do **not** proceed on eligible alone when Smoke already paid/success; Escape pair does not waive).  
4. Else proceed.

**On smoke-pass** (`Result: smoke-pass` ≡ success): set `Smoke source: Smoke-Task` on `06`. Do **not** write Notes.

**After (parent):**

1. **E1** → Notes `smoke-pass` + provenance `smoke-pass-rerun` (evidence) → Prefer review  
2. **skip-review** → same Notes + provenance (first-pass **or** Prefer-re-smoke) → Prefer paid / Gate C bar ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) Escape Notes name — canonical `smoke-pass`; alias `smoke-pass (re-run)` only)  
3. Other profiles → review/test per profile (not Gate C from Smoke alone)  
4. Prefer-re-smoke after Last stage `fix-tests` + verify-pass when Smoke fail/unpaid ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md))

Clear Notes `smoke re-run` when writing `smoke-pass` (alias `(re-run)` accepted).
