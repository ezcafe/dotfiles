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

**Owned stages:** [stages.md](stages.md) index — load **`stages/<stage-id>.md` only** (`adversarial`, `quality`, `code-review-phase`, `lens-*`, `merge-findings`, `fix-review`)

**Shared SoT (do not duplicate Happy path here):**

| Topic | File |
|-------|------|
| Runtime order | [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) Happy path |
| Review profile | [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) Mode × Review profile (+ [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) for skip-review) |
| Severity exit | [`../my-dev-flow/severity.md`](../my-dev-flow/severity.md) |
| Lens plan / api/db / tiny-tweak | [`../my-dev-flow/lenses.md`](../my-dev-flow/lenses.md) |
| Verify gate on Fix | [`../my-dev-flow/verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) |
| Max rounds / Decision N | [`../my-dev-flow/invariants.md`](../my-dev-flow/invariants.md) |
| Stage handoffs | **Required** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` ([`skills-path.md`](../my-dev-flow/skills-path.md)) · [`handoffs.md`](../my-dev-flow/handoffs.md) = edit SoT / debug only |
| Models | [`../my-dev-flow/models.md`](../my-dev-flow/models.md) |

## When to run

`run my-dev-flow-review`, review the draft, or when `my-dev-flow` reaches review after Build verify-pass + Smoke.

## Principles (owned here)

- Never trust the first draft. Writers (Fix) never self-approve; verifiers re-check after Fix.
- **skip-review → do nothing** — legality: [`lenses.md`](../my-dev-flow/lenses.md) (parent Gate C).
- **Review profile full:** Adv → Quality → lenses → then `test-full`. **Review profile lite** (any Mode, including Mode full): must one `code-review-phase` (never separate Adv+Quality) → then `test-lite`.
- **Lenses / tiny-tweak / api·db:** [`lenses.md`](../my-dev-flow/lenses.md). Merge findings only if **2+** lenses.
- **Fix:** verify-pass before re-review; max 3 → Decision N ([`verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) · [`invariants.md`](../my-dev-flow/invariants.md)).
- **UI lock (Has UI):** Quality fails **Major** on Design UI / Gate A #1/#2 / chrome drift.
- Result tokens: [`results.md`](../my-dev-flow/results.md). Paste `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` output per Task (resolve per [`skills-path.md`](../my-dev-flow/skills-path.md)); plain words.

## Models

[`models.md`](../my-dev-flow/models.md) — review lenses = mechanical (Fast when Medium missing); Fix = Fast.

## Prerequisites

- Draft exists (after `my-dev-flow-code` or equivalent).
- Prefer Gate B checked; prefer Smoke **smoke-pass** in `06-test-log.md` when parent is `my-dev-flow`.
- Prefer `03`/`04` for intent checks; create `05-review-log.md` from templates if missing.

If no draft → **stop** (run code first). If parent Gate B unchecked or smoke not smoke-pass → **stop**.

## Pipeline

```
skip-review (legal per lenses.md) → stop (parent Gate C)

Review profile lite (any Mode):  code-review-phase ⇄ Fix → lenses per plan → Merge if 2+ → test-lite
Review profile full:             Adv ⇄ Fix → Quality ⇄ Fix → lenses → Merge if 2+ → Fix loop → test-full
```

Parent runtime order: [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) Happy path (Mode × Review profile table).

## Severity exit

[`severity.md`](../my-dev-flow/severity.md) — Adv/Quality clean at zero Critical/Major; lens loop clean when Merge Result **clean** (or single-lens parent copy). Enhancements → Deferred.

## Orchestrator rules

- **skip-review** → stop immediately (nothing to do here). Parent Gate C only when legal ([lenses.md](../my-dev-flow/lenses.md)).
- **Review profile lite** (even if Mode full) → must launch `code-review-phase`; never separate Adv+Quality.
- **Review profile full** → Adv then Quality, each with Fix loops; then Lens plan only.
- Before lenses: read Lens plan (default **none**); auto-add api/db per [`lenses.md`](../my-dev-flow/lenses.md). Isolated Tasks for api/db when listed (not tiny-tweak). Parallel when 2+.
- Merge Task only if **2+** lenses; 1 lens → parent copies into Merged lenses.
- After Fix: advance only on **verify-pass** (or docs-only skip); verify-fail max 3 → Decision N.
- If Fix changed tests/behavior → re-run Adv (or Lite) once (+ Quality if structure changed).
- When clean → `my-dev-flow-test` **test-full** (Review profile full) or **test-lite** (Review profile lite), then Gate C. Do not pick test mode from Mode alone.

## Skills used

| Stage | Skills |
|-------|--------|
| Quality / code-review-phase | `code-review-and-quality` |
| API | `api-and-interface-design` |
| DB | `database-and-data-model` |
| Security | `security-and-hardening` (OWASP Top 10) + `review-security` |
| Performance | `performance-optimization` (+ `vercel-react-best-practices` if React/Next) |
| Memory | [stages/lens-memory.md](stages/lens-memory.md) |
| Merge / Fix | [stages/merge-findings.md](stages/merge-findings.md) · [stages/fix-review.md](stages/fix-review.md); Fix uses same build skills as my-dev-flow-code |

## Artifacts

- `05-review-log.md` — adversarial, quality, merged lenses, deferred, fix notes
- `05-lens-*.md` — only for lenses in Lens plan (overwrite each round)

## Start checklist

1. Confirm draft + Smoke; init `05-review-log.md`; read Review profile + Lens plan.
2. Resolve models (Fast-on-simple; Medium|Fast on full).
3. Before `fix-review`: open code [clarity-check.md](../my-dev-flow-code/stages/clarity-check.md); log `clarity-check ok — fix-review`.
4. Review profile lite → code-review-phase; Review profile full → Adv → Quality → lenses → Fix until clean ([stages.md](stages.md) · parent Happy path).
