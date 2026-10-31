---
title: Topic index
project: PROJECT_SLUG
tags: [routing, topic-index]
entity_type: reference
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
summary: Thin topic → page map for agents — load this before opening full project pages.
claims: []
confidence: high
aliases: []
---

# Topic index

Routing only. Keep this page short. Agents: match the user question to a **Topic**, open the linked page, then answer. Do not paste the whole project into context.

## Topic map

| Topic | Page | Notes |
|-------|------|-------|
| architecture / deploy / boundaries | [[projects/PROJECT_SLUG/architecture]] | Project-wide structure |
| decisions / trade-offs / when to use | [[projects/PROJECT_SLUG/decisions]] | Judgment rules |
| glossary / naming | [[projects/PROJECT_SLUG/glossary]] | Terms |
| features (hub) | [[projects/PROJECT_SLUG/solution-design]] | Feature index |

After feature confirmation, add one row per feature pointing at `projects/PROJECT_SLUG/solution-design/{feature-slug}`.
Add how-to rows for ops tasks under `projects/PROJECT_SLUG/how-to/{task}`.
Add synonym rows when the same page answers multiple phrasings (e.g. `auth` and `login`).

## Key claims

- Topic rows point at real wiki pages for this project at `validated_against` — `workspace:REPO_PATH`

## See also

- [[projects/PROJECT_SLUG/architecture|Architecture]]
- [[projects/PROJECT_SLUG/decisions|Decisions]]
- [[projects/PROJECT_SLUG/solution-design|Solution design]]
- [[projects/PROJECT_SLUG/glossary|Glossary]]
