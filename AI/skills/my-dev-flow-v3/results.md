# Result tokens

**Advance only on paying Results.** Parent updates file-top and section Results.

## Design-review (overall + isolated)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid (Amend / Upgrade invalidate) |
| `clean` | Paid |
| `needs update` | Must Prefer design-update / re-review |
| `skipped` | Isolated only, when Has=no or tiny |

**Design clean** = overall `clean` **and** required isolated paid — [derive-next.md](derive-next.md).

## Grill

`frontier-empty` \| `needs-round` \| `skipped` (+ Notes grill-skip).

## Code review (`05-review-log.md`)

Adv + Quality section Results: `clean` \| `needs fix` \| `pending`.  
**Review clean** = both sections `clean`. File-top alone never pays.

## Lenses / Merged

Result-bearing = `clean` \| `needs fix`. Missing/`pending` = unpaid.

## Tests (`06`)

`success` \| `fail` \| `pending`. Smoke section + **Smoke source**.

## Parent habit

On verify-pass: set Last Verify, Last verify-pass at (ISO-8601 Run-log local wall time), Last verify settle-gen — [verify.md](verify.md).

## Artifact-presence stages

`design-phase` advances on **Done when**: design artifacts **and** Grill closed / Notes grill-skip — not files alone.
