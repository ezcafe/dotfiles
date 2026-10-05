---
name: my-dev-flow
description: >-
  Orchestrates the full delivery pipeline by running my-dev-flow-design
  (Ideation → Gate A → skim → Analyze → Grill → Design), my-dev-flow-design-review
  (until clean; isolated API/DB reviews when flagged), optional TDD test-case
  review (only when planned tests exist), HITL-tiered Gate B, Build, smoke,
  my-dev-flow-review (lite/skip-review for simple; conditional lenses), full or
  lite my-dev-flow-test, then blocking Gate C (commit/push/PR/merge need explicit
  user approval — never auto). Soft HITL: auto / async-notify / blocking for
  Gate B only. Classifies simple vs complex. Stage-scoped handoffs + Orchestrator
  card. Artifacts under .my-docs/workflow. Use when the user says run my-dev-flow,
  start my-dev-flow, run my-plan-flow / my-workflow (legacy), simple mode,
  ideate → build → merge, grill / stress-test this plan, or wants the
  AI-assisted delivery pipeline.
---

# my-dev-flow

End-to-end **orchestrator only**. Stage prompts live in subflows. Canonical step
order, Mode/HITL, lenses, usage-limit, and progress rules:
**[stages.md](stages.md)**. Grill: **[grill.md](grill.md)**.

Practices: [AI-assisted engineering](https://newsletter.eng-leadership.com/p/how-to-do-ai-assisted-engineering) —
design-heavy, never ship first draft, generation ≠ verification.

## Package files

| File | Role |
|------|------|
| [SKILL.md](SKILL.md) | Thin orchestrator — when to run, non-negotiables, subflow index |
| [stages.md](stages.md) | Canonical pipeline · Mode · HITL · lenses · models · progress |
| [handoffs.md](handoffs.md) | Stage-scoped handoffs · Decision shape · size caps |
| [artifacts/INDEX.md](artifacts/INDEX.md) | Split artifact templates (one file per stage) |
| [severity.md](severity.md) | Critical/Major vs Enhancement exit rules |
| [skills-path.md](skills-path.md) | Resolve `{my-dev-flow}` and sibling skills |
| [grill.md](grill.md) | Grill (frontier + glossary/ADR) |
| [LEGACY.md](LEGACY.md) | Removed Gate A2 / `01b` / `ui-refs` |

## Sub-workflows

| Order | Skill | Role |
|-------|--------|------|
| 1 | [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md) | Ideation → Gate A → skim → Analyze → Grill → Design; Update from design review |
| 2 | [`my-dev-flow-design-review`](../my-dev-flow-design-review/SKILL.md) | Design gaps → Fix ask until clean (isolated API/DB when flagged) |
| 3 | [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) | Optional TDD review → Build (draft); Fix from test failures |
| 4 | [`my-dev-flow-test`](../my-dev-flow-test/SKILL.md) | Smoke before review; full or lite test after review |
| 5 | [`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) | Adversarial → Quality → Conditional lenses ⇄ Fix (or skip) |
| 6 | [`my-dev-flow-merge`](../my-dev-flow-merge/SKILL.md) | Gate C (**blocking**) → commit/push/PR/merge only after explicit yes |

Each subflow can run **alone** when its prerequisites are met.

## When to run

- **Default:** `run my-dev-flow` / `start my-dev-flow` / `ideate → build → merge` → classify Mode (see stages.md), then pipeline.
- **Legacy alias:** `run my-plan-flow` / `my-workflow` → same as `my-dev-flow` (not Build).
- **Override:** `simple` / `full` / `skip-review` in the trigger → do not re-classify.
- **Grill-only:** `grill` / `grill-with-docs` / `stress-test this plan` → [grill.md](grill.md) (needs Analyze / idea).

## Non-negotiables

1. **Gate C always blocking.** Never commit, push, open a PR, or merge without an explicit user yes that names each action.
2. **No secrets** in commits; never force-push.
3. **Design before code.** Design-review clean before Build (and before optional 04a).
4. **Generation ≠ verification.** Smoke before code review (unless skip-review → Gate C). Test before merge (except skip-review after smoke).
5. **Fresh Task context** + **stage-scoped handoff** ([handoffs.md](handoffs.md)) — never the full artifact catalog.
6. **Orchestrator card** in `00-run.md`: next Task = card + one `stages.md` section. Load each subflow `SKILL.md` **once per phase** (or when Mode/profile changes).
7. **Usage limit:** wait 5s → retry same model once → retry with **`inherit`** once → then main-thread for **that** stage only (later stages still Tasks). Details in stages.md.
8. **User rejects a gate or says stop / change scope** → Status `stopped`; do not auto-resume without a new Decision (stages.md **Abort**).
9. **No UI concept step** — see [LEGACY.md](LEGACY.md).
10. **Plain words.** Decision N when 2+ choices (handoffs.md). User-first picks on Gate B auto / async-notify.

## Start (Step 0)

1. **Classify** simple vs full unless resume or user named Mode → stages.md **Mode selection**. Ambiguous → Decision N.
2. Pick slug `YYYYMMDD-feature-x` (UTC date + kebab feature). Seed `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md).
3. Resolve High / Medium / Fast from Task allowlist → `00-run.md` (stages.md **Models**). Set Mode, Review profile, HITL Gate B, **HITL Gate C: blocking**, Orchestrator card.
4. Chat one line: Mode + Review profile + why.
5. Mode **simple** without `01-idea.md` → bootstrap thin idea; note skipped early gates. Do not invent legacy UI-concept artifacts.
6. Run pipeline in [stages.md](stages.md). After each step: ≤5 lines summary + path; update Orchestrator card.

## Parent load rule

| Need | Read |
|------|------|
| Next step | `00-run.md` Orchestrator card + **one** stages.md section |
| Task prompt | handoffs.md row for stage id + that stage’s stages.md rules |
| New artifact body | one file under [artifacts/](artifacts/INDEX.md) only |
| Grill | grill.md (once when entering Grill) |
| Phase entry | that subflow `SKILL.md` once |

Do **not** re-read this whole SKILL every step.
