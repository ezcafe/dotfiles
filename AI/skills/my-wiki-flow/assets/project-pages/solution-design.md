---
title: Solution design
project: PROJECT_SLUG
tags: [solution-design, features]
entity_type: concept
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
summary: Master index of feature-level solution designs for this project.
claims: []
---

# Solution design

One page per feature under `solution-design/`. Group related work under a master feature. Each feature page uses Mermaid **`sequenceDiagram`**. Link canonical schemas; full API field tables only when the feature owns the contract.

> **Tip** Confirm the feature list before adding pages. Prefer depth on complex flows over many shallow CRUD pages.

## Feature index

Confirm the feature list with the user, then add rows.
Use `wiki-add-feature.sh PROJECT_SLUG {feature} [master]` to create pages.

| Master feature | Feature page | Owner | Status | Entry points in code |
|----------------|--------------|-------|--------|----------------------|
| _(none yet)_ | — | — | — | — |

## How to add a feature page

1. Run `wiki-add-feature.sh PROJECT_SLUG {feature-slug} [master-feature]`.
2. Fill sections from **code** — not README/docs.
3. Set `nav_group:` (or `master_feature:`) so the sidebar nests under this hub.
4. Add a row to the table above (include Owner and Status).
5. Set `validated_against` on the feature page.
6. API: Spec summary always; full field tables + curl only when **Owns contract?** is `yes`.

## Key claims

- Feature index matches confirmed discovery list — `workspace:REPO_PATH`

## See also

- [[projects/PROJECT_SLUG/architecture|Architecture]]
- [[projects/PROJECT_SLUG/glossary|Glossary]]
