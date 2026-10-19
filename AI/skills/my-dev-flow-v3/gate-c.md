# Gate C — merge bar

**Always blocking.** Named user yes for each of: commit / push / PR / merge (subset allowed → stay `paused` until remaining yes).

## Test bar ≡ Tests success

**SoT** (one definition — [derive-next.md](derive-next.md) Definitions copy this):

| Profile | Bar |
|---------|-----|
| **lite** / **full** | `06` Result **success** + **Test path last run** matches profile **and** unpaid `review-stale` / `test-stale` **cleared** |
| **skip-review** | verify-pass + independent Smoke (`Smoke source: Smoke-Task`) + one escape Notes↔provenance **and** stale cleared (`review-stale` N/A cleared; `test-stale` cleared) |

Independent Smoke SoT: [verify.md](verify.md). Build-writes-Smoke alone does **not** pay skip-review / E1.

## Prefer

- Tests success + Gate C unpaid → Prefer `gate-c`  
- Tests success + `merge` ∈ Gate C approved (+ provenance) → Prefer `merge`  
- Non-empty approved without `merge` (PR-only) → Prefer `gate-c` for remaining **or** stay `paused`  
- Status `done` / `stopped` → Stop (do not Prefer stages)

## Read before you decide

Confirm Tests success (bar above). Confirm named actions. Do not invent approval.
