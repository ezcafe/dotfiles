## lens-perf — Performance

**Stage id:** `lens-perf`  
**Skills:** `{performance-optimization}/SKILL.md` + `vercel-react-best-practices` if React/Next  
**Task description:** `Performance review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-v3-review Performance Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Paste output of: compose handoff from {my-dev-flow-v3}/handoffs.md for lens-perf>

Read {performance-optimization}/SKILL.md.
If React/Next UI changed, also read {vercel-react-best-practices}/SKILL.md.

Look for N+1, unbounded fetches, missing pagination, waterfalls, hot-path waste, bundle bloat.
Write .my-docs/workflow/<slug>/05-lens-perf.md using the lens template (Lens: perf).
Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow-v3}/results.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-perf.md.
```

**After:** Return FIRST LINE Result only. Wait siblings (plan 2+) before Hard stop when parent launched parallel. **Hard stop** — do **not** Prefer Next / write card fields. Parent re-derives ([../../my-dev-flow-v3/derive-next-post.md](../../my-dev-flow-v3/derive-next-post.md) · [lenses-overview.md](lenses-overview.md) · [lenses.md](../../my-dev-flow-v3/lenses.md)).

### Ban-when

Shared table — [lenses-overview.md](lenses-overview.md) Ban-when.
