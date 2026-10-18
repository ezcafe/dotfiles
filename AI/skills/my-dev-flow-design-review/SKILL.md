---
name: my-dev-flow-design-review
description: >-
  Reviews design artifacts for gaps against real-world best practices, then hands
  findings to my-dev-flow-design for updates. Mode full: isolated API∥DB reviews
  (both 03a-* missing → same-turn parallel; one exists → missing only / resume
  serialize) then general design-review. Mode simple: one design-verify-phase
  Task. Checks UI alignment with Gate A / Design UI specs (does not re-litigate
  80/20). Use when the user says run my-dev-flow-design-review, review the
  design, or after my-dev-flow-design before my-dev-flow-code.
---

# my-dev-flow-design-review

Design verification subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Generation ≠ verification: this skill **reviews** design docs; it does **not** rewrite them (updates go to [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md)).

**Details:** [stages.md](stages.md) index · load **`stages/<stage-id>.md` only** · parent order [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) · handoff **required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` ([`skills-path.md`](../my-dev-flow/skills-path.md) · [`handoffs.md`](../my-dev-flow/handoffs.md) = edit SoT / debug only) · lenses [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) · severity [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md) · models [`../my-dev-flow/models.md`](../my-dev-flow/models.md) · invariants [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) · LEGACY [`../my-dev-flow/LEGACY.md`](../my-dev-flow/LEGACY.md) · templates [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md)

## When to run

`run my-dev-flow-design-review`, review the design, or when `my-dev-flow` finishes
the first design pass and before code.

## Principles

Owned here only — parent Happy path / Mode order live in [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md). Has API/DB routing + tiny-tweak: [`lenses.md`](../my-dev-flow/lenses.md).

- Never trust the first design. Challenge gaps, vagueness, and weak practices.
- **Writers ≠ verifiers:** this skill writes only `03a-*`. Do **not** edit `01`–`04`. Design updates → [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md) Update.
- **Has API / Has DB:**
  - Mode **full** → isolated API / DB Tasks **unless** Notes `tiny-contract-tweak`; when both yes and not tiny-tweak → launch API∥DB in the **same** turn when **both** `03a-*` are missing; if one `03a-*` already exists, launch only the missing stage (resume serialize per [`lenses.md`](../my-dev-flow/lenses.md)).
  - Mode **simple** → fold into **design-verify-phase** (writes `03a-api` / `03a-db` only when flagged and not tiny-tweak).
  - Has = **no** or tiny-tweak → Notes skip only; **never** invent empty `03a-api` / `03a-db`; fold light checks into general log / design-verify-phase.
- **Overall clean** = API clean|skipped ∧ DB clean|skipped ∧ general clean. Skipped = Has no, or Notes `tiny-contract-tweak` (no isolated file required).
- **Done when / reads / re-run:** require isolated `03a-api` / `03a-db` **only when present and not tiny-tweak**.
- **Severity:** [`severity.md`](../my-dev-flow/severity.md) — clean = zero Critical/Major. Enhancements → Deferred.
- Fail Major on missing/thin Analyze What/Why/How; Mode full also Solution branches. Fail Major on missing Problem map (full) / vague Core problem. Fail Major if Design re-opens Settled grill locks without new evidence, or Build-critical frontier never closed.
- **Security:** OWASP Top 10 coverage required in `03-design.md`.
- **UI:** when Has UI, mobile + a11y basics; fail on drift from Gate A #1/#2 or Design UI locks; fail Major if locks missing. Mode **simple**: thin UI-alignment inside `design-verify-phase` (not full Gate A) — [`stages/design-verify-phase.md`](stages/design-verify-phase.md). **Do not re-litigate Gate A 80/20.** — [`LEGACY.md`](../my-dev-flow/LEGACY.md).
- Result tokens: [`results.md`](../my-dev-flow/results.md). Max **3** rounds → Decision N — [`invariants.md`](../my-dev-flow/invariants.md).
- Plain words in `03a-*`.

## Models

Resolve tiers once in `00-run.md`. Follow [`../my-dev-flow/models.md`](../my-dev-flow/models.md) (API/DB/design-review = mechanical → Fast when Medium missing; Fast-on-simple). Tiny fold: [`lenses.md`](../my-dev-flow/lenses.md).

## Prerequisites

- `01-idea.md`, `02-analysis.md`, `03-design.md`, `04-tasks.md` present.
- Prefer Gate A checked; Chosen design filled or Recommendation clear (user-first).
- Prefer `02-skim.md` when present (full always; simple if already written).
- Prefer **Has API** and **Has DB** set in `00-run.md` (yes/no). If unknown and `03-design.md` has API contracts → treat Has API **yes**. If unknown and Database contracts / migrations in scope → treat Has DB **yes**.
- Create review artifacts from [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md) if missing (`03a-*` as needed — never invent empty API/DB files when skipped).

If design docs are missing → **stop** and tell the user to run `my-dev-flow-design` first.

## Pipeline

Short — parent order: [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) Happy path. Tiny-tweak / Has flags: [`lenses.md`](../my-dev-flow/lenses.md).

```
Mode full:
  if Has API ∧ Has DB (not tiny-contract-tweak):
    both 03a-* missing → API ‖ DB (same turn)
    one 03a-* exists → missing stage only (resume serialize)
  else if Has API (not tiny): API only
  else if Has DB (not tiny): DB only
  # tiny-contract-tweak or Has=no: Notes-skip isolated files
  → Design review → 03a-design-review-log.md

