# Smoke

## FIRST

1. **missing required api/db** → `Result: blocked — missing required api/db` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)).  
2. Smoke fail ∧ Last stage ≠ (`fix-tests` + verify-pass) → `Result: blocked — Prefer fix-tests first` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) Skip-review ordered recovery · [../../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md](../../my-dev-flow-v3/examples/smoke-fail-fix-resmoke.md)).  
3. ¬ (E1|skip-review Smoke unpaid ∨ (Smoke unpaid∨fail ∧ Prefer-re-smoke eligible)) → `Result: blocked — Smoke not Prefer unpaid` (Prefer unpaid = E1 or skip-review Smoke unpaid; Prefer-re-smoke eligible = Last stage `fix-tests` + verify-pass; Prefer-re-smoke proceed **only** when Smoke unpaid∨fail ∧ Prefer-re-smoke eligible — do **not** proceed on eligible alone when Smoke already paid/success; Escape pair does not waive).  
4. Else proceed.

**On smoke-pass** (`Result: smoke-pass` ≡ success): set `Smoke source: Smoke-Task` on `06`. Do **not** write Notes / card **Last stage** / **Next** / verify stamps.

## After

Return `Result: smoke-pass` \| fail token only. **Hard stop** — do **not** Prefer Next / write parent-only fields. Parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md)).

**After (parent / labeled solo as orchestrator):** on smoke-pass, stamp Notes `smoke-pass` + provenance `smoke-pass-rerun` (evidence) when E1 or skip-review require the escape pair — then re-derive. **Orchestrated:** parent stamps escape after Parent-relay / After signals. **Labeled solo:** stamps escape when acting as orchestrator ([../../my-dev-flow-v3/solo-entry.md](../../my-dev-flow-v3/solo-entry.md) · [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md) Escape Notes). Clear Notes `smoke re-run` when writing `smoke-pass` (alias `(re-run)` accepted).
