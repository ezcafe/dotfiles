# Result tokens

**Advance only on paying Results.** Parent updates file-top and section Results.

## Gate A (`01a`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid |
| `ok` | Paid — **unpaid Gate A** = missing **or** Result ≠ `ok` ([derive-next-defs-pre.md](derive-next-defs-pre.md)) |
| `escalate` | Soft Gate A Decision N path — still unpaid until `ok` |

## Skim (`02-skim`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid |
| `done` | Paid — **unpaid skim** = Gate A paid **and** (missing **or** Result ≠ `done`) ([derive-next-defs-pre.md](derive-next-defs-pre.md)) |

## Analyze (`02-analysis`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid — **not** Analyze paid |
| `done` | Paying — **Analyze paid** = file exists **and** Result `done` ([derive-next-defs-pre.md](derive-next-defs-pre.md)) |

## Design-review (overall + isolated)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid (Amend / Upgrade invalidate) |
| `clean` | Paid |
| `needs update` | Unpaid under **design-update unpaid** (any `03a*` Result **`needs update`**, **or** **backloop rewrite unpaid**) — Definitions SoT [derive-next-defs-pre.md](derive-next-defs-pre.md). Allowed write — advance only on `clean` |
| `skipped` | Isolated only — Has=no **or** Notes `tiny-contract-tweak` ([lenses.md](lenses.md)); `unknown` ≠ skip (file required like yes); never invent empty files |

**Design clean** / **Verify clean** — [derive-next-defs-pre.md](derive-next-defs-pre.md) (also Post twin).

## Grill

Tokens: `frontier-empty` \| `needs-round` \| `pending` (+ Notes grill-skip). Result `skipped` is **not** a paying close. **Grill open** / **Grill closed** — [derive-next-defs-pre.md](derive-next-defs-pre.md) · [grill.md](grill.md).

## TDD plan (`04a`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid when **04a unpaid / dirty** holds ([derive-next-defs-pre.md](derive-next-defs-pre.md)) |
| `clean` | Paid (or Notes `04a skipped`) |
| `needs more tests` | Dirty — Prefer re-`tdd-review`; do **not** advance to `gate-b` / `build` |

**04a unpaid / dirty** / **04a ok** — Definitions SoT: [derive-next-defs-pre.md](derive-next-defs-pre.md).

## Code review (`05-review-log.md`)

Adv + Quality section Results: `clean` \| `needs fix` \| `pending`.  
**Review clean** — [derive-next-defs-post.md](derive-next-defs-post.md). File-top alone never pays.

## Lenses / Merged

Result-bearing = `clean` \| `needs fix`. Missing/`pending` = unpaid.  
**Lenses clean** / **Lenses dirty** / Prefer — name+link only ([derive-next-defs-post.md](derive-next-defs-post.md) · [derive-next-post.md](derive-next-post.md)).

## Tests (`06`)

`success` \| `fail` \| `pending`. Smoke section + **Smoke source**.

## Parent habit

On verify-pass: set Last Verify, Last verify-pass at (ISO-8601 Run-log local wall time), Last verify settle-gen — [verify.md](verify.md).

## Design (`03`)

| Token | Meaning |
|-------|---------|
| `pending` | Unpaid — **not** Design present |
| `done` | Paying — **Design present** = file exists **and** Result `done` ([derive-next-defs-pre.md](derive-next-defs-pre.md)) |

## Artifact-presence stages

`design-phase` advances on **Done when**: design artifacts **and** Grill closed (Notes `grill-skip` **or** Result `frontier-empty` only) — not files alone.  
`ideation` advances when ¬ **ideation unpaid** (Notes `ideation-confirmed` + provenance **or** Notes `ideation-skip` — parent after Parent-relay **or** labeled solo after AskQuestion; [brainstorm.md](brainstorm.md) · [hitl.md](hitl.md) · [solo-entry.md](solo-entry.md)). Prefer while unpaid — name+link ([derive-next-defs-pre.md](derive-next-defs-pre.md) · [derive-next-pre.md](derive-next-pre.md)).
