# Derive next (agent checklist)

Given Mode, Review profile, and artifacts under `.my-docs/workflow/<slug>/`, compute **expected Next**. If card Next disagrees → fix card or `card-override` + provenance ([preflight.md](preflight.md)). **`card-override` carve:** only for Next↔derive mismatch — **never** to skip unpaid `test-*` / Gate C test bar when Review profile is **lite** or **full** ([gate-c.md](gate-c.md)).

## Gate B settled

| HITL Gate B | Settled when |
|-------------|--------------|
| **blocking** | **Gate B approved** set + provenance `gate-b-approved` |
| **async-notify** | durable **Build armed: yes** + Run log arm HH:MM later than digest + Notes `async-gap-pending — <digest-HH:MM>` ([gate-b.md](gate-b.md)) |
| **auto** | digest posted (or N/A) + `Gate B veto: none` — **Gate B approved** may stay `none` |

## Pre-Build (Mode full)

**First-match:** scan top→bottom; stop at the first matching row.

| State | Expected Next |
|-------|---------------|
| No `01-idea` | `ideation` |
| `01a` missing or ≠ `ok` | `gate-a` (or `ideation-update` if Fix ask) |
| `01a` ok, no skim | `skim` |
| No `02-analysis` | `analyze` (clarity first) |
| Grill open / needs-round | `grill` |
| No `03-design` | `design` |
| Any `03a*` Result **needs update** | `design-update` |
| Design present, review not clean | isolated `api-contract-review` / `db-design-review` if missing; else `design-review` |
| Design clean, planned tests, no 04a / skip note | `tdd-review` |
| Design clean (+04a Result **clean** or Notes `04a skipped`), Gate B not settled | `gate-b` |
| Gate B settled, ready to code | `build` |

**Fail-closed:** never past Gate A while `01a` ≠ `ok`.

## Pre-Build (Mode simple)

**First-match:** scan top→bottom; stop at the first matching row.

| State | Expected Next |
|-------|---------------|
| No `01-idea` | bootstrap idea then `design-phase` |
| No design bundle | `design-phase` |
| Any `03a*` Result **needs update** | `design-update` |
| Design present, verify not clean | `design-verify-phase` |
| Verify clean, planned tests, no 04a / skip note | `tdd-review` |
| Verify clean (+04a Result **clean** or Notes `04a skipped`), Gate B not settled | `gate-b` |
| Gate B settled, ready to code | `build` |

## Post-Build

**First-match:** scan top→bottom; stop at the first matching row.

**Lenses paid** (unpaid-check only — [lenses.md](lenses.md)):

| Lens plan | Paid when |
|-----------|-----------|
| **2+** | `05` Merged lenses Result **`clean`** \| **`needs fix`** recorded |
| **1** | that planned `05-lens-*` Result **`clean`** \| **`needs fix`** |
| **`none`** | N/A |

**`needs fix` is paid** for unpaid-check (do not re-launch lenses while Fix is pending). **Exception:** after `fix-review` **verify-pass** for Fix Mode `merged-lenses` or plan-1 lens Fix, treat planned `05-lens-*` + Merged as **unpaid** until Result is **`clean`** again (Prefer re-lens below).

**Lenses clean** (required before `test-*` / `gate-c`): Merged (plan **2+**) or planned `05-lens-*` (plan **1**) Result **`clean`** only — not unpaid/pending and not `needs fix`.

