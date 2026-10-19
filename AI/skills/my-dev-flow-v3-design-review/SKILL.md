---
name: my-dev-flow-v3-design-review
description: >-
  Reviews design artifacts. Prefer design-update first when Result needs update.
  Prefer re-run Isolated/design-review only when unpaid ≠ needs update (missing
  or Result pending). Mode full: both Isolated unpaid → same-turn parallel only;
  Prefer general design-review after Isolated paid. Mode simple:
  design-verify-phase. Use when run my-dev-flow-v3-design-review or after design
  before Build.
---

# my-dev-flow-v3-design-review

**Orchestrator SoT:** Isolated unpaid, Design clean — `../my-dev-flow-v3/derive-next.md` · `derive-next-pre.md` · `results.md`.

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen on `00-run.md`.  
2. Unpaid bans: no Isolated / design-review / design-verify while ¬ Design present, design-update unpaid, Notes `design-stale`, or **Grill open** ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) unsafe jumps · [../my-dev-flow-v3/grill.md](../my-dev-flow-v3/grill.md)).  
3. Parent-only ([../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)): never write Gate B consent / waiver Notes / settle gen, **lifecycle Notes** (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), or **card Has** — Stages return `candidate …` / `proposed Has` only.  
4. Derive Next: [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · Prefer SoT [../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) · stage index [stages.md](stages.md).  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Stages

| Id | File |
|----|------|
| api-contract-review | [stages/api-contract-review.md](stages/api-contract-review.md) |
| db-design-review | [stages/db-design-review.md](stages/db-design-review.md) |
| design-review | [stages/design-review.md](stages/design-review.md) |
| design-verify-phase | [stages/design-verify-phase.md](stages/design-verify-phase.md) |

## Principles

1. Unpaid = missing **or** Result ≠ `clean` (incl. `pending`). Prefer unpaid `design-update` when Result **`needs update`** (or **backloop rewrite unpaid**) — Prefer **Grill open** → `grill` first; else Prefer `design-update` when **Grill closed**. Prefer re-run Isolated / design-review / design-verify only when unpaid ≠ **`needs update`** (e.g. missing / `pending`) — [../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md).  
2. Allowed Results: `clean` \| `needs update` \| `pending` (Isolated also `skipped`). Advance-on-clean / Done when = `clean` only; writing **`needs update`** allowed ≠ Done.  
3. Result **`needs update`** **or** rewrite unpaid → Prefer unpaid `design-update` when needed (Grill-open rule above). **Pay is parent-only** after `design-update` Task complete: Run-log `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** ([../my-dev-flow-v3/design-backloop.md](../my-dev-flow-v3/design-backloop.md) · [../my-dev-flow-v3/preflight.md](../my-dev-flow-v3/preflight.md) Always §7) — do **not** invent Run-log pay from this skill / Prefer. Then re-run Isolated / design-review / design-verify ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)).  
4. Mode full: Prefer Isolated / design-review only when Design present (`03` exists **and** Result `done`) **and** ¬ design-update unpaid **and** ¬ Notes `design-stale` **and** ¬ **Grill open**.  
5. Both Isolated unpaid → same-turn parallel **only**; Prefer general `design-review` **after** Isolated paid when required; resume Prefer only unpaid sibling.  
6. Mode **simple** `design-verify-phase`: Has API/DB ∈ {yes, unknown} (not tiny) → **must write** matching Isolated `03a-api`/`03a-db` + Results; Has=no / Notes `tiny-contract-tweak` → Notes-skip only ([stages/design-verify-phase.md](stages/design-verify-phase.md)). Prefer never launches Isolated Prefer stages under Mode simple.  
7. Do not deep-re-review paid isolated Results. Point API/DB skills from Isolated stages.  
8. Never write Gate B consent.
