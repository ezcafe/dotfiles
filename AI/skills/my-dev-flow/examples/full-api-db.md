# Golden path — Mode full (API + DB)

Minimal walkthrough. Parent follows [stages.md](../stages.md) Happy path (full).
Anti-patterns: [anti-patterns.md](anti-patterns.md). API/DB rules: [lenses.md](../lenses.md).

## Ask

> Add a new care-log **attachment** resource: POST/GET routes, authz (caregiver must own the log), and a new `attachments` table with migration. Not a one-field tweak.

## Step 0

- Status **`running`**; Mode **full**, Review profile **full**, Lens plan starts **none** (add **api** + **db** before code review; **security** if authz is in scope)
- Slug e.g. `20261013-care-log-attachments`
- Has API / Has DB → set **yes** once Design has contracts (force yes\|no before design-review)
- **Pending parallel:** `api|db` until both `03a-api` and `03a-db` exist, then `none`
- HITL Gate B **blocking** (required for Mode full); HITL Grill **async-notify**; Gate C **blocking**
- `Gate B veto: none`
- **Never** skip-review when Has API or Has DB = yes
- **Lint (required):** `scripts/lint-run.py …` then `--before-design-review` / `--before-build`

## Parent before each Task (fixed)

1. Open clarity boundary when Next ∈ clarity stages ([parent-next.md](../parent-next.md)); log `clarity-check ok — <Next>`.
2. Boundary-matched: before `analyze` / `grill` / `design` → matching token each time (a prior token does **not** unlock the next).
3. Boundary-matched: before `build` → `clarity-check ok — build`.
4. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
5. `--snapshot-consent` before launch; `--check-consent-writes` after ([hitl.md](../hitl.md))
6. After any parent consent/waiver write: Run log `parent consent write — <kind>` → re-snapshot
7. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`.

## Pipeline

| # | Stage id | Result |
|---|----------|--------|
| 1 | `ideation` | `01-idea.md`; Has UI as needed |
| 2 | `gate-a` | `01a-gate-a.md` Result ok (auto) |
| 3 | `skim` | `02-skim.md` |
| 4 | `analyze` | Boundary-matched clarity + `--next --derive` + handoff → `02-analysis.md`; frontier may list contract/authz choices |
| 5 | `grill` | Boundary-matched clarity + `--next --derive` → `02b-grill.md` frontier-empty (or skip only if frontier empty) |
| 6 | `design` | Boundary-matched clarity + `--next --derive` → two options in `03-design.md` + `04-tasks.md`; Verify commands; Has API/DB **yes** |
| 7 | `api-contract-review` ∥ `db-design-review` | Both `03a-*` missing → **same parent turn** (parallel); one `03a-*` exists → launch **missing only** (resume serialize — do not re-parallel); Pending parallel `api|db` → `none` when both done; both clean or Fix ask ([lenses.md](../lenses.md)) |
| 8 | `design-review` | General clean (after isolated clean); Deferred Enhancements OK |
| 9 | (04a) | Only if `04-tasks` lists concrete tests; else skip Notes |
| 10 | Gate B | **blocking** required as default (Mode **full** — never async-notify default; [hitl-gate-b.md](../hitl-gate-b.md)); on approve **parent** sets `Gate B approved: yes` (or named pick) + `Gate B veto: none` **+** Notes `- provenance — gate-b-approved — user: "yes go build"` + Run log `parent consent write — gate-b-approved` → re-snapshot ([hitl.md](../hitl.md)) |
| 11 | `build` | Boundary-matched clarity + `--next --derive` + handoff → veto check → TDD → verify-pass → Smoke section |
| 12 | Smoke Task | Notes `smoke re-run` **once** → independent Smoke → Run log stage `smoke` / 06 after Last verify-pass at → Notes `smoke-pass (re-run)` + Run log `parent consent write — smoke-pass-rerun` → re-snapshot (Mode full + profile full — required; bare Notes alone do not unlock Adv; [verify-and-fix.md](../verify-and-fix.md) E1); Build-writes-Smoke alone blocked before Adv |
| 13 | Lens plan | Set `api+db` (+ **security** when authz/PII in scope) |
| 14 | `adversarial` → `quality` | Separate Tasks; clean |
| 15 | `lens-api` ∥ `lens-db` (∥ `lens-security` if planned) | Parallel when 2+ → `merge-findings` |
| 16 | `test-full` | One Task; Result **success** (**Test path last run:** `full`) |
| 17 | Gate C | blocking — user names commit / push / PR / merge; set `Gate C approved: commit,push,pr,merge` **+** Notes `- provenance — gate-c-approved — user: "commit push PR and merge"` + Run log `parent consent write — gate-c-approved` → re-snapshot ([hitl.md](../hitl.md)) |
| 18 | `merge` | Only approved actions; Status **`done`** only when Result **success** **and** `merge` ∈ Gate C approved (PR-only / commit-only → stay **paused**) + calibration Notes (≤3) + append same ≤3 lines to `_calibration.md` ([stages.md](../stages.md) Done criteria) |

## Tiny-tweak variant (not this ask)

If the change is **one field / one column / one validator**, no new auth/PII/cross-service, one package → Notes `tiny-contract-tweak`; fold API/DB into general design-review; do **not** force isolated Tasks or api/db lenses; do **not** invent empty `03a-api` / `03a-db`. Mode may stay **simple** only when [lenses.md](../lenses.md) API/DB Mode rule + tiny-tweak criteria allow; **never** `skip-review`.

## Parent habits

- After each step: ≤5 lines + path; update Orchestrator card
- Pre-launch: **Parent before each Task** block above · [orchestrator-rules.md](../orchestrator-rules.md) (Decision shapes → [invariants.md](../invariants.md))
- Never commit without Gate C yes
- On design invalid after Build → [failure-playbook.md](../failure-playbook.md) design-backloop
- Pipeline SoT: [stages.md](../stages.md) Full pipeline order
