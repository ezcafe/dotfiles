# my-dev-flow-merge stages (index)

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task (do not load this whole package of prompts).

Stage-scoped handoff: **required** `scripts/handoff-for.py <stage-id>` (`{my-dev-flow}/handoffs.md` = edit SoT / debug only).  
Gate C bar: `{my-dev-flow}/hitl-gate-c.md`. Provenance: `{my-dev-flow}/hitl.md`. Models: `{my-dev-flow}/models.md`.  
Parent Happy path / Status: `{my-dev-flow}/stages.md`.  
PR body: `{my-dev-flow}/artifacts/pr-body.md` (not INDEX.md).

**Owned stage ids:** `merge`

## Per-stage prompts

| Stage id | File |
|----------|------|
| `merge` | [stages/merge.md](stages/merge.md) |
