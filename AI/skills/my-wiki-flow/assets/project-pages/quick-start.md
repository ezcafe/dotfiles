---
title: Quick start
project: PROJECT_SLUG
tags: [setup, quick-start]
entity_type: how-to
source: workspace:REPO_PATH
validated_against: workspace:REPO_PATH@GIT_SHA
updated: YYYY-MM-DD
summary: Task-oriented prerequisites, setup, run, and verify steps for this project.
claims: []
---

# Quick start

Keep this page task-oriented. Put deeper design context in [[projects/PROJECT_SLUG/architecture|Architecture]] or feature [[projects/PROJECT_SLUG/solution-design|Solution design]] pages.

## Prerequisites

| Tool / account | Version | Permissions / notes | Verified from |
|----------------|---------|---------------------|---------------|
| … | … | … | `workspace:…` |

## Setup

1. Clone or open the repo at `REPO_PATH`.
2. Install dependencies (exact command from package scripts, Makefile, Taskfile, or CI — not README prose).
3. Configure env from `.env.example` / config schema in code only — never paste secrets into the wiki.
4. Apply any required local config (ports, feature flags) found in compose files, config modules, or CI.

## Run locally

```bash
# Exact command from the repo
```

Expected result: describe the successful output (URL, CLI message, or process state).

## Verify

| Check | Command or action | Pass criteria |
|-------|-------------------|---------------|
| Smoke / health | … | … |

## Common setup issues

| Symptom | Fix |
|---------|-----|
| … | … |

## Next steps

- [[projects/PROJECT_SLUG/architecture|Architecture]] — system shape and constraints
- [[projects/PROJECT_SLUG/solution-design|Solution design]] — feature designs relevant after setup

## Key claims

-

## See also

- [[projects/PROJECT_SLUG/index|Overview]]
