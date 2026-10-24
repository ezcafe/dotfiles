# Adversarial

## FIRST

**Order:** missing required api/db → E1 Smoke unpaid → Adv (Prefer finalize → Smoke → Adv).

If Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (Lens plan = `none` **or** missing required `api`/`db`) → `Result: blocked — missing required api/db` — **Hard stop**; parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)). True **Lens plan unpaid** (plan≠`none` + unpaid `05-lens-*`) is a separate unpaid `lens-*` path — not this token.

If E1 (Mode full + profile full) and `Smoke source` ≠ `Smoke-Task` → `Result: blocked — Smoke unpaid` ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)). Notes companion alone does not unlock.

## Do

Hunt breakages, security holes, missing edge cases. Write Adv section Result.  
Be ambitious about structural simplification when findings allow — prefer deleting complexity.
