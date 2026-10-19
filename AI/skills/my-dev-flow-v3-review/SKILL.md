---
name: my-dev-flow-v3-review
description: >-
  Verifies a code draft: full profile Adv→Quality→lenses; lite code-review-phase
  then lenses. Five-axis review + structural ambition. Fix until clean. Use when
  run my-dev-flow-v3-review or after Build.
---

# my-dev-flow-v3-review

Axes (correctness, readability, architecture, security, performance) from [addyosmani code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md). Structural ambition from [thermo-nuclear](https://raw.githubusercontent.com/cursor/plugins/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md). Simplification bias from [code-simplification](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md).

## Solo FIRST

1. Min card: Mode, profile, Has flags, settle gen, Smoke source on `00-run.md`.  
2. Unpaid bans: E1 needs `Smoke source: Smoke-Task` before Adv; Lens plan api/db **before Smoke and before Adv/lenses** (match Post-Build / [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md)); ban Prefer `test-*` / `gate-c` / `merge` while **Lenses dirty** **or** ¬ **Lenses clean** (match Unsafe jumps — [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md)).  
3. Parent-only ([../my-dev-flow-v3/hitl.md](../my-dev-flow-v3/hitl.md)): never write Gate B/C consent / escape Notes / settle gen, **lifecycle Notes** (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), or **card Has** — Stages return `candidate …` / `proposed Has` only.  
4. Derive Next: [../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) · Prefer SoT [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · stage index [stages.md](stages.md).  
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

**Order:** missing required api/db → E1 Smoke unpaid → Adv (Prefer finalize → Smoke → Adv).

If Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (Lens plan = `none` **or** missing required `api`/`db`) → `blocked — missing required api/db` (Prefer `finalize-lens-plan` — same FIRST on [stages/adversarial.md](stages/adversarial.md) · [stages/quality.md](stages/quality.md) · [stages/code-review-phase.md](stages/code-review-phase.md) · [../my-dev-flow-v3/lenses.md](../my-dev-flow-v3/lenses.md) · [../my-dev-flow-v3/derive-next-post.md](../my-dev-flow-v3/derive-next-post.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md)). True **Lens plan unpaid** (plan≠`none` + unpaid `05-lens-*`) stays Prefer unpaid `lens-*` — not this token.

If E1 (Mode full + profile full) and `Smoke source` ≠ `Smoke-Task` → `blocked — Smoke unpaid` (same FIRST on those stages). Notes companion only — not unlock. See [../my-dev-flow-v3/parent-next.md](../my-dev-flow-v3/parent-next.md) · [../my-dev-flow-v3/verify.md](../my-dev-flow-v3/verify.md).

Lens **`needs fix`** → Prefer `fix-review`; Prefer `merge-findings` only when planned lenses **clean** (or after Fix re-unpay). Ban Prefer `test-*` / `gate-c` / `merge` while **Lenses dirty** **or** ¬ **Lenses clean** ([../my-dev-flow-v3/derive-next.md](../my-dev-flow-v3/derive-next.md) Unsafe jumps).
