# TDD plan review (optional)

Review planned cases in `04` / `04a` before Gate B when useful.

**planned tests present** (SoT): `04-tasks.md` has a **Planned tests** (or equivalent cases) section with ≥1 named test case — [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md). Empty / `N/A` / missing → not present.

**Optional waiver:** Notes `04a skipped` (**parent-only** named yes + provenance `04a-skipped` — [../../my-dev-flow-v3/hitl.md](../../my-dev-flow-v3/hitl.md)) → treat as paid (no Prefer `tdd-review`). Stage returns **`candidate 04a skipped`** only — never write the Note.  
**Prefer `tdd-review` only** when Design clean **and** **04a unpaid / dirty**: planned tests present ∧ ¬Notes skip ∧ (`04a` missing **or** Result ∉ {`clean`}) — incl. Result **`pending`** \| **`needs more tests`**.  
**04a ok** = ¬ unpaid / dirty (incl. ¬ planned tests present) → Prefer `gate-b` with Design clean; do **not** Prefer `tdd-review`.

**Result** (first line of `04a`): `pending` \| `clean` \| `needs more tests`.

| Token / state | Advance |
|---------------|---------|
| `clean` | **04a ok** — Prefer `gate-b` (with Design clean) |
| Notes `04a skipped` (parent-written) | Same (**04a ok** waiver) |
| ¬ planned tests present | **04a ok** (vacuous) — Prefer `gate-b`; no Prefer `tdd-review` |
| `needs more tests` \| `pending` \| missing **and** planned tests present ∧ ¬Notes skip | **04a unpaid / dirty** — Prefer `tdd-review`; unsafe to Prefer `gate-b` / `build` |

**After:** may return `candidate 04a skipped` to parent when waiver is appropriate; parent writes Notes + provenance.

Parent SoT: [../../my-dev-flow-v3/derive-next.md](../../my-dev-flow-v3/derive-next.md) · [../../my-dev-flow-v3/results.md](../../my-dev-flow-v3/results.md).
