---
name: my-dev-flow-design-review
description: >-
  Reviews design artifacts for gaps against real-world best practices, then hands
  findings to my-dev-flow-design for updates. Mode full: isolated API∥DB reviews
  (must parallel when both) then general design-review. Mode simple: one
  design-verify-phase Task. Checks UI alignment with Gate A / Design UI specs
  (does not re-litigate 80/20). Use when the user says run
  my-dev-flow-design-review, review the design, or after my-dev-flow-design before
  my-dev-flow-code.
---

# my-dev-flow-design-review

Design verification subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md).
Generation ≠ verification: this skill **reviews** design docs; it does **not**
rewrite them (updates go to [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md)).

**Details:** [stages.md](stages.md) · handoffs [`../my-dev-flow/handoffs.md`](../my-dev-flow/handoffs.md) · templates [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md) · severity [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md)

## When to run

`run my-dev-flow-design-review`, review the design, or when `my-dev-flow` finishes
the first design pass and before code.

## Principles

- Never trust the first design. Challenge gaps, vagueness, and weak practices.
- **Has API → API contract review:** When `00-run.md` **Has API = yes**, deep-check API contracts against [`api-and-interface-design`](../api-and-interface-design/SKILL.md). Mode **full:** isolated Task. Mode **simple:** fold into `design-verify-phase` (same Task writes `03a-api-contract-review.md`).
- **Has DB → DB design review:** When `00-run.md` **Has DB = yes**, deep-check schema/migrations/queries against [`database-and-data-model`](../database-and-data-model/SKILL.md). Mode **full:** isolated Task. Mode **simple:** fold into `design-verify-phase`.
- **API ∥ DB (Mode full):** When both yes, parent **must** launch both isolated Tasks in the **same** turn (parallel). Never serial API-then-DB.
- Check against **real-world best practices** for this stack — plain words.
- **Analyze deep dive:** fail Major if `02-analysis.md` skips or hand-waves What / Why / How (other ways + best practices). Mode **full:** also fail Major if **Solution branches** (Quick wins / Systemic / Creative) missing or hand-wavy.
- **Problem map:** Mode **full:** fail Major if `01-idea.md` lacks Problem map Steps 1–2 + Core problem (one sentence), or mind map has no ★ priority. Mode **simple:** Core problem line or stub OK.
- **Grill:** Mode full expects `02b-grill.md` frontier-empty (or skip with reason). Fail Major if Design re-opens Settled grill locks without new evidence, or Build-critical frontier was never closed.
- **Security:** require OWASP Top 10 coverage in `03-design.md`.
- **UI/UX:** when Has UI, require mobile-friendly + a11y basics; **fail on drift** from Gate A #1/#2 or Design UI specs; fail **Major** if Design/tasks lack clear UI locks when Has UI.
- **Do not re-litigate Gate A 80/20** — if Gate A was ok, check **alignment** with `01a` / Design only (unless design clearly abandoned #1/#2).
- **Legacy UI look artifacts:** do not require them — see [`LEGACY.md`](../my-dev-flow/LEGACY.md).
- Writers do not self-approve: after design updates, **re-run** until clean.
- Plain words in `03a-design-review-log.md` (+ `03a-api-contract-review.md` / `03a-db-design-review.md` when flagged).
- **Severity:** [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md) — clean = zero Critical/Major.

## Models

Resolve tiers once in `00-run.md`. Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models** (API/DB/design-review = mechanical → Fast when Medium missing).

## Prerequisites

- `01-idea.md`, `02-analysis.md`, `03-design.md`, `04-tasks.md` present.
- Prefer Gate A checked; Chosen design filled or Recommendation clear (user-first).
- Prefer `02-skim.md` when present (full mode always; simple if already written).
- Prefer **Has API** and **Has DB** set in `00-run.md` (yes/no). If unknown and `03-design.md` has API contracts, treat Has API as **yes**. If unknown and Database contracts / migrations are in scope, treat Has DB as **yes**.
- Create review artifacts from [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md) if missing (`03a-*`).

If design docs are missing → **stop** and tell the user to run `my-dev-flow-design` first.

## Pipeline

**Mode full:**

```
if Has API = yes AND Has DB = yes:
  API contract review ‖ DB design review  (MUST same turn / parallel)
else if Has API = yes: API contract review
else if Has DB = yes: DB design review
→ Design review (Medium|Fast) → 03a-design-review-log.md
```

**Mode simple:**

```
design-verify-phase (Fast preferred) — one Task:
  writes 03a-api / 03a-db when flagged + 03a-design-review-log.md
```

Overall **clean** only when API file is clean|skipped, DB file is clean|skipped, **and** general design review is clean.

## Severity exit rule

Findings: **Critical** / **Major** / **Enhancement** / Nit. See [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md).

**Clean** = zero Critical and Major across API contract review (when run), DB design review (when run), and general design review. Enhancements defer to Notes / Deferred.

If not clean → hand **Fix ask** to `my-dev-flow-design` Update mode → parent re-runs this workflow.

## Exit

| Result | Next (when parent is my-dev-flow) |
|--------|-----------------------------------|
| **clean** | TDD → Gate B → Build (verify-pass + Smoke section; skip Smoke Task) → review/test per **Review profile** (full / lite / skip-review); ensure Lens plan includes **api** when Has API and **db** when Has DB |
| **needs update** | `my-dev-flow-design` Update → re-run this skill |

Standalone: on clean say next is TDD → Gate B → Build (verify-pass + Smoke section) → review/test per Review profile.

## Orchestrator rules

- **Mode simple:** launch **one** `design-verify-phase` Task (`description`: `Design verify phase`). Do not launch separate API/DB/general Tasks.
- **Mode full — Has API = yes:** launch **API contract review** Task.
- **Mode full — Has DB = yes:** launch **DB design review** Task.
- **Mode full — both yes:** launch both isolated Tasks **in the same turn** (parallel **required**), then Design review.
- When **Has API = no**: skip API file (or mark skipped). When **Has DB = no**: skip DB file.
- Set Task **`description`** from my-dev-flow map. Fast-on-simple for mechanical.
- Do **not** edit `01`–`04` here — only write `03a-*` review files.
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

1. Confirm design artifacts; init `03a` if needed; confirm **Has API** and **Has DB**; read Mode.
2. Resolve models (Fast-on-simple; Medium|Fast on full).
3. Simple → design-verify-phase. Full → API∥DB (must parallel when both) → Design review → clean or Fix ask.
