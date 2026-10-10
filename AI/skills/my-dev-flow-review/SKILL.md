---
name: my-dev-flow-review
description: >-
  Verifies a code draft: full profile uses Adversarial then Quality then
  conditional lenses; lite profile must use one code-review-phase (Lite
  combined). Lens plan defaults to none. Merge findings when 2+ lenses; Fix
  until clean. Honors skip-review. Use when the user says run my-dev-flow-review,
  review the draft, or after my-dev-flow-code.
---

# my-dev-flow-review

Review + Fix subflow of [`my-dev-flow`](../my-dev-flow/SKILL.md). Generation ≠ verification.

**Details:** [stages.md](stages.md) · handoffs [`../my-dev-flow/handoffs.md`](../my-dev-flow/handoffs.md) · severity [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md)

## When to run

`run my-dev-flow-review`, review the draft, or when `my-dev-flow` reaches review.

## Principles

- Never trust the first output. Challenge the draft.
- Writers (Fix) never self-approve; verifiers re-check after Fix.
- **Review profile:** If `00-run.md` says **skip-review**, do not run this skill (parent goes Gate C after Build verify-pass).
- **Sequential first:** Adversarial tests, then Quality.
- **UI lock (Has UI):** Quality compares draft UI to Design UI specs + Gate A #1/#2 / existing chrome — fail **Major** on clear drift.
- **Conditional lenses:** Parent sets **Lens plan** in `00-run.md` (legacy name **SPM plan**). Launch **only** listed lenses (**API** / **DB** / Security / Perf / Memory). If **none**, skip lenses + Merge after Quality clean.
- **API lens required when Has API:** If `00-run.md` **Has API = yes**, Lens plan **must** include **api**. Launch an isolated Task — do not fold contract checks into Quality or the parent chat.
- **DB lens required when Has DB:** If `00-run.md` **Has DB = yes**, Lens plan **must** include **db**. Launch an isolated Task — do not fold schema/migration/query checks into Quality or the parent chat.
- **Merge findings:** Required only when **2+** lenses ran. **1 lens:** parent copies that lens Result into `05-review-log.md` **Merged lenses** (no Merge Task). Conflict priority when merging: **Security Critical > API/DB contract / correctness / data-integrity > Quality > Perf/Memory Enhancements**.
- **Lite required:** When Review profile **lite**, parent **must** run one Task (`Lite combined review` / stage id `code-review-phase`) for Adversarial + Quality when Lens plan is `none` or **one** lens. Do **not** launch separate Adversarial then Quality. If Lens plan has **2+** lenses: Lite combined first, then parallel lenses + Merge. See [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md).
- **One Fix** from the merged Fix ask (not parallel Fix agents).
- Re-run only the lenses in Lens plan → merge (if 2+) → Fix until clean (max 3 rounds, then pause).
- If Fix changed tests/behavior, re-run **Adversarial** (or Lite combined) once (and Quality if structure changed).
- Use **stage-scoped handoffs** (`code-review-phase`, `adversarial`, `quality`, `lens-*`, `merge-findings`, `fix-review`). Legacy `spm-*` aliases: LEGACY.md.
- Mechanical: Fast-on-simple; Mode full → Fast when Medium unavailable (see my-dev-flow).
- Plain words in the review log.

## Models

Follow [`my-dev-flow/stages.md`](../my-dev-flow/stages.md) → **Models** (review lenses = mechanical → Fast when Medium missing; Fix = Fast).

## Prerequisites

- Draft code exists (after `my-dev-flow-code` or equivalent).
- Prefer Gate B checked in `00-run.md` (required when parent is `my-dev-flow`; legacy: Gate 2).
- Prefer **smoke-pass** in `06-test-log.md` when parent is `my-dev-flow` (from Build Verify Option B or Smoke re-run).
- Prefer `03-design.md` / `04-tasks.md` present for intent checks.
- Create `05-review-log.md` from templates if missing.

