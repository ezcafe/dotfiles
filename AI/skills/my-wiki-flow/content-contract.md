# Wiki content contract

Generated and distilled Markdown **must** follow this contract so the vault works as a
**Karpathy-pattern LLM wiki** ([gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)),
parses cleanly in [Understand Anything](https://github.com/Egonex-AI/Understand-Anything),
and uses the fixed project layout from [project-structure.md](project-structure.md)
(Trail of Bits–style progressive disclosure: [trailofbits/skills](https://github.com/trailofbits/skills)).

**This file owns:** layers, frontmatter, claims, lint checklist, and “must not”.  
**project-structure.md owns:** page set, H2 titles, diagram types, feature discovery, profiles.

## Three layers (Karpathy)

| Layer | Location | Rule |
|-------|----------|------|
| **Raw sources** | `raw/` | Immutable. Agents read; never rewrite. |
| **Wiki** | `projects/`, `inbox/` | LLM-maintained Markdown with wikilinks and frontmatter. |
| **Schema** | `AGENTS.md` | Conventions and workflows. Co-evolve with the vault. |

Root `index.md`, `log.md`, `AGENTS.md` are infrastructure — not articles.

## Project pages

Canonical set, profiles (`full` / `lite`), and required H2s:
**[project-structure.md](project-structure.md)**. Scaffold:
`wiki-scaffold-project.sh`. Features: `wiki-add-feature.sh`.

No Tips and tricks or Design guide pages.

## Root catalog — `index.md`

```markdown
# Wiki index

## {Project name}

- [[projects/{slug}/index|Overview]] — …
- [[projects/{slug}/quick-start|Quick start]] — …
# full profile also lists Architecture, Solution design, Glossary
```

## Chronology — `log.md`

```markdown
## [YYYY-MM-DD] ingest | Short title
## [YYYY-MM-DD] distill | validated {slug} against {git-sha}
## [YYYY-MM-DD] update | {slug} {old} → {new}
## [YYYY-MM-DD] lint | …
## [YYYY-MM-DD] query | …
## [YYYY-MM-DD] sync-github | …
```

## Frontmatter (required)

```yaml
---
title: Display title
project: slug
tags: [topic]
entity_type: how-to   # or concept
source: workspace:path/to/repo
validated_against: workspace:path/to/repo@abc1234
updated: YYYY-MM-DD
summary: One sentence an agent can trust without reading the body.
claims: []            # optional short claim ids; must appear in Key claims if set
nav_group:            # optional; feature pages only
---
```

`validated_against` is mandatory after distill/update.

## Article body conventions

- Required H2s: project-structure (do not rename).
- Prefer GFM tables for contracts, env vars, glossaries, setup issues.
- Mermaid types: project-structure (Architecture / Sequence / context).
- Link canonical schema/code files; do not duplicate full contracts.
- End with **Key claims** (each tied to a `workspace:` path) and **See also**.
- Do not put escaped `\|` in table cells for wikilink aliases — use `[[path]]`.

## Codebase validation — code first

Primary evidence: entrypoints, handlers, schemas-as-code, package/CI scripts, tests,
infra-as-code. **Not** primary: README, `docs/**`, ADRs, prior wiki without re-read.

Trust code over prose. Steps: [project-structure.md](project-structure.md) § Codebase validation
and [stages.md](stages.md) Distill / Update.

## Lint pass

Prefer automated: `wiki-lint.py [--project slug]`.

Manual / agent checklist (same rules):

1. Missing canonical pages for profile → scaffold, then fill.
2. Stray tips-and-tricks / design-guide → remove.
3. Missing required H2s → add and fill from code.
4. Architecture without Interaction diagram (`C4Dynamic`, or flowchart + `C4Dynamic unavailable`) → fix.
5. Feature without `sequenceDiagram` → fix; API contracts need spec + curl requests + success/error responses (arrays show ≥1 item).
6. Complex logic without `workspace:` path + code fence → add both.
7. Claims citing only README/docs without code path → reject.
8. Stale `validated_against` vs HEAD → re-validate (`update` stage).
9. Frontmatter `claims` entries missing from Key claims → align.
10. Orphans / broken wikilinks → fix or link from hub/index.
11. Append `log.md`.

## What agents must not do

- Distill primarily from README/docs/ADRs instead of code.
- Invent facts not grounded in inspected code (or immutable `raw/` for non-code ingest).
- Bulk-rewrite without HITL (≥3 pages or Architecture/Solution design).
- Store secrets in the vault.
- Replace `raw/` during ingest.
- Put feature sequences on Architecture; put flowchart/C4 on feature Sequence diagram sections.
- Ship API contracts without curl requests or without success/error responses (arrays must show ≥1 item, not empty `[]`).
- Duplicate full API schemas when a canonical code file exists.
- Create unbounded feature pages without user-confirmed discovery list.

## References

- [project-structure.md](project-structure.md)
- [stages.md](stages.md)
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Understand Anything](https://github.com/Egonex-AI/Understand-Anything)
- [Diátaxis](https://diataxis.fr/)
- [Mermaid docs](https://mermaid.js.org/intro/)
