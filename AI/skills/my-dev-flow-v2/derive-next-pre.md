# Derive next — Pre-Build

Open with [derive-next.md](derive-next.md) (Definitions + selector). Use **only** when selector says **Pre-Build** — including Notes `design-backloop`, Notes `design-stale`, or when verify-pass is **not** fresh for the current Gate B settlement ([derive-next.md](derive-next.md) Pre / Post selector).

## Pre-Build (Mode full)

**First-match:** scan top→bottom; stop at the first matching row.

| State | Expected Next |
|-------|---------------|
| No `01-idea` | `ideation` |
| `01a` missing or ≠ `ok` (see **`01a` file**) | `gate-a` (or `ideation-update` if Fix ask) |
| `01a` ok, no skim | `skim` |
| Notes `design-stale` (Mode full; after Gate A / skim paid above) | Prefer first unpaid among `analyze` → `grill` → `design` only. Mode-simple `analyze`/`grill`/`03`/`03a*` are **unpaid** under Notes `design-stale` until Mode-full rewrite — do **not** treat prior Mode-simple Analyze/Grill as paid. Prior overall **and** isolated `03a*` **clean** are unpaid (parent invalidates on Upgrade — [step-0.md](step-0.md)). **While Notes `design-stale`:** do **not** match Grill open / paid Mode-simple analysis below — stay on this Prefer until rewrite; do **not** Prefer API∥DB / `design-review` / `gate-b` / `build`. **Parent clears** Notes `design-stale` only after Last stage `design` **and** `03-design.md` rewrite for Mode full — then Prefer re-run API∥DB while **Isolated API/DB unpaid** (**even if files exist**) → `design-review` until Mode-full overall **`clean`** (**Design clean** unpaid until that re-clean) ([step-0.md](step-0.md) Mid-run · [handoffs.md](handoffs.md) design After) |
| No `02-analysis` | `analyze` (clarity first) |
| Grill open | `grill` |
| Notes `design-backloop` **and** (`design-update` unpaid **or** design-review not clean) | Prefer unpaid `design-update`; else isolated `api-contract-review` if **Isolated API/DB unpaid** for API (Has API=yes **and** not Notes `tiny-contract-tweak` — Prefer even if file exists when Result unpaid/pending); `db-design-review` if **Isolated API/DB unpaid** for DB (Has DB=yes **and** not Notes `tiny-contract-tweak`); else Has=no / tiny → N/A (do **not** Prefer that stage); else `design-review`. Prior overall **and** isolated `03a*` **clean** are unpaid until fresh re-clean (parent invalidates on Amend — [design-backloop.md](design-backloop.md)). Do **not** Prefer `gate-b` / `build` on stale clean |
| No `03-design` | `design` |
| Any `03a*` Result **needs update** | `design-update` |
| Design present, design-review not clean (**and** no Notes `design-stale`) | isolated `api-contract-review` if **Isolated API/DB unpaid** for API (Has API=yes **and** not Notes `tiny-contract-tweak` — Prefer even if file exists when Result unpaid/pending); `db-design-review` if **Isolated API/DB unpaid** for DB (Has DB=yes **and** not Notes `tiny-contract-tweak`); else Has=no / tiny → N/A (do **not** Prefer that stage); else `design-review`. **API∥DB parallel (Mode full, both Has yes, not tiny):** while both **Isolated API/DB unpaid** → Expected Next = `api\|db` (or first Prefer + Pending parallel `api\|db` authorizes both same turn); on resume Prefer only the unpaid/pending sibling; clear Pending parallel when both paid (`clean`\|`skipped`) ([lenses.md](lenses.md) · [artifacts/00-run.md](artifacts/00-run.md)) |
| Design clean, planned tests, no 04a / skip note | `tdd-review` |
| Design clean, 04a Result **needs more tests** (dirty / unpaid until **clean**) | `tdd-review` — do **not** advance to `gate-b` |
| Design clean (+04a Result **clean** or Notes `04a skipped`), Gate B not settled | `gate-b` |
| Notes `design-backloop` **and** Design clean (+04a Result **clean** or Notes `04a skipped`) **and** Gate B settled | Parent clears Notes `design-backloop` **same turn** as Gate B re-settle (fail-closed — [design-backloop.md](design-backloop.md)); then `build` |
| Gate B settled, ready to code (**and** no Notes `design-backloop`) | `build` |

**Fail-closed:** never past Gate A while accepted `01a` ≠ `ok`. **Design clean** requires overall **`clean`** **and** isolated paid when required — overall token alone + **Isolated API/DB unpaid** → **design-review not clean** (Prefer API∥DB / `design-review`, not `gate-b` / `build`). Has API/DB newly yes (not tiny): invalidate overall or Prefer re-run — [lenses.md](lenses.md) · [examples/drop-skip-review-api-flip.md](examples/drop-skip-review-api-flip.md).

## Pre-Build (Mode simple)

**First-match:** scan top→bottom; stop at the first matching row.

| State | Expected Next |
|-------|---------------|
| No `01-idea` | bootstrap `01-idea` ([step-0.md](step-0.md) · [handoffs.md](handoffs.md)) then `design-phase` |
| Grill open **and** (design artifacts present **or** `02b-grill.md` exists with Result **`needs-round`**) | Expected Next always **`grill`** (Task `grill` **or** parent apply into `02b`; card Next stays `grill` until Grill closed). Do **not** Prefer `design-phase` / verify / Gate B / Build — [grill.md](grill.md). Prefer `design-phase` on Grill open **only** for true cold start: no `02b` **needs-round** **and** no design artifacts → fall through to **No design artifacts** |
| Notes `design-backloop` **and** (`design-update` unpaid **or** verify not clean) | Prefer unpaid `design-update`; else `design-verify-phase`. Prior overall **and** isolated `03a*` **clean** are unpaid until fresh re-clean (parent invalidates on Amend — [design-backloop.md](design-backloop.md)). Do **not** Prefer `gate-b` / `build` on stale clean |
| No design artifacts | `design-phase` |
| Any `03a*` Result **needs update** | `design-update` |
| Design present, verify not clean | `design-verify-phase` |
| Verify clean, planned tests, no 04a / skip note | `tdd-review` |
| Verify clean, 04a Result **needs more tests** (dirty / unpaid until **clean**) | `tdd-review` — do **not** advance to `gate-b` |
| Verify clean (+04a Result **clean** or Notes `04a skipped`), Gate B not settled | `gate-b` — **auto:** parent writes design-scoped `gate-b auto — <HH:MM>` (or digest) after current **Design clean** / **Verify clean** (Design-clean time) same turn, then Prefer `build` (no user wait) — [gate-b.md](gate-b.md) · [derive-next.md](derive-next.md) Gate B settled · Settle freshness |
| Notes `design-backloop` **and** Verify clean (+04a Result **clean** or Notes `04a skipped`) **and** Gate B settled | Parent clears Notes `design-backloop` **same turn** as Gate B re-settle (fail-closed — [design-backloop.md](design-backloop.md)); then `build` |
| Gate B settled, ready to code (**and** no Notes `design-backloop`) | `build` |

**Fail-closed (Mode simple):** Auto Gate B without the durable token is **not** settled (Prefer `gate-b`). **Verify clean** requires overall **`clean`** **and** isolated paid when required — overall token alone + **Isolated API/DB unpaid** → **verify not clean** (Prefer `design-verify-phase`, not `gate-b` / `build`). Has API/DB newly yes (not tiny): invalidate overall or Prefer re-run — [lenses.md](lenses.md) · [examples/drop-skip-review-api-flip.md](examples/drop-skip-review-api-flip.md).
