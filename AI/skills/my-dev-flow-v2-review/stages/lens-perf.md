## lens-perf — Performance

**Stage id:** `lens-perf`  
**Skills:** `{performance-optimization}/SKILL.md` + `vercel-react-best-practices` if React/Next  
**Task description:** `Performance review`

**Task prompt:**

```
You are a Senior Verifier for my-dev-flow-v2-review Performance Review. Fresh context only. You run in parallel with other lenses — write ONLY your lens file; do not edit 05-review-log.md or other lens files. Do not fix code.

<Paste output of: compose handoff from {my-dev-flow-v2}/handoffs.md for lens-perf>

Read {performance-optimization}/SKILL.md.
If React/Next UI changed, also read {vercel-react-best-practices}/SKILL.md.

Look for N+1, unbounded fetches, missing pagination, waterfalls, hot-path waste, bundle bloat.
Write .my-docs/workflow/<slug>/05-lens-perf.md using the lens template (Lens: perf).
Result = **needs fix** if any Critical/Major open; **clean** if none ({my-dev-flow-v2}/results.md · severity.md).
Return FIRST LINE exactly: Result: clean | needs fix
Then path to 05-lens-perf.md.
```

**After:** Lens plan **2+** (parent parallel): wait sibling lenses → `merge-findings` (do **not** Fix yet — even on needs fix). Plan **1** lens: clean → test; needs fix → `fix-review` Mode `plan-1-lens`. Serial next unpaid `lens-*` only when parent launched serial ([derive-next.md](../../my-dev-flow-v2/derive-next.md) · [lenses-overview.md](lenses-overview.md)).
