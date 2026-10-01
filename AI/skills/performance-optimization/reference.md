# Performance reference

## Core Web Vitals (field targets)

| Metric | Good | Needs improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |

## Example budgets (tune per project)

```
JS initial (gzip): < 200KB
CSS (gzip): < 50KB
Above-fold image: < 200KB
API p95: < 200ms (adjust to SLA)
```

## Cache layers

| Layer | Use when | Cost |
|-------|----------|------|
| In-process | Small, hot; per-instance staleness OK | Drift across instances |
| Shared (Redis) | Must agree across instances | Network + ops |
| CDN/edge | Public, identical per URL | Invalidation hard |

**Do not cache:** balances, permissions, checkout inventory, or anything where staleness is a correctness bug — unless the product explicitly allows a stated window.

## Index reading (`EXPLAIN ANALYZE`)

| Seeing | Meaning |
|--------|---------|
| Seq Scan on large filtered table | Missing or unusable index |
| rows estimate far from actual | Stale stats |
| Sort above scan | Index misses `ORDER BY` shape |

Composite: equality columns first, then range/sort. Leading `%like` needs different tooling. Expression on column ⇒ expression index.

## Pool exhaustion signature

Every endpoint slow; time spent waiting for a connection; DB sessions mostly idle → pool / multiplexing problem, not “make max bigger” blindly.

## Attempt ledger (example)

| Idea | Baseline → Result | Verdict | Why |
|------|-------------------|---------|-----|
| Memoize row | INP 240→235 | reverted | Inside noise |
| Virtualize list | INP 240→90 | kept | Long tasks gone |

Keep in PR notes or a short `PERF.md` if the team wants history.
