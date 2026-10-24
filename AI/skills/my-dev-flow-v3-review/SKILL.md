---
name: my-dev-flow-v3-review
description: >-
  Verifies a code draft: full profile Adv→Quality→lenses; lite code-review-phase
  then lenses. Five-axis review + structural ambition. Fix until clean. Runs as
  isolated Task when orchestrated; never AskQuestion for HITL (Parent-relay);
  hard-stop + Return shape; parent stamps parent-only card fields — hitl
  (consent/Status/Last stage/Next/verify). Use when run my-dev-flow-v3-review or
  after Build.
---

# my-dev-flow-v3-review

Axes (correctness, readability, architecture, security, performance) from [addyosmani code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md). Structural ambition from [thermo-nuclear](https://raw.githubusercontent.com/cursor/plugins/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md). Simplification bias from [code-simplification](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md).

**Isolation:** When parent orchestrates, this skill runs as one fresh Task. Hard stop / Return shape / skill map SoT = [../my-dev-flow-v3/spawn-contract.md](../my-dev-flow-v3/spawn-contract.md). After Task = [../my-dev-flow-v3/step-0.md](../my-dev-flow-v3/step-0.md) After Task (+ Always §8). Do **not** equate [../my-dev-flow-v3/subagents.md](../my-dev-flow-v3/subagents.md) with map/After (optional narrative only). Continue unpaid stages **in this skill only** until Hard stop (e.g. skill boundary → return). Return the spawn **Return shape**. Solo: run directly.

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen, Smoke source on `00-run.md`.  
2. Unpaid bans: E1 needs `Smoke source: Smoke-Task` before Adv; Lens plan api/db **before Smoke and before Adv/lenses** (match Post-Build / [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md)); ban Prefer `test-*` / `gate-c` / `merge` while **Lenses dirty** **or** ¬ **Lenses clean** (match Unsafe jumps — [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)).  
3. Parent-only ban: [../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md) Parent-only (orchestrated = signals only; labeled solo carve after AskQuestion — [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md)).  
4. Derive Next (solo must derive): [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · Prefer SoT [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · stage index [stages.md](stages.md). Order: missing required api/db → Prefer `finalize-lens-plan` → E1 Smoke unpaid → Adv; lens **`needs fix`** → Prefer `fix-review`; Prefer `merge-findings` only when planned lenses **clean**.  
5. Solo entry: [../my-dev-flow-v3/solo-entry.md](../my-dev-flow-v3/solo-entry.md).

## Stages

| Id | File |
|----|------|
| adversarial | [stages/adversarial.md](stages/adversarial.md) |
| quality | [stages/quality.md](stages/quality.md) |
| code-review-phase | [stages/code-review-phase.md](stages/code-review-phase.md) |
| lenses overview | [stages/lenses-overview.md](stages/lenses-overview.md) |
| lens-api | [stages/lens-api.md](stages/lens-api.md) |
| lens-db | [stages/lens-db.md](stages/lens-db.md) |
| lens-security | [stages/lens-security.md](stages/lens-security.md) |
| lens-perf | [stages/lens-perf.md](stages/lens-perf.md) |
| lens-memory | [stages/lens-memory.md](stages/lens-memory.md) |
| merge-findings | [stages/merge-findings.md](stages/merge-findings.md) |
| fix-review | [stages/fix-review.md](stages/fix-review.md) |

## FIRST (Adv / Quality / code-review-phase)

**Order (blocked Result only — parent re-derives):** missing required api/db → E1 Smoke unpaid → Adv.

If Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (Lens plan = `none` **or** missing required `api`/`db`) → `blocked — missing required api/db` — **Hard stop**; parent re-derives ([../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/lenses.md](../my-dev-flow-v3/lenses.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md) · same FIRST on [stages/adversarial.md](stages/adversarial.md) · [stages/quality.md](stages/quality.md) · [stages/code-review-phase.md](stages/code-review-phase.md)). True **Lens plan unpaid** (plan≠`none` + unpaid `05-lens-*`) is a different unpaid token — not this block.

If E1 (Mode full + profile full) and `Smoke source` ≠ `Smoke-Task` → `blocked — Smoke unpaid` (same FIRST on those stages) — **Hard stop**; parent re-derives. Notes companion only — not unlock. See [../my-dev-flow-v3/parent-next.md](../my-dev-flow-v3/parent-next.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md).

Lens **`needs fix`** → **Hard stop**; Ban Prefer `merge-findings` / `test-*` / `gate-c` / `merge` while **Lenses dirty** **or** ¬ **Lenses clean** ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) Unsafe jumps · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md)).
