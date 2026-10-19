---
name: my-dev-flow-review
description: >-
  DEPRECATED for new runs — prefer my-dev-flow-v2-review. Kept discoverable for
  in-flight v1 workflows. Verifies a code draft: full profile Adv→Quality→lenses;
  lite uses code-review-phase. Merge findings when 2+ lenses; Fix until clean.
  Use when resuming an in-flight my-dev-flow-review run, or when the user
  explicitly says run my-dev-flow-review.
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
- **Post-Build path / Review profile:** [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md) Mode × Review profile table (do not restate). Lenses / tiny-tweak: [`lenses.md`](../my-dev-flow/lenses.md). Merge findings only if **2+** lenses.
- **Fix:** verify-pass before re-review; max 3 → Decision N ([`verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) · [`invariants.md`](../my-dev-flow/invariants.md)).
- **UI lock (Has UI):** Quality fails **Major** on Design UI / Gate A #1/#2 / chrome drift.
- Result tokens: [`results.md`](../my-dev-flow/results.md). Paste `handoff-for.py <stage-id>` per Task ([`skills-path.md`](../my-dev-flow/skills-path.md)); plain words.

## Models

[`models.md`](../my-dev-flow/models.md) — review lenses = mechanical (Fast when Medium missing); Fix = Fast.

## Prerequisites

- Draft exists (after `my-dev-flow-code` or equivalent).
- Prefer Gate B checked; prefer Smoke **smoke-pass** in `06-test-log.md` when parent is `my-dev-flow`.
- Mode **full** + Review profile **full:** require independent Smoke re-run (Notes `smoke-pass (re-run)` + Smoke-stage evidence) before Adv — do **not** start on Build-writes-Smoke alone ([`verify-and-fix.md`](../my-dev-flow/verify-and-fix.md) E1 · [`stages.md`](../my-dev-flow/stages.md)).
- Prefer `03`/`04` for intent checks; create `05-review-log.md` from templates if missing.

If no draft → **stop** (run code first). If parent Gate B unchecked or smoke not smoke-pass → **stop**. If Mode full + profile full without independent re-run evidence → **stop** (parent launches Smoke first).

## Pipeline / launch

Parent Happy path + Mode × Review profile: [`../my-dev-flow/stages.md`](../my-dev-flow/stages.md). Load **`stages/<stage-id>.md` only**. Lens plan defaults / api·db: [`lenses.md`](../my-dev-flow/lenses.md).

Owned here: Fix verify-pass before re-review; after Fix that changed tests/behavior → re-run Adv (or Lite) once (+ Quality if structure changed); when clean → parent `my-dev-flow-test` per Review profile (not Mode alone).

## Severity exit

[`severity.md`](../my-dev-flow/severity.md) — Adv/Quality clean at zero Critical/Major; lens loop clean when Merge Result **clean** (or single-lens parent copy). Enhancements → Deferred.

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
4. Launch stages per parent Happy path ([`../my-dev-flow/stages.md`](../my-dev-flow/stages.md)).
