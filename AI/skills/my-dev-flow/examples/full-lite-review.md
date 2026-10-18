# Golden path — Mode full + Review profile lite

Minimal walkthrough. Parent follows [stages.md](../stages.md) Happy path (full) with post-Build **lite** path. Review follows **Review profile**, not Mode.

## Ask

> Add a small settings toggle with clear UX copy. Needs Ideation / Gate A / Design options, but not Adv→Quality→`test-full` depth.

## Step 0

- Status **`running`**; Mode **full**, Review profile **lite** (not **full**; not **skip-review**)
- Slug e.g. `20261013-settings-toggle`
- Lens plan **none**; Pending parallel **none**; Gate B veto **none**
- Resolve models ([models.md](../models.md)); HITL Gate B **blocking** (Mode full default); HITL Grill **async-notify**; Gate C **blocking**
- **Lint (required):** `scripts/lint-run.py .my-docs/workflow/<slug>/` (again `--before-build` before Build)

## Pipeline

| # | Stage id | Result |
|---|----------|--------|
| 1 | `ideation` | `01-idea.md`; Has UI as needed |
| 2 | `gate-a` | `01a` Result **ok** (auto) |
| 3 | `skim` | Result **done** |
| 4 | `analyze` | `02-analysis.md` |
| 5 | `grill` | Result **frontier-empty** (or Notes skip if empty) |
| 6 | `design` | Two options in `03-design.md` + `04-tasks.md`; Verify commands; Has API/DB |
| 7 | design-review path | Isolated API∥DB when flagged, then general → overall **clean** (or `design-verify-phase` only if reclassified simple) |
| 8 | (04a) | Only if planned tests; else Notes skip |
| 9 | Gate B | **blocking** → `Gate B approved: yes` (or named pick) + `Gate B veto: none` **+** Notes `- provenance — gate-b-approved — user: "yes go build"` ([hitl.md](../hitl.md) Provenance) |
| 10 | `build` | verify-pass → Smoke section smoke-pass |
| 11 | Smoke Task | **skipped** (Build-writes-Smoke) |
| 12 | `code-review-phase` | Lite combined (never separate Adv+Quality under lite) → **clean** |
| 13 | lenses | Per Lens plan (often none) |
| 14 | `test-lite` | Result **success** (not `test-full`) |
| 15 | Gate C | blocking — user names commit / push / PR / merge; set `Gate C approved: commit,push,pr,merge` **+** Notes `- provenance — gate-c-approved — user: "commit push PR and merge"` ([hitl.md](../hitl.md) Provenance) |
| 16 | `merge` | Only approved actions; Status **`done`** only when Result **success** **and** `merge` ∈ Gate C approved (PR-only / commit-only → stay **paused**) + calibration Notes (≤3) + append same ≤3 lines to `_calibration.md` ([stages.md](../stages.md) Done criteria) |

## Do not

- Mode **simple** + Review profile **full** (lint error — want Adv→`test-full` → Mode **full**)
- Mode **full** + **skip-review** (always illegal)
- Separate `adversarial` then `quality` when profile is **lite**

## Parent habits

- After each step: ≤5 lines + path; update Orchestrator card
- Pre-launch: [invariants.md](../invariants.md); **required** `scripts/handoff-for.py <stage-id>`
- Pipeline SoT: [stages.md](../stages.md) Mode × Review profile table
- Contrast: [full-api-db.md](full-api-db.md) (profile **full**); [simple-bugfix.md](simple-bugfix.md) (Mode simple + lite)
