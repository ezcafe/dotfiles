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
| `--next` | Print card Next hint + companion / handoff (or `do-not-launch`) |
| `--next --derive` | Also derive expected next; warn when card differs |
| `--before-build` | Gate B / veto / Build armed / Verify / design clean / clarity-check |
| `--before-code-review` | Lens plan api/db when Has API/DB yes |
| `--before-merge` | Gate C approved + test bar + stale / skip-review smoke |
| `--before-design-review` | Has API/DB set; isolated 03a when Mode full |
| `--check-stage-ids` | Registry drift vs handoffs / parent-next / stages |
| `--dry-run-seed` | Seed `00-run.md` from template, lint, stop |
| `--check-results` | Result header tokens + soft size warns |

Module layout (policy pointers in each module docstring): `lint_common.py`, `lint_stage_ids.py`, `lint_gate_b.py`, `lint_gate_c.py`, `lint_derive.py`, `lint_core.py`; `lint-run.py` is the CLI facade.

## Sync after SoT edits

When `AI/skills/my-dev-flow` exists, Step 0 requires `./AI/skills/sync-to-cursor.sh --check` (or full sync). See [skills-path.md](../skills-path.md).

## Handoff helper

```bash
python3 scripts/handoff-for.py <stage-id> [--slug <slug>] [--skill-root <abs>]
```
