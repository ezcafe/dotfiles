# Gate C

**SoT for:** Test bar + Gate C approved. Always **blocking**. Provenance: [hitl.md](hitl.md).

## Read before you decide (show to user)

When asking Gate C (commit / push / PR / merge), the **parent** pastes this reading guide to the user. Paths under `.my-docs/workflow/<slug>/`.

**Must read (decision):**

1. `06-test-log.md` + `00-run.md` Last Verify — by **Review profile** ([Test bar](#test-bar-before-merge)):
   - **lite** / **full** → Result **success** + **Test path last run** matching profile (no escape / waiver substitute) **and** unpaid stale Notes cleared (`review-stale` / `test-stale`)
   - **skip-review** → Last Verify **verify-pass** + independent Smoke **smoke-pass** per [verify.md](verify.md) Independent Smoke (SoT) **and** one required escape with matching Notes↔provenance pair ([hitl.md](hitl.md)) **and** unpaid stale Notes cleared (`review-stale` N/A cleared; `test-stale` cleared). Escape alone does **not** substitute for success under lite/full, and does **not** waive verify-pass + independent smoke-pass under skip-review.
2. `05-review-log.md` — open Critical/Major? Fix asks? Merged lenses when Lens plan 2+
3. `00-run.md` — Last Verify, Mode, Review profile, Has API/DB/auth, Gate C approved (still `none` until yes); unpaid `review-stale` / `test-stale` (skip-review: `review-stale` N/A)

**Skim for risk summary / PR:**

- `03-design.md` — Recommendation + contracts (short)
- `04-tasks.md` — acceptance left unpaid?
- `05-lens-*.md` — when Lens plan ran isolated lenses

**Decide:** name each action — `commit` · `push` · `pr` · `merge` (subset OK, e.g. “PR only”). Parent records **Gate C approved** + provenance in the **same turn**. Silence ≠ yes.

## Test bar (before merge)

**Tests success** ≡ this Test bar (one definition — [derive-next.md](derive-next.md) Definitions). Unpaid stale Notes fail the bar.

| Review profile | Required |
|----------------|----------|
| **skip-review** | Legal per [lenses.md](lenses.md) **and** verify-pass + independent smoke-pass per [verify.md](verify.md) Independent Smoke (SoT) **and** one escape **with matching Notes↔provenance pair** ([hitl.md](hitl.md)) **and** unpaid stale Notes cleared (`review-stale` N/A cleared; `test-stale` cleared). Escape kinds are valid **only** under skip-review. |
| **lite** | `06-test-log.md` Result **success** and **Test path last run:** `lite` — no escape / waiver substitute — **and** unpaid stale Notes cleared (`review-stale` / `test-stale`) |
| **full** | `06-test-log.md` Result **success** and **Test path last run:** `full` — no escape / waiver substitute — **and** unpaid stale Notes cleared (`review-stale` / `test-stale`) |

## Gate C approved

```markdown
**Gate C approved:** commit,push,pr,merge
- provenance — gate-c-approved — user: "commit push PR and merge"
```

| Value | Meaning |
|-------|---------|
| `none` | Not settled |
| subset of `commit`,`push`,`pr`,`merge` | Only what the user named |

Do not invent actions. Merge Task re-reads field before git/remote work.

**Gate C unpaid** (derive Definitions): approved `none` / empty, **or** remaining named actions unpaid — Prefer `gate-c`, not bare non-empty → `merge` ([derive-next.md](derive-next.md)).

After Merge Result **success** and `merge` ∈ approved → Status **`done`**. Subset without merge → stay `paused` (do **not** Prefer `merge`).
