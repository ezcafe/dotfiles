# Golden: simple bugfix

1. Step 0 → Mode simple, profile lite, settle gen 0  
2. design-phase → Grill frontier-empty → design-verify clean  
3. Gate B auto (API=no DB=no auth=no) → `gate-b auto — gen:0` → Build (TDD)  
4. verify-pass + Build-writes-Smoke → code-review-phase → test-lite  
5. Gate C named yes → merge → done
