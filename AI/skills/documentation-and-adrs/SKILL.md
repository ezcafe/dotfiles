---
name: documentation-and-adrs
description: >-
  Records architectural decisions and durable context. Use when making
  significant technical choices, changing public APIs, shipping behavior
  changes, or capturing why future engineers and agents need. Do not document
  obvious code or throwaway prototypes.
---

# Documentation and ADRs

Cursor-optimized adaptation of [addyosmani/agent-skills documentation-and-adrs](https://github.com/addyosmani/agent-skills/tree/main/skills/documentation-and-adrs). Document *why* — code already shows *what*.

## Project first

- Match existing ADR location/format if present (`docs/adr*`, `docs/decisions*`, `.adr-dir`, tooling).
- Follow `AGENTS.md` / `CLAUDE.md` for doc conventions.
- If conventions conflict, surface the conflict — do not invent a second scheme.

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Capture context, alternatives, and consequences for expensive decisions. Comment *why*, not *what*. |
| **Ask first** | Overwrite or replace unfinished plans/docs that belong to other in-flight work. |
| **Never** | Delete old ADRs (supersede instead). Leave large commented-out blocks. Write ADRs for trivial choices. |

## When to write an ADR (three-part bar)

Write an ADR **only when all three** are true (from domain-modeling / my-plan-flow Grill):

1. **Hard to reverse** — changing later is costly
2. **Surprising without context** — a future reader will wonder why
3. **Real trade-off** — genuine alternatives existed and you picked for specific reasons

Typical yes cases: framework / major dependency; data model or auth strategy; API architecture (REST vs GraphQL vs RPC); hosting / build / infra lock-in; context boundaries; deliberate deviation from the obvious path.

Skip ADRs for local refactors, one-line fixes, easy-to-reverse UI tweaks, and “we did the obvious thing.”

## ADR workflow

1. Search for existing ADRs and numbering scheme
2. If none: use `docs/decisions/ADR-NNN-short-title.md` (zero-pad as project prefers; start `001` only when empty). Prefer `docs/adr/` if that folder already exists.
3. Status lifecycle: `Proposed` → `Accepted` → `Superseded` / `Deprecated`
4. New decision that replaces an old one: new ADR that references and supersedes the old — keep the old file

### Prefer short form (default)

Most ADRs are enough as **1–3 sentences**: context, decision, why.

```markdown
# ADR-NNN: Title

**Status:** Accepted · **Date:** YYYY-MM-DD

{Context}. We chose {decision} because {why}. Rejected {alt} because {reason}.
```

### Long form (optional — when rejected options or consequences matter)

```markdown
# ADR-NNN: Title

## Status
Accepted

## Date
YYYY-MM-DD

## Context
What problem and constraints?

## Decision
What we chose.

## Alternatives considered
### Option A
- Pros / Cons
- Why rejected or not chosen

## Consequences
Follow-ups, risks, what becomes easier/harder.
```

## Glossary (with Grill)

When settling domain terms during grill / design:

- Prefer repo-root `GLOSSARY.md`, or follow `GLOSSARY-MAP.md` for multi-context repos
- Create lazily on the first resolved term
- Definitions only — no implementation paths; pick one canonical term + `_Avoid_:` aliases
- Update inline when a term resolves (do not batch)

## Inline docs

**Do comment:** non-obvious intent, invariants, gotchas, links to ADRs.

**Do not comment:** restating the next line; TODOs you can do now; dead commented-out code (delete; git has history).

## API docs

Prefer types + short JSDoc on public functions (`@param`, `@returns`, `@throws`, one `@example` when non-obvious). OpenAPI only if the project already uses it.

## README bar (if missing or stale)

Quick start, main commands table, short architecture pointer (+ link to ADRs), how to contribute / PR bar. Keep it short.

## Agent-oriented docs

Keep `AGENTS.md` / rules current when conventions change so agents do not re-decide settled issues.

## Checklist

- [ ] ADR exists for each expensive decision in this change (or explicitly N/A with three-part bar reason)
- [ ] Glossary updated when new domain terms were settled (or N/A)
- [ ] Existing ADR convention matched
- [ ] No unfinished unrelated plan overwritten without asking
- [ ] Comments explain why / gotchas only
- [ ] Public surfaces have types (and minimal docs if public)

## Related

- Spec first: [myplan](../myplan/SKILL.md)
- Grill + domain modeling: [my-plan-flow/grill.md](../my-plan-flow/grill.md)
- Task lists after a spec: [planning-and-task-breakdown](../planning-and-task-breakdown/SKILL.md)
