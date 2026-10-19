# Golden: Pre-Build Prefer order (F1 / F2 / F5 / F6 / F10 / F11 / F12)

**SoT:** [../derive-next.md](../derive-next.md) + [../derive-next-pre.md](../derive-next-pre.md) Pre-Build first-match.  
**Seed habit:** Step 0 writes **only** `00-run.md` — no stub `02b` / `03` / `04` ([../step-0.md](../step-0.md)).

## F1 — Grill open before ¬ Design present → `design`

**Setup:** Mode full; **Analyze paid** (`02-analysis` exists **and** Result `done`); **Grill unpaid** (no `02b` ∧ ¬Notes `grill-skip`); ¬ Design present.  
**Prefer:** `grill` — **not** `design`.  
**Same Prefer** when `02b` exists with Result **`pending`** or **`needs-round`** ∧ ¬Notes `grill-skip` (template `pending` alone does **not** close Grill).  
**After** Grill closed (Notes `grill-skip` — even if `02b` still `pending`/`needs-round` — **or** Result `frontier-empty` only; Result `skipped` does **not** close) + still ¬ Design present → Prefer `design`.

## F1b — ¬ Design present → Prefer `design`

**Setup:** Mode full; Analyze + Grill paid; `03` missing **or** Result ≠ `done` (e.g. `pending`); Isolated/`03a` missing.  
**Prefer:** `design` — **not** `design-review` / `api|db`.  
**After** Design present (`03` + Result `done`) + unpaid Isolated → Prefer Isolated → else `design-review`.

## Cold start (Mode simple)

**Setup:** After Step 0 (only `00-run`); ideation paid; ¬ Design present; none of {`02-analysis`, `03`, `04`} on disk (true cold start — ¬(all three present) ≠ cold start); **Grill unpaid**.  
**Prefer:** `design-phase` — **not** `design-verify-phase` / `grill`.  
**Same Prefer** when Notes `grill-skip` (Grill closed) + still ¬ Design present / none of {`02-analysis`, `03`, `04`} on disk — Prefer `design-phase`, **not** `design-verify-phase` (unsafe: ¬ Design present).  
**Same Prefer** when `03` missing or Result ≠ `done` (incomplete Design — partial set) ∧ ¬ (**Grill open** ∧ ¬carve) — Prefer `design-phase` before `design-verify-phase` ([../derive-next-pre.md](../derive-next-pre.md) incomplete Design row; not cold-start carve alone).  
**Mid-open (Mode simple):** **Grill open** ∧ ¬carve (e.g. any of {`02-analysis`, `03`, `04`} on disk, **or** `02b` Result `skipped`/`needs-round`/`pending` ∧ ¬Notes `grill-skip`) → Prefer `grill` — **not** re-`design-phase`.  
**Do not:** Pre-seed stub `03` / `02b` `pending` then Prefer `design-verify-phase` or treat Grill closed without Notes `grill-skip` / Result `frontier-empty` (Result `skipped` alone never closes).

## F2 — `needs update` → Prefer `design-update`

