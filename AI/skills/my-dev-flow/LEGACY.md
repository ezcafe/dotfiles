# my-dev-flow legacy (do not create on new runs)

These steps and artifacts were **removed**. New runs ignore them.

| Removed | What it was | What to do instead |
|---------|-------------|--------------------|
| **Gate A2** | UI look gate | Specify UI in `03-design.md` / `04-tasks.md`; match existing app chrome + Gate A 80/20 |
| **`01b-ui-concept.md`** | Separate UI concept doc | UI specs live in Design when **Has UI** |
| **`ui-refs/`** | Look-gate screenshots / :8765 serve | Do not create; do not serve look-gate servers |

**Resume old runs:** treat Gate A2 / `01b` / `ui-refs` as skipped/N/A. Do not re-open them.

**Aliases (still valid):**

| Legacy | Prefer now |
|--------|------------|
| Gate 1 + Gate 2-UI | Gate A |
| Gate 2 | Gate B |
| Gate 3 | Gate C |
| **SPM plan** | **Lens plan** |
| Stage ids `spm-api` … `spm-memory` | `lens-api` … `lens-memory` (accept old ids on resume) |
| **Merged SPM** / mode `merged-spm` | **Merged lenses** / mode `merged-lenses` |
| Separate test Tasks: Coverage / Add missing e2e / Run suite | One Task `test-full` (resume: treat old three as that step) |
| Mode simple: separate Analyze → Grill → Design | One Task `design-phase` |
| Mode simple: separate API/DB + design-review | One Task `design-verify-phase` |
| Lite: optional separate Adversarial + Quality | **Required** `code-review-phase` / Lite combined when profile lite |

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
`~/.cursor/skills/` — keep them in sync with `AI/skills/sync-to-cursor.sh`.
