# Golden: simple bugfix

1. Step 0 → Mode simple, profile lite, settle gen 0 — seed **only** `00-run.md` (no stub `02b`/`03`)  
2. Spawn `my-dev-flow-v3-design` Task (Expected Next `ideation`) → Task writes Q into `01-idea` + Return `Blocked / questions` → hard-stop `hitl:ideation` (never AskQuestion)  
3. Parent presents Q → stamps Notes `ideation-confirmed` + provenance → re-spawn design Task Expected Next `design-phase`  
4. Prefer `design-phase` (cold-start carve — [../grill.md](../grill.md)) → if Grill frontier Qs → hard-stop → Parent-relay → re-spawn until Grill closed → design-verify clean  
5. Gate B auto (API=no ∧ DB=no ∧ auth/PII/schema=no) → `gate-b auto — gen:0` → spawn code Task → Build (TDD)  
6. verify-pass + Build-writes-Smoke → code-review-phase → test-lite  
7. Gate C named yes → merge → done
