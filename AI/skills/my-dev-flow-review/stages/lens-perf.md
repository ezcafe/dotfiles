## lens-perf — Performance

**Stage id:** `lens-perf`  
**Skills:** `{performance-optimization}/SKILL.md` + `vercel-react-best-practices` if React/Next  
**Task description:** `Performance review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-review Performance Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Stage-scoped handoff for stage id lens-perf from {my-dev-flow}/handoffs.md>

Read {performance-optimization}/SKILL.md.
If React/Next UI changed, also read {vercel-react-best-practices}/SKILL.md.

Look for N+1, unbounded fetches, missing pagination, waterfalls, hot-path waste, bundle bloat.
Write .my-docs/workflow/<slug>/05-lens-performance.md using the lens template (Lens: performance).
Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow}/results.md · severity.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-performance.md.
```
