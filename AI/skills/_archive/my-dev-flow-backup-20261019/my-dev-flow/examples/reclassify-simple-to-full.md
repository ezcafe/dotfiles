# Golden path — mid-run reclassify simple → full

Short recovery. Parent follows [step-0.md](../step-0.md) Mid-run reclassify + [invariants.md](../invariants.md). Drop skip-review when contracts appear ([lenses.md](../lenses.md)).

## Ask started as

> Tiny copy tweak on settings label.

## What changed mid-run

Design discovers a new public route + persistence. Has API → **yes**, Has DB → **yes**.

## Parent before each Task (fixed)

1. Clarity boundary when Next ∈ clarity stages; log `clarity-check ok — <Next>`.
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py` launch pack)
3. `--snapshot-consent` before launch; `--check-consent-writes` after ([hitl.md](../hitl.md))
4. After any parent consent/waiver write: Run log `parent consent write — <kind>` → re-snapshot
5. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`

## Parent actions

1. Pause; **Decision N** (reclassify): Stay simple · Upgrade to **full** · New slug/stop.
2. Prefer Option **Upgrade to full**.
3. Set Mode **full**; Review profile **full** or **lite** (never keep **skip-review**).
4. Notes: `reclassify simple→full — API+DB appeared`; clear skip-review if set.
5. Resume Full pipeline from incomplete step (usually Analyze/Design → design-review with Pending parallel `api|db` when both yes).
6. Gate B → **blocking** ([hitl-gate-b.md](../hitl-gate-b.md) — Mode full never async-notify default).

## Do not

- Keep Mode simple + skip-review after Has API/DB yes
- Invent Ideation redo unless Decision N / Fix ask requires it
