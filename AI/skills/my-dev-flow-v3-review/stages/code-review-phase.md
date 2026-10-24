# Code-review-phase (lite)

## FIRST

**Order:** missing required api/db → E1 Smoke unpaid → review (Prefer finalize → Smoke → review).

If Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (Lens plan = `none` **or** missing required `api`/`db`) → `Result: blocked — missing required api/db` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)). True **Lens plan unpaid** (plan≠`none` + unpaid `05-lens-*`) is a separate unpaid `lens-*` path — not this token.

If E1 (Mode full + profile full) and `Smoke source` ≠ `Smoke-Task` → `Result: blocked — Smoke unpaid` ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)). Notes companion alone does not unlock. (E1 normally uses Adv/Quality; keep this gate if somehow launched under E1.)

## Do

Bundled Adv+Quality into sections. **Review clean** requires both section Results `clean`. File-top alone never pays. Missing/`pending` section = unpaid.
