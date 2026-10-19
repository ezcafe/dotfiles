# my-dev-flow-test stages (index)

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task (do not load this whole package of prompts).

Stage-scoped handoff: **required** `scripts/handoff-for.py <stage-id>` (`{my-dev-flow}/handoffs.md` = edit SoT / debug only).  
Verify: `{my-dev-flow}/verify-and-fix.md`. Gate C bar: `{my-dev-flow}/hitl-gate-c.md`. Provenance: `{my-dev-flow}/hitl.md`.  
Models: `{my-dev-flow}/models.md`. Parent Happy path: `{my-dev-flow}/stages.md`.  
Template: `{my-dev-flow}/artifacts/06-test-log.md`.

**Owned stage ids:** `smoke` · `test-full` · `test-lite`

## Per-stage prompts

| Stage id | File |
|----------|------|
| `smoke` | [stages/smoke.md](stages/smoke.md) |
| `test-lite` | [stages/test-lite.md](stages/test-lite.md) |
| `test-full` | [stages/test-full.md](stages/test-full.md) |
