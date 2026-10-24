# Preflight

## Always (before every Task)

1. Status not `done` / `stopped` (unless abort resume). **paused-wait** → stay paused; do **not** Prefer `gate-b` / stages ([resume.md](resume.md) · Pre/Post halves — same checkable union). Status `paused` ∧ ¬ **paused-wait** → fall-through Prefer (evaluate next unpaid row — not a Next value) ([derive-next.md](derive-next.md)).  
2. Card Next = derive Expected Next (or parent-inline / labeled-solo gate — `gate-b` / `gate-c` / `finalize-lens-plan`).  
3. Illegal Mode×profile → stop ([stages.md](stages.md) Forbidden).  
4. **Has apply (parent **or** labeled solo as orchestrator):** If stage After returned `proposed Has: …`, write card Has on `00-run.md` ([lenses.md](lenses.md) · [solo-entry.md](solo-entry.md) · [hitl.md](hitl.md)). Then if Has flip `no`→`yes` **or** `unknown`→`yes` → apply full [lenses.md](lenses.md) Has flip §1–5 — **do not partial-copy** (mandatory §1: profile skip-review → drop **lite** — agents must **not** keep skip-review after API/UI/auth → **yes**; §2 Gate B tier; §3–4 bump settle gen + clear approved/armed/auto + Notes `has-flip — <flags> — gen:<N>`; §5 overall `03a`→`pending` + Prefer re-verify when API/DB/UI/auth newly **yes**). Otherwise (Has remains `yes` or stays `no`/`unknown` without flip) → **only verify** Gate B settled before Build — do **not** bump settle gen merely because Has is already yes. Same turn after any design Task that returns a Has flip / proposed Has that flips.  
5. Compose handoff **row only** for Expected Next (skip for `gate-b` / `gate-c` / `finalize-lens-plan`) — [step-0.md](step-0.md) Load budget row-only.  
6. **Clarity-check** when Next ∈ the set in [clarity-check.md](clarity-check.md) — open that file **before** stage (**in addition to** Open 1–2 — Load budget §4); log `clarity-check ok — <Next>` ([parent-next.md](parent-next.md) · [step-0.md](step-0.md)).  
7. **Isolate (orchestrator):** if Next maps to a subflow skill ([spawn-contract.md](spawn-contract.md) Skill map · [parent-next.md](parent-next.md) Skill column) → open [spawn-contract.md](spawn-contract.md) → spawn **fresh** local `Task`; do **not** run the stage inline. Parent-inline only for `gate-b` / `gate-c` / `finalize-lens-plan` / Step 0 / HITL.  
8. After Task: follow [step-0.md](step-0.md) After Task checklist — apply After signals ([hitl.md](hitl.md)); stamp **Status** from `candidate Status: done|paused` when present; update Last stage, Result tokens, Run-log ≤5 lines; on verify-pass stamp fields ([verify.md](verify.md)); on `design-update` complete: append `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** ([design-backloop.md](design-backloop.md)); present Parent-relay HITL Qs; then re-derive — do **not** keep Task transcripts. Never apply `candidate design-stale` without Mode=full.

## Before Gate A / skim / Analyze / design / design-phase

- ¬ **ideation unpaid** — else Prefer `ideation` ([derive-next-defs-pre.md](derive-next-defs-pre.md) · [derive-next.md](derive-next.md) Unsafe jumps · [brainstorm.md](brainstorm.md)).

## Before Build

- **Design clean** / **Verify clean** · Grill closed · **04a ok** · **Gate B settled** — defs [derive-next-defs-pre.md](derive-next-defs-pre.md).  
- No Notes `design-stale` / `design-backloop`.  
- Settle post-dates current Has set / Design clean via settle gen (not clock invent).

## Before design-review / design-verify / api|db

- **Design present** · Grill closed · ¬ **design-stale unpaid** · ¬ **design-update unpaid** — defs + Prefer [derive-next-defs-pre.md](derive-next-defs-pre.md) · [derive-next-pre.md](derive-next-pre.md) · cold-start carve [grill.md](grill.md).  
- Notes `design-backloop` / `03a*` **`needs update`** → Prefer **Grill open** → `grill` first; else `design-update` when closed (pay Run-log + all `03a*` → `pending` — [design-backloop.md](design-backloop.md)).

## Before Adv / Quality / Smoke / test-* / gate-c / merge

- Prefer order SoT: [derive-next-post.md](derive-next-post.md) (+ [derive-next-defs-post.md](derive-next-defs-post.md)) — **missing required api/db** → `finalize-lens-plan` **before Smoke and before Adv**.  
- E1: independent Smoke (`Smoke source: Smoke-Task`) **before** Adv unlock.  
- skip-review: unpaid Smoke / Prefer paid — [verify.md](verify.md).  
- Lite/full: Prefer unpaid `test-*` only when **Review clean** ∧ **Lenses clean** ∧ **Tests unpaid**.  
- Prefer `gate-c` / Merge bars: **Tests success** ∧ **Lenses clean** ∧ Gate C named yes — defs-post · [gate-c.md](gate-c.md) · clarity-check [Merge](clarity-check.md#merge).

## Seed checklist

1. Seed **only** `00-run.md` ([step-0.md](step-0.md)) — Mode, profile, Has flags, settle gen `0`, Status `running`.  
2. Do **not** pre-create `01`–`06` / `03a*` stubs. Stages copy from [artifacts/INDEX.md](artifacts/INDEX.md) when they write.  
3. Mode × profile legal; Gate B tier matches [gate-b.md](gate-b.md) (simple auto only when API=no ∧ DB=no ∧ auth/PII/schema=no — explicit `no`; `unknown` ≠ `no`).
