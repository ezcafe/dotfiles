# Gate C

**SoT for:** Test bar + Gate C approved. Always **blocking**. Provenance: [hitl.md](hitl.md).

## Test bar (before merge)

| Review profile | Required |
|----------------|----------|
| **skip-review** | Legal per [lenses.md](lenses.md) **and** verify-pass + smoke-pass **and** one escape **with matching Notes↔provenance pair** ([hitl.md](hitl.md)): Notes `smoke-pass (re-run)` ↔ provenance `smoke-pass-rerun`; or `docs-only` ↔ `docs-only`; or `smoke-waive` / `gate-c-test-override` with same-kind provenance. Build-writes-Smoke alone is **not** enough. Escape kinds are valid **only** under skip-review. |
| **lite** | `06-test-log.md` Result **success** and **Test path last run:** `lite` — no escape / waiver substitute |
| **full** | `06-test-log.md` Result **success** and **Test path last run:** `full` — no escape / waiver substitute |

## Gate C approved

```markdown
**Gate C approved:** commit,push,pr,merge
- provenance — gate-c-approved — user: "commit push PR and merge"
```

| Value | Meaning |
|-------|---------|
| `none` | Not settled |
| subset of `commit`,`push`,`pr`,`merge` | Only what the user named |

Do not invent actions. Merge Task re-reads field before git/remote work.

After Merge Result **success** and `merge` ∈ approved → Status **`done`**. Subset without merge → stay `paused`.
