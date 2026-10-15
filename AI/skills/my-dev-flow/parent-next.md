# Parent next (discovery)

Given `00-run.md` Orchestrator card **Stage id** / **Next step**, open **1–2 files** + handoff. Do **not** re-read orchestrator [SKILL.md](SKILL.md).

**Also:** `python {my-dev-flow}/scripts/lint-run.py <run-dir> --next` prints the same hint from a live run (resolve `{my-dev-flow}` per [skills-path.md](skills-path.md)).

**Handoff command (canonical):** `python {my-dev-flow}/scripts/handoff-for.py <stage-id>` (optional `--slug`, `--skill-root`).

**Before launch (clarity-check — parent habit, not a Task / no handoffs id):**

| Boundary | Open |
|----------|------|
| Before Analyze / Grill / Design (Mode **full** standalone stages) | [../my-dev-flow-design/stages/clarity-check.md](../my-dev-flow-design/stages/clarity-check.md) — full-mode gates |
| Before `design-phase` (Mode **simple** only) | Same file — **design-phase entry** section only (`01-idea` + Mode simple; do **not** require `02-analysis` / `02b` yet) |
| Before TDD review / Build / Fix | [../my-dev-flow-code/stages/clarity-check.md](../my-dev-flow-code/stages/clarity-check.md) |

If clarity-check fails → ask the user; do **not** launch the Task.

