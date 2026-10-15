---
name: my-dev-flow-design
description: >-
  Runs Ideation → Gate A → skim → Analyze → Grill → Design (Mode full), or one
  design-phase Task bundling Analyze+Grill+Design (Mode simple). Gate B comes
  later (after design-review / design-verify-phase + optional TDD review). Also
  updates design docs from my-dev-flow-design-review findings. Writes framing,
  skim, analysis, grill, design options (two in full; one in simple), system
  design + design-patterns, sequence diagrams, API/database contracts, and
  TDD-ready tasks under .my-docs/workflow. Use when the user says run
  my-dev-flow-design, design-only workflow, update design from review, or after
  my-dev-flow-design-review.
---

# my-dev-flow-design

Design-only subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). No production code.

**Honor parent SoT** (do not restate Happy path / veto / skip-review / Gate B here):

| Topic | File |
|-------|------|
| Runtime order / Mode | [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) |
| Stage prompts | [stages.md](stages.md) index → load **`stages/<stage-id>.md` only** |
| Handoffs | **Required** `scripts/handoff-for.py <stage-id>` · [`handoffs.md`](../my-dev-flow/handoffs.md) = edit SoT / debug only |
| Grill / HITL | [`../my-dev-flow/grill.md`](../my-dev-flow/grill.md) · [`../my-dev-flow/hitl.md`](../my-dev-flow/hitl.md) |
| Has API/DB / tiny-tweak | [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) |
| Max rounds / backloop | [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) |
| Result tokens | [`../my-dev-flow/results.md`](../my-dev-flow/results.md) |
| Templates | [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md) |
| Legacy (no UI concept step) | [`../my-dev-flow/LEGACY.md`](../my-dev-flow/LEGACY.md) |

## When to run

`run my-dev-flow-design`, design-only, update design from review, or when `my-dev-flow` reaches design / design↔review.

## Principles (owned here)

- Design is the main artifact. Attack assumptions; ask “is this clear?”
- **Design options:** Mode **full** → two options + tradeoffs; Mode **simple** → one recommended + ≤3-line rejected alternative. Decision shape: handoffs.md.
- **Required in `03-design.md`:** keep headings (System design, Sequence, Contracts, Design patterns, UI, OWASP) — expand when Has API/DB/UI or Mode full ([artifacts/03-design.md](../my-dev-flow/artifacts/03-design.md)).
- **Has UI:** set in Ideation → `00-run.md`. When yes, lock layout/IA in `03` + acceptance in `04`; match chrome + Gate A 80/20 when `01a` exists.
- **Has API / Has DB:** set `yes`/`no` in Analyze or Design. This skill does **not** write `03a-*`.
- **Gate A** (full): day-to-day + 80/20 → `01a`; auto when Result **ok**.
- **Grill** after Analyze: grill.md. Do not start Design on `needs-round`. HITL Grill ≠ Gate B.
- **Update from review:** only `03a` Fix ask; stay aligned with Gate A idea.
- Plain words. Max 3 design↔review rounds → Decision N (invariants.md).

## Models

[`../my-dev-flow/models.md`](../my-dev-flow/models.md).

## Prerequisites

**Full:** user idea; create slug/`00-run.md` if standalone.  
**Simple:** `01-idea.md` present (or parent bootstrap); Mode simple; do not invent Ideation/Gate A/skim.  
**Update:** `03a` Result **needs update** + existing `01`–`04`.

If not ready → **stop**.

## Pipeline

Parent order: [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md).

```
Full:   Ideation → Gate A → skim → Analyze → Grill → Design → (parent) design-review → …
Simple: design-phase → (parent) design-verify-phase → …
Update: Update from 03a → (parent) re-review
```

## Orchestrator rules

- Detect: `03a` needs update → Update; Mode simple → **design-phase** only; else Full.
- Full: separate Tasks; Gate A before Analyze; Grill before Design.
- Simple: one `design-phase` Task; Grill inside bundle when frontier open / Has API/DB.
- Fresh Task + `stages/<id>.md` + paste `scripts/handoff-for.py <stage-id>` output (do not load whole handoffs.md for launch).
- After Design: parent runs design-review / design-verify-phase before Gate B — do not Gate B from this skill.
- Design-backloop / veto / skip-review: parent SoT links above.

## Skills used

| Stage | Skills |
|-------|--------|
| Ideation | `myplan` |
| Gate A / skim | none / explore |
| Analyze | explore; `dev-decision-routing` if front-end |
| Grill | grill.md; `documentation-and-adrs` |
| Design / Update | `myplan`; `planning-and-task-breakdown`; `documentation-and-adrs`; `api-and-interface-design`; `database-and-data-model`; `security-and-hardening`; UI skills when Has UI |

## Start checklist

1. Confirm Full / Simple / Update + files; resolve models.
2. Run stage prompts per Mode.
3. Hand off to design-review / design-verify-phase (parent).
