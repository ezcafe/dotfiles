---
name: my-dev-flow-v3-test
description: >-
  Supports smoke (E1 / skip-review Prefer unpaid), test-full, and test-lite.
  Runs as isolated Task when orchestrated; never AskQuestion for HITL
  (Parent-relay); hard-stop + Return shape; parent stamps parent-only card
  fields — hitl (consent/Status/Last stage/Next/verify). Use when run
  my-dev-flow-v3-test or after review before merge.
---

# my-dev-flow-v3-test

**Isolation:** When parent orchestrates, this skill runs as one fresh Task. Hard stop / Return shape / skill map SoT = [../my-dev-flow-v3/spawn-contract.md](../my-dev-flow-v3/spawn-contract.md). After Task = [../my-dev-flow-v3/step-0.md](../my-dev-flow-v3/step-0.md) After Task (+ Always §8). Do **not** equate [../my-dev-flow-v3/subagents.md](../my-dev-flow-v3/subagents.md) with map/After (optional narrative only). Continue unpaid stages **in this skill only** until Hard stop (e.g. skill boundary → code skill). Return the spawn **Return shape**. Solo: run directly.

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen, Last Verify on `00-run.md`.  
2. Unpaid bans: E1 / skip-review Prefer unpaid independent Smoke (`Smoke source: Smoke-Task`); Build-writes-Smoke does not waive. Smoke fail → Prefer `fix-tests` first (Prefer-re-smoke only after fix-tests + verify-pass) — Mode×profile [../my-dev-flow-v3/stages.md](../my-dev-flow-v3/stages.md) · [stages/smoke.md](stages/smoke.md). Smoke FIRST leads with **missing required api/db**; test-full/lite FIRST order: (1) **missing required api/db** → (2) **Lenses dirty** / ¬ **Lenses clean** → (3) ¬ **Review clean** → `Result: blocked — …` (same FIRST on [stages/smoke.md](stages/smoke.md) · [stages/test-full.md](stages/test-full.md) · [stages/test-lite.md](stages/test-lite.md) — [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/preflight.md](../my-dev-flow-v3/preflight.md)).
3. Parent-only ban: [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated = signals only — Task sets Smoke source; labeled solo carve after AskQuestion — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md)).  
4. Derive Next (solo must derive): Prefer first-match SoT = parent [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) (+ [../my-dev-flow-v3/derive-next-defs-post.md](../my-dev-flow-v3/derive-next-defs-post.md) · [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) Unsafe jumps). Prefer `merge`\|`gate-c` only when **Tests success** **and** **Lenses clean**. Local [stages.md](stages.md) = **negative guards only** — not Prefer Next lookup.  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Start

1. Derive Expected Next (solo) **or** run Expected Next from parent spawn.  
2. Smoke Task sets `Smoke source: Smoke-Task` only; parent owns Notes (orchestrated) / labeled solo stamps Notes+provenance when required.  
3. On test-full/lite success: return `candidate clear test-stale` when Lite/full clear met — **Hard stop**; parent re-derives ([../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md) · [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)).

## Stages

| Id | File |
|----|------|
| smoke | [stages/smoke.md](stages/smoke.md) |
| test-full | [stages/test-full.md](stages/test-full.md) |
| test-lite | [stages/test-lite.md](stages/test-lite.md) |
