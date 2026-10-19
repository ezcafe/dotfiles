# Solo subflow entry

When user runs a subflow alone:

1. Require min-state on `00-run.md` (Mode, profile, settle gen, Has flags).  
2. Preflight → derive still apply if orchestrating multi-step.  
3. Respect Gate B/C parent-only consent.  
4. E1: independent Smoke with `Smoke source: Smoke-Task` before Adv (Notes companion only).  
5. **skip-review:** Prefer unpaid independent Smoke (`Smoke source: Smoke-Task`); Build-writes-Smoke does **not** waive. Prefer-re-smoke order + Prefer paid escape Notes↔provenance — [verify.md](verify.md) · [../my-dev-flow-v3-test/SKILL.md](../my-dev-flow-v3-test/SKILL.md).  
6. Gate B: `unknown` ≠ `no` (blocking / no auto until explicit `no`) — [lenses.md](lenses.md) · [gate-b.md](gate-b.md).  
7. test-full/lite: on success parent clears `test-stale` when Lite/full clear met ([hitl.md](hitl.md) · [verify.md](verify.md)); Prefer `merge`\|`gate-c` only when **Tests success** **and** **Lenses clean**.
8. **Lifecycle / Has / provenance:** never write lifecycle Notes (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), card Has, or provenance — return `candidate …` / `proposed Has` / `candidate clear …` only; parent applies ([hitl.md](hitl.md)).
