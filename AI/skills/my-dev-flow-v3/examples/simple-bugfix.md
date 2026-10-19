# Golden: simple bugfix

1. Step 0 → Mode simple, profile lite, settle gen 0 — seed **only** `00-run.md` (no stub `02b`/`03`)  
2. Prefer `ideation` while **ideation unpaid** (¬Notes `ideation-skip` ∧ ¬Notes `ideation-confirmed`) → Stage returns `candidate ideation-confirmed` → parent stamps Notes `ideation-confirmed` + provenance `user:"…" ≥12 chars` → write `01-idea`  
3. Prefer `design-phase` (cold start: none of {`02-analysis`, `03`, `04`} on disk **and** (**Grill unpaid** ∨ **Grill closed** / Notes `grill-skip`)) → Grill frontier-empty → design-verify clean  
4. Gate B auto (API=no ∧ DB=no ∧ auth/PII/schema=no) → `gate-b auto — gen:0` → Build (TDD)  
5. verify-pass + Build-writes-Smoke → code-review-phase → test-lite  
6. Gate C named yes → merge → done
