# my-dev-flow-code stages (index)

**Progressive disclosure:** Principles live in [SKILL.md](SKILL.md).  
**Load one file only:** `stages/<stage-id>.md` for the current Task (do not load this whole package of prompts).

Stage-scoped handoff: **required** `scripts/handoff-for.py <stage-id>` (`{my-dev-flow}/handoffs.md` = edit SoT / debug only).  
Verify/Fix/veto: `{my-dev-flow}/verify-and-fix.md` · `{my-dev-flow}/hitl.md`.  
Models: `{my-dev-flow}/models.md`. Parent Happy path: `{my-dev-flow}/stages.md`.

**Owned stage ids:** `tdd-review` · `build` · `fix-tests`

## Per-stage prompts

| Stage id | File |
|----------|------|
| `tdd-review` | [stages/tdd-review.md](stages/tdd-review.md) |
| `build` | [stages/build.md](stages/build.md) |
| `fix-tests` | [stages/fix-tests.md](stages/fix-tests.md) |
| clarity (parent) | [stages/clarity-check.md](stages/clarity-check.md) |
