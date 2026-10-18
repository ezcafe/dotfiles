# my-dev-flow scripts

Maintainer notes for lint and handoff helpers. Policy SoT stays in the markdown companions (`hitl.md`, `stages.md`, `parent-next.md`, …); these scripts enforce selected rules.

## Tests

From this directory or repo root:

```bash
python3 AI/skills/my-dev-flow/scripts/test_lint_run.py
# or
cd AI/skills/my-dev-flow/scripts && python3 test_lint_run.py
```

## Key `lint-run.py` flags

| Flag | Role |
|------|------|
| `--next` | Print card Next hint + companion / handoff (or `do-not-launch`). Auto-runs phase-gate lint from card Next (same as `--before-*` below). Exit **1** when printing `handoff: do-not-launch`; exit **0** when emitting a Task handoff; exit **2** on missing `00-run.md` |
| `--next --derive` | **Required habit** before each Task: derive expected next + phase gates auto from Next; unsafe mismatch → error + `do-not-launch` (exit 1) unless Notes `card-override` + provenance `card-override` |
| `--before-build` | Gate B / veto / Build armed / async turn-boundary gap / provenance / Verify / design clean / clarity-check; **also auto** when card Next=`build` |
| `--before-code-review` | Lens plan api/db when Has API/DB yes; **also auto** when Next ∈ Adv / `code-review-phase` |
| `--before-merge` | Gate C approved + provenance + test bar + stale / skip-review smoke; **also auto** when Next=`merge` |
| `--before-design-review` | Has API/DB set; isolated 03a when Mode full; **also auto** when Next ∈ design-review / design-verify-phase / api|db-review |
| `--check-stage-ids` | Registry drift vs handoffs / parent-next / stages |
| `--dry-run-seed` | Seed `00-run.md` from template, lint, stop |
| `--check-results` | Result header tokens + soft size warns |

Module layout (policy pointers in each module docstring): `lint_common.py`, `lint_stage_ids.py`, `lint_gate_b.py`, `lint_gate_c.py`, `lint_derive.py`, `lint_core.py`; `lint-run.py` is the CLI facade.

## Sync after SoT edits

When `AI/skills/my-dev-flow` exists, Step 0 requires `./AI/skills/sync-to-cursor.sh --check` (or full sync). See [skills-path.md](../skills-path.md).

## Handoff helper

```bash
python3 scripts/handoff-for.py <stage-id> [--slug <slug>] [--skill-root <abs>]
python3 scripts/handoff-for.py build --check-descriptions
```

Prints base block + R/W row + **Description** from handoffs.md Task description map.
