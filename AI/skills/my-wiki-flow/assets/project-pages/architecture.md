---
title: Architecture
project: PROJECT_SLUG
tags: [architecture]
entity_type: concept
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
summary: Project-wide architecture — interactions, components, data flows, deployment, and constraints.
claims: []
---

# Architecture

Project-wide structure only. Feature-specific sequence diagrams belong in [[projects/PROJECT_SLUG/solution-design|Solution design]].

## Purpose and scope

Architectural boundaries and what this page covers (and what it deliberately omits).

## Interaction diagram

Use a **Mermaid C4 Dynamic / interaction diagram** (`C4Dynamic`). Show numbered runtime interactions among major components derived from real call paths. Do not use flowchart or `C4Component` here. Feature-level sequences stay on Solution design pages.

```mermaid
C4Dynamic
title Interaction diagram — PROJECT_SLUG

Container(ui, "UI", "…", "Client-facing surface")
Container_Boundary(app, "Application") {
  Component(api, "API", "…", "Request handlers / routes")
  Component(domain, "Domain", "…", "Business logic")
}
ContainerDb(db, "Database", "…", "Primary store")

Rel(ui, api, "1. Requests", "HTTPS/JSON")
Rel(api, domain, "2. Delegates")
Rel(domain, db, "3. Reads/writes")

UpdateElementStyle(ui, $bgColor="#eaf3ff", $borderColor="#3366cc")
UpdateElementStyle(api, $bgColor="#e8f5e9", $borderColor="#2a7a3a")
UpdateElementStyle(domain, $bgColor="#fff8e6", $borderColor="#fc3")
UpdateElementStyle(db, $bgColor="#eef2f5", $borderColor="#54595d")
```

Reference: [Mermaid C4 Dynamic](https://mermaid.js.org/syntax/c4.html) (interaction / dynamic view). Site theme + `UpdateElementStyle` supply colors.

> **Note:** If `C4Dynamic` fails to render in the browser, replace the fence with a `flowchart` that shows the same numbered interactions and include the phrase `C4Dynamic unavailable` in the block so `wiki-lint.py` accepts the fallback.

## Component responsibilities

| Component | Path / package | Responsibility |
|-----------|----------------|----------------|
| … | `…` | … |

## Key interactions and data flows

How components communicate (sync APIs, events, queues). Summarize; detail sequences on feature pages.

## Cross-cutting concerns

| Concern | Approach | Source |
|---------|----------|--------|
| Security | … | `workspace:…` |
| Observability | … | `workspace:…` |
| Error handling | … | `workspace:…` |
| Resilience | … | `workspace:…` |

## Deployment view

| Environment | Where components run | Notes |
|-------------|----------------------|-------|
| Local | … | … |
| Staging / prod | … | … |

## Key decisions and constraints

| Decision / constraint | Summary | Detail |
|-----------------------|---------|--------|
| … | Brief summary grounded in code | Optional link to ADR after verifying the code still matches |

## Related solution designs

- [[projects/PROJECT_SLUG/solution-design|Solution design hub]]

## Key claims

-

## See also

- [[projects/PROJECT_SLUG/index|Overview]]
- [[projects/PROJECT_SLUG/solution-design|Solution design]]
