# Cutover: v1 → v2

**New runs (2026-10+):** prefer [`my-dev-flow-v3`](../my-dev-flow-v3/SKILL.md) — leaner SoT (settle generation, single derive file). Finish in-flight v2 on v2. See [v3 CUTOVER](../my-dev-flow-v3/CUTOVER.md).

## What changed

| v1 | v2 |
|----|-----|
| `scripts/lint-run.py`, `handoff-for.py`, `preflight.py` | Agent checklists: [preflight.md](preflight.md), [derive-next.md](derive-next.md), [handoffs.md](handoffs.md) |
| Consent snap / `.lint-*` sidecars | Parent Notes + Run log habits only |
| Dense companion mesh (~14k LOC Python) | Core policy + soft checklists |
| Skill names `my-dev-flow*` | Skill names `my-dev-flow-v2*` |

## Backup

Full v1 tree: `AI/skills/_archive/my-dev-flow-backup-20261019/`.  
Live v1 remains at `AI/skills/my-dev-flow*` until you delete it.

## Discoverability

Live v1 skill YAML descriptions say **DEPRECATED for new runs — prefer my-dev-flow-v2**. Agents still find v1 for in-flight resumes; new work should start with `my-dev-flow-v2`.

## Run v2

```
run my-dev-flow-v2
```

Sync: `./AI/skills/sync-to-cursor.sh` then `--check`.

## When to delete v1

After you trust v2 on 1–2 real runs:

1. Confirm backup exists under `_archive/`.
2. Remove `AI/skills/my-dev-flow` and sibling `my-dev-flow-{design,design-review,code,review,test,merge}` (not `-v2`).
3. Optionally rename `my-dev-flow-v2*` → `my-dev-flow*` and update triggers — or keep `-v2` names.

## In-flight runs

v1 `.my-docs/workflow/<slug>/00-run.md` files still work with v2 if you:

- Stop using Python lint flags in Notes.
- Follow [preflight.md](preflight.md) instead.
- Point Task prompts at `{my-dev-flow-v2}` paths ([skills-path.md](skills-path.md)).

## Field alias (resume)

| v1 / LEGACY label | v2 durable field | Where |
|-------------------|------------------|--------|
| **Mode last run** | **Test path last run** | `06-test-log.md` Smoke / full / lite |
| `01a-idea-ui-review.md` | `01a-gate-a.md` | Gate A Result artifact |

On resume only: if `06-test-log.md` still has **Mode last run**, treat it as **Test path last run** (`smoke` \| `full` \| `lite`). New writes use **Test path last run**. Gate C and derive read the v2 name; accept the LEGACY alias when the new field is absent ([artifacts/06-test-log.md](artifacts/06-test-log.md) · [gate-c.md](gate-c.md)).

On resume only: if `01a-gate-a.md` is absent and `01a-idea-ui-review.md` exists, derive / Gate A treat the LEGACY file as `01a` ([derive-next.md](derive-next.md) · [artifacts/INDEX.md](artifacts/INDEX.md)). New runs write `01a-gate-a.md` only.

## Stage alias (resume)

Prefer current stage ids on new runs. On resume only, accept these legacy Task / stage names and map them to the v2 one-Task stages:

| Legacy (separate Tasks) | Prefer now |
|-------------------------|------------|
| Coverage / Add missing e2e / Run suite (`coverage`, `add-e2e`, `run`) | One Task `test-full` ([my-dev-flow-v2-test/stages/test-full.md](../my-dev-flow-v2-test/stages/test-full.md)) |
| Mode simple: separate Analyze → Grill → Design | One Task `design-phase` |
| Mode simple: separate API/DB + design-review | One Task `design-verify-phase` |

Do **not** launch separate `coverage` / `add-e2e` / `run` Tasks on new runs — `test-full` already covers those steps in one Task.
