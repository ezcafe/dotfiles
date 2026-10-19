# Derive next (Expected Next SoT)

**Load:** this file (Definitions + Unsafe jumps) **plus** the matching half — [derive-next-pre.md](derive-next-pre.md) or [derive-next-post.md](derive-next-post.md) — before each Task. First-match wins.

## Selector Pre vs Post

| Condition | Half |
|-----------|------|
| Notes `design-backloop` or `design-stale` | **Pre-Build** — open [derive-next-pre.md](derive-next-pre.md) |
| No Build verify-pass for **current** Gate B settle gen | **Pre-Build** — open [derive-next-pre.md](derive-next-pre.md) |
| Build verify-pass with **Last verify settle-gen** == current settle gen | **Post-Build** — open [derive-next-post.md](derive-next-post.md) |

On verify-pass, parent sets **Last verify settle-gen** = current **Gate B settle gen**.

## Definitions

| Term | Meaning |
|------|---------|
| **unpaid Gate A** | Mode full: `01a` missing **or** Result ≠ `ok` ([results.md](results.md)) |
| **unpaid skim** | Mode full: Gate A paid (`01a` Result `ok`) **and** (`02-skim` missing **or** Result ≠ `done`) ([results.md](results.md)) |
| **ideation unpaid** | ¬Notes `ideation-skip` **and** ¬Notes `ideation-confirmed` ([brainstorm.md](brainstorm.md)). Paid = Notes `ideation-confirmed` + provenance `ideation-confirmed` (`user:"…" ≥12 chars`) **or** Notes `ideation-skip` / preferred `ideation skipped — <reason>` (parent-only + provenance). Stages return `candidate ideation-confirmed` / `candidate ideation-skip` only ([hitl.md](hitl.md); no Prefer on waive) |
| **Analyze unpaid** | Mode full: `02-analysis` missing **or** Result ≠ `done` ([results.md](results.md)) |
| **Analyze paid** | `02-analysis` exists **and** Result **`done`** (mirror Design present — file alone / Result `pending` never pays) |
| **Design present** | `03-design.md` exists **and** Result **`done`** (paying token — Step 0 seeds **only** `00-run.md`; never treat a pre-seeded stub / Result `pending` as present — [step-0.md](step-0.md)) |
| **Design clean** / **Verify clean** | Overall `03a` **clean** **and** Isolated API/DB paid when required (`clean`\|`skipped`; Has ∈ {yes, unknown} ∧ ¬tiny / ¬Notes `tiny-contract-tweak` → file required; Mode simple: `design-verify-phase` writes those files). Notes `tiny-contract-tweak` → Isolated N/A skipped ([lenses.md](lenses.md)). **Mode simple:** Verify clean ≡ Design clean (same predicate) |
| **design-review not clean** | ¬ Design clean (incl. Isolated unpaid) |
| **backloop rewrite unpaid** | Notes `design-backloop` **and** no Run-log paying line `design-update — settle-gen:<N>` for **current** Gate B settle gen (after Notes set). Parent appends that line when `design-update` completes |
| **design-stale unpaid** | Notes `design-stale` until Notes clear after Mode-full `design` + `03` rewrite — do **not** require design-update Run-log ([step-0.md](step-0.md)). Under Notes: Prefer **Grill open** → `grill` first, then unpaid **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale** |
| **design unpaid under design-stale** | Notes `design-stale` ∧ ¬ **Grill open** → Prefer `design` rewrite **even if** `03`+Result `done` exists, until Notes clear (Mid-run Upgrade also sets `03` → `pending` — [step-0.md](step-0.md)). Never Prefer `design` while Grill open (deadlock ban) |
| **design-update paid** | Run-log has `design-update — settle-gen:<N>` for current settle gen (pays **backloop rewrite**). Cleared when settle gen bumps / Notes re-set |
| **design-update unpaid** | Any `03a*` Result **`needs update`**, **or** **backloop rewrite unpaid** |
| **Isolated API/DB unpaid** | Has ∈ {yes, unknown} (not tiny / ¬Notes `tiny-contract-tweak`) and file missing **or** Result ≠ `clean` (incl. `pending`) — Prefer re-run **even if files exist**. Mode simple: Prefer `design-verify-phase` (that stage pays Isolated) — not Isolated Prefer stages |
| **Grill unpaid** | no `02b` **and** ¬Notes `grill-skip` ([grill.md](grill.md)). Missing file only — Step 0 does not seed `02b` |
| **Grill open** | ¬Notes `grill-skip` **and** (no `02b` **or** `02b` Result ≠ `frontier-empty`) — Notes `grill-skip` closes even if `02b` is `pending`/`needs-round`; Result `skipped` does **not** close (invent-waive ban); template `pending` alone does **not** close |
| **Grill closed** | ¬ **Grill open** (Notes `grill-skip` parent-only + provenance **or** Result `frontier-empty` only) |
| **design artifacts** | `02-analysis` + `03` + `04` present (ignore Grill). **Cold start** = none of {`02-analysis`, `03`, `04`} on disk — ¬(all three present) ≠ cold start (partial set = mid-run / incomplete Design) |
| **planned tests present** | `04-tasks.md` has a **Planned tests** (or equivalent cases) section with ≥1 named test case. Empty / `N/A` / missing section → **not** present (no Prefer `tdd-review`; optional Notes `04a skipped — no planned test cases` — parent-only) |
| **04a unpaid / dirty** | **planned tests present** **and** ¬Notes `04a skipped` **and** (`04a` missing **or** Result ∉ {`clean`}) — incl. Result `pending` \| `needs more tests`. Prefer `tdd-review` **only** when this holds. Waiver = Notes `04a skipped` (parent-only named yes — [hitl.md](hitl.md); no Prefer). ¬ **planned tests present** → **not** unpaid (vacuous — no Prefer `tdd-review`) |
| **04a ok** | ¬ **04a unpaid / dirty** — i.e. ¬ planned tests present **or** Notes `04a skipped` **or** `04a` Result `clean`. Shorthand for Prefer `gate-b` / preflight Before Build / design-backloop clear (clear also needs **Gate B settled post-Notes**) |
| **Review clean** | Adv + Quality section Results both **clean** (file-top alone never pays) |
| **code-review unpaid** | Planned Adv/Quality missing **or** section Result missing/`pending` (not `needs fix`) |
| **Review needs fix** | Adv and/or Quality section Result = `needs fix` |
| **missing required api/db** | Has API/DB ∈ {yes, unknown} ∧ ¬tiny / ¬Notes `tiny-contract-tweak` ∧ Lens plan lacks matching `api`/`db` (incl. plan=`none`) — Prefer `finalize-lens-plan` ([derive-next-post.md](derive-next-post.md) · [lenses.md](lenses.md)) |
| **Lens plan unpaid** | Lens plan ≠ `none` **and** (planned `05-lens-*` missing **or** Result missing/`pending`) — incl. Result `pending`. Result-bearing = `clean`\|`needs fix` only. Prefer unpaid `lens-*` **only** when this holds. Lens plan `none` → **not** unpaid; **Lenses clean** vacuous only when ¬ **missing required api/db** (else Prefer `finalize-lens-plan`) |
| **Lenses dirty** | Lens plan ≠ `none` **and** (Lens plan unpaid **or** any planned / Merged Result = `needs fix`). **Dual-false notes** (clean=false ∧ dirty=false — intentional): (1) plan=`none` ∧ **missing required api/db** → Prefer / unsafe-jump owner is **missing required api/db** → `finalize-lens-plan`, **not** Lenses dirty; (2) plan 2+ ∧ planned lenses **clean** ∧ **Merged unpaid** → Prefer `merge-findings` owns it ([derive-next-post.md](derive-next-post.md)); unsafe also bans `test-*` / `gate-c` / `merge` while ¬ **Lenses clean** |
| **Lenses clean** | (Lens plan `none` **and** ¬ **missing required api/db**) **or** (every planned `05-lens-*` **clean** **and** (plan 2+ → Merged **clean**)). Plan=`none` with **missing required api/db** → **not** clean. Plan 2+ with Merged unpaid/pending → **not** clean. **Dual-false notes:** same two cases as **Lenses dirty** — Prefer owners `finalize-lens-plan` / `merge-findings`; do **not** Prefer `test-*` / `gate-c` / `merge` while ¬ clean |
| **Smoke unpaid** | E1 or skip-review: unpaid until `Smoke source: Smoke-Task`. Lite: Build-writes-Smoke may pay |
| **Smoke fail** | Independent Smoke (or `06` smoke) Result **fail** / **smoke-fail**. Prefer-re-smoke eligible = Last stage `fix-tests` + verify-pass; Prefer-re-smoke proceed only when Smoke unpaid∨fail ∧ Prefer-re-smoke eligible (same Prefer as unpaid — not eligible alone when Smoke paid/success) |
| **Tests success** | ≡ Gate C test bar ([gate-c.md](gate-c.md)) |
| **Tests unpaid** | Profile ≠ skip-review **and** ¬(`06` success **and** path matches profile) |
| **skip-review Prefer paid** | Legal skip-review **and** Tests success (verify-pass + `Smoke source: Smoke-Task` + escape Notes↔provenance + stale cleared — [gate-c.md](gate-c.md) · [verify.md](verify.md)) |
| **Gate C unpaid** | approved `none`/empty **or** remaining named actions unpaid |
| **Gate B settled** | Token gen == current settle gen ([gate-b.md](gate-b.md)) |
| **Gate B settled post-Notes** | Notes `design-backloop` **and** durable settle token for **current** settle gen **and** a Run-log line for that settle that appears **after** the Notes `design-backloop` line (or ISO stamp proving after — [design-backloop.md](design-backloop.md) · [gate-b.md](gate-b.md) Prefer after settle). Pre-Notes / uncleared settle does **not** count even if gen still matches — Prefer `gate-b`, not clear→`build` (incl. Mode simple auto same turn). Parent alone clears Notes `design-backloop` ([hitl.md](hitl.md)) |