| State | Expected Next |
|-------|---------------|
| Notes `design-backloop` | Prefer: `design-update` ([design-backloop.md](design-backloop.md)) |
| Last Verify ≠ verify-pass at Build/Fix | same Fix stage or Decision N |
| Last stage `fix-tests` + Last Verify = **verify-pass** | Prefer: `smoke` if Smoke unpaid/fail (or Notes re-smoke); else `test-full` / `test-lite` if test-fail unpaid (or Notes re-test); else continue table below. **Do not** stay on `fix-tests`. |
| Last stage `fix-review` + Last Verify = **verify-pass** | Prefer: re-run **dirty** verifier by Fix Mode / profile — (1) Mode `code-review-phase` (lite) → `code-review-phase`; (2) Mode `adversarial-tests` \| `quality` (full) → that section; both dirty/unclear → `adversarial` then `quality`; (3) Mode `merged-lenses` **or** plan-1 lens Fix → mark planned `05-lens-*` + Merged **unpaid**/pending → Prefer re-run dirty `lens-*` (or all planned) → `merge-findings` if 2+. If already clean → else continue table below. **Do not** stay on `fix-review`. Examples: [fix-review-rereview.md](examples/fix-review-rereview.md) · [fix-review-relens.md](examples/fix-review-relens.md). |
| Smoke fail / test fail (**only while** Last Verify ≠ verify-pass **or** Last stage ≠ `fix-tests` after verify-pass) | `fix-tests` (wins over skip-review Prefer and Smoke unpaid; re-smoke / re-test only after verify-pass — [verify.md](verify.md)) |
| **Legal skip-review** (after Build verify-pass; **not** smoke-fail / test-fail) | Ordered recovery ([verify.md](verify.md) Skip-review + Smoke): Prefer unpaid Notes `smoke re-run` → `smoke`; Prefer paid — Notes `smoke-pass (re-run)` + provenance `smoke-pass-rerun` → **`gate-c`** (do **not** else-drop to lite); else **peer alternatives** — drop skip-review → lite (`code-review-phase` → lenses → `merge-findings` if 2+ → `test-lite`) **or** Gate C escape+provenance ([gate-c.md](gate-c.md)). **Do not** match review/test rows below while profile stays skip-review. |
| Mode full + profile full, Smoke unpaid (**not** smoke-fail) | `smoke` (Notes `smoke re-run`) |
| Notes `review-stale` | Prefer: unpaid review (next verifier by profile) — prior clean not paid ([verify.md](verify.md) Stale) |
| Notes `test-stale` | Prefer: unpaid `test-full` / `test-lite` — prior success not paid ([verify.md](verify.md) Stale) |
| Review needs fix (**profile ≠ skip-review**; **only while** Last stage ≠ `fix-review` after verify-pass **or** 05 still needs fix **and** Last Verify ≠ verify-pass from Fix) | `fix-review` |
| Profile full, review unpaid (**≠ skip-review**) | next unpaid in order: `adversarial` then `quality`; then lenses → `merge-findings` if 2+ |
| Profile lite, review unpaid (**≠ skip-review**) | `code-review-phase` (does **not** pay lenses) |
| Review clean, Lens plan unpaid (**profile ≠ skip-review**) | parent launches unpaid `lens-*` (parallel when 2+; serial only when parent chose serial) → wait siblings → `merge-findings` if 2+ (never treat in-band notes as paid) |
| Lens plan **2+**, all planned `05-lens-*` exist, Merged lenses unpaid/pending (**profile ≠ skip-review**) | Prefer: `merge-findings` |
| Review clean (+ lenses **clean** / plan `none`), tests unpaid (**profile ≠ skip-review**) | `test-full` (profile full) or `test-lite` (lite) |
| Tests success, Gate C unpaid (**profile ≠ skip-review**) | `gate-c` |
| Gate C approved set | `merge` |

## Unsafe jumps (do-not-launch)

Always unsafe (no `card-override` waiver):

- `merge` / `gate-c` while tests unpaid under profile **lite** or **full** — require `06` Result **success** + Test path last run `lite`|`full` ([gate-c.md](gate-c.md)). **`card-override` never** waives this bar.
- Legal **skip-review** Gate C only when test bar / escape+provenance met ([gate-c.md](gate-c.md)): Notes↔provenance (`smoke-pass-rerun` / `docs-only` / `smoke-waive` / `gate-c-test-override`). Still no `card-override` for unpaid lite/full tests.
- `test-full` / `test-lite` / `gate-c` while Lens plan **2+** or **1** and lenses not **clean** — unpaid/pending (2+) → Prefer `merge-findings`; unpaid (1) → Prefer that `lens-*`; **`needs fix`** → `fix-review` (or Prefer re-lens after Fix verify-pass) ([lenses.md](lenses.md) · [preflight.md](preflight.md))
- Review / test / `gate-c` / `merge` / `build` while Notes `design-backloop`
- `gate-c` / `merge` while Notes `review-stale` or `test-stale`
- `build` while design not clean or Gate B unsettled
- Review/test stages while still pre-Build
- Profile-full-only stages (`adversarial`, `quality`, `test-full`) while profile lite (and inverse) — reclassify; do **not** unlock with `card-override`
- `test-full` / `test-lite` / `code-review-phase` / `adversarial` / `quality` while Review profile is still **skip-review**

`card-override` + provenance applies **only** when card Next ≠ derive expected Next (mismatch carve) — not the bullets above.

## Max rounds

If Round / Verify attempts hit caps in [decisions.md](decisions.md) → Decision N; do not launch.
