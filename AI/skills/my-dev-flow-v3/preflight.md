# Preflight

## Always (before every Task)

1. Status not `done` / `stopped` (unless abort resume).  
2. Card Next = derive Expected Next (or parent-only gate).  
3. Illegal Mode×profile → stop ([stages.md](stages.md) Forbidden).  
4. Has flip no→yes → settle clear + bump settle gen + Notes `has-flip — <flags> — gen:<N>` ([lenses.md](lenses.md)). When **any** Has=yes, enforce Gate B settle freshness ([gate-b.md](gate-b.md)).  
5. Compose handoff **row** (skip for `gate-b` / `gate-c`).  
6. After Task: update Last stage, Result tokens, Run-log ≤5 lines; on verify-pass stamp fields ([verify.md](verify.md)).

## Before Build

- Design clean / Verify clean (not overall token alone).  
- No Notes `design-stale` / `design-backloop`.  
- Grill closed.  
- Gate B settled (token gen == current).  
- Settle post-dates current Has set / Design clean via settle gen (not clock invent).

## Before design-review / design-verify / api|db

- Grill closed (Mode simple Prefer `grill` when artifacts present or `02b` needs-round).

## Before Adv / Quality / Smoke / gate-c / merge

- E1 / skip-review: `Smoke source: Smoke-Task` before Adv/Quality unlock.  
- Lite/full: Prefer/launch `gate-c` only when **Tests success**.  
- Before Merge: (1) Tests success ≡ Gate C bar only; (2) `merge` ∈ Gate C approved (+ provenance); (3) unpaid stale Notes cleared.

## Seed checklist

Copy templates from [artifacts/INDEX.md](artifacts/INDEX.md); set Mode, profile, Has flags, settle gen `0`.
