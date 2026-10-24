---
name: my-dev-flow-v3-design
description: >-
  Ideation/brainstorm → Gate A → skim → Analyze → Grill → Design (Mode full),
  or design-phase bundling Analyze+Grill+Design (Mode simple). Also
  design-update from review findings. Runs as isolated Task when orchestrated;
  never AskQuestion for HITL (Parent-relay); hard-stop + Return shape; parent
  stamps parent-only card fields — hitl (consent/Status/Last stage/Next/verify).
  Use when run my-dev-flow-v3-design, design-phase, or parent after Step 0 seed.
---

# my-dev-flow-v3-design

**Orchestrator SoT:** `../my-dev-flow-v3/` (derive, gates, lenses). Load only the current stage file below.

**Isolation:** When parent orchestrates, this skill runs as one fresh Task. Hard stop / Return shape / skill map SoT = [../my-dev-flow-v3/spawn-contract.md](../my-dev-flow-v3/spawn-contract.md). After Task = [../my-dev-flow-v3/step-0.md](../my-dev-flow-v3/step-0.md) After Task (+ Always §8). Do **not** equate [../my-dev-flow-v3/subagents.md](../my-dev-flow-v3/subagents.md) with map/After (optional narrative only). Continue unpaid stages **in this skill only** until Hard stop (HITL, parent-only Next, skill boundary). Return the spawn **Return shape**. Solo: run directly ([../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md)).

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen on `00-run.md`.  
2. Unpaid bans: **ideation unpaid** before Gate A / skim / Analyze / Design / `design-phase` (FIRST `blocked — ideation unpaid`); skim FIRST also **unpaid Gate A** → `blocked — Gate A unpaid` ([stages/skim.md](stages/skim.md)); **Grill open** before Design / `design-update` (both Modes — Mode simple mid-open ≡ Grill open ∧ ¬carve — [../my-dev-flow-v3/grill.md](../my-dev-flow-v3/grill.md)); Notes `design-stale` bans Prefer `design-update` + `design-verify-phase` + Isolated / `design-review` (full unsafe-jump set — [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)); design-update unpaid before Isolated / design-review / design-verify (only when Grill closed).  
3. Parent-only ban: [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated = signals only; labeled solo carve after AskQuestion — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md)).  
4. Derive Next: [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · Prefer SoT [../my-dev-flow-v3/derive-next-pre.md](../my-dev-flow-v3/derive-next-pre.md) · stage index [stages.md](stages.md).  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Stages

| Id | File |
|----|------|
| brainstorm / ideation | [stages/ideation.md](stages/ideation.md) |
| gate-a | [stages/gate-a.md](stages/gate-a.md) |
| skim | [stages/skim.md](stages/skim.md) |
| analyze | [stages/analyze.md](stages/analyze.md) |
| grill | [stages/grill.md](stages/grill.md) |
| design | [stages/design.md](stages/design.md) |
| design-phase | [stages/design-phase.md](stages/design-phase.md) |
| design-update | [stages/design-update.md](stages/design-update.md) |

## Principles

1. Brainstorm hard-gate before Design ([../my-dev-flow-v3/brainstorm.md](../my-dev-flow-v3/brainstorm.md)).  
2. **Grill closed** before Design (Mode full / mid-open — Notes `grill-skip` **or** Result `frontier-empty` only). Mode simple cold-start carve may Prefer `design-phase` while Grill unpaid — [../my-dev-flow-v3/grill.md](../my-dev-flow-v3/grill.md).  
3. Two design options + recommendation.  
4. After design stages: **Orchestrated Task:** return `proposed Has: …` / Has flip / candidate tiny / `candidate grill-skip` / `candidate ideation-confirmed` **signal** only + Parent-relay — parent writes card Has + Notes via Always §4 ([../my-dev-flow-v3/lenses.md](../my-dev-flow-v3/lenses.md) · [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) · [../my-dev-flow-v3/preflight.md](../my-dev-flow-v3/preflight.md)). **Labeled solo:** stamps Notes+provenance after AskQuestion ([../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md) · [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)).  
5. Never write parent-only card fields — [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated Task); labeled solo carve — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).
