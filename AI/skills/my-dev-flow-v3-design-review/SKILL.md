---
name: my-dev-flow-v3-design-review
description: >-
  Reviews design artifacts. Prefer design-update first when Result needs update.
  Prefer re-run Isolated/design-review only when unpaid ≠ needs update (missing
  or Result pending). Mode full: both Isolated unpaid → same-turn parallel only;
  Prefer general design-review after Isolated paid. Mode simple:
  design-verify-phase. Runs as isolated Task when orchestrated; never AskQuestion
  for HITL (Parent-relay); hard-stop + Return shape; parent stamps parent-only
  card fields — hitl (consent/Status/Last stage/Next/verify). Use when run
  my-dev-flow-v3-design-review or after design before Build.
---

# my-dev-flow-v3-design-review

**Orchestrator SoT:** Isolated unpaid, Design clean — `../my-dev-flow-v3/derive-next.md` · `derive-next-pre.md` · `results.md`.

**Isolation:** When parent orchestrates, this skill runs as one fresh Task. Hard stop / Return shape / skill map SoT = [../my-dev-flow-v3/spawn-contract.md](../my-dev-flow-v3/spawn-contract.md). After Task = [../my-dev-flow-v3/step-0.md](../my-dev-flow-v3/step-0.md) After Task (+ Always §8). Do **not** equate [../my-dev-flow-v3/subagents.md](../my-dev-flow-v3/subagents.md) with map/After (optional narrative only). Continue unpaid stages **in this skill only** until Hard stop. Parallel `api|db` = two Tasks same turn. Return the spawn **Return shape**. Solo: run directly.

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen on `00-run.md`.  
2. Unpaid bans: no Isolated / design-review / design-verify while ¬ Design present, design-update unpaid, Notes `design-stale`, or **Grill open** ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) unsafe jumps · [../my-dev-flow-v3/grill.md](../my-dev-flow-v3/grill.md)).  
3. Parent-only ban: [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated = signals only; labeled solo carve after AskQuestion — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md)).  
4. Derive Next (solo must derive): [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · Prefer SoT [../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) · stage index [stages.md](stages.md). Prefer unpaid `design-update` when **design-update unpaid**; Prefer **Grill open** → `grill` first; Prefer re-run Isolated / design-review / design-verify only when unpaid ≠ **`needs update`** — defs [../my-dev-flow-v3/derive-next-defs-pre.md](../my-dev-flow-v3/derive-next-defs-pre.md). If derived Next ∉ this skill’s stage ids (`design-update` / `grill` / …) → open that skill’s stage via [../my-dev-flow-v3/parent-next.md](../my-dev-flow-v3/parent-next.md) Open 1–2 **or** hard-stop `skill-boundary:<id>` — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md) skill-boundary.  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md) (incl. skill-boundary when Next outside this skill).

## Stages

| Id | File |
|----|------|
| api-contract-review | [stages/api-contract-review.md](stages/api-contract-review.md) |
| db-design-review | [stages/db-design-review.md](stages/db-design-review.md) |
| design-review | [stages/design-review.md](stages/design-review.md) |
| design-verify-phase | [stages/design-verify-phase.md](stages/design-verify-phase.md) |

## Principles

1. Unpaid = missing **or** Result ≠ `clean` (incl. `pending`). **design-update unpaid** / **Grill open** / Isolated unpaid — name+link only ([../my-dev-flow-v3/derive-next-defs-pre.md](../my-dev-flow-v3/derive-next-defs-pre.md) · [../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md)). Orchestrated Task: write Result → **Hard stop** — do **not** Prefer Next; parent re-derives.  
2. Allowed Results: `clean` \| `needs update` \| `pending` (Isolated also `skipped`). Advance-on-clean / Done when = `clean` only; writing **`needs update`** allowed ≠ Done.  
3. Result **`needs update`** **or** rewrite unpaid → **Hard stop**; parent pays Run-log `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** after `design-update` Task complete ([../my-dev-flow-v3/design-backloop.md](../my-dev-flow-v3/design-backloop.md) · [../my-dev-flow-v3/preflight.md](../my-dev-flow-v3/preflight.md) Always §8) — do **not** invent Run-log pay from this skill.  
4. Mode full: launch Isolated / design-review only when Design present **and** ¬ design-update unpaid **and** ¬ Notes `design-stale` **and** ¬ **Grill open** — else FIRST blocked / Hard stop ([../my-dev-flow-v3/derive-next-defs-pre.md](../my-dev-flow-v3/derive-next-defs-pre.md)).  
5. Both Isolated unpaid → same-turn parallel **only**; general `design-review` after Isolated paid when required; resume only unpaid sibling — parent Prefer SoT ([../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md)).  
6. Mode **simple** `design-verify-phase`: Has API/DB ∈ {yes, unknown} (not tiny) → **must write** matching Isolated `03a-api`/`03a-db` + Results; Has=no / Notes `tiny-contract-tweak` → Notes-skip only ([stages/design-verify-phase.md](stages/design-verify-phase.md)). Never launch Isolated Prefer stages under Mode simple.  
7. Do not deep-re-review paid isolated Results. Point API/DB skills from Isolated stages.  
8. Never write parent-only card fields — [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated Task); labeled solo carve — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).
