---
name: my-dev-flow-v3-merge
description: >-
  After explicit Gate C approval (always blocking), commits (if approved),
  pushes, opens PR, then merges. Requires Tests success and Lenses clean;
  never invent Gate C named yes; never write Status (return candidate Status
  only). Parent stamps parent-only card fields — hitl (consent/Status/Last
  stage/Next/verify). Runs as isolated Task after parent Gate C consent;
  hard-stop if merge not in approved. Use when run my-dev-flow-v3-merge or
  after Gate C test bar is met.
---

# my-dev-flow-v3-merge

**Isolation:** When parent orchestrates, this skill runs as one fresh Task **after** Gate C parent-inline consent. Hard stop / Return shape / skill map SoT = [../my-dev-flow-v3/spawn-contract.md](../my-dev-flow-v3/spawn-contract.md). After Task = [../my-dev-flow-v3/step-0.md](../my-dev-flow-v3/step-0.md) After Task (+ Always §8). Do **not** equate [../my-dev-flow-v3/subagents.md](../my-dev-flow-v3/subagents.md) with map/After (optional narrative only). Hard-stop if `merge` ∉ approved. Return the spawn **Return shape**. Solo: run directly.

## Solo FIRST

1. Min card: Mode, profile, Gate C approved + provenance, Tests success fields on `00-run.md`.  
2. Unpaid bans: never Prefer/launch `merge` while ¬ **Tests success**, **Lenses dirty**, **missing required api/db**, ¬ **Lenses clean**, stale Notes unpaid, or `merge` ∉ Gate C approved. **Tests unpaid** is vacuous for skip-review (profile ≠ skip-review only — [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)); Gate C bar = **Tests success** per [../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md), not `06` success alone. Match parent Unsafe jumps ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)).  
3. Parent-only ban: [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated = signals only incl. `candidate Status: done|paused`; labeled solo carve after AskQuestion — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md)).  
4. Derive Next (solo must derive): Prefer first-match SoT = parent [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) (+ [../my-dev-flow-v3/derive-next-defs-post.md](../my-dev-flow-v3/derive-next-defs-post.md) · [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) Unsafe jumps). Local [stages.md](stages.md) = **negative guards only** — not Prefer Next lookup. Bar: [../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md).  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Start

Confirm **Tests success** ≡ Gate C bar ([../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md)) including unpaid stale Notes cleared — not `06` success alone (skip-review needs verify-pass + Smoke-Task + escape Notes↔provenance).  
Confirm **Lenses clean** (covers ¬ Lenses dirty ∧ ¬ missing required ∧ Merged paid when plan 2+ — [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)).  
Confirm each named action ∈ Gate C approved (+ provenance).  
Skip-review: independent Smoke (`Smoke-Task`) required; Build-writes-Smoke alone fails closed; **Tests unpaid** vacuous — bar still **Tests success**.  
Abort if unpaid stale Notes remain or ¬ **Lenses clean**.

## Stages

| Id | File |
|----|------|
| merge | [stages/merge.md](stages/merge.md) |
