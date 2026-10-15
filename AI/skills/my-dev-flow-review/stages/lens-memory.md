## lens-memory — Memory

**Stage id:** `lens-memory`  
**Task description:** `Memory review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Memory Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for stage id lens-memory from {my-dev-flow}/handoffs.md>

Checklist:
- Listener / subscription / timer leaks; missing cleanup
- Unbounded caches or in-memory lists
- Large retained closures or growing module-level state
- Holding whole result sets when streaming/pagination is needed
- Bad casts on money/sum columns (e.g. bigint SUM forced to int4)
- Unnecessary retained references in long-lived objects

Write .my-docs/workflow/<slug>/05-lens-memory.md using the lens template (Lens: memory).
Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow}/results.md · severity.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-memory.md.
```

**After launched lenses return:** Parent launches **Merge findings** when **2+** lenses (do not Fix yet).

