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

One page per feature or substantial change under `solution-design/`.
Group related work under a master feature row; link to each feature page.
Each feature page must include a Mermaid **`sequenceDiagram`** (not flowchart or C4).
Keep full contracts and schemas in their canonical files; link instead of copying.

## Feature index

Confirm the feature list with the user (see project-structure feature discovery), then add rows.
Use `wiki-add-feature.sh PROJECT_SLUG {feature} [master]` to create pages.

| Master feature | Feature page | Status | Entry points in code |
|----------------|--------------|--------|----------------------|
| _(none yet)_ | — | — | — |

## How to add a feature page

1. Run `wiki-add-feature.sh PROJECT_SLUG {feature-slug} [master-feature]` (or copy the skill template).
2. Fill every required section from **code** (handlers, schemas, tests) — not from README/docs.
3. Set `nav_group:` (or `master_feature:`) to the master feature name so the sidebar nests the page under this hub.
4. Add a row to the table above.
5. Set `validated_against` on the feature page.

## Key claims

-

## See also

- [[projects/PROJECT_SLUG/architecture|Architecture]]
- [[projects/PROJECT_SLUG/glossary|Glossary]]
