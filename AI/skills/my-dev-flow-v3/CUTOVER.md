# Cutover → v3

## Rule

- **New runs:** use `my-dev-flow-v3` (+ v3 subflows).
- **v2 removed:** `my-dev-flow-v2*` is no longer in SoT or Cursor discovery. Do not resume a v2 skill path.
- **v1:** kept discoverable only for in-flight v1 resumes; prefer v3 for new work.
- Do not mix Mode cards between versions in the same slug.

## What changed in v3 (vs former v2)

| Topic | Former v2 | v3 |
|-------|-----------|----|
| Gate B freshness | Clock compare (HH:MM vs ISO) | **Settle generation** integer |
| Derive load | pre/post split files | Thin [derive-next.md](derive-next.md) (Definitions + Unsafe) + [derive-next-pre.md](derive-next-pre.md) / [derive-next-post.md](derive-next-post.md) halves |
| Ideation | Implicit | Explicit [brainstorm.md](brainstorm.md) hard-gate (always; Prefer `ideation` while **ideation unpaid** = ¬Notes `ideation-confirmed` ∧ ¬Notes `ideation-skip`; both Modes) |
| Grill | Custom | Mattpocock frontier format |
| TDD plan review | Prefer `tdd-review` + token `needs more tests` | **Restored** Prefer only when **04a unpaid / dirty**; Prefer `gate-b` when **04a ok** (incl. ¬ planned tests); Result `needs more tests` ([results.md](results.md) · [derive-next.md](derive-next.md)) |
| TDD build | In code skill | Iron law front-and-center |
| Review | Adv/Quality/lenses | + five-axis + structural ambition |
| SoT drift | Many restated bars | One SoT + pointers |

## Mapping

| Former v2 | v3 |
|-----------|----|
| `my-dev-flow-v2` | `my-dev-flow-v3` |
| `*-design` / `*-design-review` / `*-code` / `*-review` / `*-test` / `*-merge` | matching `my-dev-flow-v3-*` |

Artifact templates are compatible in spirit; prefer v3 `artifacts/` for new slugs.
