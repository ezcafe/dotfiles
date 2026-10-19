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

**Unlock = `Smoke source: Smoke-Task` only.** Notes `smoke-pass` and Run-log are **companions**, not substitutes.

| Who writes | Field |
|------------|-------|
| Smoke Task | `Smoke source: Smoke-Task` on `06` |
| Parent | Notes `smoke-pass` + provenance `smoke-pass-rerun` (evidence form); clear Notes `smoke re-run` |
| Build | `Smoke source: Build-verify` only |

Applies to: Mode full + profile full (**E1**) and legal **skip-review**. Build-writes-Smoke does **not** waive Prefer unpaid for those paths.

### Escape Notes name (first-pass vs re-run)

Literal Notes token is **`smoke-pass`** ↔ provenance **`smoke-pass-rerun`**.

**Alias:** Notes `smoke-pass (re-run)` ≡ `smoke-pass` (historical name). Prose / `06` Result `smoke-pass` may **label** the same event only when parent also writes the escape Notes↔provenance pair after Smoke-Task success (first-pass or Prefer-re-smoke) — Result alone never pays.

**Unlock vs escape (do not conflate):**
- **E1 Adv unlock** = `Smoke source: Smoke-Task` **only** (Notes/Run-log are companions — never substitutes).
- **skip-review Prefer paid / Gate C escape** = `Smoke source: Smoke-Task` **and** one escape Notes↔provenance (typically `smoke-pass` ↔ `smoke-pass-rerun`).

**`06` Result alone does not pay escape:** a Smoke / `06` Result of `smoke-pass` / **success** (or prose “smoke-pass”) is **not** Prefer paid and **not** Gate C escape by itself. Parent must still write the Notes↔provenance escape pair. Accept Result/prose `smoke-pass` only as a **label** when that pair is written — never as a substitute for Notes or provenance ([gate-c.md](gate-c.md)).

| When | Use |
|------|-----|
| **First-pass** independent Smoke success (E1 or skip-review) | Same Notes + evidence provenance — required for skip-review Prefer paid / Gate C escape pair |
| **Prefer-re-smoke** after `fix-tests` + verify-pass | Same Notes + evidence provenance (overwrite / refresh evidence for current settle gen) |

Do **not** invent a different first-pass Notes name. Other escape kinds (`docs-only` / `smoke-waive` / `gate-c-test-override`) still need named user yes + same-kind provenance ([hitl.md](hitl.md)).

## Skip-review ordered recovery

**SoT** for Mode×profile skip-review cell and mermaid ([stages.md](stages.md)) — do not invent a shorter order; stages.md is pointer-only.

1. **Smoke fail** → Prefer `fix-tests` first (even if an escape pair exists). Prefer-re-smoke only after Last stage `fix-tests` + verify-pass ([derive-next.md](derive-next.md) · [derive-next-post.md](derive-next-post.md)). Parent may set Notes `smoke re-run` once before re-smoke launch.  
2. **Smoke unpaid** → Prefer unpaid independent `smoke` (Build-writes-Smoke does not waive).  
3. **Prefer paid** — when **skip-review Prefer paid** ([derive-next.md](derive-next.md)): Tests success (verify-pass + `Smoke source: Smoke-Task` + one escape Notes↔provenance — typically `smoke-pass` ↔ `smoke-pass-rerun` on first-pass or re-smoke; alias `smoke-pass (re-run)` — + stale cleared — [gate-c.md](gate-c.md)) **and** **Lenses clean**. Destination: if `merge` ∈ Gate C approved → Prefer `merge`; else Prefer `gate-c` ([derive-next-post.md](derive-next-post.md)).
4. **Else** — Decision N ([decisions.md](decisions.md)): Smoke unpaid → ask escape **or run Smoke**; Smoke-Task set ∧ only escape missing → escape/drop only (**not** run Smoke). Do not drop profile or write escape Notes without named user yes.

## Prefer order vs finalize-lens-plan (E1 / skip-review)

**Intentional** Post-Build first-match ([derive-next-post.md](derive-next-post.md) · [lenses.md](lenses.md)): when **missing required api/db**, Prefer `finalize-lens-plan` **before Smoke and before Adv** — gates Prefer-re-smoke, E1/skip-review Smoke unpaid, Adv / `code-review-phase` / lenses / test. Safety: never Prefer Smoke or Adv with Lens plan=`none` while required api/db missing. After plan set: E1/skip-review unpaid Smoke (`Smoke source: Smoke-Task`) still before Adv.

## Stale after rebuild / Amend

Parent alone marks / clears `review-stale` / `test-stale` ([hitl.md](hitl.md)). Mark when prior Results look paid but design changed. Stages return `candidate review-stale` / `candidate test-stale` only. Prefer unpaid review on Notes `review-stale` **before** Lens plan unpaid when Adv/Quality still look `clean` ([derive-next-post.md](derive-next-post.md)).

### Lite / full clear

- Clear `review-stale` when Run-log shows Adv+Quality (or `code-review-phase`) **after** rebuild **Last verify-pass at** **and** Review clean.  
- Clear `test-stale` when `06` **Updated** (or Run-log `test-*`) is **after** that timestamp **and** Result **success** + matching Test path.

### Skip-review clear

- `review-stale` = N/A (clear).  
- Clear `test-stale` on fresh `Smoke source: Smoke-Task` after **Last verify-pass at**.

## Build Gate B check (first action)

1. ¬ Design clean / Verify clean → `blocked — Design not clean` ([preflight.md](preflight.md) Before Build · [results.md](results.md))  
2. **Grill open** → `blocked — Grill open` ([grill.md](grill.md))  
3. ¬ **04a ok** → `blocked — 04a unpaid/dirty` ([preflight.md](preflight.md) Before Build)  
4. Notes `design-stale` / `design-backloop` → `blocked — …`  
5. ¬ **Gate B settled** → `blocked — Gate B not settled` (missing blocking approval+provenance, missing matching auto token, missing Build armed on async, gen mismatch — [gate-b.md](gate-b.md))  
6. Else proceed
