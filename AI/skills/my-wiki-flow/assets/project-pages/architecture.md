---
title: Architecture
project: PROJECT_SLUG
tags: [architecture]
entity_type: concept
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
summary: Project-wide architecture — quality goals, building blocks, interactions, deployment, risks, and constraints.
claims: []
---

# Architecture

Project-wide structure only. Feature sequences belong in [[projects/PROJECT_SLUG/solution-design|Solution design]].

> **Tip** Keep this page at one abstraction level. Put feature sequences on Solution design pages.

## Purpose and quality goals

Boundaries this page covers (and what it omits). Top quality goals with a checkable signal from code or config.

| Goal | Metric or signal | Source |
|------|------------------|--------|
| … | e.g. p95 latency, RPO, consistency model | `workspace:…` |

## Building block view

Static structure at one abstraction level (deployable containers, or modules for a modular monolith). Same ids are reused in the Interaction diagram.

```mermaid
C4Container
title Building blocks — PROJECT_SLUG

UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")

Person(user, "User", "Primary actor")
System_Boundary(sys, "PROJECT_SLUG") {
  Container(ui, "UI", "Web/App", "Client surface")
  Container(api, "API", "HTTP", "Routes / handlers")
  Container(worker, "Worker", "Jobs", "Async work")
  ContainerDb(db, "Database", "SQL", "Primary store")
}
System_Ext(ext, "External", "Upstream / downstream")

Rel(user, ui, "Uses")
Rel(ui, api, "HTTPS")
Rel(api, db, "SQL")
Rel(api, worker, "Enqueue")
Rel(api, ext, "Calls")

UpdateRelStyle(user, ui, $offsetY="-25")
UpdateRelStyle(ui, api, $offsetY="-25")
UpdateRelStyle(api, db, $offsetX="30")
UpdateRelStyle(api, worker, $offsetY="25")
UpdateRelStyle(api, ext, $offsetY="-25")
```

| Component | Path / package | Responsibility | Key interface |
|-----------|----------------|----------------|---------------|
| … | `…` | … | e.g. HTTP routes, queue topic |

## Interaction diagram

One or two architecturally relevant runtime scenarios. Numbered relations among the same building-block ids. Feature-level sequences stay on Solution design pages.

```mermaid
C4Dynamic
title Interaction — happy path (replace with real scenario)

%% One shape per row keeps steps readable (C4Dynamic default packs 4/row and overlaps).
UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="1")

Container(ui, "UI", "Web/App", "Client")
Container(api, "API", "HTTP", "Handlers")
ContainerDb(db, "Database", "SQL", "Store")

%% Prefer downward-only numbered steps; avoid crossing return arrows on the same stack.
Rel(ui, api, "1 Request", "HTTPS")
Rel(api, db, "2 Query", "SQL")
Rel(api, ui, "3 Response", "HTTPS")

UpdateRelStyle(ui, api, $offsetX="48")
UpdateRelStyle(api, db, $offsetX="48")
UpdateRelStyle(api, ui, $offsetX="-48")
```

> **Note** Prefer `flowchart TB` with the phrase `C4Dynamic unavailable` when the scenario has return paths or more than three participants — Mermaid C4Dynamic often overlaps labels. If you keep `C4Dynamic`, you **must** include `UpdateLayoutConfig($c4ShapeInRow="1")` and avoid reverse Rel arrows on the same stack.

## Communication and data

Protocols, sync vs async, and data ownership — do not re-narrate the diagrams.

| From | To | Protocol | Sync / async | Data owned |
|------|----|----------|--------------|------------|
| … | … | HTTPS / gRPC / queue / … | sync / async | … |

## Cross-cutting concerns

Project-wide only. Feature-specific deltas go on Solution design pages.

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

Add a deployment Mermaid when more than one deployable unit maps to distinct hosts or clusters.

## Risks and technical debt

| Risk or debt | Impact | Mitigation | Source |
|--------------|--------|------------|--------|
| … | … | … | `workspace:…` |

## Key decisions and constraints

| Decision | Status | Date | Summary | Consequences |
|----------|--------|------|---------|--------------|
| … | accepted / superseded / proposed | YYYY-MM-DD | Grounded in code | … |

Link an ADR only after confirming the code still matches.

## Related solution designs

- [[projects/PROJECT_SLUG/solution-design|Solution design hub]]

## Key claims

- Building blocks and quality signals match code at `validated_against` — `workspace:REPO_PATH`

## See also

- [[projects/PROJECT_SLUG/solution-design|Solution design]]
- [[projects/PROJECT_SLUG/glossary|Glossary]]
