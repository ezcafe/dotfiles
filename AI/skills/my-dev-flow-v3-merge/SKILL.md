---
name: my-dev-flow-v3-merge
description: >-
  After explicit Gate C approval, commits (if approved), pushes, opens PR, then
  merges. Never commit/push without named user yes. Use when run
  my-dev-flow-v3-merge or after Gate C test bar is met.
---

# my-dev-flow-v3-merge

## Solo FIRST

1. Min card: Mode, profile, Gate C approved + provenance, Tests success fields on `00-run.md`.  
2. Unpaid bans: never Prefer/launch `merge` while ¬ **Tests success**, **Lenses dirty**, **missing required api/db**, ¬ **Lenses clean**, stale Notes unpaid, or `merge` ∉ Gate C approved. **Tests unpaid** is vacuous for skip-review (profile ≠ skip-review only — [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)); Gate C bar = **Tests success** per [../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md), not `06` success alone. Match parent Unsafe jumps ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)).  
3. Parent-only ([../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)): never invent Gate C named yes / provenance, **lifecycle Notes** (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), or **card Has** — Stages return `candidate …` only.  
4. Derive Next: Prefer first-match SoT = parent [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) (+ [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) Definitions / Unsafe jumps). Local [stages.md](stages.md) = **negative guards only** — not Prefer Next lookup. Bar: [../my-dev-flow-v3/gate-c.md](../my-dev-flow-v3/gate-c.md).  
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
