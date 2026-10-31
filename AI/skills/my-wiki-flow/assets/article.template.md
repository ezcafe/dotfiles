---
title: Page title
project: project-slug
tags: []
entity_type: explanation
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD
summary: One sentence for agents and index listings.
claims: []
confidence: low
aliases: []
---

# Page title

**When to use this file:** overflow notes under `projects/{slug}/references/` only
(long dumps, catalogs). Prefer the canonical templates in
`assets/project-pages/` (Architecture, Solution design, Glossary, how-to, concept)
and `solution-design-feature.md` for features.

Literature / prose fold-in starts at `confidence: low` until confirmed in code.

## Content

Use GFM tables and Mermaid where the page role requires them (see project-structure.md).

## Key claims

- Cite `workspace:` paths for `confidence: high`, or mark `confidence: low` + source.

## See also

- [[projects/project-slug/topic-index|Topic index]]
- [[projects/project-slug/architecture|Architecture]]
- [[projects/project-slug/decisions|Decisions]]
