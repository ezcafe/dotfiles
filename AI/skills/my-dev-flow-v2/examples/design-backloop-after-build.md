# Golden: design-backloop after Build

**Trigger:** Build/Fix cannot stay aligned with `03`/`04` without contract or IA change.  
**Parent actions** ([design-backloop.md](../design-backloop.md)):

1. Decision N: Amend design · Fix-only · Stop. Prefer Amend when contracts/IA must change.
2. Notes `design-backloop`; **Gate B approved: none**; **Build armed: none**; clear veto-window tokens; Next `design-update`.
3. Prior `05`/`06` Results → Notes `review-stale` / `test-stale` ([verify.md](../verify.md) Stale).
4. Resume: `design-update` → design-review / design-verify-phase → Gate B again → Fix/Build.
5. Clear `design-backloop` only after Gate B re-settle; clear stale Notes only after fresh review clean / test success.

**Do not:** Launch Build while Notes still say `design-backloop`; silently rewrite `03`/`04` inside Build/Fix; go to Gate C with a known design mismatch.
