---
name: my-dev-flow-v2-design
description: >-
  Runs Ideation → Gate A → skim → Analyze → Grill → Design (Mode full), or one
  design-phase Task bundling Analyze+Grill+Design (Mode simple). Also updates
  design docs from design-review findings. Writes framing, analysis, grill,
  design options, contracts, and TDD-ready tasks under .my-docs/workflow. Use
  when the user says run my-dev-flow-v2-design, design-only workflow, or after
  my-dev-flow-v2-design-review.
---

# my-dev-flow-v2-design

Design-only subflow of [`my-dev-flow-v2`](../my-dev-flow-v2/SKILL.md). No production code.

| Topic | File |
|-------|------|
| Runtime order | [`../my-dev-flow-v2/stages.md`](../my-dev-flow-v2/stages.md) |
| Stage prompts | load **`stages/<id>.md` only** |
| Handoffs | compose from [`../my-dev-flow-v2/handoffs.md`](../my-dev-flow-v2/handoffs.md) |
| Grill / HITL | [`../my-dev-flow-v2/grill.md`](../my-dev-flow-v2/grill.md) · [`../my-dev-flow-v2/hitl.md`](../my-dev-flow-v2/hitl.md) |
| Has API/DB | [`../my-dev-flow-v2/lenses.md`](../my-dev-flow-v2/lenses.md) |
| Max rounds | [`../my-dev-flow-v2/decisions.md`](../my-dev-flow-v2/decisions.md) |
| Results | [`../my-dev-flow-v2/results.md`](../my-dev-flow-v2/results.md) |
| Templates | [`../my-dev-flow-v2/artifacts/INDEX.md`](../my-dev-flow-v2/artifacts/INDEX.md) |

## Principles

- Design is the main artifact. Mode **full** → two options; Mode **simple** → one + ≤3-line reject.
- Set Has UI / API / DB / auth/PII/schema when known. Do **not** write `03a-*`.
- Gate A (full): auto when Result **ok**. Grill before Design; do not Design on `needs-round`.
- Update from `03a` Fix ask or Notes `design-backloop`. Max 3 design↔review rounds → Decision N.

## Pipeline

```
Full:   Ideation → Gate A → skim → Analyze → Grill → Design → (parent) design-review
Simple: design-phase → (parent) design-verify-phase
Update: design-update → (parent) re-review
```

## Start

1. Confirm Full / Simple / Update + files; resolve models ([models.md](../my-dev-flow-v2/models.md)).
2. Clarity when Next ∈ design boundaries ([stages/clarity-check.md](stages/clarity-check.md)).
3. Compose handoff; run `stages/<id>.md`.
4. Hand off to design-review / design-verify (parent).