Mode simple:
  design-verify-phase (one Task)
    → 03a-api / 03a-db when flagged and not tiny-tweak
    → + 03a-design-review-log.md
```

Overall **clean** only when API clean|skipped ∧ DB clean|skipped ∧ general clean.

## Orchestrator rules

- **Mode simple:** launch **one** `design-verify-phase` (`description`: `Design verify phase`). Do not launch separate API/DB/general Tasks.
- **Mode full — Has API = yes:** launch **api-contract-review** unless tiny-tweak (fold into general).
- **Mode full — Has DB = yes:** launch **db-design-review** unless tiny-tweak.
- **Mode full — both yes (not tiny-tweak):** when both `03a-*` missing → launch both **in the same turn**; when one exists → launch only the missing stage (resume serialize), then Design review.
- When Has = no or Notes `tiny-contract-tweak`: Notes skip only for isolated `03a-api` / `03a-db` — **never** invent empty files.
- Set Task **`description`** from my-dev-flow map. Fresh Task per stage id; paste `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` output (resolve per [`skills-path.md`](../my-dev-flow/skills-path.md); do not load whole handoffs.md for launch).
- Do **not** edit `01`–`04` here — only write `03a-*`. No production code.
- **needs update** → `my-dev-flow-design` Update → re-run: require isolated API/DB again **only when present and not tiny-tweak**; else re-run general / design-verify-phase only.
- **clean** → parent: optional TDD → Gate B → Build (verify-pass + Smoke). May draft Lens plan **api**/**db** when Has API/DB and not tiny-tweak; finalize before code review — [`lenses.md`](../my-dev-flow/lenses.md).
- Cap: max **3** rounds, then Decision N ([`invariants.md`](../my-dev-flow/invariants.md)).
- Progress = subagent card; parent shows short summary + path for `03a`.

## Skills used

| Focus | Skills |
|-------|--------|
| Spec / plan quality | `myplan`, `planning-and-task-breakdown`, `documentation-and-adrs` |
| APIs / contracts | `api-and-interface-design` — isolated when Has API (full, not tiny-tweak); else design-verify-phase / fold |
| Database / schema | `database-and-data-model` — isolated when Has DB (full, not tiny-tweak); else design-verify-phase / fold |
| Security / OWASP | `security-and-hardening` |
| UI / UX / mobile | frontend / clean-minimal / web-design-guidelines when UI |

## Start checklist

1. Confirm design artifacts; init `03a` if needed; confirm **Has API** and **Has DB**; read Mode + tiny-tweak Notes.
2. Resolve models (Fast-on-simple; Medium|Fast on full).
3. Simple → design-verify-phase. Full → API∥DB (both missing → same-turn parallel; one exists → missing only) → Design review → clean or Fix ask.
