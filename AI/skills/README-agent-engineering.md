# Agent engineering skills

Cursor-optimized adaptations of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). Concise workflows with safety rails; deep examples live in each skill’s `reference.md` where needed.

## Source of truth and Cursor sync

**Canonical copy:** this directory (`AI/skills/` in the dotfiles repo).

Cursor discovers skills from `~/.cursor/skills/`. After editing here, sync:

```bash
./AI/skills/sync-to-cursor.sh
```

That copies each package with a `SKILL.md` into `~/.cursor/skills/<name>/` without deleting unrelated skills. Task prompts should resolve `{skill-name}` to `AI/skills/<name>/` first (see [my-dev-flow/skills-path.md](my-dev-flow/skills-path.md)).

## When to use which

| Skill | Use when |
|-------|----------|
| [planning-and-task-breakdown](planning-and-task-breakdown/SKILL.md) | Spec exists; need ordered, verifiable tasks |
| [api-and-interface-design](api-and-interface-design/SKILL.md) | Designing APIs, module contracts, or public interfaces |
| [frontend-ui-engineering](frontend-ui-engineering/SKILL.md) | Building UI structure, state, a11y, loading/empty/error |
| [security-and-hardening](security-and-hardening/SKILL.md) | Auth, input, secrets, SSRF, supply chain, LLM features |
| [performance-optimization](performance-optimization/SKILL.md) | Measured slowness, CWV, N+1, caching, indexes |
| [code-simplification](code-simplification/SKILL.md) | Code works but is hard to read; refactor without behavior change |
| [code-review-and-quality](code-review-and-quality/SKILL.md) | Before merge; multi-axis review of a change |
| [documentation-and-adrs](documentation-and-adrs/SKILL.md) | Recording *why*; sparse ADRs + glossary (used by Grill) |

## Complementary skills (already installed)

| Skill | Role |
|-------|------|
| [my-dev-flow](my-dev-flow/SKILL.md) | Full delivery pipeline; Speed defaults (simple phase bundles, test-full one Task); [stages.md](my-dev-flow/stages.md); [verify-and-fix.md](my-dev-flow/verify-and-fix.md); [severity.md](my-dev-flow/severity.md) |
| [my-dev-flow-design](my-dev-flow-design/SKILL.md) | Design phase (Ideation → Grill → Design) |
| [my-dev-flow-design-review](my-dev-flow-design-review/SKILL.md) | Design verification (+ isolated API/DB reviews) |
| [my-dev-flow-code](my-dev-flow-code/SKILL.md) | TDD review + Build / Fix (Verify gate; Smoke Option B) |
| [my-dev-flow-test](my-dev-flow-test/SKILL.md) | Smoke re-run / full / lite (uses Verify commands) |
| [my-dev-flow-review](my-dev-flow-review/SKILL.md) | Code review lenses (`lens-*` stage ids) |
| [my-dev-flow-merge](my-dev-flow-merge/SKILL.md) | Gate C → commit / push / PR / merge |
| [my-gtd-flow](my-gtd-flow/SKILL.md) | Lazy GTD: GitHub Projects / Reminders, Calendar / Outlook, 9–5 plan |
| [myplan](myplan/SKILL.md) | Discovery → spec → plan (use *before* task breakdown) |
| [vercel-react-best-practices](vercel-react-best-practices/SKILL.md) | React/Next performance rule catalog |
| [clean-minimal-ui](clean-minimal-ui/SKILL.md) | Visual tokens and clean-minimal styling |
| [web-design-guidelines](web-design-guidelines/SKILL.md) | UI guideline compliance audit |

## Project overrides

If the repo has `AGENTS.md`, `CLAUDE.md`, or `docs/DESIGN_GUIDE.md`, those win over generic skill advice.
