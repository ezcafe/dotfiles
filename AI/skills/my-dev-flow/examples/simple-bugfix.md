# Golden path — Mode simple bug fix

Minimal walkthrough. Parent follows [stages.md](../stages.md) Happy path (simple). Do not invent Ideation / Gate A / skim.

## Ask

> Fix timeout handling in the HTTP retry helper — one function, no auth/schema change.

## Step 0

- Status **`running`**; Mode **simple**, Review profile **lite**, Lens plan **none**, Pending parallel **none**, Gate B veto **none**
- Slug e.g. `20261013-fix-http-retry-timeout`
- **Has auth/PII/schema:** **no** (non-auth helper — keeps Gate B **auto** eligible)
- Bootstrap thin `01-idea.md` (Core problem one line)
- Resolve models ([models.md](../models.md)); HITL Gate B prefer **auto**; HITL Grill **auto**; Gate C **blocking**
- **Lint (required):** `scripts/lint-run.py .my-docs/workflow/<slug>/` (again `--before-build` before Build)

## Parent before each Task (fixed)

1. Open clarity boundary file when Next ∈ clarity stages ([parent-next.md](../parent-next.md)); log `clarity-check ok — <Next>`.
2. Boundary-matched example: before `design-phase` → `clarity-check ok — design-phase`.
3. Boundary-matched example: before `build` → `clarity-check ok — build` (a prior design-phase token does **not** unlock Build).
4. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
5. `--snapshot-consent` before launch; `--check-consent-writes` after ([hitl.md](../hitl.md))
6. After any parent consent/waiver write: Run log `parent consent write — <kind>` → re-snapshot
7. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` → paste Description.

## Pipeline

| # | Stage id | Result |
|---|----------|--------|
| 1 | `design-phase` | Boundary-matched clarity + `--next --derive` + handoff → writes `02-analysis.md`, skip grill Notes, `03-design.md` (one option), `04-tasks.md`; sets Verify commands + Has API/DB **no** + Has auth/PII/schema **no** |
| 2 | `design-verify-phase` | `03a-design-review-log.md` Result **clean** (no empty `03a-api` / `03a-db`) |
| 3 | (04a) | Notes `04a skipped — no planned test cases` (unless tasks list tests) |
| 4 | Gate B | Prefer **auto** only when Has API/DB=no + no auth/PII/schema; **async-notify** only when user asks for a veto window ([hitl-gate-b.md](../hitl-gate-b.md)); `Gate B veto: none`. If async: one turn gap + **Build armed** then `build` |
| 5 | `build` | Boundary-matched clarity + `--next --derive` + handoff → re-read veto = none → TDD → verify-pass → write Smoke section smoke-pass |
| 6 | Smoke Task | **skipped** (Build-writes-Smoke — [verify-and-fix.md](../verify-and-fix.md)) |
| 7 | `code-review-phase` | Lite combined → Result **clean** |
| 8 | `test-lite` | Result **success** (**Test path last run:** `lite`) |
| 9 | Gate C | blocking — user names commit / push / PR / merge; set `Gate C approved: commit,push,pr,merge` **+** Notes `- provenance — gate-c-approved — user: "commit push PR and merge"` + Run log `parent consent write — gate-c-approved` → re-snapshot ([hitl.md](../hitl.md)) |
| 10 | `merge` | Boundary-matched clarity + `--next --derive` + handoff → only approved actions; Status **`done`** only when Result **success** **and** `merge` ∈ Gate C approved (PR-only / commit-only → stay **paused**) + calibration Notes (≤3) + append same ≤3 lines to `_calibration.md` ([stages.md](../stages.md) Done criteria) |

## Legal skip-review variant

If Mode **simple**, Review profile **skip-review**, and Has API=no **and** Has DB=no: after Build verify-pass + Smoke section → Gate C **only with** a fail-closed escape **+ provenance** (no `code-review-phase` / `test-lite`). Mode full never uses this path. If either flag flips to yes → drop skip-review ([lenses.md](../lenses.md)).

**Before Gate C (required):** one escape **with provenance** — e.g. Notes `smoke-waive` **+** `- provenance — smoke-waive — user: "waive independent smoke for this copy tweak"` (or `smoke-pass-rerun` / `gate-c-test-override` / `docs-only` with matching kinds) **+** Run log `parent consent write — <kind>` → re-snapshot. Bare tokens alone are rejected. Else lint `--before-merge` **errors** on Build-writes-Smoke alone. SoT: [hitl-gate-c.md](../hitl-gate-c.md) · [hitl.md](../hitl.md) Provenance · recovery [verify-and-fix.md](../verify-and-fix.md).

## Parent habits

- After each step: ≤5 lines + path; update Orchestrator card (Stage id = position; Status = lifecycle)
- Pre-launch: **Parent before each Task** block above · [orchestrator-rules.md](../orchestrator-rules.md) (Decision shapes → [invariants.md](../invariants.md))
- Never commit without Gate C yes
- Anti-patterns: [anti-patterns.md](anti-patterns.md)
- Pipeline SoT: [stages.md](../stages.md) Simple pipeline order
