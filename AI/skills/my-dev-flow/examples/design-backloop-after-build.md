# Golden path — design-backloop after Build

Short recovery. SoT: [design-backloop.md](../design-backloop.md) · [invariants.md](../invariants.md) · [failure-playbook.md](../failure-playbook.md).

## Trigger

Build/Fix verify-fail (or review Critical/Major) cannot stay aligned with `03`/`04` without contract or IA change.

## Parent before each Task (fixed)

1. Clarity boundary when Next ∈ clarity stages; log `clarity-check ok — <Next>`.
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
3. `--snapshot-consent` before launch; `--check-consent-writes` after ([hitl.md](../hitl.md))
4. After any parent consent/waiver write: Run log `parent consent write — <kind>` → re-snapshot
5. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`

## Parent actions

1. Pause; **Decision N**: Amend design · Fix-only · Stop.
2. Prefer **Amend design** when contracts/IA must change.
3. Log Notes `design-backloop`; prior Gate B **invalid**.
4. Set **`Gate B approved: none`**; clear Notes **Build armed** and veto-window tokens; card Next = `design-update`. Decision N Option 1 is enough entry — no prior `03a` Fix ask required.
5. If prior `05` / `06` Results exist: add Notes `- review-stale` and `- test-stale` (or clear those Results) — [verify-and-fix.md](../verify-and-fix.md) Stale · [design-backloop.md](../design-backloop.md) §3.
6. Do **not** silently rewrite `03`/`04` inside Build/Fix.
7. Resume: `design-update` → design-review / design-verify-phase → **Gate B** (Next=`gate-b` while token still present) → Fix/Build.
8. After Gate B re-settle, clear Notes `design-backloop` by HITL tier: **blocking** → clear + approved yes/named pick **+** `provenance — gate-b-approved — user: "…"` + Run log `parent consent write — gate-b-approved` → re-snapshot ([hitl.md](../hitl.md)); **auto** → clear (approved may stay `none`); **async-notify** → clear + Build armed + `parent consent write — build-armed` → re-snapshot. Then Build when armed.
9. Clear `review-stale` / `test-stale` only after fresh review clean / test success. Advance only on Result tokens in [results.md](../results.md) (`clean`, then `verify-pass`).

## Do not

- Launch Build while Notes still say `design-backloop` (lint error — including soft Gate B / approved `none`; `--next` redirects `build` only)
- Set Next `build` before design-update + re-review; after re-review, Next=`gate-b` with token still present is correct until settle
- Go to Gate C with a known design mismatch
- Treat Gate B veto-after-Build as the same Decision (options in [hitl-gate-b.md](../hitl-gate-b.md) · tables in [invariants.md](../invariants.md))
