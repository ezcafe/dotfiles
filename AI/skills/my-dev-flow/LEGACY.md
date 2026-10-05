# my-dev-flow legacy (do not create on new runs)

These steps and artifacts were **removed**. New runs ignore them.

| Removed | What it was | What to do instead |
|---------|-------------|--------------------|
| **Gate A2** | UI look gate | Specify UI in `03-design.md` / `04-tasks.md`; match existing app chrome + Gate A 80/20 |
| **`01b-ui-concept.md`** | Separate UI concept doc | UI specs live in Design when **Has UI** |
| **`ui-refs/`** | Look-gate screenshots / :8765 serve | Do not create; do not serve look-gate servers |

**Resume old runs:** treat Gate A2 / `01b` / `ui-refs` as skipped/N/A. Do not re-open them.

**Aliases (still valid):** Gate 1 + Gate 2-UI ≈ Gate A; Gate 2 ≈ Gate B; Gate 3 ≈ Gate C; **SPM plan** ≈ **Lens plan** (prefer **Lens plan** in new docs); stage ids `spm-api` … `spm-memory` ≈ lens Tasks (prefer **Lens plan** wording in chat); **Merged SPM** ≈ **Merged lenses** in `05-review-log.md`.

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
