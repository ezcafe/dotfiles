---
name: my-design-review-subflow
description: >-
  Reviews design artifacts for gaps and issues against real-world best practices,
  then hands findings to my-design-subflow for updates. When Has API, runs an
  isolated API contract review Task first. When Has DB, runs an isolated DB
  design review Task. Checks UI alignment with Gate A / Design UI specs (does not
  re-litigate 80/20). Use when the user says run my-design-review-subflow, review
  the design, or after my-design-subflow before my-code-subflow.
---

# my-design-review-subflow

Design verification subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md).
Generation ≠ verification: this skill **reviews** design docs; it does **not**
rewrite them (updates go to [`my-design-subflow`](../my-design-subflow/SKILL.md)).

**Details:** [stages.md](stages.md) · templates [`../my-dev-flow/templates.md`](../my-dev-flow/templates.md)

## When to run

`run my-design-review-subflow`, review the design, or when `my-dev-flow` finishes
the first design pass and before code.

## Principles

- Never trust the first design. Challenge gaps, vagueness, and weak practices.
- **Has API → isolated API contract review:** When `00-run.md` **Has API = yes**, launch a **separate** Task (fresh context) that reviews API contracts against [`api-and-interface-design`](../api-and-interface-design/SKILL.md). Do not rely on the general design-review agent alone for deep API contract checks.
- **Has DB → isolated DB design review:** When `00-run.md` **Has DB = yes**, launch a **separate** Task (fresh context) that reviews schema/migrations/queries against [`database-and-data-model`](../database-and-data-model/SKILL.md). Do not rely on the general design-review agent alone for deep DB checks.
- Check against **real-world best practices** for this stack — plain words.
- **Analyze deep dive:** fail Major if `02-analysis.md` skips or hand-waves What / Why / How (other ways + best practices).
- **Grill:** Mode full expects `02b-grill.md` frontier-empty (or skip with reason). Fail Major if Design re-opens Settled grill locks without new evidence, or Build-critical frontier was never closed.
- **Security:** require OWASP Top 10 coverage in `03-design.md`.
- **UI/UX:** when Has UI, require mobile-friendly + a11y basics; **fail on drift** from Gate A #1/#2 or Design UI specs; fail **Major** if Design/tasks lack clear UI locks when Has UI.
- **Do not re-litigate Gate A 80/20** — if Gate A was ok, check **alignment** with `01a` / Design only (unless design clearly abandoned #1/#2).
- **No Gate A2 / ui-refs:** do not require `01b` or HTML look refs; legacy files are ignored.
- Writers do not self-approve: after design updates, **re-run** until clean.
- Plain words in `03a-design-review-log.md`.

## Models

| Tier | Stages | Preferred slug |
|------|--------|----------------|
| **Medium** | API contract review; DB design review; Design review | `gpt-5.6-sol-medium` |

### Model availability

Follow [`my-dev-flow`](../my-dev-flow/SKILL.md) → **Model availability (auto fallback)**.

## Prerequisites

- `01-idea.md`, `02-analysis.md`, `03-design.md`, `04-tasks.md` present.
- Prefer Gate A checked; Chosen design filled or Recommendation clear (user-first).
- Prefer `02-skim.md` when present (full mode always; simple if already written).
- Prefer **Has API** and **Has DB** set in `00-run.md` (yes/no). If unknown and `03-design.md` has API contracts, treat Has API as **yes**. If unknown and Database contracts / migrations are in scope, treat Has DB as **yes**.
- Create `03a-design-review-log.md` from templates if missing.

If design docs are missing → **stop** and tell the user to run `my-design-subflow` first.

## Pipeline

```
if Has API = yes:
  API contract review (Medium|Fast) → write 03a “API contract review” section
  if needs update → Fix ask → design Update → re-run from API contract review
if Has DB = yes:
  DB design review (Medium|Fast) → write 03a “DB design review” section
  if needs update → Fix ask → design Update → re-run from DB design review
→ Design review (Medium|Fast) → Result: clean | needs update
```

API and DB isolated Tasks may run **in parallel** when both flags are yes. Overall **clean** only when API section is clean|skipped, DB section is clean|skipped, **and** general design review is clean.

## Severity exit rule

Findings: **Critical** / **Major** / **Enhancement** (nits/FYI do not block).

**Clean** = zero Critical, Major, and Enhancement across API contract review (when run), DB design review (when run), and design review.

If not clean → hand **Fix ask** to `my-design-subflow` Update mode → parent re-runs this workflow.

## Exit

| Result | Next (when parent is my-dev-flow) |
|--------|-----------------------------------|
| **clean** | TDD → Gate B → Build → Smoke → review/test per **Review profile** (full / lite / skip-review); ensure SPM plan includes **api** when Has API and **db** when Has DB |
| **needs update** | `my-design-subflow` Update → re-run this skill |

Standalone: on clean say next is TDD → Gate B → Build → Smoke → review/test per Review profile.

## Orchestrator rules

- When **Has API = yes**: launch **API contract review** Task (`description`: `API contract review`).
- When **Has DB = yes**: launch **DB design review** Task (`description`: `DB design review`).
- When both yes: launch both isolated Tasks (parallel OK), then Design review.
- When **Has API = no**: skip API contract Task; mark 03a API section **skipped**.
- When **Has DB = no**: skip DB design Task; mark 03a DB section **skipped**.
- Set Task **`description`** from my-dev-flow map.
- Do **not** edit `01`–`04` here — only write `03a`.
- Do not write production code.
- Progress = subagent card; parent shows short summary + path for `03a`.
- Cap: max **3** design↔review rounds, then pause.

## Skills used

| Focus | Skills |
|-------|--------|
| Spec / plan quality | `myplan`, `planning-and-task-breakdown`, `documentation-and-adrs` |
| APIs / contracts | `api-and-interface-design` — **isolated Task** when Has API |
| Database / schema | `database-and-data-model` — **isolated Task** when Has DB |
| Security / OWASP | `security-and-hardening` |
| UI / UX / mobile | frontend / clean-minimal / web-design-guidelines when UI |

## Start checklist

1. Confirm design artifacts; init `03a` if needed; confirm **Has API** and **Has DB**.
2. Resolve Medium model.
3. If Has API → API contract review; if Has DB → DB design review; then Design review → clean or hand off Fix ask.
