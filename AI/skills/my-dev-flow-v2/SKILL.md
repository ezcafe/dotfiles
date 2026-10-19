---
name: my-dev-flow-v2
description: >-
  Orchestrates the AI-assisted delivery pipeline (design → review → build →
  test → merge) without Python helpers. Classifies Mode simple vs full. Gate C
  always blocking; Mode full Gate B blocking; Mode simple Gate B auto only when
  Has API=no AND Has DB=no AND no auth/PII/schema (else blocking). Gate B
  async-notify only when user asks for a veto window on that low-risk path.
  Use when the user says run my-dev-flow-v2, start my-dev-flow-v2, or wants the
  v2 end-to-end delivery pipeline (markdown checklists, no lint scripts).
---

# my-dev-flow-v2

**TL;DR:** Classify Mode → seed `.my-docs/workflow/<slug>/` → follow [stages.md](stages.md) → Gate C always **blocking**. No Python: agent runs [preflight.md](preflight.md) + [derive-next.md](derive-next.md) before each Task.

End-to-end **orchestrator only**. Stage prompts live in subflows.  
**Runtime order (SoT):** [stages.md](stages.md).  
Practices: [AI-assisted engineering](https://newsletter.eng-leadership.com/p/how-to-do-ai-assisted-engineering).

## Start (Step 0)

Follow [step-0.md](step-0.md). Honor [Load budget](step-0.md#load-budget).

**Skills sync:** When `AI/skills/my-dev-flow-v2` exists, run `./AI/skills/sync-to-cursor.sh --check` (or sync) before classify — [skills-path.md](skills-path.md).

**Before every Task:** [preflight.md](preflight.md) → [derive-next.md](derive-next.md) → compose handoff from [handoffs.md](handoffs.md) → load subflow `stages/<id>.md` only ([parent-next.md](parent-next.md)).

## When to run

- **Default:** `run my-dev-flow-v2` / `start my-dev-flow-v2` → classify Mode, then pipeline.
- **Solo subflow:** [solo-entry.md](solo-entry.md).
- **Override:** `simple` / `full` → that Mode; `skip-review` → profile skip-review (Mode simple only unless Decision N).
- **Grill-only:** `grill` / `stress-test this plan` → [grill.md](grill.md).
- **v1:** `my-dev-flow` (archived backup + live v1) — [CUTOVER.md](CUTOVER.md).

## Non-negotiables

1. **Gate C always blocking** — never commit/push/PR/merge without explicit user yes naming each action ([hitl.md](hitl.md)).
2. **No secrets** in commits; never force-push.
3. **Design before code** — design-review or design-verify-phase Result **clean** before Build.
4. **Verify gate** — do not advance on verify-fail ([verify.md](verify.md)).
5. **Do not invent approval** — parent-only consent; Tasks never write Gate B/C approved, Build armed, or provenance.

## Routing

| Need | Read |
|------|------|
| Happy path / Mode × profile | [stages.md](stages.md) |
| Classify / seed | [step-0.md](step-0.md) |
| Pre-Task checks | [preflight.md](preflight.md) · [derive-next.md](derive-next.md) |
| Next → open 1–2 files | [parent-next.md](parent-next.md) |
| Task handoff R/W | [handoffs.md](handoffs.md) |
| Gates / consent | [hitl.md](hitl.md) · [gate-b.md](gate-b.md) · [gate-c.md](gate-c.md) |
| Verify / Smoke / Fix | [verify.md](verify.md) |
| Has API/DB/auth / lenses / skip-review | [lenses.md](lenses.md) |
| Models | [models.md](models.md) |
| Result tokens | [results.md](results.md) |
| Max rounds / Decisions | [decisions.md](decisions.md) |
| Hard-stop chat | [failure.md](failure.md) |
| Resume / abort | [resume.md](resume.md) |
| Design invalid after Build | [design-backloop.md](design-backloop.md) |
| Templates | [artifacts/INDEX.md](artifacts/INDEX.md) |
| Golden paths | [examples/INDEX.md](examples/INDEX.md) |
| Resolve `{skill}` | [skills-path.md](skills-path.md) |
| Cutover from v1 | [CUTOVER.md](CUTOVER.md) |

## Subflows

| Skill | Role |
|-------|------|
| [`my-dev-flow-v2-design`](../my-dev-flow-v2-design/SKILL.md) | Ideation→Design (full) or design-phase (simple) |
| [`my-dev-flow-v2-design-review`](../my-dev-flow-v2-design-review/SKILL.md) | API∥DB + general, or design-verify-phase |
| [`my-dev-flow-v2-code`](../my-dev-flow-v2-code/SKILL.md) | TDD review → Build → Fix |
| [`my-dev-flow-v2-review`](../my-dev-flow-v2-review/SKILL.md) | Adv→Quality→lenses (full) or code-review-phase→lenses (lite) |
| [`my-dev-flow-v2-test`](../my-dev-flow-v2-test/SKILL.md) | Smoke / test-full / test-lite |
| [`my-dev-flow-v2-merge`](../my-dev-flow-v2-merge/SKILL.md) | Gate C → commit/push/PR/merge |

Do **not** re-read this SKILL every step. Load card + Open row + stage prompt only.
