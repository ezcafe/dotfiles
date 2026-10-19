# Quality

## FIRST

**Order:** missing required api/db → E1 Smoke unpaid → Quality (Prefer finalize → Smoke → Adv/Quality).

If Has API/DB ∈ {yes, unknown} ∧ ¬tiny ∧ (Lens plan = `none` **or** missing required `api`/`db`) → `Result: blocked — missing required api/db` (Prefer `finalize-lens-plan` — [../../my-dev-flow-v3/lenses.md](../../my-dev-flow-v3/lenses.md) · [../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)). True **Lens plan unpaid** (plan≠`none` + unpaid `05-lens-*`) is a separate Prefer unpaid `lens-*` path — not this token.

If E1 (Mode full + profile full) and `Smoke source` ≠ `Smoke-Task` → `Result: blocked — Smoke unpaid` ([../../my-dev-flow-v3/verify.md](../../my-dev-flow-v3/verify.md)). Notes companion alone does not unlock.

## Do

Five-axis pass: correctness, readability, architecture, security, performance.  
Flag spaghetti growth, file-size explosions, thin wrappers, wrong-layer logic.  
Approval bar: improves code health (not perfection).
