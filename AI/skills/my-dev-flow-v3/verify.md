# Verify / Smoke / Fix / Stale

**SoT for:** Verify gate, Independent Smoke, skip-review ordered recovery, stale clear.

## Verify gate

Build / Fix must end with `Result: verify-pass` (max 3 attempts). On verify-pass, parent same turn:

- `Last Verify: verify-pass`  
- `Last verify-pass at: <ISO-8601 Run-log local wall time>`  
- `Last verify settle-gen: <current Gate B settle gen>`  
- Build may set `Smoke source: Build-verify` on `06`

Do not advance while `Last Verify=verify-pass` and `Last verify-pass at=none`.

## Independent Smoke (SoT)

**Unlock = `Smoke source: Smoke-Task` only.** Notes `smoke-pass (re-run)` and Run-log are **companions**, not substitutes.

| Who writes | Field |
|------------|-------|
| Smoke Task | `Smoke source: Smoke-Task` on `06` |
| Parent | Notes `smoke-pass (re-run)` + evidence provenance; clear Notes `smoke re-run` |
| Build | `Smoke source: Build-verify` only |

Applies to: Mode full + profile full (**E1**) and legal **skip-review**. Build-writes-Smoke does **not** waive Prefer unpaid for those paths.

## Skip-review ordered recovery

1. **Prefer unpaid** — independent Smoke while Smoke unpaid/fail (even if an escape pair exists). Parent may set Notes `smoke re-run` once before launch.  
2. **Prefer paid** — when Tests success (Gate C bar): if `merge` ∈ Gate C approved → Prefer `merge`; else Prefer `gate-c`.  
3. **Else** — Decision N ([decisions.md](decisions.md)); do not drop profile or write escape Notes without named user yes.

## Stale after rebuild / Amend

Mark `review-stale` / `test-stale` when prior Results look paid but design changed.

### Lite / full clear

- Clear `review-stale` when Run-log shows Adv+Quality (or `code-review-phase`) **after** rebuild **Last verify-pass at** **and** Review clean.  
- Clear `test-stale` when `06` **Updated** (or Run-log `test-*`) is **after** that timestamp **and** Result **success** + matching Test path.

### Skip-review clear

- `review-stale` = N/A (clear).  
- Clear `test-stale` on fresh `Smoke source: Smoke-Task` after **Last verify-pass at**.

## Build Gate B check (first action)

1. Notes `design-stale` / `design-backloop` → `blocked — …`  
2. Gate B settle gen mismatch / auto missing → `blocked — Gate B settle stale` / `… auto not settled`  
3. Else proceed
