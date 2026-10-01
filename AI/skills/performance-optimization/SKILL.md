---
name: performance-optimization
description: >-
  Optimizes performance with measure-first workflow across frontend, backend,
  queries, and caching. Use when CWV or latency regresses, N+1 appears, bundles
  grow, or SLAs exist. Defers React/Next rule catalogs to vercel-react-best-practices.
---

# Performance Optimization

Cursor-optimized adaptation of [addyosmani/agent-skills performance-optimization](https://github.com/addyosmani/agent-skills/tree/main/skills/performance-optimization). Measure → fix one bottleneck → re-measure. Guessing is not a strategy.

## Project first

- React/Next specific rules → [vercel-react-best-practices](../vercel-react-best-practices/SKILL.md)
- Follow existing APM, logging, and DB access patterns in the repo

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Establish a baseline before changing code. Change one variable per experiment. Keep tests green. Revert neutral or worse results. |
| **Ask first** | `CREATE INDEX` / DDL on shared or production DBs; connection pool size changes; new shared cache (Redis) infrastructure; public `Cache-Control` on authenticated responses. |
| **Never** | Optimize without evidence. Keep complexity that did not beat noise. Skip validation/auth to “go faster.” Cache per-user data under a key that omits the viewer. |

## Workflow

```
1. MEASURE  → baseline (synthetic + RUM when user-facing)
2. IDENTIFY → real bottleneck from data
3. FIX      → one change aimed at that bottleneck
4. VERIFY   → same method/conditions; keep or revert
5. GUARD    → budget or monitor on the user-felt metric
```

### Symptom → where to look

| Slow thing | Start here |
|------------|------------|
| First load | Bundle, TTFB, render-blocking, LCP image |
| Click/input lag | Long tasks, re-renders, large DOM |
| After navigation | API waterfalls, client render |
| One API | Query plan, indexes, N+1 |
| All APIs | Pool exhaustion, CPU/mem, locks |
| Intermittent | GC, external deps, lock contention |

### Common fixes (do after measuring)

- **N+1** — join/include/dataloader; one round trip
- **Unbounded lists** — pagination / limits
- **Index** — `EXPLAIN ANALYZE` before and after; index for filter+sort shape; revert unused indexes (write tax)
- **Pool** — one pool per process; `instances × max` under DB `max_connections`; proxy when serverless multiplies
- **Images** — dimensions, modern formats, `fetchpriority` for LCP, lazy below fold
- **Bundle** — route-level `lazy` / dynamic import for heavy rare UI
- **Cache** — only expensive + read-heavy data; key must include every input that changes the response (tenant, locale, auth); one invalidation strategy; stampede protection

React memo/`useMemo` everywhere is a smell — profile first. Details: [reference.md](reference.md).

### Verify rule

| Result vs baseline | Action |
|--------------------|--------|
| Clear win, tests green | Keep; record before/after |
| Inside noise / worse / tests red | **Revert** |

Neutral is a revert. Log attempts (kept and reverted) so the next agent does not repeat failures.

## Checklist

- [ ] Before/after numbers exist (same method)
- [ ] Improvement exceeds run-to-run noise
- [ ] Neutrals reverted
- [ ] Attempt logged
- [ ] No N+1 / unbounded fetch in new paths
- [ ] New index justified by plans; write cost considered
- [ ] New cache: key inputs + staleness stated
- [ ] User-felt metric has a budget or monitor when appropriate
- [ ] Tests still pass

## Related

- [reference.md](reference.md) — CWV targets, cache layers, index notes
- [vercel-react-best-practices](../vercel-react-best-practices/SKILL.md)
- [code-review-and-quality](../code-review-and-quality/SKILL.md)
