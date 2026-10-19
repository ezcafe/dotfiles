# Result first-line tokens

```
Result: <token>
```

Optional note: `Result: blocked — Gate B veto`. Parent reads first ~40 lines.

| Domain | Tokens | Advance when |
|--------|--------|--------------|
| Verify | `verify-pass` \| `verify-fail` | `verify-pass` (docs-only Fix: same token + Notes `TDD/Verify skipped — docs-only` — not a separate token) |
| Blocked | `blocked — <reason>` (incl. `blocked — E1 smoke re-run unpaid`) | settle reason first |
| Design review overall (`03a-design-review-log` / verify-phase) | `pending` \| `clean` \| `needs update` | overall `clean` **and** isolated API/DB `clean`\|`skipped` when required ([lenses.md](lenses.md) · [design-review SKILL](../my-dev-flow-v2-design-review/SKILL.md)) — Advance only on overall `clean` (+ isolated paid when required). **`pending`** = unpaid (Amend / Upgrade invalidate) — do **not** advance |
| Design review isolated (`03a-api` / `03a-db`) | `pending` \| `clean` \| `needs update` \| `skipped` | that file `clean` or Notes-skip / Has=no / `tiny-contract-tweak` (`skipped`) — feeds overall clean rule above. Advance only on `clean`\|`skipped` when that file is in scope. **`pending`** = unpaid (Amend / Upgrade invalidate) — do **not** advance |
| Gate A (`01a`) | `ok` \| `needs update` \| `escalate` | `ok` |
| Grill (`02b`) | `frontier-empty` \| `needs-round` \| `skipped` | `frontier-empty` or `skipped` |
| Skim | `done` \| `skipped` | either |
| TDD (`04a`) | `clean` \| `needs more tests` | **`clean`** or Notes `04a skipped` only — **`needs more tests` does not advance** (re-`tdd-review` until clean — [derive-next.md](derive-next.md)) |
| Code review (`05*`) | `clean` \| `needs fix` | **Review clean** = Adv+Quality section Results both **`clean`** (no file-top fallback) → unpaid `lens-*` if Lens plan ≠ **`none`**; else unpaid `test-*` — [derive-next.md](derive-next.md) Definitions · Post-Build; **code-review unpaid** when Adv/Quality section Result missing/**`pending`** (same Result-bearing bar as lenses); **overall Result** may also include Merged (plan **2+**) — do not equate; file-top optional |
| Test / Smoke (`06`) | `success` \| `failure` \| `smoke-pass` \| `smoke-fail` | `success` / `smoke-pass` |
| Merge | `success` \| `aborted` | `success` and `merge` ∈ Gate C approved |

**Clean (code review / severity default)** = zero open Critical/Major ([severity.md](severity.md)).

**Clean (design-review)** = zero Critical/Major **and** API/DB `clean`\|`skipped` when required — full rule in [design-review SKILL](../my-dev-flow-v2-design-review/SKILL.md) · [lenses.md](lenses.md) (overall vs isolated tokens above). Do **not** treat overall clean as “severity only.”

## Artifact-presence stages (no first-line Result)

These design write stages are **exempt** from `Result: <token>` on the first line. Parent advances on **Done when** (not “files exist” alone):

- `ideation`, `ideation-update`, `analyze`, `design`, `design-update` — advance when Done when / required paths are satisfied
- `design-phase` — advance only when design artifacts are present **and** Grill is closed (`02b` Result **`frontier-empty`** \| **`skipped`**, or Notes grill-skip) — do **not** advance on files alone while Grill is open ([grill.md](grill.md) · [derive-next-pre.md](derive-next-pre.md))

Stages that **do** require a first-line Result (Gate A, skim, grill, design-review / verify, TDD, Verify, review, test, merge) still follow the table above.

## Parent habit

1. Read Result first line (skip when artifact-presence stage — check Done when / paths; for `design-phase` also require Grill closed / Notes grill-skip).
2. Update card + Last Verify when Verify applies. On **verify-pass**, same turn set **Last Verify:** `verify-pass` **and** **Last verify-pass at:** `<ISO-8601 Run-log local wall time>` (same SoT clock as Gate B settle expansion — [derive-next.md](derive-next.md) Freshness). **Fail-closed:** do not advance while **Last Verify** = `verify-pass` **and** **Last verify-pass at** = `none` ([artifacts/00-run.md](artifacts/00-run.md) · [preflight.md](preflight.md)).
3. Advance only per table (or Done when for exempt stages — not files alone for `design-phase`).
4. Max 3 attempts → Decision N ([decisions.md](decisions.md)).
