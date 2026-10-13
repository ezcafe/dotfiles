---
name: my-dev-flow
description: >-
  Orchestrates the full delivery pipeline. Runtime order only in stages.md
  Happy path (after Build: Smoke → review → test → Gate C). Design →
  design-review → optional TDD → Gate B → Build (Verify + Smoke Option B) →
  review (lite must code-review-phase) → test-full/lite → blocking Gate C.
  Design-backloop Decision when Build proves design wrong. Soft HITL for Gate B
  and Grill (independent). Classifies simple vs full. Skills SoT: AI/skills
  (sync-to-cursor.sh). Artifacts under .my-docs/workflow. Use when the user says
  run my-dev-flow, start my-dev-flow, run my-plan-flow / my-workflow (legacy),
  simple mode, ideate → build → merge, grill / stress-test this plan, or wants
  the AI-assisted delivery pipeline.
---

# my-dev-flow

End-to-end **orchestrator only**. Stage prompts live in subflows. Canonical step
order, Mode/HITL, lenses, usage-limit, and progress rules:
**[stages.md](stages.md)**. Grill: **[grill.md](grill.md)**. Verify/Fix:
**[verify-and-fix.md](verify-and-fix.md)**.

Practices: [AI-assisted engineering](https://newsletter.eng-leadership.com/p/how-to-do-ai-assisted-engineering) —
design-heavy, never ship first draft, generation ≠ verification.

## Package files

| File | Role |
|------|------|
| [SKILL.md](SKILL.md) | Thin orchestrator — when to run, non-negotiables, subflow index |
| [stages.md](stages.md) | Canonical pipeline · Mode · HITL · lenses · models · progress |
| [handoffs.md](handoffs.md) | Stage-scoped handoffs · Decision shape · size caps |
| [verify-and-fix.md](verify-and-fix.md) | Shared Verify gate + Fix rules (Build / Fix-from-tests / review Fix) |
| [artifacts/INDEX.md](artifacts/INDEX.md) | Split artifact templates (one file per stage) |
| [severity.md](severity.md) | Critical/Major vs Enhancement exit rules |
| [skills-path.md](skills-path.md) | Resolve `{my-dev-flow}`; SoT `AI/skills/` |
| [grill.md](grill.md) | Grill (frontier + glossary/ADR) |
| [LEGACY.md](LEGACY.md) | Removed Gate A2 / `01b` / `ui-refs`; `spm-*` → `lens-*` |

## Sub-workflows (inventory — not runtime order)

**Runtime order** lives only in [stages.md](stages.md) (**Happy path** + Full/Simple pipeline).
Canonical after Build: **Smoke → review → test → Gate C**. Do **not** infer order from this table.

| Skill | Role |
|-------|------|
| [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md) | Full chain or simple **design-phase**; Update from design review; design-backloop updates |
| [`my-dev-flow-design-review`](../my-dev-flow-design-review/SKILL.md) | Full: API∥DB parallel + general; simple: **design-verify-phase** |
| [`my-dev-flow-code`](../my-dev-flow-code/SKILL.md) | Optional TDD review → Build (draft + Verify gate + Smoke section); Fix from tests/review |
| [`my-dev-flow-review`](../my-dev-flow-review/SKILL.md) | Full: Adv→Quality→lenses; lite: **must** code-review-phase |
| [`my-dev-flow-test`](../my-dev-flow-test/SKILL.md) | Smoke re-run (usually skipped); **test-full** or **test-lite** (after review clean) |
| [`my-dev-flow-merge`](../my-dev-flow-merge/SKILL.md) | Gate C (**blocking**) → commit/push/PR/merge only after explicit yes |

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
4. **Generation ≠ verification.** After Build verify-pass, skip Smoke Task by default (Option B); full/lite still re-verify before merge (unless skip-review → Gate C on verify-pass).
5. **Build / Fix Verify gate.** Build and Fix must reach **verify-pass** (Verify commands; max 3 attempts) before the parent advances; first return line `Result: verify-pass | verify-fail`. See [verify-and-fix.md](verify-and-fix.md).
6. **Fresh Task context** + **stage-scoped handoff** ([handoffs.md](handoffs.md)) — never the full artifact catalog. Mode simple uses phase-bundle stage ids (stages.md **Speed defaults**).
7. **Orchestrator card** in `00-run.md`: next Task = card + one `stages.md` section. Load each subflow `SKILL.md` **once per phase** (or when Mode/profile changes).
8. **Usage limit:** wait 5s → retry same model once → retry with **`inherit`** once → then main-thread for **that** stage only (later stages still Tasks). Details in stages.md.
9. **User rejects a gate or says stop / change scope** → Status `stopped`; do not auto-resume without a new Decision (stages.md **Abort**). async-notify veto after Build started → Decision N (discard / keep / stop).
10. **Design-backloop after Build** when Fix cannot stay aligned with `03-design` / `04-tasks` → Decision N (amend design → re-review → Gate B / Fix-only / stop). See stages.md **Design-backloop**.
11. **No UI concept step** — see [LEGACY.md](LEGACY.md).
12. **Plain words.** Decision N when 2+ choices (handoffs.md). User-first picks on Gate B / Grill auto / async-notify. **HITL Grill** is independent of Gate B.
13. **Skills SoT:** edit under `AI/skills/`; run `AI/skills/sync-to-cursor.sh` so `~/.cursor/skills` matches.

## Start (Step 0)

1. **Classify** simple vs full unless resume or user named Mode → stages.md **Mode selection**. Ambiguous → Decision N.
2. Pick slug `YYYYMMDD-feature-x` (UTC date + kebab feature). Seed `00-run.md` from [artifacts/00-run.md](artifacts/00-run.md).
3. Resolve High / Medium / Fast from Task allowlist → `00-run.md` (stages.md **Models**). Set Mode, Review profile, HITL Gate B, **HITL Grill**, **HITL Gate C: blocking**, Orchestrator card.
4. Chat one line: Mode + Review profile + why.
5. Mode **simple** without `01-idea.md` → bootstrap thin idea; note skipped early gates. Do not invent legacy UI-concept artifacts.
6. Run pipeline in [stages.md](stages.md). After each step: ≤5 lines summary + path; update Orchestrator card (incl. Last Verify after Build/Fix).

## Parent load rule

| Need | Read |
|------|------|
| Next step | `00-run.md` Orchestrator card + **one** stages.md section |
| Task prompt | handoffs.md row for stage id + that stage’s stages.md rules |
| New artifact body | one file under [artifacts/](artifacts/INDEX.md) only |
| Grill | grill.md (once when entering Grill) |
| Verify / Fix rules | verify-and-fix.md (once when entering Build / Fix) |
| Phase entry | that subflow `SKILL.md` once |

Do **not** re-read this whole SKILL every step.
