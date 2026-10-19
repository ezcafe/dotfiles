# Golden: simple skip-review

1. Step 0 → Mode simple, skip-review (Has UI/API/DB/auth/PII/schema all explicit `no` — not seed `unknown`) — seed **only** `00-run.md`  
2. Prefer `ideation` while **ideation unpaid** → parent Notes `ideation-confirmed` + provenance (or `ideation-skip`)  
3. Prefer `design-phase` → design-verify clean → Prefer `tdd-review` if **04a unpaid / dirty**; else Prefer `gate-b` when **04a ok** → Gate B auto (API=no ∧ DB=no ∧ auth/PII/schema=no) → Build  
4. Prefer unpaid independent Smoke **while Smoke unpaid only** → `Smoke source: Smoke-Task`; parent Notes **`smoke-pass`** + provenance **`smoke-pass-rerun`** (evidence) — **same token on first-pass and Prefer-re-smoke** (alias `smoke-pass (re-run)` only). **Smoke fail is not this step** — Prefer `fix-tests` first, then Prefer-re-smoke after `fix-tests` + verify-pass ([smoke-fail-fix-resmoke.md](smoke-fail-fix-resmoke.md) · [prefer-order-post-build.md](prefer-order-post-build.md) F3 · [../verify.md](../verify.md) Skip-review ordered recovery).  
5. Prefer paid (**skip-review Prefer paid**): **Lenses clean** (vacuous when plan=`none` ∧ ¬ missing required) + Tests success (verify-pass + Smoke-Task + that escape pair + stale cleared) → Prefer `gate-c` (or `merge` if merge already ∈ approved)
6. Else Decision N ([../decisions.md](../decisions.md)): **split** — Smoke unpaid → stay + ask escape **or run Smoke** vs drop → lite; `Smoke source: Smoke-Task` set ∧ only escape missing → stay + ask escape vs drop → lite (**not** run Smoke). Named yes.
