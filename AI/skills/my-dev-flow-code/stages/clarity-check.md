## Clarity check (parent)

Before TDD review, Build, or Fix:

> Are the instructions, dependencies, and reference files clear enough to proceed?

If no → ask the user; do not launch the Task.  
If Verify commands missing before Build → set them (or ask) first.

After pass, log the **boundary-matched** token for the Next stage (high-risk set — [parent-next.md](../../my-dev-flow/parent-next.md)):

`clarity-check ok — tdd-review` | `clarity-check ok — build` | `clarity-check ok — fix-review` | `clarity-check ok — fix-tests` | `clarity-check ok — merge`

Design-boundary clarity tokens do **not** unlock these.

### Merge

Before launching **`merge`**:

- **Gate C approved** is a non-empty action subset **+** provenance `gate-c-approved` ([hitl.md](../../my-dev-flow/hitl.md))
- Gate C **test bar** met for this Review profile (or waiver + matching provenance)
- No secrets in the commit set

If no → ask the user; do not launch. Log `clarity-check ok — merge` when clear.
