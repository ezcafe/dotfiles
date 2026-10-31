---
title: Decisions
project: PROJECT_SLUG
tags: [decisions]
entity_type: how-to
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
summary: Practitioner judgment for this project — use-when rules, anti-patterns, and trade-offs grounded in code.
claims: []
confidence: high
aliases: []
---

# Decisions

Actionable judgment for agents and humans. Write **Use X when Y**, not “the system supports X”.

- **Architecture** [[projects/PROJECT_SLUG/architecture|Architecture]] keeps ADR-lite records (Status / Date / Summary / Consequences).
- **This page** keeps the decision layer: rules, anti-patterns, trade-offs you apply while coding.
- Every rule must cite `workspace:` evidence. Prose under `raw/` or `references/` may suggest candidates — confirm in code before claiming.

## Decision rules

| Rule | Use when | Avoid when | Source |
|------|----------|------------|--------|
| … | … | … | `workspace:…` |

## Anti-patterns

| Anti-pattern | Why it hurts | Prefer instead | Source |
|--------------|--------------|----------------|--------|
| … | … | … | `workspace:…` |

## Trade-offs

| Choice A | Choice B | Pick A when | Pick B when | Source |
|----------|----------|-------------|-------------|--------|
| … | … | … | … | `workspace:…` |

## Related architecture decisions

Link ADR-lite rows from Architecture (do not duplicate full tables):

- [[projects/PROJECT_SLUG/architecture#Key decisions and constraints|Architecture — Key decisions]]

## Key claims

- Decision rules match behavior enforced in code at `validated_against` — `workspace:REPO_PATH`

## See also

- [[projects/PROJECT_SLUG/topic-index|Topic index]]
- [[projects/PROJECT_SLUG/architecture|Architecture]]
- [[projects/PROJECT_SLUG/solution-design|Solution design]]
- [[projects/PROJECT_SLUG/glossary|Glossary]]
