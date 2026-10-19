# Result tokens

**Advance only on paying Results.** Parent updates file-top and section Results.

## Gate A (`01a`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid |
| `ok` | Paid — **unpaid Gate A** = missing **or** Result ≠ `ok` ([derive-next.md](derive-next.md)) |
| `escalate` | Soft Gate A Decision N path — still unpaid until `ok` |

## Skim (`02-skim`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid |
| `done` | Paid — **unpaid skim** = Gate A paid **and** (missing **or** Result ≠ `done`) ([derive-next.md](derive-next.md)) |

## Analyze (`02-analysis`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid — **not** Analyze paid |
| `done` | Paying — **Analyze paid** = file exists **and** Result `done` ([derive-next.md](derive-next.md)) |

## Design-review (overall + isolated)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid (Amend / Upgrade invalidate) |
| `clean` | Paid |
| `needs update` | Prefer **Grill open** → `grill` first; else Prefer unpaid `design-update` when **Grill closed**. On `design-update` complete: same-turn Run-log `design-update — settle-gen:<N>` **and** set **ALL** `03a*` → **`pending`** (not only `needs update` — same as backloop invalidate; else Prefer loops). Then Prefer unpaid Isolated / `design-review` / `design-verify-phase` per Mode ([derive-next.md](derive-next.md) · [design-backloop.md](design-backloop.md)). Allowed write — advance only on `clean` |
| `skipped` | Isolated only — Has=no **or** Notes `tiny-contract-tweak` ([lenses.md](lenses.md)); `unknown` ≠ skip (file required like yes); never invent empty files |

**Design clean** = overall `clean` **and** required isolated paid — [derive-next.md](derive-next.md).  
**Verify clean** (Mode simple) ≡ **Design clean** (same predicate).

## Grill

`frontier-empty` \| `needs-round` \| `pending` (+ Notes grill-skip). Result `skipped` is **not** a paying close token.

| Token / Notes | Grill |
|---------------|-------|
| Notes `grill-skip` | **Closed** — parent-only + provenance; closes even if `02b` Result is `pending`/`needs-round` |
| `frontier-empty` | **Closed** (paid frontier) |
| `needs-round` \| `pending` \| `skipped` \| missing file (∧ ¬Notes `grill-skip`) | **Open** — template `pending` / Task `skipped` alone does **not** close ([grill.md](grill.md) · [derive-next.md](derive-next.md)) |

## TDD plan (`04a`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid — **04a unpaid / dirty** when planned tests present ∧ ¬Notes skip ([derive-next.md](derive-next.md)) |
| `clean` | Paid (or Notes `04a skipped`) |
| `needs more tests` | Dirty — same unpaid/dirty bucket; Prefer re-`tdd-review`; do **not** advance to `gate-b` / `build` |

**04a unpaid / dirty** = planned tests present ∧ ¬Notes `04a skipped` ∧ (missing **or** Result ∉ {`clean`}) — incl. `pending`.  
**04a ok** = ¬ unpaid / dirty (incl. ¬ planned tests present) — Prefer `gate-b` / Before Build when Design clean ∧ **04a ok**.

## Code review (`05-review-log.md`)

Adv + Quality section Results: `clean` \| `needs fix` \| `pending`.  
**Review clean** = both sections `clean`. File-top alone never pays.

## Lenses / Merged

Result-bearing = `clean` \| `needs fix`. Missing/`pending` = unpaid.  
`needs fix` → Prefer `fix-review` (not `merge-findings` / `test-*`). Prefer `merge-findings` only when planned lenses **clean** (or after Fix re-unpay → re-lens).

## Tests (`06`)

`success` \| `fail` \| `pending`. Smoke section + **Smoke source**.

## Parent habit

On verify-pass: set Last Verify, Last verify-pass at (ISO-8601 Run-log local wall time), Last verify settle-gen — [verify.md](verify.md).

## Design (`03`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid — **not** Design present |
| `done` | Paying — **Design present** = file exists **and** Result `done` ([derive-next.md](derive-next.md)) |

## Artifact-presence stages

`design-phase` advances on **Done when**: design artifacts **and** Grill closed (Notes `grill-skip` **or** Result `frontier-empty` only) — not files alone.  
`ideation` advances when ¬ **ideation unpaid** (Notes `ideation-confirmed` + provenance **or** Notes `ideation-skip` — parent-only; [brainstorm.md](brainstorm.md)).
