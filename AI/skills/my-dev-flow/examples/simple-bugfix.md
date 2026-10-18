# Golden path — Mode simple bug fix

Minimal walkthrough. Parent follows [stages.md](../stages.md) Happy path (simple). Do not invent Ideation / Gate A / skim.

## Ask

> Fix timeout handling in login helper — one function, no schema change.

## Step 0

- Status **`running`**; Mode **simple**, Review profile **lite**, Lens plan **none**, Pending parallel **none**, Gate B veto **none**
- Slug e.g. `20261013-fix-login-timeout`
- Bootstrap thin `01-idea.md` (Core problem one line)
- Resolve models ([models.md](../models.md)); HITL Gate B prefer **auto**; HITL Grill **auto**; Gate C **blocking**
- **Lint (required):** `scripts/lint-run.py .my-docs/workflow/<slug>/` (again `--before-build` before Build)

## Parent before each Task (fixed)

1. Open clarity boundary file when Next ∈ clarity stages ([parent-next.md](../parent-next.md)); log `clarity-check ok — <Next>`.
2. Boundary-matched example: before `design-phase` → `clarity-check ok — design-phase`.
3. Boundary-matched example: before `build` → `clarity-check ok — build` (a prior design-phase token does **not** unlock Build).
4. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive`
5. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` → paste Description.

## Pipeline

| # | Stage id | Result |
|---|----------|--------|
| 1 | `design-phase` | Boundary-matched clarity + `--next --derive` + handoff → writes `02-analysis.md`, skip grill Notes, `03-design.md` (one option), `04-tasks.md`; sets Verify commands + Has API/DB **no** |
| 2 | `design-verify-phase` | `03a-design-review-log.md` Result **clean** (no empty `03a-api` / `03a-db`) |
| 3 | (04a) | Notes `04a skipped — no planned test cases` (unless tasks list tests) |
| 4 | Gate B | Prefer **auto**; **async-notify** only when user asks for a veto window ([hitl.md](../hitl.md) narrow rule); `Gate B veto: none`. If async: one turn gap + **Build armed** then `build` |
| 5 | `build` | Boundary-matched clarity + `--next --derive` + handoff → re-read veto = none → TDD → verify-pass → write Smoke section smoke-pass |
| 6 | Smoke Task | **skipped** (Build-writes-Smoke — [verify-and-fix.md](../verify-and-fix.md)) |
| 7 | `code-review-phase` | Lite combined → Result **clean** |
| 8 | `test-lite` | Result **success** (**Test path last run:** `lite`) |
| 9 | Gate C | blocking — user names commit / push / PR / merge; set `Gate C approved: commit,push,pr,merge` **+** Notes `- provenance — gate-c-approved — user: "commit push PR and merge"` ([hitl.md](../hitl.md) Provenance) |
| 10 | `merge` | Boundary-matched clarity + `--next --derive` + handoff → only approved actions; Status **`done`** only when Result **success** **and** `merge` ∈ Gate C approved (PR-only / commit-only → stay **paused**) + calibration Notes (≤3) + append same ≤3 lines to `_calibration.md` ([stages.md](../stages.md) Done criteria) |

## Legal skip-review variant

If Mode **simple**, Review profile **skip-review**, and Has API=no **and** Has DB=no: after Build verify-pass + Smoke section → Gate C **only with** a fail-closed escape **+ provenance** (no `code-review-phase` / `test-lite`). Mode full never uses this path. If either flag flips to yes → drop skip-review ([lenses.md](../lenses.md)).

**Before Gate C (required):** one escape **with provenance** — e.g. Notes `smoke-waive` **+** `- provenance — smoke-waive — user: "waive independent smoke for this copy tweak"` (or `smoke-pass-rerun` / `gate-c-test-override` / `docs-only` with matching kinds). Bare tokens alone are rejected. Else lint `--before-merge` **errors** on Build-writes-Smoke alone. SoT: [hitl.md](../hitl.md) Gate C test bar / Provenance · recovery [verify-and-fix.md](../verify-and-fix.md).

## Parent habits

- After each step: ≤5 lines + path; update Orchestrator card (Stage id = position; Status = lifecycle)
- Pre-launch: **Parent before each Task** block above · [orchestrator-rules.md](../orchestrator-rules.md) (Decision shapes → [invariants.md](../invariants.md))
- Never commit without Gate C yes
- Anti-patterns: [anti-patterns.md](anti-patterns.md)
- Pipeline SoT: [stages.md](../stages.md) Simple pipeline order
