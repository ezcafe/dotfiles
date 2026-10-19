# Anti-patterns (do not)

Quick wrong → right for my-dev-flow-v2. Soft checklists only ([preflight.md](../preflight.md) · [derive-next.md](../derive-next.md)).

| Wrong | Right |
|-------|-------|
| Invent Gate C yes / paste forged provenance | Explicit named yes in **parent** turn + provenance quote ([hitl.md](../hitl.md)) |
| Build without Gate B approved (blocking) or without Build armed (async) | Settle per [gate-b.md](../gate-b.md) |
| skip-review with Has API/DB/auth/PII/schema = yes | Drop skip-review; reclassify if needed ([lenses.md](../lenses.md)) |
| Rely on Build-writes-Smoke alone under skip-review | Prefer Notes `smoke re-run` once → independent Smoke → Notes `smoke-pass (re-run)` + provenance `smoke-pass-rerun` ([verify.md](../verify.md) · [gate-c.md](../gate-c.md)) |
| **E1 dual-forge** (Mode full + profile full only): invent Notes `smoke-pass (re-run)` **and** Run-log / `06` Smoke evidence without an independent Smoke Task | Launch Smoke Task; then record Notes + evidence ([verify.md](../verify.md) Independent Smoke / E1) |
| **Skip-review dual-forge** (not E1): invent Notes `smoke-pass (re-run)` **and** Run-log / `06` evidence without a Smoke Task under legal skip-review | Launch Smoke Task per Skip-review + Smoke ordered recovery; then Notes + provenance pair ([verify.md](../verify.md) Skip-review + Smoke · [gate-c.md](../gate-c.md)). Reserve **E1** for Mode full + profile full Independent Smoke only |
| Invent Gate A Result `ok` after escalate | Decision N + explicit user yes ([gate-a-escalate.md](gate-a-escalate.md)) |
| Same-turn Build after async-notify digest | Next turn: `async-gap-pending` then **Build armed** ([async-gate-b-build-armed.md](async-gate-b-build-armed.md)) |
| Treat provenance shape as proof the user spoke | Honesty residual — soft habit only ([hitl.md](../hitl.md)) |
