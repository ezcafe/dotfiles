---
name: my-review-subflow
description: >-
  Verifies a code draft with adversarial test review then quality, then
  conditional API/DB/security/performance/memory lenses (only when SPM plan
  signals match). Merge findings when 2+ lenses; one Fix round; re-loop until
  clean. Honors Review profile lite/skip-review from my-plan-flow. Use when the
  user says run my-review-subflow, review the draft, or after my-code-subflow.
---

# my-review-subflow

Review + Fix subflow of [`my-plan-flow`](../my-plan-flow/SKILL.md). Generation ≠ verification.

**Details:** [stages.md](stages.md) · templates [`../my-plan-flow/templates.md`](../my-plan-flow/templates.md)

## When to run

`run my-review-subflow`, review the draft, or when `my-plan-flow` reaches review.

## Principles

- Never trust the first output. Challenge the draft.
- Writers (Fix) never self-approve; verifiers re-check after Fix.
- **Review profile:** If `00-run.md` says **skip-review**, do not run this skill (parent goes Gate C after smoke).
- **Sequential first:** Adversarial tests, then Quality.
- **UI lock (Has UI):** Quality compares draft UI to Design UI specs + Gate A #1/#2 / existing chrome — fail **Major** on clear drift.
- **Conditional lenses:** Parent sets **SPM plan** in `00-run.md`. Launch **only** listed lenses (**API** / **DB** / Security / Perf / Memory). If **none**, skip lenses + Merge after Quality clean.
- **API lens required when Has API:** If `00-run.md` **Has API = yes**, SPM plan **must** include **api**. Launch an isolated Task — do not fold contract checks into Quality or the parent chat.
- **DB lens required when Has DB:** If `00-run.md` **Has DB = yes**, SPM plan **must** include **db**. Launch an isolated Task — do not fold schema/migration/query checks into Quality or the parent chat.
- **Merge findings:** Required only when **2+** lenses ran. **1 lens:** parent copies that lens Result into `05-review-log.md` Merged SPM (no Merge Task). Conflict priority when merging: **Security Critical > API/DB contract / correctness / data-integrity > Quality > Perf/Memory Enhancements**.
- **One Fix** from the merged Fix ask (not parallel Fix agents).
- Re-run only the lenses in SPM plan → merge (if 2+) → Fix until clean (max 3 rounds, then pause).
- If Fix changed tests/behavior, re-run **Adversarial** once (and Quality if structure changed).
- Use **stage-scoped handoffs** (`adversarial`, `quality`, `spm-api`, `spm-db`, `spm-*`, `merge-findings`, `fix-review`).
- Mechanical stages → Fast when Medium unavailable (see my-plan-flow).
- Plain words in the review log.

## Models

| Tier | Stages | Preferred slug |
|------|--------|----------------|
| **Medium** | Adversarial; Quality; API; DB; Security; Performance; Memory; **Merge findings** | `gpt-5.6-sol-medium` |
| **Fast** | Fix | `composer-2.5-fast` |

### Model availability

Follow [`my-plan-flow`](../my-plan-flow/SKILL.md) → **Model availability (auto fallback)**.  
Medium → Fast → `inherit`. Fast → `inherit`. Record the resolved slug (and any fallback) in `00-run.md`. Do not stop to ask unless no Task can run.

## Prerequisites

- Draft code exists (after `my-code-subflow` or equivalent).
- Prefer Gate B checked in `00-run.md` (required when parent is `my-plan-flow`; legacy: Gate 2).
- Prefer **smoke-pass** in `06-test-log.md` when parent is `my-plan-flow` (do not review a draft that fails build/unit).
- Prefer `03-design.md` / `04-tasks.md` present for intent checks.
- Create `05-review-log.md` from templates if missing.

If there is no draft to review → **stop** and tell the user to run `my-code-subflow` first.
If parent is `my-plan-flow` and Gate B is unchecked → **stop** and wait for Gate B.
If parent is `my-plan-flow` and smoke is not **smoke-pass** → **stop** and run `my-test-subflow` smoke first.

## Pipeline

```
(skip entirely if Review profile = skip-review)

Adversarial (Medium|Fast) ⇄ Fix (Fast) until clean
→ Quality (Medium|Fast) ⇄ Fix (Fast) until clean
→ if SPM plan = none → done (go to test per Review profile)
→ Loop (max 3, then pause):
    Launch only lenses in SPM plan (parallel when 2+)
    → if 2+ lenses: Merge findings → ranked Fix ask
    → if 1 lens: parent copies into Merged SPM
    → if clean → exit loop
    → else Fix (Fast) from Fix ask
    → if Fix changed tests/behavior → Adversarial once (Quality if structure changed)
→ lenses clean (or none) → done
```

## Severity exit rule

Findings: **Critical** / **Major** / **Enhancement** (nits/FYI do not block).

- Adversarial / Quality: clean only at zero Critical, Major, Enhancement for that lens; Fix → re-run **same** lens until clean.
- Lens loop: clean only when Merge findings Result is **clean** (no open Critical/Major/Enhancement after merge). Dropped losers stay documented as deferred/Nit.

## TDD on Fix

For behavior findings: Red → Green → Refactor → Verify. Docs/comments only: note “TDD skipped” in `05-review-log.md`.

## Orchestrator rules

- If Review profile **skip-review** → stop (nothing to do).
- Launch Adversarial, then Quality, each with Fix loops — **not** in parallel with SPM/API lenses.
- Before lenses: read **SPM plan** from `00-run.md`. If **Has API = yes** and plan omits **api**, add **api**. If **Has DB = yes** and plan omits **db**, add **db**. Launch **only** matching lenses (0–5). Do **not** always launch all five.
- Wait for launched lenses. Merge findings only if **2+** lenses. Single lens: parent copies into Merged SPM. Do **not** Fix until that is done.
- Launch **one** Fix Task from the Fix ask only.
- Stage-scoped handoffs; Task **`description`** from my-plan-flow map.
- Bugbot only if the user asks.
- Parent: Result header summary + path; update Orchestrator card.
- When clean: next is `my-test-subflow` **full** (profile full) or **lite** (profile lite), then Gate C (unless parent is `my-plan-flow`).

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
| Fix | same build skills as my-code-subflow; merged Fix ask only |

## Artifacts

- `05-review-log.md` — adversarial, quality, merged SPM, fix notes
- `05-lens-*.md` — only for lenses in SPM plan (overwrite each round), including `05-lens-api.md` when api and `05-lens-db.md` when db

## Start checklist

1. Confirm draft exists; init `05-review-log.md` if needed.
2. Resolve Medium + Fast models.
3. Adversarial → Quality → Conditional lenses (per SPM plan; **api** when Has API; **db** when Has DB) → Fix until clean.
