---
name: my-dev-flow-v3-review
description: >-
  Verifies a code draft: full profile Adv→Quality→lenses; lite code-review-phase
  then lenses. Five-axis review + structural ambition. Fix until clean. Use when
  run my-dev-flow-v3-review or after Build.
---

# my-dev-flow-v3-review

Axes (correctness, readability, architecture, security, performance) from [addyosmani code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md). Structural ambition from [thermo-nuclear](https://raw.githubusercontent.com/cursor/plugins/main/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md). Simplification bias from [code-simplification](https://github.com/addyosmani/agent-skills/blob/main/skills/code-simplification/SKILL.md).

## Stages

| Id | File |
|----|------|
| adversarial | [stages/adversarial.md](stages/adversarial.md) |
| quality | [stages/quality.md](stages/quality.md) |
| code-review-phase | [stages/code-review-phase.md](stages/code-review-phase.md) |
| lens-* | [stages/lenses-overview.md](stages/lenses-overview.md) |
| merge-findings | [stages/merge-findings.md](stages/merge-findings.md) |
| fix-review | [stages/fix-review.md](stages/fix-review.md) |

## FIRST (Adv / Quality)

Require `Smoke source: Smoke-Task` when E1 (Mode full + profile full). Notes companion only — not unlock.
