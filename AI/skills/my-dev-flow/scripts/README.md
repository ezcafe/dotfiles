# my-dev-flow scripts

Maintainer notes for lint and handoff helpers. Policy SoT stays in the markdown companions (`hitl.md`, `hitl-gate-b.md`, `hitl-gate-c.md`, `stages.md`, `parent-next.md`, …); these scripts enforce selected rules.

## Tests

From this directory or repo root:

```bash
python3 AI/skills/my-dev-flow/scripts/test_lint_run.py
# or
cd AI/skills/my-dev-flow/scripts && python3 test_lint_run.py
```

## Preflight / launch pack (optional)

```bash
python3 scripts/preflight.py <run-dir>
```

One-shot **launch pack**: card Stage/Next + Open paths (soft-cap 2) + clarity gate + `lint-run.py --next --derive` + lint exit + **always** `--snapshot-consent`. Optional Step 0 / session habit — does **not** replace per-Task `--next --derive` ([step-0.md](../step-0.md) · [orchestrator-rules.md](../orchestrator-rules.md) · [parent-next.md](../parent-next.md)).

## Key `lint-run.py` flags

| Flag | Role |
|------|------|
| `--next` | Print card Next hint + companion / handoff (or `do-not-launch`). Auto-runs phase-gate lint from card Next (same as `--before-*` below). Exit **1** when printing `handoff: do-not-launch`; exit **0** when emitting a Task handoff; exit **2** on missing `00-run.md`. Also enforces max-round caps ([invariants.md](../invariants.md)) |
| `--next --derive` | **Required habit** before each Task: derive expected next + phase gates auto from Next; unsafe mismatch → error + `do-not-launch` (exit 1) unless Notes `card-override` + provenance `card-override` |
| `--before-build` | Gate B / veto / Build armed / async turn-boundary gap / provenance / Verify / design clean / clarity-check; **also auto** when card Next=`build` |
| `--before-code-review` | Lens plan api/db when Has API/DB yes; Mode full + profile full independent smoke (E1); **also auto** when Next ∈ Adv / `code-review-phase` |
| `--before-merge` | Gate C approved + provenance + test bar + stale / skip-review smoke; **also auto** when Next=`merge` |
| `--before-design-review` | Has API/DB + Has auth/PII/schema yes\|no; isolated 03a when Mode full; **also auto** when Next ∈ design-review / design-verify-phase / api|db-review |
| `--snapshot-consent` | Write `.lint-consent-snap` before Task (Gate B/C / Build armed / provenance / waivers); **preflight always runs this** |
| `--check-consent-writes` | Error if those fields changed since snap without new Run log `parent consent write` (missing snap → error). Also auto when a snap **exists**: `--next` / `--before-build` / `--before-merge` (missing snap → no-op) |
| `--check-stage-ids` | Registry drift vs handoffs / parent-next / stages |
| `--dry-run-seed` | Seed `00-run.md` from template, lint, stop |
| `--check-results` | Result header tokens + soft size warns |

Module layout (policy pointers in each module docstring): `lint_common.py`, `lint_stage_ids.py`, `lint_gate_b.py`, `lint_gate_c.py`, `lint_derive.py`, `lint_core.py`; `lint-run.py` is the CLI facade.

## Local sidecars (do-not-commit)

| File | Role |
|------|------|
| `.lint-async-gap` | Written by `--next` on async Gate B digest-only pause |
| `.lint-consent-snap` | Written by `--snapshot-consent` before Task |
| `.consent.md` | Optional parent-only consent scratchpad (Tasks never Write) |

**Local only — do not commit** (unless team policy says otherwise for `.consent.md`). Policy: [hitl.md](../hitl.md) · [hitl-gate-b.md](../hitl-gate-b.md).

## Sync after SoT edits

When `AI/skills/my-dev-flow` exists, Step 0 requires `./AI/skills/sync-to-cursor.sh --check` (or full sync). See [skills-path.md](../skills-path.md).

## Handoff helper

```bash
python3 scripts/handoff-for.py <stage-id> [--slug <slug>] [--skill-root <abs>]
python3 scripts/handoff-for.py build --check-descriptions
```

Prints base block + R/W row + **Description** from handoffs.md Task description map. Base block forbids Task writes of Gate B/C approved, Build armed, provenance, card-override, smoke-waive.
