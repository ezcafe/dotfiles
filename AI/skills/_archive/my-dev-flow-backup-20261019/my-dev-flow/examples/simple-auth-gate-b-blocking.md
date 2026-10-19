# Golden path — Mode simple + auth/PII/schema yes → Gate B blocking

Short walkthrough. Parent follows [stages.md](../stages.md) Happy path (simple). SoT: [hitl-gate-b.md](../hitl-gate-b.md).

## Ask

> Add a login-required settings toggle that stores a preference — Mode simple, no new public API, no DB schema migration (in-memory / existing session only).

## Step 0

- Status **`running`**; Mode **simple**, Review profile **lite**, Lens plan later **security** (or none if tiny), Pending parallel **none**, Gate B veto **none**
- Slug e.g. `20261018-simple-auth-toggle`
- **Has API:** **no**; **Has DB:** **no**; **Has auth/PII/schema:** **yes**
- HITL Gate B **blocking** (required when Has auth/PII/schema yes — not auto/async-notify)
- HITL Grill **auto**; Gate C **blocking**
- **Lint:** `scripts/lint-run.py .my-docs/workflow/<slug>/`

## Parent before each Task (fixed)

1. Clarity boundary + `clarity-check ok — <Next>` ([parent-next.md](../parent-next.md)).
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
3. `--snapshot-consent` before launch; `--check-consent-writes` after
4. After any parent consent/waiver write: Run log `parent consent write — <kind>` → re-snapshot
5. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>` → paste Description

## Pipeline (Gate B focus)

| # | Stage id | Result |
|---|----------|--------|
| 1 | `design-phase` | Sets Has API **no**, Has DB **no**, Has auth/PII/schema **yes**; Verify commands; one design option |
| 2 | `design-verify-phase` | `03a-design-review-log.md` **clean** (no empty `03a-api` / `03a-db`) |
| 3 | Gate B | **blocking** digest (prefer AskQuestion); user says e.g. `yes go build the auth toggle`; **parent** sets `Gate B approved: yes` **+** Notes `- provenance — gate-b-approved — user: "yes go build the auth toggle"` + Run log `parent consent write — gate-b-approved` → re-snapshot ([hitl.md](../hitl.md)); `Gate B veto: none` |
| 4 | `build` | Re-read veto = none + approved + provenance → verify-pass + Smoke |

## Lint check

Mode simple + Has auth/PII/schema yes + HITL Gate B `auto`/`async-notify` → lint **error**. Provenance quote: lint = shape only; parent habit = latest-message substring ([hitl.md](../hitl.md)).

## Anti-pattern

| Wrong | Right |
|-------|-------|
| Keep Gate B **auto** because Has API/DB are no | Set HITL Gate B **blocking** when auth/PII/schema is in scope |

Index: [INDEX.md](INDEX.md).
