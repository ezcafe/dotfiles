---
name: my-dev-flow-v3
description: >-
  Orchestrates AI-assisted delivery (brainstorm → grill → design → review →
  TDD build → quality review → test → merge) with markdown checklists only —
  no Python/JS lint scripts. Classifies Mode simple vs full. Gate C always
  blocking. Mode full Gate B blocking. Mode simple Gate B auto only when Has
  API=no AND Has DB=no AND Has auth/PII/schema=no (explicit no only;
  unknown ≠ no; else blocking). Settle gen freshness; seed only 00-run.md;
  spawn isolated Tasks for subflow skills; parent-inline only Step 0 / Gate
  B·C / finalize-lens-plan / HITL (Parent-relay — Task never AskQuestion);
  Gate C always blocking / no invent consent.
  Use when the user says run my-dev-flow-v3, start my-dev-flow-v3, or wants
  the v3 end-to-end delivery pipeline.
---

# my-dev-flow-v3

**TL;DR:** Classify Mode → seed **only** `00-run.md` under `.my-docs/workflow/<slug>/` → follow [stages.md](stages.md). Each later turn: **routing pack** ([preflight.md](preflight.md) + [derive-next.md](derive-next.md) + matching defs + Prefer half) + **handoff row** + **parent-next Open 1–2** + [clarity-check.md](clarity-check.md) when Next ∈ set (**in addition to** Open 1–2 — not a competing slot). **Orchestrator:** parent stays thin — spawn a **fresh** isolated `Task` per **subflow skill** (open [spawn-contract.md](spawn-contract.md) — Skill map inlined; After = [step-0.md](step-0.md) After Task + Always §8; [subagents.md](subagents.md) optional narrative only); parent-inline only for Step 0 / Gate B·C / `finalize-lens-plan` / HITL (Parent-relay). **SoT:** [step-0.md](step-0.md) Load budget (incl. After Task). Never re-read this full SKILL every step. Gate C always **blocking**. Parent (orchestrated) **or** labeled solo after AskQuestion writes consent ([hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)).

Inspired by APEX step loading, brainstorm hard-gates, frontier grilling, TDD iron law, and multi-axis review — see [references.md](references.md).

## Start (Step 0)

Follow [step-0.md](step-0.md). Honor **Load budget** (SoT there — not restated).

**Before every Task:** routing pack → handoff **row** → **parent-next Open 1–2** → clarity-check when Next ∈ set (**extra** open — does not spend an Open 1–2 slot) ([step-0.md](step-0.md) Load budget) → if Next maps to a subflow skill, open [spawn-contract.md](spawn-contract.md) → **spawn** isolated Task (do not run that stage inline).

## When to run

| Trigger | Action |
|---------|--------|
| `run my-dev-flow-v3` / `start my-dev-flow-v3` | Classify Mode → full pipeline |
| `simple` / `full` | Force that Mode |
| `skip-review` | Profile skip-review — Mode **simple** only when legal ([lenses.md](lenses.md)); else Decision N |
| `grill` / stress-test plan | [grill.md](grill.md) only |
| Solo subflow | [solo-entry.md](solo-entry.md) |
| In-flight v1 resume | Stay on `my-dev-flow` / v1 subflows ([CUTOVER.md](CUTOVER.md)) |
| Former v2 slug / new work | Use `my-dev-flow-v3` (+ v3 subflows); never Prefer `my-dev-flow-v2*` ([CUTOVER.md](CUTOVER.md)) |

## Non-negotiables

1. **Gate C always blocking** — never commit/push/PR/merge without explicit user yes naming each action ([hitl.md](hitl.md)).
2. **No invent consent** — **Orchestrated Task** never writes parent-only fields ([hitl.md](hitl.md)): Gate B/C approved, Build armed, settle gen bumps, provenance, waiver/consent Notes (`has-flip`, `tiny-contract-tweak`, `ideation-skip`, `ideation-confirmed`, `grill-skip`, `04a skipped`, escapes, …), lifecycle Notes (`design-stale` / `design-backloop` / `review-stale` / `test-stale` / `waiting — <reason>`), card Has flags, Status / **Last stage** / card **Next** / Round, profile drop, verify stamps — return `candidate …` / Parent-relay only. **Labeled solo** may stamp after AskQuestion / when applying After signals ([solo-entry.md](solo-entry.md)).
3. **Brainstorm hard-gate** — always (not Has-UI-only); do not Design until Notes `ideation-confirmed` (or waive) ([brainstorm.md](brainstorm.md)).
4. **Design clean before Build** — overall + required isolated reviews paid ([results.md](results.md)).
5. **TDD iron law** — no production code without a failing test first ([../my-dev-flow-v3-code/SKILL.md](../my-dev-flow-v3-code/SKILL.md)).
6. **Verify gate** — do not advance on verify-fail ([verify.md](verify.md)).
7. **No secrets** in commits; never force-push.
8. **No code lint for this skill** — markdown checklists only (no Python/JS skill linters).
9. **Isolated subflows** — orchestrator spawns a fresh skill Task (open [spawn-contract.md](spawn-contract.md) — map inlined; After = step-0 After Task); parent does not run skill-mapped stages inline.

## Routing

| Need | Read |
|------|------|
| Happy path / Mode × profile | [stages.md](stages.md) |
| Classify / seed | [step-0.md](step-0.md) |
| Next stage | [derive-next.md](derive-next.md) (+ defs-pre/post + Prefer halves) · [preflight.md](preflight.md) |
| Clarity-check | [clarity-check.md](clarity-check.md) (preflight Always §6) |
| Open 1–2 files | [parent-next.md](parent-next.md) |
| Isolated subflows (Option B) | spawn open = [spawn-contract.md](spawn-contract.md) (map inlined); After = [step-0.md](step-0.md) After Task; [subagents.md](subagents.md) optional |
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
| Model hints | [models.md](models.md) |
| Templates | [artifacts/INDEX.md](artifacts/INDEX.md) |
| Goldens | [examples/INDEX.md](examples/INDEX.md) |
| Credits | [references.md](references.md) |
| Cutover from v2 | [CUTOVER.md](CUTOVER.md) |

## Subflows

**Orchestrator:** each subflow skill runs in an **isolated Task** when Prefer enters it. **Full skill map SoT only:** [spawn-contract.md](spawn-contract.md). **Solo:** same stage contracts; solo agent runs the skill directly ([solo-entry.md](solo-entry.md)). **Parent-inline only:** Step 0, `gate-b`, `gate-c`, `finalize-lens-plan`. `api|db` both unpaid → two design-review Tasks same turn. Optional narrative: [subagents.md](subagents.md).

## v3 design intent (vs v2)

- **Settle generation** replaces clock-compare freshness ([gate-b.md](gate-b.md)).
- **Prefer/Unsafe SoT is derive-*** — long predicate cells live only in [derive-next-defs-pre.md](derive-next-defs-pre.md) / [derive-next-defs-post.md](derive-next-defs-post.md); narrative files name+link (do not restate cells).
- **Load only current step** — APEX-style progressive disclosure.
- **Isolated subflow Tasks** — one fresh Task per skill entry to save parent context ([spawn-contract.md](spawn-contract.md)).
- **Grill = frontier rounds** with recommended answers ([grill.md](grill.md)).
- **Ideation = brainstorm hard-gate** ([brainstorm.md](brainstorm.md)).
