# Gate C — merge bar

**Always blocking.** Named user yes for each of: commit / push / PR / merge (subset allowed → stay `paused` until remaining yes).

## Test bar ≡ Tests success

**SoT** (one definition — [derive-next-defs-post.md](derive-next-defs-post.md) **Tests success** copies this):

| Profile | Bar |
|---------|-----|
| **lite** / **full** | `06` Result **success** + **Test path last run** matches profile **and** unpaid `review-stale` / `test-stale` **cleared** (parent **or** labeled solo clear — [hitl.md](hitl.md) · [solo-entry.md](solo-entry.md) · [verify.md](verify.md) Stale) |
| **skip-review** | verify-pass + independent Smoke (`Smoke source: Smoke-Task`) + one escape Notes↔provenance **and** stale cleared (`review-stale` N/A cleared; `test-stale` cleared — parent **or** labeled solo) |

**Escape pair (typical happy path):** Notes `smoke-pass` ↔ provenance `smoke-pass-rerun` (evidence form) — used on **first-pass and Prefer-re-smoke**; alias `smoke-pass (re-run)` ≡ `smoke-pass`. Prose / `06` Result `smoke-pass` is a **label only** — it does **not** pay Prefer paid / Gate C escape without the Notes↔provenance pair ([verify.md](verify.md) Escape Notes name). Alternates: `docs-only` / `smoke-waive` / `gate-c-test-override` with same-kind user provenance ([hitl.md](hitl.md)).

Independent Smoke SoT: [verify.md](verify.md). Build-writes-Smoke alone does **not** pay skip-review / E1. `06` Result alone does **not** pay Prefer paid / Gate C escape.

## Prefer

- Tests success + **Lenses clean** + Gate C unpaid → Prefer `gate-c`  
- skip-review Prefer paid predicate: [derive-next.md](derive-next.md) · [verify.md](verify.md) — still requires **Lenses clean**  
- Tests success + **Lenses clean** + `merge` ∈ Gate C approved (+ provenance) → Prefer `merge`  
- Non-empty approved without `merge` (PR-only) → Prefer `gate-c` for remaining **or** stay `paused`  
- Status `done` / `stopped` → Stop (do not Prefer stages)

## Read before you decide

Confirm Tests success (bar above) **and** **Lenses clean**. Confirm named actions. Do not invent approval.
