# Golden path — max-round → Decision N

Short walkthrough when a stage hits the round cap. SoT: [invariants.md](../invariants.md) · [failure-playbook.md](../failure-playbook.md).

## Trigger

Parent incremented artifact **Round** (or Run metrics / Verify attempts) after each cycle. Lint `--next` → `do-not-launch` when e.g.:

- `03a-design-review-log.md` **Round ≥ 3** + Result **needs update**
- `01a` **Round ≥ 3** + Result ≠ **ok**
- Verify attempts ≥ 3 + Last Verify **verify-fail**
- `05` Round / `review fix rounds` ≥ 3 with not clean
- `06` Round / smoke↔fix·test↔fix rounds ≥ 3 with failure

## Parent before each Task (fixed)

1. Clarity boundary + `clarity-check ok — <Next>` ([parent-next.md](../parent-next.md)).
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py`)
3. `--snapshot-consent` before launch; `--check-consent-writes` after
4. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`

## Pipeline (Decision N focus)

| # | Action |
|---|--------|
| 1 | `--next` prints `do-not-launch` + max-round reason |
| 2 | Pause; **Decision N**: raise cap · proceed if clean (Enhancements-only) · Stop / reclassify |
| 3 | If raise cap: Notes `- max-round-cap — <domain> — <N> — user: "<verbatim ≥12 chars>"` (`design-review` \| `gate-a` \| `verify` \| `review-fix` \| `test-fix`; `<N>` ≥ 3) |
| 4 | After parent consent-shaped Notes write: Run log `parent consent write — max-round-cap` (if snap exists) → re-snapshot |
| 5 | Resume chosen path only — do not continue the old failing loop |

## Do not

- Re-launch the same Fix/Update loop without Decision N after the cap
- Leave **Round** at 1 across ≥3 same-stage cycles (max-round lint cannot fire — [invariants.md](../invariants.md))

## Anti-pattern

| Wrong | Right |
|-------|-------|
| Ignore `do-not-launch` and re-run Update/Fix | Decision N first; raise cap only with provenance-shaped Notes |

Index: [INDEX.md](INDEX.md).
