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

## Pipeline

| # | Stage id | Result |
|---|----------|--------|
| 1 | `design-phase` | Writes `02-analysis.md`, skip grill Notes, `03-design.md` (one option), `04-tasks.md`; sets Verify commands + Has API/DB **no** |
| 2 | `design-verify-phase` | `03a-design-review-log.md` Result **clean** (no empty `03a-api` / `03a-db`) |
| 3 | (04a) | Notes `04a skipped — no planned test cases` (unless tasks list tests) |
| 4 | Gate B | Prefer **auto** (or **async-notify** only if [hitl.md](../hitl.md) narrow rule allows — Mode simple + no API/DB/auth/PII/schema); `Gate B veto: none`. If async: one turn gap + **Build armed** then `build` |
| 5 | `build` | Re-read veto = none → TDD → verify-pass → write Smoke section smoke-pass |
| 6 | Smoke Task | **skipped** (Build-writes-Smoke — [verify-and-fix.md](../verify-and-fix.md)) |
| 7 | `code-review-phase` | Lite combined → Result **clean** |
| 8 | `test-lite` | Result **success** |
| 9 | Gate C | blocking — user names commit / push / PR / merge |
| 10 | `merge` | Only approved actions; Status **`done`** only when Result **success** **and** `merge` ∈ Gate C approved (PR-only / commit-only → stay **paused**) + calibration Notes (≤3) |

## Legal skip-review variant

If Mode **simple**, Review profile **skip-review**, and Has API=no **and** Has DB=no: after Build verify-pass + Smoke section → Gate C (no `code-review-phase` / `test-lite`). Mode full never uses this path. If either flag flips to yes → drop skip-review ([lenses.md](../lenses.md)).

## Parent habits

- After each step: ≤5 lines + path; update Orchestrator card (Stage id = position; Status = lifecycle)
- Pre-launch: [invariants.md](../invariants.md) checklist; **required** `scripts/handoff-for.py <stage-id>`
- Never commit without Gate C yes
- Anti-patterns: [anti-patterns.md](anti-patterns.md)
- Pipeline SoT: [stages.md](../stages.md) Simple pipeline order
