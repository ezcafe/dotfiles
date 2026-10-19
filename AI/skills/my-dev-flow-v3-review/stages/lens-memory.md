## lens-memory — Memory

**Stage id:** `lens-memory`  
**Task description:** `Memory review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-v3-review Memory Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Paste output of: compose handoff from {my-dev-flow-v3}/handoffs.md for lens-memory>

Checklist:
- Listener / subscription / timer leaks; missing cleanup
- Unbounded caches or in-memory lists
- Large retained closures or growing module-level state
- Holding whole result sets when streaming/pagination is needed
- Bad casts on money/sum columns (e.g. bigint SUM forced to int4)
- Unnecessary retained references in long-lived objects

Write .my-docs/workflow/<slug>/05-lens-memory.md using the lens template (Lens: memory).
Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow-v3}/results.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-memory.md.
```

**After:** Wait siblings (plan 2+). Any planned lens **`needs fix`** → Prefer `fix-review` Mode `merged-lenses` (plan 2+) / `plan-1-lens` (plan 1). Prefer `merge-findings` only when planned lenses **clean** + Merged unpaid (plan 2+). Plan **1**: parent copies Result into Merged. Serial next unpaid `lens-*` only when parent launched serial ([derive-next.md](../../my-dev-flow-v3/derive-next.md) · [lenses-overview.md](lenses-overview.md) · [lenses.md](../../my-dev-flow-v3/lenses.md)).
