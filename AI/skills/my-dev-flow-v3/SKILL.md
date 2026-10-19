---
name: my-dev-flow-v3
description: >-
  Orchestrates AI-assisted delivery (brainstorm → grill → design → review →
  TDD build → quality review → test → merge) with markdown checklists only —
  no Python/JS lint scripts. Classifies Mode simple vs full. Gate C always
  blocking. Mode full Gate B blocking. Mode simple Gate B auto only when Has
  API=no AND Has DB=no AND no auth/PII/schema. Prefer subflows or run stages
  from this skill. Use when the user says run my-dev-flow-v3, start
  my-dev-flow-v3, or wants the v3 end-to-end delivery pipeline.
---

# my-dev-flow-v3

**TL;DR:** Classify Mode → seed `.my-docs/workflow/<slug>/` → follow [stages.md](stages.md). Load **only** the current phase file. Gate C always **blocking**. Parent alone writes consent.

Inspired by APEX step loading, brainstorm hard-gates, frontier grilling, TDD iron law, and multi-axis review — see [references.md](references.md).

## Start (Step 0)

Follow [step-0.md](step-0.md). Honor **Load budget**.

**Before every Task:** [preflight.md](preflight.md) → [derive-next.md](derive-next.md) → handoff row from [handoffs.md](handoffs.md) → open 1–2 files via [parent-next.md](parent-next.md) → subflow `stages/<id>.md` **or** orchestrator stage if solo.

Do **not** re-read this SKILL every step.

## When to run

| Trigger | Action |
|---------|--------|
| `run my-dev-flow-v3` / `start my-dev-flow-v3` | Classify Mode → full pipeline |
| `simple` / `full` | Force that Mode |
| `skip-review` | Profile skip-review — Mode **simple** only when legal ([lenses.md](lenses.md)); else Decision N |
| `grill` / stress-test plan | [grill.md](grill.md) only |
| Solo subflow | [solo-entry.md](solo-entry.md) |
| v2 resume | Prefer stay on v2; see [CUTOVER.md](CUTOVER.md) |

## Non-negotiables

1. **Gate C always blocking** — never commit/push/PR/merge without explicit user yes naming each action ([hitl.md](hitl.md)).
2. **No invent consent** — Tasks never write Gate B/C approved, Build armed, settle gen, or provenance.
3. **Brainstorm hard-gate** — do not Design until shared understanding ([brainstorm.md](brainstorm.md)).
4. **Design clean before Build** — overall + required isolated reviews paid ([results.md](results.md)).
5. **TDD iron law** — no production code without a failing test first ([../my-dev-flow-v3-code/SKILL.md](../my-dev-flow-v3-code/SKILL.md)).
6. **Verify gate** — do not advance on verify-fail ([verify.md](verify.md)).
7. **No secrets** in commits; never force-push.
8. **No code lint for this skill** — markdown checklists only (no Python/JS skill linters).

## Routing

| Need | Read |
|------|------|
| Happy path / Mode × profile | [stages.md](stages.md) |
| Classify / seed | [step-0.md](step-0.md) |
| Next stage | [derive-next.md](derive-next.md) · [preflight.md](preflight.md) |
| Open 1–2 files | [parent-next.md](parent-next.md) |
| Handoff R/W | [handoffs.md](handoffs.md) |
| Gates / consent | [hitl.md](hitl.md) · [gate-b.md](gate-b.md) · [gate-c.md](gate-c.md) |
| Smoke / Fix / stale | [verify.md](verify.md) |
| Has flags / lenses / skip-review | [lenses.md](lenses.md) |
| Result tokens | [results.md](results.md) |
| Grill / brainstorm | [grill.md](grill.md) · [brainstorm.md](brainstorm.md) |
| Caps / Decision N | [decisions.md](decisions.md) |
| Hard-stop | [failure.md](failure.md) |
| Resume | [resume.md](resume.md) |
| Design invalid after Build | [design-backloop.md](design-backloop.md) |
| Templates | [artifacts/INDEX.md](artifacts/INDEX.md) |
| Goldens | [examples/INDEX.md](examples/INDEX.md) |
| Credits | [references.md](references.md) |
| Cutover from v2 | [CUTOVER.md](CUTOVER.md) |

## Subflows (optional)

Run via orchestrator **or** solo. Same stage contracts either way.

| Skill | Role |
|-------|------|
| [`my-dev-flow-v3-design`](../my-dev-flow-v3-design/SKILL.md) | Brainstorm → Gate A → Analyze → Grill → Design (full) or design-phase (simple) |
| [`my-dev-flow-v3-design-review`](../my-dev-flow-v3-design-review/SKILL.md) | API∥DB + general, or design-verify-phase |
| [`my-dev-flow-v3-code`](../my-dev-flow-v3-code/SKILL.md) | TDD → Build → Fix |
| [`my-dev-flow-v3-review`](../my-dev-flow-v3-review/SKILL.md) | Adv → Quality → lenses (full) or code-review-phase (lite); structural ambition |
| [`my-dev-flow-v3-test`](../my-dev-flow-v3-test/SKILL.md) | Smoke / test-full / test-lite |
| [`my-dev-flow-v3-merge`](../my-dev-flow-v3-merge/SKILL.md) | Gate C → commit/push/PR/merge |

## v3 design intent (vs v2)

- **Settle generation** replaces clock-compare freshness ([gate-b.md](gate-b.md)).
- **One SoT per concern** — copies point; do not restate long bars.
- **Load only current step** — APEX-style progressive disclosure.
- **Grill = frontier rounds** with recommended answers ([grill.md](grill.md)).
- **Ideation = brainstorm hard-gate** ([brainstorm.md](brainstorm.md)).
