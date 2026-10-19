# Solo subflow entry

When user runs a subflow alone:

1. Require min-state on `00-run.md` (Mode, profile, settle gen, Has flags).  
2. Preflight → derive still apply if orchestrating multi-step.  
3. Respect Gate B/C parent-only consent.  
4. E1: independent Smoke with `Smoke source: Smoke-Task` before Adv (Notes companion only).  
5. test-full/lite: on success clear `test-stale` when Lite/full clear met; Prefer `merge`\|`gate-c` only when **Tests success**.
