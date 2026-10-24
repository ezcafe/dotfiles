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
| [my-dev-flow-v3](my-dev-flow-v3/SKILL.md) | **Current** end-to-end delivery orchestrator (settle gen; seed only `00-run.md`; isolated subflow Tasks). Prefer for new runs — [CUTOVER.md](my-dev-flow-v3/CUTOVER.md) |
| [my-dev-flow-v3-design](my-dev-flow-v3-design/SKILL.md) | v3 design (Ideation → Grill → Design / design-phase) |
| [my-dev-flow-v3-design-review](my-dev-flow-v3-design-review/SKILL.md) | v3 design verification (+ isolated API/DB) |
| [my-dev-flow-v3-code](my-dev-flow-v3-code/SKILL.md) | v3 TDD → Build → Fix |
| [my-dev-flow-v3-review](my-dev-flow-v3-review/SKILL.md) | v3 Adv / Quality / lenses / code-review-phase |
| [my-dev-flow-v3-test](my-dev-flow-v3-test/SKILL.md) | v3 Smoke / test-full / test-lite |
| [my-dev-flow-v3-merge](my-dev-flow-v3-merge/SKILL.md) | v3 Gate C → commit / push / PR / merge |
| [my-dev-flow](my-dev-flow/SKILL.md) | **v1 resume-only** — in-flight v1 cards; not for new runs. Full pipeline + Speed defaults; [stages.md](my-dev-flow/stages.md); [results.md](my-dev-flow/results.md); [parent-next.md](my-dev-flow/parent-next.md); [failure-playbook.md](my-dev-flow/failure-playbook.md); [verify-and-fix.md](my-dev-flow/verify-and-fix.md); [severity.md](my-dev-flow/severity.md); lint `scripts/lint-run.py` |
| [my-dev-flow-design](my-dev-flow-design/SKILL.md) | v1 design (resume-only with v1 orchestrator) |
| [my-dev-flow-design-review](my-dev-flow-design-review/SKILL.md) | v1 design verification (resume-only) |
| [my-dev-flow-code](my-dev-flow-code/SKILL.md) | v1 TDD review + Build / Fix (resume-only) |
| [my-dev-flow-test](my-dev-flow-test/SKILL.md) | v1 Smoke re-run / full / lite (resume-only) |
| [my-dev-flow-review](my-dev-flow-review/SKILL.md) | v1 code review lenses (resume-only) |
| [my-dev-flow-merge](my-dev-flow-merge/SKILL.md) | v1 Gate C → commit / push / PR / merge (resume-only) |
| [my-gtd-flow](my-gtd-flow/SKILL.md) | Lazy GTD: GitHub Projects / Reminders, Calendar / Outlook, 9–5 plan |
| [myplan](myplan/SKILL.md) | Discovery → spec → plan (use *before* task breakdown) |
| [vercel-react-best-practices](vercel-react-best-practices/SKILL.md) | React/Next performance rule catalog |
| [clean-minimal-ui](clean-minimal-ui/SKILL.md) | Visual tokens and clean-minimal styling |
| [web-design-guidelines](web-design-guidelines/SKILL.md) | UI guideline compliance audit |

## Project overrides

If the repo has `AGENTS.md`, `CLAUDE.md`, or `docs/DESIGN_GUIDE.md`, those win over generic skill advice.
