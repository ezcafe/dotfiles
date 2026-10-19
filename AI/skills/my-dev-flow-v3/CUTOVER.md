# Cutover v2 → v3

## Rule

- **In-flight v2 runs:** finish on `my-dev-flow-v2` (+ v2 subflows).  
- **New runs:** prefer `my-dev-flow-v3`.  
- Do not mix Mode cards between versions in the same slug.

## What changed in v3

| Topic | v2 | v3 |
|-------|----|----|
| Gate B freshness | Clock compare (HH:MM vs ISO) | **Settle generation** integer |
| Derive load | pre/post split files | Single short [derive-next.md](derive-next.md) |
| Ideation | Implicit | Explicit [brainstorm.md](brainstorm.md) hard-gate |
| Grill | Custom | Mattpocock frontier format |
| TDD | In code skill | Iron law front-and-center |
| Review | Adv/Quality/lenses | + five-axis + structural ambition |
| SoT drift | Many restated bars | One SoT + pointers |

## Mapping

| v2 | v3 |
|----|----|
| `my-dev-flow-v2` | `my-dev-flow-v3` |
| `*-design` / `*-design-review` / `*-code` / `*-review` / `*-test` / `*-merge` | matching `my-dev-flow-v3-*` |

Artifact templates are compatible in spirit; prefer v3 `artifacts/` for new slugs.
