# my-dev-flow legacy (do not create on new runs)

These steps and artifacts were **removed**. New runs ignore them.
Aliases below stay for **resume** of old runs only.

| Removed | What it was | What to do instead |
|---------|-------------|--------------------|
| **Gate A2** | UI look gate | Specify UI in `03-design.md` / `04-tasks.md`; match existing app chrome + Gate A 80/20 |
| **`01b-ui-concept.md`** | Separate UI concept doc | UI specs live in Design when **Has UI** |
| **`ui-refs/`** | Look-gate screenshots / :8765 serve | Do not create; do not serve look-gate servers |

**Resume old runs:** treat Gate A2 / `01b` / `ui-refs` as skipped/N/A. Do not re-open them.

## Aliases (resume only — not for new runs)

Prefer current names on new runs. Accept these when reading old `00-run.md` / handoffs:

| Legacy | Prefer now |
|--------|------------|
| Gate 1 + Gate 2-UI | Gate A |
| Gate 2 | Gate B |
| Gate 3 | Gate C |
| **SPM plan** / **Merged SPM** / mode `merged-spm` | **Lens plan** / **Merged lenses** / `merged-lenses` |
| Stage ids `spm-api` … `spm-memory` | `lens-api` … `lens-memory` |
| “Shared handoff block” | Paste `scripts/handoff-for.py <stage-id>` output ([handoffs.md](handoffs.md) = edit SoT / debug only) |
| Separate test Tasks: Coverage / Add missing e2e / Run suite | One Task `test-full` |
| Mode simple: separate Analyze → Grill → Design | One Task `design-phase` |
| Mode simple: separate API/DB + design-review | One Task `design-verify-phase` |
| Lite: optional separate Adversarial + Quality | **Required** `code-review-phase` / Lite combined when profile lite |
| Lens Result `has findings` | `needs fix` ([results.md](results.md); Critical/Major open → needs fix, else clean) |
| Old Status values without phase bundles | Map to card **Stage id** `design-phase` / `design-verify-phase` / `code-review-phase` / `test-full` / `test-lite` |
| Status used as pipeline position (`ideation`, `review`, `test`, `gate-b`, …) | **Status** = `running\|paused\|stopped\|done` only; put position on **Last stage** / Orchestrator card Stage id |
| **Complexity** as simple\|complex second classifier | Complexity = **one-line reason** only; Mode remains the classifier |

## Renamed subflow skills

| Old name | New name |
|----------|----------|
| `my-design-subflow` | `my-dev-flow-design` |
| `my-design-review-subflow` | `my-dev-flow-design-review` |
| `my-code-subflow` | `my-dev-flow-code` |
| `my-test-subflow` | `my-dev-flow-test` |
| `my-review-subflow` | `my-dev-flow-review` |
| `my-merge-subflow` | `my-dev-flow-merge` |

Treat old trigger phrases as the new skill names.

## Skill install path

Canonical skill text lives in the repo under **`AI/skills/`**. Cursor loads copies from
`~/.cursor/skills/` — keep them in sync with `AI/skills/sync-to-cursor.sh` (optional `--check`).

## Doc layout note

Runtime order: [stages.md](stages.md) **Full/Simple pipeline order**. Progress paths / Task descriptions → [handoffs.md](handoffs.md). HITL → [hitl.md](hitl.md). Models → [models.md](models.md). Lenses → [lenses.md](lenses.md). Parent checklist → [invariants.md](invariants.md). After Build: Mode × Review profile table in stages.md (legal skip-review → [lenses.md](lenses.md) · [hitl.md](hitl.md)).
