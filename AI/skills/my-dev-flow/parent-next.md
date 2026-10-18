# Parent next (discovery)

Given `00-run.md` Orchestrator card **Stage id** / **Next step**, open the **Open (1–2)** row below + handoff (+ clarity file when Next ∈ clarity stages). Full per-stage set: [Load budget](step-0.md#load-budget). Do **not** re-read orchestrator [SKILL.md](SKILL.md).

**Also (required habit):** before every Task, follow the [orchestrator-rules.md](orchestrator-rules.md) **Pre-launch checklist card**, then run `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (resolve `{my-dev-flow}` per [skills-path.md](skills-path.md)). Derive computes expected next from Mode/profile + artifacts. Phase gates **auto** from card Next (design-review* → `--before-design-review`; Adv / `code-review-phase` → `--before-code-review`; `build` → `--before-build`; `merge` → `--before-merge`). Soft mismatches (peer/parallel / minor reorder) stay warn. After design **clean**, derive returns `tdd-review` until `04a` exists or Notes `04a skipped` ([lenses.md](lenses.md)); `--next` / `--before-build` require `03a` Result **clean** before Build.

**Unsafe** card vs derived → **error** + `do-not-launch` (exit **1**) unless Notes `card-override — <reason>` **and** `provenance — card-override — user: "…"` (+ optional Decision N):

| Card Next | Derived / state | Notes |
|-----------|-----------------|-------|
| `merge` | earlier than merge | |
| `build` | design not clean / pre-Build | |
| `code-review-phase` / `adversarial` / `quality` / `test-*` / `fix-*` / `smoke` / `gate-c` | still pre-Build or `build` | |
| `test-*` / `fix-tests` / `gate-c` / `merge` (post-Build) | still in review (`adversarial` / `quality` / `code-review-phase` / `lens-*` / `merge-findings` / `fix-review`) | skip-review profile exempt |
| `quality` | `adversarial` | |
| `smoke` / `fix-tests` | review-entry | OK with Notes `smoke re-run` / Fix ask |
| `lens-*` / `merge-findings` | still `adversarial` / `quality` / `code-review-phase` / `fix-review` (pre-lens) | OK when derived is that lens (unpaid Lens plan) or card-override + provenance |

**Gate A fail-closed (Mode full):** `--next` emits `handoff: do-not-launch` when card Next is past Gate A (`skim`, `analyze`, …) while `01a` Result ≠ `ok` — same rule as `--derive` ([stages.md](stages.md) · [results.md](results.md)).

**Handoff command (canonical):** `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` (optional `--slug`, `--skill-root`) — prints base block + R/W row + **Description** from the Task description map. Paste that output into the Orchestrator card **Task description**.

**Before launch (clarity-check — required at design/code boundaries per [invariants.md](invariants.md) checklist; not a Task / no handoffs id):**

| Boundary | Open |
|----------|------|
| Before Analyze / Grill / Design (Mode **full** standalone stages) | [../my-dev-flow-design/stages/clarity-check.md](../my-dev-flow-design/stages/clarity-check.md) — full-mode gates |
| Before `design-phase` (Mode **simple** only) | Same file — **design-phase entry** section only (`01-idea` + Mode simple; do **not** require `02-analysis` / `02b` yet) |
| Before TDD review / Build / Fix / Merge | [../my-dev-flow-code/stages/clarity-check.md](../my-dev-flow-code/stages/clarity-check.md) |

**Intentional skip:** `design-update` is **not** a clarity boundary (no `clarity-check ok — design-update`; not in lint `CLARITY_CHECK_STAGES`). Entry is gated by `03a` Fix ask or Notes `design-backloop` + derive/handoff — repair scoped work under existing design clarity.

If clarity-check fails → ask the user; do **not** launch the Task.

**Log token:** after a passing clarity-check, add to Notes or Run log: `clarity-check ok — <boundary>` where `<boundary>` is the stage id (e.g. `design-phase`, `build`, `fix-review`, `merge`).

| Next class | Lint rule |
|------------|-----------|
| **Design boundaries** (`design-phase`, `analyze`, `grill`, `design`) | **Boundary-matched:** must have `clarity-check ok — <exact Next>` (e.g. Next `analyze` needs `clarity-check ok — analyze`; a prior `design-phase` token does **not** unlock later Analyze/Grill/Design). Parent still opens the clarity file for content checks (Problem map / What-Why-How). Clarity tokens ≠ stage gates (derive/lint still enforce e.g. open Grill blocks Design). |
| **High-risk** (`tdd-review`, `build`, `fix-review`, `fix-tests`, `merge`) | **Boundary-matched:** must have `clarity-check ok — <exact Next>` (e.g. Next `build` needs `clarity-check ok — build`) |

Fail-closed: Lint **errors** / `--next` → `do-not-launch` when the rule above is not met ([invariants.md](invariants.md)).

| Stage id / Next | Open (1–2) | Handoff |
|-----------------|------------|---------|
| (Step 0 / classify) | [step-0.md](step-0.md) · [artifacts/00-run.md](artifacts/00-run.md) | — seed + `lint-run.py` |
| `ideation` | [../my-dev-flow-design/stages/ideation.md](../my-dev-flow-design/stages/ideation.md) · design [SKILL.md](../my-dev-flow-design/SKILL.md) once | `python3 {my-dev-flow}/scripts/handoff-for.py ideation` |
| `gate-a` | [../my-dev-flow-design/stages/gate-a.md](../my-dev-flow-design/stages/gate-a.md) | `python3 {my-dev-flow}/scripts/handoff-for.py gate-a` |
| `ideation-update` | [../my-dev-flow-design/stages/ideation-update.md](../my-dev-flow-design/stages/ideation-update.md) | `python3 {my-dev-flow}/scripts/handoff-for.py ideation-update` |
| `skim` | [../my-dev-flow-design/stages/skim.md](../my-dev-flow-design/stages/skim.md) | `python3 {my-dev-flow}/scripts/handoff-for.py skim` |
| `analyze` | [../my-dev-flow-design/stages/analyze.md](../my-dev-flow-design/stages/analyze.md) | `python3 {my-dev-flow}/scripts/handoff-for.py analyze` |
| `grill` | [grill.md](grill.md) · [../my-dev-flow-design/stages/grill.md](../my-dev-flow-design/stages/grill.md) | `python3 {my-dev-flow}/scripts/handoff-for.py grill` |
| `design` | [../my-dev-flow-design/stages/design.md](../my-dev-flow-design/stages/design.md) | `python3 {my-dev-flow}/scripts/handoff-for.py design` |
| `design-phase` | [../my-dev-flow-design/stages/design-phase.md](../my-dev-flow-design/stages/design-phase.md) | `python3 {my-dev-flow}/scripts/handoff-for.py design-phase` |
| `design-update` | [../my-dev-flow-design/stages/design-update.md](../my-dev-flow-design/stages/design-update.md) | `python3 {my-dev-flow}/scripts/handoff-for.py design-update` |
| `api-contract-review` | [../my-dev-flow-design-review/stages/api-contract-review.md](../my-dev-flow-design-review/stages/api-contract-review.md) | `python3 {my-dev-flow}/scripts/handoff-for.py api-contract-review` |
| `db-design-review` | [../my-dev-flow-design-review/stages/db-design-review.md](../my-dev-flow-design-review/stages/db-design-review.md) | `python3 {my-dev-flow}/scripts/handoff-for.py db-design-review` |
| `design-review` | [../my-dev-flow-design-review/stages/design-review.md](../my-dev-flow-design-review/stages/design-review.md) | `python3 {my-dev-flow}/scripts/handoff-for.py design-review` |
| `design-verify-phase` | [../my-dev-flow-design-review/stages/design-verify-phase.md](../my-dev-flow-design-review/stages/design-verify-phase.md) | `python3 {my-dev-flow}/scripts/handoff-for.py design-verify-phase` |
| `tdd-review` | [../my-dev-flow-code/stages/tdd-review.md](../my-dev-flow-code/stages/tdd-review.md) · [verify-and-fix.md](verify-and-fix.md) | `python3 {my-dev-flow}/scripts/handoff-for.py tdd-review` |
| `gate-b` | [hitl.md](hitl.md) · card Next | digest only — set **Gate B approved** when blocking **+ provenance**; no handoff Task |
| `build` (armed / approved) | [../my-dev-flow-code/stages/build.md](../my-dev-flow-code/stages/build.md) · [verify-and-fix.md](verify-and-fix.md) · [hitl.md](hitl.md) if async gap | `python3 {my-dev-flow}/scripts/handoff-for.py build` |
| `build` (async gap, not armed) | [hitl.md](hitl.md) — set **Build armed** on this resume turn; do not launch yet if veto pending | — |
| `build` (blocking, Gate B approved none) | [hitl.md](hitl.md) — set **Gate B approved** yes / named pick **+ provenance**; do not launch | — |
| `smoke` | [../my-dev-flow-test/stages/smoke.md](../my-dev-flow-test/stages/smoke.md) | `python3 {my-dev-flow}/scripts/handoff-for.py smoke` |
| `code-review-phase` | [../my-dev-flow-review/stages/code-review-phase.md](../my-dev-flow-review/stages/code-review-phase.md) · Lens plan ([lenses.md](lenses.md)) | `python3 {my-dev-flow}/scripts/handoff-for.py code-review-phase` |
| `adversarial` | [../my-dev-flow-review/stages/adversarial.md](../my-dev-flow-review/stages/adversarial.md) · Lens plan ([lenses.md](lenses.md)) | `python3 {my-dev-flow}/scripts/handoff-for.py adversarial` |
| `quality` | [../my-dev-flow-review/stages/quality.md](../my-dev-flow-review/stages/quality.md) | `python3 {my-dev-flow}/scripts/handoff-for.py quality` |
| `lens-*` | [../my-dev-flow-review/stages/](../my-dev-flow-review/stages/) matching file · [lenses.md](lenses.md) once | `python3 {my-dev-flow}/scripts/handoff-for.py lens-<name>` |
| `merge-findings` | [../my-dev-flow-review/stages/merge-findings.md](../my-dev-flow-review/stages/merge-findings.md) | `python3 {my-dev-flow}/scripts/handoff-for.py merge-findings` |
| `fix-review` | [../my-dev-flow-review/stages/fix-review.md](../my-dev-flow-review/stages/fix-review.md) · [verify-and-fix.md](verify-and-fix.md) | `python3 {my-dev-flow}/scripts/handoff-for.py fix-review` |
| `test-full` | [../my-dev-flow-test/stages/test-full.md](../my-dev-flow-test/stages/test-full.md) · [verify-and-fix.md](verify-and-fix.md) | `python3 {my-dev-flow}/scripts/handoff-for.py test-full` |
| `test-lite` | [../my-dev-flow-test/stages/test-lite.md](../my-dev-flow-test/stages/test-lite.md) · [verify-and-fix.md](verify-and-fix.md) | `python3 {my-dev-flow}/scripts/handoff-for.py test-lite` |
| `fix-tests` | [../my-dev-flow-code/stages/fix-tests.md](../my-dev-flow-code/stages/fix-tests.md) · [verify-and-fix.md](verify-and-fix.md) | `python3 {my-dev-flow}/scripts/handoff-for.py fix-tests` |
| `gate-c` | [hitl.md](hitl.md) Gate C bar | blocking ask — no merge yet |
| `merge` (Gate C approved set) | [../my-dev-flow-merge/stages/merge.md](../my-dev-flow-merge/stages/merge.md) · [hitl.md](hitl.md) | `python3 {my-dev-flow}/scripts/handoff-for.py merge` |
| `merge` (approved missing or none) | [hitl.md](hitl.md) Gate C — ask + set **Gate C approved** **+ provenance**; do not launch | — |

**Resume:** [resume-abort.md](resume-abort.md) · async Build arm: [hitl.md](hitl.md).
