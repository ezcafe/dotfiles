# Severity exit

| Level | Blocks **clean**? |
|-------|-------------------|
| Critical | Yes |
| Major | Yes |
| Enhancement | No — defer |
| Nit / FYI | No |

**Clean (code review / default)** = zero open Critical and Major. Fix ask = Critical/Major only ([size-caps.md](size-caps.md)).

**Clean (design-review overall)** = zero Critical/Major in the overall log **and** API/DB are **`clean`**\|**`skipped`** when required (Has=yes not tiny → isolated `03a-*` Result **clean**; Has=no or Notes `tiny-contract-tweak` → skipped via Notes — missing file alone ≠ skipped when Has=yes). Full rule + tokens: [results.md](results.md) · [lenses.md](lenses.md) · [design-review SKILL](../my-dev-flow-v2-design-review/SKILL.md). Do **not** treat overall design-review clean as severity-only.
