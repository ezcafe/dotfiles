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

Owned here only — Happy path / Mode order: [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md). Has API/DB + tiny-tweak + parallel/serialize: [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) (do not restate routing here).

- Never trust the first design. Challenge gaps, vagueness, and weak practices.
- **Writers ≠ verifiers:** this skill writes only `03a-*`. Do **not** edit `01`–`04`. Design updates → [`my-dev-flow-design`](../my-dev-flow-design/SKILL.md) Update.
- **Overall clean** = API clean|skipped ∧ DB clean|skipped ∧ general clean (skipped per lenses.md).
- **Severity:** [`severity.md`](../my-dev-flow/severity.md) — clean = zero Critical/Major. Enhancements → Deferred.
- Fail Major on missing/thin Analyze What/Why/How; Mode full also Solution branches. Fail Major on missing Problem map (full) / vague Core problem. Fail Major if Design re-opens Settled grill locks without new evidence, or Build-critical frontier never closed.
- **Security:** OWASP Top 10 coverage required in `03-design.md`.
- **UI:** when Has UI, mobile + a11y basics; fail on drift from Gate A #1/#2 or Design UI locks; fail Major if locks missing. Mode **simple**: thin UI-alignment inside `design-verify-phase` — [`stages/design-verify-phase.md`](stages/design-verify-phase.md). **Do not re-litigate Gate A 80/20.** — [`LEGACY.md`](../my-dev-flow/LEGACY.md).
- Result tokens: [`results.md`](../my-dev-flow/results.md). Max **3** rounds → Decision N — [`invariants.md`](../my-dev-flow/invariants.md).
- Plain words in `03a-*`.

## Models

[`../my-dev-flow/models.md`](../my-dev-flow/models.md) (API/DB/design-review = mechanical → Fast when Medium missing; Fast-on-simple).

## Prerequisites

- `01-idea.md`, `02-analysis.md`, `03-design.md`, `04-tasks.md` present.
- Prefer Gate A checked; Chosen design filled or Recommendation clear (user-first).
- Prefer **Has API** / **Has DB** set (yes/no) — unknown inference: [`lenses.md`](../my-dev-flow/lenses.md).
- Create `03a-*` from [`../my-dev-flow/artifacts/INDEX.md`](../my-dev-flow/artifacts/INDEX.md) only when required (never invent empty API/DB files when skipped).

If design docs are missing → **stop** and tell the user to run `my-dev-flow-design` first.

## Pipeline / launch

Parent order + Has API/DB launch rules: [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) · [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md). Load **`stages/<stage-id>.md` only**. Paste `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` ([`skills-path.md`](../my-dev-flow/skills-path.md)).

Owned here: write only `03a-*`; **needs update** → design Update → re-review; **clean** → parent optional TDD → Gate B → Build; max 3 → Decision N.

## Skills used

| Focus | Skills |
|-------|--------|
| Spec / plan quality | `myplan`, `planning-and-task-breakdown`, `documentation-and-adrs` |
| APIs / contracts | `api-and-interface-design` (when Has API path applies — lenses.md) |
| Database / schema | `database-and-data-model` (when Has DB path applies — lenses.md) |
| Security / OWASP | `security-and-hardening` |
| UI / UX / mobile | frontend / clean-minimal / web-design-guidelines when UI |

## Start checklist

1. Confirm design artifacts; Has API/DB + Mode + tiny-tweak Notes ([lenses.md](../my-dev-flow/lenses.md)).
2. Resolve models; launch per parent Happy path (not a local routing table).