If there is no draft to review → **stop** and tell the user to run `my-dev-flow-code` first.
If parent is `my-dev-flow` and Gate B is unchecked → **stop** and wait for Gate B.
If parent is `my-dev-flow` and smoke is not **smoke-pass** → **stop** (Build should have written Smoke, or run Smoke re-run).

## Pipeline

```
(skip entirely if Review profile = skip-review)

Review profile lite:
  code-review-phase / Lite combined (Fast) ⇄ Fix until clean
  → if Lens plan = none → done
  → if 1 lens → that lens (or included in combined when practical) → parent copies Merged
  → if 2+ lenses → parallel lenses → Merge → Fix loop (max 3)

Review profile full:
  Adversarial ⇄ Fix until clean
  → Quality ⇄ Fix until clean
  → if Lens plan = none → done
  → Loop (max 3): parallel lenses (must when 2+) → Merge if 2+ → Fix → optional Adv/Quality recheck
→ done → test per Review profile
```

## Severity exit rule

Findings: see [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md).

- Adversarial / Quality: clean at zero Critical/Major; Fix → re-run **same** lens until clean.
- Lens loop: clean when Merge findings Result is **clean** (no open Critical/Major after merge). Enhancements → Deferred; dropped losers stay Nit/deferred.

## TDD on Fix

For behavior findings: Red → Green → Refactor → Verify. Docs/comments only: note “TDD skipped” in `05-review-log.md`.

**Verify gate:** Shared rules in [`../my-dev-flow/verify-and-fix.md`](../my-dev-flow/verify-and-fix.md). When code/tests changed, Fix must **verify-pass** (Verify commands; max 3 attempts; first return line `Result: verify-pass | verify-fail`) before parent re-runs verifiers.

## Orchestrator rules

- If Review profile **skip-review** → stop (nothing to do).
- If Review profile **lite** → **must** launch `code-review-phase` (`Lite combined review`). Do **not** launch separate Adversarial + Quality.
- If Review profile **full** → Adversarial, then Quality, each with Fix loops — **not** in parallel with lens Tasks.
- After Fix: advance only on **verify-pass** (or docs-only skip); on **verify-fail** (max 3) → Decision N or re-launch Fix.
- Before lenses: read **Lens plan** from `00-run.md` (default **none**). If **Has API = yes** and plan omits **api**, add **api**. If **Has DB = yes** and plan omits **db**, add **db**. Launch **only** matching lenses (0–5).
- Wait for launched lenses. Merge findings only if **2+** lenses (**must** parallel). Single lens: parent copies into Merged lenses.
- Launch **one** Fix Task from the Fix ask only.
- Stage-scoped handoffs; Task **`description`** from my-dev-flow map.
- Bugbot only if the user asks.
- Parent: Result header summary + path; update Orchestrator card.
- When clean: next is `my-dev-flow-test` **test-full** (profile full) or **test-lite** (profile lite), then Gate C.

## Skills used

| Stage | Skills |
|-------|--------|
| Quality | `code-review-and-quality` |
| API | `api-and-interface-design` |
| DB | `database-and-data-model` |
| Security | `security-and-hardening` (OWASP Top 10 required) + `review-security` |
| Performance | `performance-optimization` (+ `vercel-react-best-practices` if React/Next) |
| Memory | checklist in [stages.md](stages.md) |
| Merge findings | conflict rules in [stages.md](stages.md); reads launched lens files |
| Fix | same build skills as my-dev-flow-code; merged Fix ask only |

## Artifacts

- `05-review-log.md` — adversarial, quality, merged lenses, deferred, fix notes
- `05-lens-*.md` — only for lenses in Lens plan (overwrite each round), including `05-lens-api.md` when api and `05-lens-db.md` when db

## Start checklist

1. Confirm draft exists; init `05-review-log.md` if needed; read Review profile + Lens plan (default none).
2. Resolve models (Fast-on-simple; Medium|Fast on full).
3. lite → code-review-phase; full → Adversarial → Quality → lenses → Fix until clean.
