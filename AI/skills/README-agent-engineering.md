# Agent engineering skills

Cursor-optimized adaptations of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). Concise workflows with safety rails; deep examples live in each skill’s `reference.md` where needed.

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
| [my-plan-flow](my-plan-flow/SKILL.md) | Full delivery pipeline; includes [grill.md](my-plan-flow/grill.md) (design-tree frontier + glossary/ADR) |
| [myplan](myplan/SKILL.md) | Discovery → spec → plan (use *before* task breakdown) |
| [vercel-react-best-practices](vercel-react-best-practices/SKILL.md) | React/Next performance rule catalog |
| [clean-minimal-ui](clean-minimal-ui/SKILL.md) | Visual tokens and clean-minimal styling |
| [web-design-guidelines](web-design-guidelines/SKILL.md) | UI guideline compliance audit |

## Project overrides

If the repo has `AGENTS.md`, `CLAUDE.md`, or `docs/DESIGN_GUIDE.md`, those win over generic skill advice.
