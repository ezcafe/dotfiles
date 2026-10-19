## Clarity check (parent)

Before TDD review, Build, or Fix:

> Are the instructions, dependencies, and reference files clear enough to proceed?

If no → ask the user; do not launch the Task.  
If Verify commands missing before Build → set them (or ask) first.

After pass, log the **boundary-matched** token for the Next stage (high-risk set — [parent-next.md](../../my-dev-flow-v2/parent-next.md)):

`clarity-check ok — tdd-review` | `clarity-check ok — build` | `clarity-check ok — fix-review` | `clarity-check ok — fix-tests` | `clarity-check ok — merge`

Design-boundary clarity tokens do **not** unlock these.

### Merge

Before launching **`merge`**:

- **Gate C approved** is a non-empty action subset **+** provenance `gate-c-approved` ([gate-c.md](../../my-dev-flow-v2/gate-c.md) · [hitl.md](../../my-dev-flow-v2/hitl.md))
- Gate C **test bar** met for this Review profile ([gate-c.md](../../my-dev-flow-v2/gate-c.md) · [preflight.md](../../my-dev-flow-v2/preflight.md)):
  - Profile **lite** / **full** → `06-test-log.md` Result **success** + **Test path last run** matching profile (no escape / waiver substitute) **and** unpaid stale Notes cleared (`review-stale` / `test-stale`)
  - Profile **skip-review** only → Last Verify **verify-pass** + independent Smoke **smoke-pass** per [verify.md](../../my-dev-flow-v2/verify.md) Independent Smoke (SoT) **and** one escape Notes↔provenance pair per [hitl.md](../../my-dev-flow-v2/hitl.md) **and** unpaid stale Notes cleared (`review-stale` N/A cleared; `test-stale` cleared)
- No secrets in the commit set

If no → ask the user; do not launch. Log `clarity-check ok — merge` when clear.
