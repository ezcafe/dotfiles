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

**After:** Wait siblings (plan 2+). Any planned lens **`needs fix`** → Prefer `fix-review` Mode `merged-lenses` (plan 2+) / `plan-1-lens` (plan 1). Prefer `merge-findings` only when planned lenses **clean** + Merged unpaid (plan 2+). Plan **1**: parent copies Result into Merged. Serial next unpaid `lens-*` only when parent launched serial ([derive-next.md](../../my-dev-flow-v3/derive-next.md) · [lenses-overview.md](lenses-overview.md) · [lenses.md](../../my-dev-flow-v3/lenses.md)).
