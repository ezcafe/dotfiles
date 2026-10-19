---
name: my-dev-flow-v2-review
description: >-
  Verifies a code draft: full profile uses Adversarial then Quality then
  conditional lenses; lite profile uses code-review-phase then lenses per plan
  (merge-findings if 2+). Lens plan defaults to none. Fix until clean. Use when
  the user says run my-dev-flow-v2-review, review the draft, or after
  my-dev-flow-v2-code.
---

# my-dev-flow-v2-review

Review + Fix subflow of [`my-dev-flow-v2`](../my-dev-flow-v2/SKILL.md).

**Owned stages:** `adversarial`, `quality`, `code-review-phase`, `lens-*`, `merge-findings`, `fix-review` — load `stages/<id>.md` only.

| Topic | File |
|-------|------|
| Post-Build path | [`../my-dev-flow-v2/stages.md`](../my-dev-flow-v2/stages.md) |
| Lens plan / skip-review | [`../my-dev-flow-v2/lenses.md`](../my-dev-flow-v2/lenses.md) |
| Verify on Fix | [`../my-dev-flow-v2/verify.md`](../my-dev-flow-v2/verify.md) |
| Severity / Results | [`../my-dev-flow-v2/severity.md`](../my-dev-flow-v2/severity.md) · [`../my-dev-flow-v2/results.md`](../my-dev-flow-v2/results.md) |
| Handoffs | compose from [`../my-dev-flow-v2/handoffs.md`](../my-dev-flow-v2/handoffs.md) |

## Principles

- Writers (Fix) never self-approve; verifiers re-check after Fix.
- skip-review → do nothing here (parent Gate C path).
- Profile **full:** first unpaid pass Adv → Quality (Adv before Quality on that pass) → lenses → merge-findings if 2+. After `fix-review` verify-pass, defer to Prefer dirty ([derive-next.md](../my-dev-flow-v2/derive-next.md)) — do **not** force Adv before Quality when Prefer names Quality (or re-lens) only.
- Profile **lite:** `code-review-phase` → lenses per plan → merge-findings if 2+.
- Mode **full** + profile **full:** E1 independent Smoke **required** before Adv / Quality ([verify.md](../my-dev-flow-v2/verify.md) Independent Smoke (SoT)).
- Parent always launches unpaid `lens-*` Tasks; `code-review-phase` may note signals but does not write `05-lens-*` or mark lenses paid.
- Fix → verify-pass before re-review; Prefer re-run **dirty** verifier / re-lens ([derive-next.md](../my-dev-flow-v2/derive-next.md) Prefer · [After Fix](stages/fix-review.md#after-fix)); max 3 → Decision N.

## Start

1. Confirm Build verify-pass + Smoke rules for Mode×profile (E1 before Adv when full×full).
2. Preflight code-review checks; compose handoff; run `stages/<id>.md`.
3. On `needs fix` → fix-review; on `clean` → unpaid `lens-*` per plan → `merge-findings` if 2+ → hand off to test.