## Unsafe jumps (never Prefer / launch)

- Illegal Mode×profile  
- `gate-a` / `skim` / `analyze` / `design` / `design-phase` while **ideation unpaid** (Prefer `ideation` first — both Modes; paid = Notes `ideation-confirmed`|`ideation-skip` + provenance — [brainstorm.md](brainstorm.md))  
- Build / Post-Build while `design-stale` or `design-backloop` (until clear rules met)  
- Isolated / `design-review` / `design-verify-phase` / `design-update` while Notes `design-stale` (until Mode-full `design` + `03` rewrite clears Notes — Prefer **Grill open** → `grill` first, then unpaid among **Analyze unpaid** → **Grill unpaid** → **design unpaid under design-stale**)  
- `design` / `design-review` / `design-verify-phase` / `design-update` / `gate-b` / `build` while **Grill open** (both Modes — incl. under Notes `design-stale` / `design-backloop`; never Prefer `design` unpaid under design-stale until Grill closed; Prefer `grill` before `design-update`)  
- `design-phase` while **Grill open** ∧ ¬ cold-start carve (carve = none of {`02-analysis`, `03`, `04`} on disk ∧ (**Grill unpaid** ∨ **Grill closed**); mid-open Prefer `grill` for full **Grill open**, not only artifacts∨`needs-round`|`pending` — [grill.md](grill.md))  
- Isolated / `design-review` / `design-verify-phase` while ¬ Design present (Mode full Prefer `design`; Mode simple Prefer `design-phase` per cold start carve — [grill.md](grill.md); file alone / Result `pending` never pays)  
- Isolated / `design-review` / `design-verify-phase` while design-update unpaid (**backloop rewrite unpaid** **or** any `03a*` **`needs update`**) — Prefer **Grill open** → `grill` first; else Prefer `design-update` first  
- `gate-b` / `build` while **04a unpaid / dirty** (requires **planned tests present**; missing / `pending` / `needs more tests` alone when ¬ planned tests → **04a ok**)  
- `gate-c` / `merge` while ¬ Tests success or unpaid stale Notes  
- `test-*` / `gate-c` / `merge` while **Lenses dirty** **or** ¬ **Lenses clean** (covers Merged-unpaid dual-false when plan 2+ — Prefer `merge-findings`; plan=`none` dual-false → **missing required api/db** row)  
- Prefer-re-smoke / unpaid `smoke` / Adv / `code-review-phase` / `lens-*` / `test-*` / `gate-c` / `merge` while **missing required api/db** (Prefer `finalize-lens-plan` first — before Smoke **and** before Adv — even if Lens plan=`none`)  
- `merge` unless Tests success **and** **Lenses clean** **and** `merge` ∈ Gate C approved  
- Stages while Status `done` \| `stopped`  
- Post-Build while verify settle-gen ≠ current Gate B settle gen  

`card-override` cannot waive these.

## Halves

| Half | File |
|------|------|
| Pre-Build | [derive-next-pre.md](derive-next-pre.md) |
| Post-Build | [derive-next-post.md](derive-next-post.md) |
