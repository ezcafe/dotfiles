# Preflight

## Always (before every Task)

1. Status not `done` / `stopped` (unless abort resume). **paused-wait** → stay paused; do **not** Prefer `gate-b` / stages ([resume.md](resume.md) · Pre/Post halves — same checkable union). Status `paused` ∧ ¬ **paused-wait** → Prefer continue.  
2. Card Next = derive Expected Next (or parent-only gate).  
3. Illegal Mode×profile → stop ([stages.md](stages.md) Forbidden).  
4. **Has apply (parent-only):** If stage After returned `proposed Has: …`, write card Has on `00-run.md` ([lenses.md](lenses.md)). Then if Has flip `no`→`yes` **or** `unknown`→`yes` → apply full [lenses.md](lenses.md) Has flip §1–5 — **do not partial-copy** (mandatory §1: profile skip-review → drop **lite** — agents must **not** keep skip-review after API/UI/auth → **yes**; §2 Gate B tier; §3–4 bump settle gen + clear approved/armed/auto + Notes `has-flip — <flags> — gen:<N>`; §5 overall `03a`→`pending` + Prefer re-verify when API/DB/UI/auth newly **yes**). Otherwise (Has remains `yes` or stays `no`/`unknown` without flip) → **only verify** Gate B settled before Build — do **not** bump settle gen merely because Has is already yes. Same turn after any design Task that returns a Has flip / proposed Has that flips.  
5. Compose handoff **row only** for Expected Next (skip for `gate-b` / `gate-c` / `finalize-lens-plan`) — [step-0.md](step-0.md) Load budget row-only.  
6. **Clarity-check** when Next ∈ the set in [clarity-check.md](clarity-check.md) — open that file **before** stage (**in addition to** Open 1–2 — Load budget §4); log `clarity-check ok — <Next>` ([parent-next.md](parent-next.md) · [step-0.md](step-0.md)).  
7. After Task: update Last stage, Result tokens, Run-log ≤5 lines; on verify-pass stamp fields ([verify.md](verify.md)); on `design-update` complete: append `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** (not only `needs update` — same as backloop invalidate) ([design-backloop.md](design-backloop.md)).

## Before Gate A / skim / Analyze / design / design-phase

- ¬ **ideation unpaid** — Notes `ideation-confirmed` + provenance **or** Notes `ideation-skip` / preferred `ideation skipped — <reason>` + provenance; else Prefer `ideation` ([brainstorm.md](brainstorm.md) · [derive-next.md](derive-next.md) Unsafe jumps).

## Before Build

- Design clean / Verify clean (not overall token alone; Mode simple: Verify clean ≡ Design clean).  
- No Notes `design-stale` / `design-backloop`.  
- Grill closed.  
- **04a ok** = ¬ **04a unpaid / dirty** (reject only when planned tests present ∧ ¬Notes `04a skipped` ∧ missing / `pending` / `needs more tests`; ¬ planned tests present is vacuous ok — [derive-next.md](derive-next.md)).  
- Gate B settled (token gen == current).  
- Settle post-dates current Has set / Design clean via settle gen (not clock invent).

## Before design-review / design-verify / api|db

- Design present (`03` exists **and** Result `done` — Mode full Prefer `design` if ¬ Design present; Mode simple Prefer `design-phase` per cold start carve — [grill.md](grill.md)).  
- Grill closed — not **Grill open** ([grill.md](grill.md)); Mode full Prefer `grill` while Grill open; Mode simple cold start carve — [grill.md](grill.md).  
- Notes `design-stale` / **design-stale unpaid** → Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** (unsafe-jump: do **not** Prefer `design` while Grill open; do **not** Prefer Isolated / design-review / design-verify / design-update; clear Notes after Mode-full `design` + `03` rewrite — no design-update Run-log).  
- Notes `design-backloop` **or** any `03a*` **`needs update`** → Prefer **Grill open** → `grill` first; else Prefer `design-update` first when **Grill closed** (pay Run-log + set **ALL** `03a*` → `pending`).  
- Else ¬ design-update unpaid — no `03a*` **needs update** **and** ¬ **backloop rewrite unpaid** (Run-log `design-update — settle-gen:<N>` when Notes `design-backloop`).

## Before Adv / Quality / Smoke / test-* / gate-c / merge

- E1: independent Smoke (`Smoke source: Smoke-Task`) **before** Adv/Quality unlock.  
- skip-review: unpaid Smoke for Gate C bar / Prefer paid — not an Adv unlock path.  
- Lite/full: Prefer unpaid `test-*` only when **Review clean** ∧ **Lenses clean** ∧ **Tests unpaid**.  
- Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (Lens plan=`none` or plan lacks matching `api`/`db`) → Prefer `finalize-lens-plan` **before Smoke and before Adv** (**not** Prefer-re-smoke / unpaid Smoke / Adv / lenses / `test-*`) — [derive-next-post.md](derive-next-post.md) · [verify.md](verify.md) Prefer order vs finalize-lens-plan.  
- Lite/full: Prefer `gate-c` when **Tests success** ∧ **Lenses clean** ∧ **Gate C unpaid** (not while Tests unpaid, Lenses dirty, missing required, or Merged unpaid when plan 2+).  
- Before Merge: (1) Tests success ≡ Gate C bar; (2) **Lenses clean** (¬ Lenses dirty ∧ ¬ missing required ∧ Merged paid when plan 2+); (3) `merge` ∈ Gate C approved (+ provenance); (4) unpaid stale Notes cleared; (5) clarity-check [Merge](clarity-check.md#merge).

## Seed checklist

1. Seed **only** `00-run.md` ([step-0.md](step-0.md)) — Mode, profile, Has flags, settle gen `0`, Status `running`.  
2. Do **not** pre-create `01`–`06` / `03a*` stubs. Stages copy from [artifacts/INDEX.md](artifacts/INDEX.md) when they write.  
3. Mode × profile legal; Gate B tier matches [gate-b.md](gate-b.md) (simple auto only when API=no ∧ DB=no ∧ auth/PII/schema=no — explicit `no`; `unknown` ≠ `no`).