**Setup:** Mode full; Design present (`03` Result `done`); any `03a*` Result **`needs update`**; ¬ Notes `design-stale`; **Grill closed**.  
**Prefer:** `design-update` — **not** Isolated / `design-review` first.  
**After** (same turn as Task complete): Run-log `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** (not only `needs update` — same as backloop invalidate) — else Prefer loops on `design-update`. Then Prefer unpaid Isolated → else `design-review`. Mode simple: Prefer `design-verify-phase` only.  
Same entry under Notes `design-backloop` / **backloop rewrite unpaid** when **Grill closed** ([../design-backloop.md](../design-backloop.md) · [design-backloop-after-build.md](design-backloop-after-build.md)).  
**While Grill open** (backloop or `needs update`): Prefer `grill` first — **not** `design-update`.  
**Unsafe while Notes `design-stale`:** do **not** Prefer Isolated / design-review / design-verify / design-update — Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** (Upgrade sets `03` → `pending`; Prefer rewrite even if prior `done` — [../step-0.md](../step-0.md) · [../derive-next.md](../derive-next.md)). See F11 / F12.

## F5 — ideation unpaid

**ideation unpaid** = ¬Notes `ideation-skip` **and** ¬Notes `ideation-confirmed`. Paid = Notes `ideation-confirmed` + provenance (`user:"…" ≥12 chars`) **or** Notes `ideation-skip` (parent-only — Stages return candidates only; no Prefer on waive).

| Mode | Prefer |
|------|--------|
| full | `ideation` until paid (`ideation-confirmed` **or** Notes waive) — before Gate A |
| simple | `ideation` until paid (`ideation-confirmed` **or** Notes waive) — before `design-phase` |

Brainstorm hard-gate is **always** ([../brainstorm.md](../brainstorm.md)) — not Has-UI-only. Bare chat / `01-idea` alone ≠ Done.

## F6 — `tdd-review` / Prefer `gate-b` when **04a ok**

**Setup (unpaid):** Design clean; **planned tests present** (`04` Planned tests section ≥1 named case); ¬Notes `04a skipped`; `04a` missing **or** Result ∉ {`clean`} (incl. **`pending`** \| **`needs more tests`**).  
**Prefer:** `tdd-review` **only** while **04a unpaid / dirty**. Optional waiver = Notes `04a skipped` (no Prefer). Unsafe: Prefer `gate-b` / `build` while unpaid/dirty.  
**Advance → Prefer `gate-b`** when Design clean ∧ **04a ok** = ¬ unpaid / dirty: Result `clean`, **or** Notes `04a skipped`, **or** ¬ **planned tests present**.  
**Not present (vacuous ok):** empty / `N/A` / missing Planned tests → no Prefer `tdd-review`; Prefer `gate-b` (if Gate B not settled) without requiring `04a` file or Notes skip (optional Notes `04a skipped — no planned test cases`).

## Unpaid Gate A / skim / Analyze (F10)

Mode full:
- **unpaid Gate A** (`01a` missing **or** Result ≠ `ok`) → `gate-a`
- **unpaid skim** (Gate A paid **and** (`02-skim` missing **or** Result ≠ `done`)) → `skim`
- **Analyze unpaid** (`02-analysis` missing **or** Result ≠ `done`) → `analyze` — before Grill / Design

**Analyze paid** = file exists **and** Result `done` (mirror Design present).

## F11 — Happy Upgrade → design-stale unpaid chain

**Setup:** Mid-run Upgrade simple→full writes card **Mode = full** (+ drop skip-review → lite|full if set — [../step-0.md](../step-0.md)); parent Notes `design-stale`; Gate A + skim paid; **Grill closed** (Notes `grill-skip` **or** `02b` Result `frontier-empty`); **Analyze unpaid** (`02-analysis` missing **or** Result ≠ `done`, or optionally invalidated → `pending`); `03` Result `pending` (Upgrade invalidate). Prefer assumes **Mode full** (Mode simple Prefer rows do **not** apply).  
**Prefer:** `analyze` (Analyze unpaid) — **not** Isolated / design-review / design-update / gate-b / build.  
**After** Analyze paid + Grill closed + still Notes `design-stale` → Prefer **design unpaid under design-stale** → `design` rewrite (even if prior `03` looked `done` before Upgrade).  
**Clear:** parent clears Notes only after Mode-full `design` + `03` Result `done` (`candidate clear design-stale`).

## F12 — design-stale + Grill open → `grill` first

**Setup:** Notes `design-stale`; Analyze paid; **Grill open** (`02b` Result `pending` or `needs-round` ∧ ¬Notes `grill-skip` — Grill unpaid alone is also open); `03` unpaid under design-stale.  
**Prefer:** `grill` — **not** `design` / Analyze / Isolated / design-review (deadlock ban: never Prefer `design` while Grill open under design-stale).  
**After** Grill closed (Notes `grill-skip` **or** Result `frontier-empty`) → Prefer unpaid Analyze → else **design unpaid under design-stale**.  
**Optional Upgrade:** invalidate/re-open `02b` → `pending` so this Prefer fires after Upgrade ([../step-0.md](../step-0.md)).