| Stage id / Next | Open (1–2) | Handoff |
|-----------------|------------|---------|
| (Step 0 / classify) | [stages.md](stages.md) Step 0 · [artifacts/00-run.md](artifacts/00-run.md) | — seed + `lint-run.py` |
| `ideation` | [../my-dev-flow-design/stages/ideation.md](../my-dev-flow-design/stages/ideation.md) · design [SKILL.md](../my-dev-flow-design/SKILL.md) once | `python {my-dev-flow}/scripts/handoff-for.py ideation` |
| `gate-a` | [../my-dev-flow-design/stages/gate-a.md](../my-dev-flow-design/stages/gate-a.md) | `python {my-dev-flow}/scripts/handoff-for.py gate-a` |
| `ideation-update` | [../my-dev-flow-design/stages/ideation-update.md](../my-dev-flow-design/stages/ideation-update.md) | `python {my-dev-flow}/scripts/handoff-for.py ideation-update` |
| `skim` | [../my-dev-flow-design/stages/skim.md](../my-dev-flow-design/stages/skim.md) | `python {my-dev-flow}/scripts/handoff-for.py skim` |
| `analyze` | [../my-dev-flow-design/stages/analyze.md](../my-dev-flow-design/stages/analyze.md) | `python {my-dev-flow}/scripts/handoff-for.py analyze` |
| `grill` | [grill.md](grill.md) · [../my-dev-flow-design/stages/grill.md](../my-dev-flow-design/stages/grill.md) | `python {my-dev-flow}/scripts/handoff-for.py grill` |
| `design` | [../my-dev-flow-design/stages/design.md](../my-dev-flow-design/stages/design.md) | `python {my-dev-flow}/scripts/handoff-for.py design` |
| `design-phase` | [../my-dev-flow-design/stages/design-phase.md](../my-dev-flow-design/stages/design-phase.md) | `python {my-dev-flow}/scripts/handoff-for.py design-phase` |
| `design-update` | [../my-dev-flow-design/stages/design-update.md](../my-dev-flow-design/stages/design-update.md) | `python {my-dev-flow}/scripts/handoff-for.py design-update` |
| `api-contract-review` | [../my-dev-flow-design-review/stages/api-contract-review.md](../my-dev-flow-design-review/stages/api-contract-review.md) | `python {my-dev-flow}/scripts/handoff-for.py api-contract-review` |
| `db-design-review` | [../my-dev-flow-design-review/stages/db-design-review.md](../my-dev-flow-design-review/stages/db-design-review.md) | `python {my-dev-flow}/scripts/handoff-for.py db-design-review` |
| `design-review` | [../my-dev-flow-design-review/stages/design-review.md](../my-dev-flow-design-review/stages/design-review.md) | `python {my-dev-flow}/scripts/handoff-for.py design-review` |
| `design-verify-phase` | [../my-dev-flow-design-review/stages/design-verify-phase.md](../my-dev-flow-design-review/stages/design-verify-phase.md) | `python {my-dev-flow}/scripts/handoff-for.py design-verify-phase` |
| `tdd-review` | [../my-dev-flow-code/stages/tdd-review.md](../my-dev-flow-code/stages/tdd-review.md) · [verify-and-fix.md](verify-and-fix.md) | `python {my-dev-flow}/scripts/handoff-for.py tdd-review` |
| `gate-b` | [hitl.md](hitl.md) · card Next | digest only — set **Gate B approved** when blocking; no handoff Task |
| `build` (armed / approved) | [../my-dev-flow-code/stages/build.md](../my-dev-flow-code/stages/build.md) · [verify-and-fix.md](verify-and-fix.md) · [hitl.md](hitl.md) if async gap | `python {my-dev-flow}/scripts/handoff-for.py build` |
| `build` (async gap, not armed) | [hitl.md](hitl.md) — set **Build armed** on this resume turn; do not launch yet if veto pending | — |
| `build` (blocking, Gate B approved none) | [hitl.md](hitl.md) — set **Gate B approved** yes / named pick; do not launch | — |
| `smoke` | [../my-dev-flow-test/stages/smoke.md](../my-dev-flow-test/stages/smoke.md) | `python {my-dev-flow}/scripts/handoff-for.py smoke` |
| `code-review-phase` | [../my-dev-flow-review/stages/code-review-phase.md](../my-dev-flow-review/stages/code-review-phase.md) · Lens plan ([lenses.md](lenses.md)) | `python {my-dev-flow}/scripts/handoff-for.py code-review-phase` |
| `adversarial` | [../my-dev-flow-review/stages/adversarial.md](../my-dev-flow-review/stages/adversarial.md) · Lens plan ([lenses.md](lenses.md)) | `python {my-dev-flow}/scripts/handoff-for.py adversarial` |
| `quality` | [../my-dev-flow-review/stages/quality.md](../my-dev-flow-review/stages/quality.md) | `python {my-dev-flow}/scripts/handoff-for.py quality` |
| `lens-*` | [../my-dev-flow-review/stages/](../my-dev-flow-review/stages/) matching file · [lenses.md](lenses.md) once | `python {my-dev-flow}/scripts/handoff-for.py lens-<name>` |
| `merge-findings` | [../my-dev-flow-review/stages/merge-findings.md](../my-dev-flow-review/stages/merge-findings.md) | `python {my-dev-flow}/scripts/handoff-for.py merge-findings` |
| `fix-review` | [../my-dev-flow-review/stages/fix-review.md](../my-dev-flow-review/stages/fix-review.md) · [verify-and-fix.md](verify-and-fix.md) | `python {my-dev-flow}/scripts/handoff-for.py fix-review` |
| `test-full` | [../my-dev-flow-test/stages/test-full.md](../my-dev-flow-test/stages/test-full.md) · [verify-and-fix.md](verify-and-fix.md) | `python {my-dev-flow}/scripts/handoff-for.py test-full` |
| `test-lite` | [../my-dev-flow-test/stages/test-lite.md](../my-dev-flow-test/stages/test-lite.md) · [verify-and-fix.md](verify-and-fix.md) | `python {my-dev-flow}/scripts/handoff-for.py test-lite` |
| `fix-tests` | [../my-dev-flow-code/stages/fix-tests.md](../my-dev-flow-code/stages/fix-tests.md) · [verify-and-fix.md](verify-and-fix.md) | `python {my-dev-flow}/scripts/handoff-for.py fix-tests` |
| `gate-c` | [hitl.md](hitl.md) Gate C bar | blocking ask — no merge yet |
| `merge` (Gate C approved set) | [../my-dev-flow-merge/stages/merge.md](../my-dev-flow-merge/stages/merge.md) · [hitl.md](hitl.md) | `python {my-dev-flow}/scripts/handoff-for.py merge` |
| `merge` (approved missing or none) | [hitl.md](hitl.md) Gate C — ask + set **Gate C approved**; do not launch | — |

**Resume:** [stages.md](stages.md) Resume · async Build arm: [hitl.md](hitl.md).
