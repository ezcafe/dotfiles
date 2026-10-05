---
name: my-dev-flow-design
description: >-
  Runs Ideation (set Has UI; Problem map diagnose-before-framing) → Gate A
  day-to-day auto-approve → light repo skim → Analyze (What/Why/How +
  Solution branches) → Grill (design tree + glossary/ADR; auto-settle by
  default) → Design. Gate B comes later (after design-review + optional TDD
  test-case review). Also updates design docs from my-dev-flow-design-review
  findings. Writes framing, skim, analysis, grill, design options (two in full;
  one in simple), system design + design-patterns teach sections, sequence
  diagrams, API/database contracts, and TDD-ready tasks under .my-docs/workflow.
  Use when the user says run my-dev-flow-design, design-only workflow, update
  design from review, or after my-dev-flow-design-review.
---

# my-dev-flow-design

Design-only subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). No production code.

**Details:** [stages.md](stages.md) · handoffs [`../my-dev-flow/handoffs.md`](../my-dev-flow/handoffs.md) · artifacts [`../my-dev-flow/artifacts.md`](../my-dev-flow/artifacts.md)

## When to run

`run my-dev-flow-design`, design-only, update design from review, or when `my-dev-flow`
reaches the design phase / design↔review loop.

## Principles

- Design is the main artifact. Spend attention here before code.
- Attack assumptions; ask “is this clear?”
- **Design options:** Mode **full** → two plausible designs + tradeoffs; Mode **simple** → one recommended design + ≤3-line rejected alternative (full Option 1/2 only if 2+ approaches still unsettled). Decision options shape when 2+ options — see [`my-dev-flow`](../my-dev-flow/SKILL.md).
- **User-first picks:** When recommending / auto-picking an option, stand in the user’s shoes — day-to-day user value first, then system convenience. Record rationale when parent HITL is auto.
- **Sequence diagram** + **API/DB contracts** + **example queries** required in `03-design.md`.
- **System design (required heading in `03-design.md`):** Teach runtime shape when architecture matters. **Triggers:** Has API or Has DB → Overview required (not N/A); Mode full + new boundary/data-flow → Overview required; simple copy/token → prefer N/A. Ownership: runtime/boundaries only (not code patterns). Anti-dupe: point to sequence/contracts/OWASP — do not restate. Budgets: Overview ≤ ~12 bullets; ≤3 Concept N. See artifacts → **System design**.
- **Design patterns used (required heading in `03-design.md`):** Teach code/module patterns when they matter. Prefer repo patterns; invent-new when a repo pattern exists is a design-review fail. Ownership: code structure only. Budgets: ≤3 patterns; ≤ ~8 lines each. See artifacts → **Design patterns used**.
- **Has UI early:** Ideation sets Has UI in `00-run.md`.
- **Primary sources in Ideation:** Investigate the question against primary sources (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it. Record those sources in `01-idea.md`.
- **UI in Design:** When Has UI, put layout/IA/chrome in `03-design.md` + acceptance in `04-tasks.md`; match existing app patterns and Gate A 80/20. Removed UI-concept step — see [`LEGACY.md`](../my-dev-flow/LEGACY.md).
- **Has API:** Set/refine in `00-run.md` during Analyze or Design when public contracts change (`yes` / `no`). When **yes**, design-review runs an isolated **API contract review** Task; code review includes the **api** lens.
- **Has DB:** Set/refine in `00-run.md` during Analyze or Design when schema, migrations, or persistence queries change (`yes` / `no`). When **yes**, design-review runs an isolated **DB design review** Task; code review includes the **db** lens.
- **Gate A after Ideation:** user-role day-to-day + 80/20 → `01a`. Auto-approve when ok.
- **Light skim after Gate A:** `02-skim.md` constraints before Analyze.
- **Grill after Analyze (before Design):** follow [`my-dev-flow/grill.md`](../my-dev-flow/grill.md) — design-tree frontier + glossary/ADR. Mode **full** always (unless already frontier-empty). Mode **simple** when frontier open or Has API/DB; else skip. Prefer **auto** user-first settle (HITL Gate B). Do not start Design on `needs-round`.
- Analyze/Design must not abandon Gate A #1/#2. Design review checks **alignment**, not re-litigation of Gate A 80/20. Design honors grill Settled decisions.
- **Diagnose before design:** Ideation fills **Problem map** (3 WHAT branches → Core problem → mind map with ★) before Outcome. Mode **full** required; Mode **simple** stub OK.
- **Analyze + spike deep dive (required):** For the feature and each major solution piece, answer in `02-analysis.md` (ask the user when unclear):
  1. **What is this?** (align with Core problem)
  2. **Why do we need this?**
  3. **How to do this?** Other ways? Best practices? Plus **Solution branches** (Quick wins / Systemic / Creative) from Core problem — Mode full required; Mode simple stub OK.
  Optional **spikes** (throwaway exploration only) during Analyze must use the same three questions and write findings into `02-analysis.md`. No production code in this skill.
- **UI / UX / mobile** + **OWASP** as in artifacts / security-and-hardening (in Design when Has UI).
- When updating from review: **only** address `03a` Fix ask; stay aligned with Gate A idea.
- Plain words in all docs.

## Models

| Tier | Stages | Preferred slug |
|------|--------|----------------|
| **Medium** | Ideation; Gate A; Ideation update; Light skim; Grill | `claude-opus-5-5-medium` |
| **High** | Analyze; Design; Update from design review | `claude-sonnet-5-5-high` |

### Model availability

Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models** (usage-limit: wait 5s → retry → **inherit** → main-thread for that stage).  
Record resolved slug in `00-run.md`. Do not stop to ask unless no Task can run.

## Gates

1. **Gate A (after Ideation)** — user-role Task → `01a-idea-ui-review.md`. Auto-check when Result **ok**. (Full mode only.)
2. **Light skim** — `02-skim.md` Result **done** (or skipped with Notes). (Full mode only.)
3. **After Design is clean** — parent: design-review → optional TDD review → **Gate B** (HITL) → Build. **No code in this skill.**

Reject / escalate after max rounds → stop (or ask human).

## Pipeline

```
Full:
  Ideation (Medium; set Has UI)
  → Gate A (Medium) → ok → auto-approve Gate A
  → Light skim (Medium) → 02-skim.md
  → Analyze (High) → Grill (Medium; auto-settle) → Design (High)
  → (parent) design-review → optional TDD review → GATE B (HITL) → Build

Simple (from my-dev-flow):
  Analyze (High) → Grill (Medium; or skip) → Design (High; **one option by default**)
  → (parent) design-review → optional TDD review → GATE B (HITL) → Build
  (requires 01-idea — existing framing or parent bootstrap for new simple runs;
   prefer Gate A / skim when already present; do not invent them)

Update mode: Update from 03a (High) → (parent) re-run design-review
```

## Prerequisites

**Full:**

- **Standalone:** a user idea. Create `<slug>` and `00-run.md` if missing.
- **From my-dev-flow:** slug and models already in `00-run.md`.

**Simple (Analyze → Design only):**

- `01-idea.md` present — from prior framing **or** parent bootstrap (thin idea + Has UI) when Mode is simple
- Prefer Gate A checked / `02-skim.md` when those already exist
- Parent Mode: simple
- Do **not** stop solely because early framing artifacts are missing on a new simple run

**Update-from-design-review mode:**

- `03a-design-review-log.md` with **Result: needs update** and Fix ask
- Existing `01`–`04` design artifacts

If neither mode’s files are ready → **stop**.

## Outputs

- `01-idea.md`, `01a-idea-ui-review.md` (full; may already exist in simple)
- `02-skim.md` (full; may already exist in simple)
- `02-analysis.md`, `02b-grill.md` (or skip note in `00-run.md`), `03-design.md`, `04-tasks.md`

Do **not** create removed UI-concept artifacts — see [`LEGACY.md`](../my-dev-flow/LEGACY.md).

## Orchestrator rules

- Detect mode: `03a` needs update → Update; else parent Mode **simple** → Analyze → Design only; else Full.
- **Full:** do **not** skip Gate A; do **not** start Analyze until Gate A checked and skim done (or skim skipped with Notes). Do **not** start Design until Grill is frontier-empty or skipped.
- **Simple:** do **not** re-run Ideation / Gate A / skim; start at Analyze. Accept parent-bootstrapped `01-idea.md` when early framing was skipped. Grill when frontier open / Has API/DB; else skip. Design: **one option by default**. Honor artifact size caps.
- One **fresh** Task per stage; prompts from [stages.md](stages.md); **stage-scoped handoffs**.
- Task **`description`** from my-dev-flow map (`Ideation problem framing`, `User day-to-day review`, `Light repo skim`, …).
- **Gate A auto-approve:** when `01a` Result **ok**, check Gate A in `00-run.md` — no human chat turn.
- **Gate A needs update:** Ideation update → re-run Gate A (max 3).
- **From my-dev-flow:** after Design, do **not** Gate B yet — design-review → optional TDD → Gate B (HITL) → Build.
- **Update mode:** do not re-run Ideation/Gate A/skim unless Fix ask requires it; do not re-litigate Gate A 80/20 unless Fix ask says so.
- Clarity check before Analyze and Grill/Design (include What / Why / How deep dive before Grill/Design).

## Skills used

| Stage | Skills |
|-------|--------|
| Ideation | `myplan` (discovery + specify); **Problem map** before Outcome |
| Gate A | none — user-role review of `01-idea.md` |
| Light skim | explore / quick repo scan |
| Analyze | explore; `dev-decision-routing` if front-end; honor skim; **What/Why/How deep dive** + **Solution branches** (+ optional spike notes); Design tree stub |
| Grill | [`my-dev-flow/grill.md`](../my-dev-flow/grill.md); `documentation-and-adrs` (glossary + sparse ADR) |
| Design / Update | `myplan` plan; `planning-and-task-breakdown`; `documentation-and-adrs`; `api-and-interface-design`; `security-and-hardening`; when Has UI: `clean-minimal-ui` + `frontend-ui-engineering` + DESIGN_GUIDE — lock Build to Design UI specs + existing chrome; honor `02b-grill` |

## Start checklist

1. Confirm mode (Full / Simple / Update) + files; resolve models → `00-run.md`. Parent should already have set Mode from complexity (or override).
2. Full: Ideation → Gate A → skim → Analyze → Grill → Design. Simple: Analyze → Grill (or skip) → Design (`01-idea` present or parent-bootstrapped).
3. Hand off to design-review → optional TDD → Gate B (HITL) → Build.
