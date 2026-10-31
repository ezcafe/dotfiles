# Wiki content contract

Generated and distilled Markdown **must** follow this contract so the vault works as a
**Karpathy-pattern LLM wiki** ([gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)),
parses cleanly in [Understand Anything](https://github.com/Egonex-AI/Understand-Anything),
and uses the fixed project layout from [project-structure.md](project-structure.md)
(Trail of Bits–style progressive disclosure: [trailofbits/skills](https://github.com/trailofbits/skills)).

**This file owns:** layers, frontmatter, claims lifecycle, lint checklist, and “must not”.  
**project-structure.md owns:** page set, H2 titles, diagram types, feature discovery.

**Identity:** code-validated project wiki — not a full Diátaxis site. See [philosophy.md](philosophy.md).

## Three layers (Karpathy)

| Layer | Location | Rule |
|-------|----------|------|
| **Raw sources** | `raw/` | Immutable. Agents read; never rewrite. |
| **Wiki** | `projects/`, `concepts/`, `inbox/` | LLM-maintained Markdown with wikilinks and frontmatter. |
| **Schema** | `AGENTS.md` | Conventions and workflows. Co-evolve with the vault. |

Root `index.md`, `log.md`, `AGENTS.md` are infrastructure — not articles.

## Project pages

Canonical set and required H2s: **[project-structure.md](project-structure.md)**.
Scaffold: `wiki-scaffold-project.sh`. Features: `wiki-add-feature.sh`.
How-tos: `wiki-add-howto.sh`. Concepts: `wiki-add-concept.sh`.

Project set: Architecture, Topic index, Solution design (+ features), Decisions, Glossary.
Optional: `how-to/` (ops tasks), `references/` (prose fold-in).
Cross-project: `concepts/` evergreen notes.

No Overview, Quick start, Tips and tricks, or Design guide pages.

## Progressive disclosure (query)

1. `ai/INDEX.md` / root `index.md` → pick project or Concepts.
2. `topic-index.md` (or Concepts topic map) → pick page.
3. Open that page (`summary` then body). Prefer Decisions for “when / avoid” questions.
4. **Two-hop max:** after the primary page, also open Decisions (if not already) and at most one See also / Related link. Do not dump the whole project.

## Root catalog — `index.md`

```markdown
# Wiki index

## Concepts

- [[concepts/{slug}|…]] — …

## {Project name}

- [[projects/{slug}/architecture|Architecture]] — …
- [[projects/{slug}/topic-index|Topic index]] — …
- [[projects/{slug}/solution-design|Solution design]] — …
- [[projects/{slug}/decisions|Decisions]] — …
- [[projects/{slug}/glossary|Glossary]] — …
```

## Chronology — `log.md`

```markdown
## [YYYY-MM-DD] ingest | Short title
## [YYYY-MM-DD] analyze | {slug} @ {git-sha}
## [YYYY-MM-DD] distill | validated {slug} against {git-sha}
## [YYYY-MM-DD] update | {slug} {old} → {new}
## [YYYY-MM-DD] fold-in | {slug} {source}
## [YYYY-MM-DD] maintain | …
## [YYYY-MM-DD] lint | …
## [YYYY-MM-DD] query | …
## [YYYY-MM-DD] sync-github | …
```

## Frontmatter (required)

```yaml
---
title: Display title
project: slug          # or concepts for evergreen pages
tags: [topic]
entity_type: explanation   # tutorial | how-to | reference | explanation
                           # (Diátaxis-inspired label; nav/query may use it)
source: workspace:path/to/repo
validated_against: workspace:path/to/repo@abc1234
updated: YYYY-MM-DD
reviewed: YYYY-MM-DD       # optional; required for concepts/ + references/ after fold-in
summary: One sentence an agent can trust without reading the body.
claims: []                 # optional short claim ids; must appear in Key claims if set
confidence: high           # high = code-confirmed; medium = mixed; low = literature only
aliases: []                # optional former titles/paths for redirects + link resolution
nav_group:                 # optional; feature pages only
---
```

`validated_against` is mandatory after distill/update on project pages.
`confidence: low` pages must not assert Architecture / sequence / Key claims without a
code-confirmed follow-up.

## Claims and decision lifecycle

| Field | Where | Values / rule |
|-------|-------|----------------|
| **Status** (ADR-lite) | Architecture Key decisions | `proposed` \| `accepted` \| `superseded` \| `deprecated` |
| **Date** | Architecture ADR-lite | Decision date; do **not** rewrite history — add a new row and mark old `superseded` |
| **confidence** | Frontmatter + claim bullets | `high` / `medium` / `low` |
| **reviewed** | Concepts, references, glossary prose | ISO date; lint warns if older than 90 days |

Decisions page voice remains **Use X when Y**. Prefer Status on Architecture records;
actionable rules stay on `decisions.md`.

## Article body conventions

- Required H2s: project-structure (do not rename).
- Prefer GFM tables for contracts, env vars, glossaries, topic maps, decisions.
- Mermaid types: project-structure (Architecture / Sequence).
- Link canonical schema/code files; do not duplicate full contracts.
- Prefer **inline contextual wikilinks** in prose; keep **See also** short.
- End with **Key claims** (each tied to a `workspace:` path, or `confidence: low` + source) and **See also**.
- Do not put escaped `\|` in table cells for wikilink aliases — use `[[path]]`.
- Decisions voice: **Use X when Y** (density over completeness; no raw dumps).

## Codebase validation — code first

Primary evidence: entrypoints, handlers, schemas-as-code, package/CI scripts, tests,
infra-as-code. **Not** primary: README, `docs/**`, ADRs, prior wiki without re-read.

Prose under `raw/` / `references/` may seed Glossary or Decisions **candidates** only.
Confirm every claim in code (see [stages.md](stages.md) Stage 3e).

Trust code over prose. Steps: [project-structure.md](project-structure.md) § Codebase validation
and [stages.md](stages.md) Distill / Update.

## Lint pass

Prefer automated: `wiki-lint.py [--project slug] [--maintain]`.

Manual / agent checklist (same rules):

1. Missing canonical pages → scaffold, then fill.
2. Stray overview / quick-start / tips-and-tricks / design-guide → remove.
3. Missing required H2s → add and fill from code.
4. Architecture without Building block (`C4Container`/`C4Component`) or Interaction (`C4Dynamic`, or flowchart + `C4Dynamic unavailable`) → fix.
5. Topic index without Topic map table + wikilinks → fix.
6. Decisions without Decision rules / Anti-patterns / Trade-offs / Related architecture decisions → fix.
7. Feature without `sequenceDiagram` → fix; Scope needs Business requirements; API Spec summary always; full field tables + curl only when Owns contract? = yes (arrays ≥1 item).
8. How-to without Prerequisites / Steps / Verify → fix.
9. Complex logic without `workspace:` path (+ code fence, or N/A) → fix.
10. Claims citing only README/docs without code path → reject (unless `confidence: low` and not on Architecture/feature Key claims).
11. Stale `validated_against` vs HEAD → re-validate (`update` stage).
12. Frontmatter `claims` entries missing from Key claims → align.
13. Orphans / broken wikilinks → fix or link from hub/root index.
14. Inbox items older than 14 days → process or delete (`maintain`).
15. Concepts / references missing `reviewed` or older than 90 days → review.
16. Print coverage summary (fresh vs stale SHA, inbox depth, feature count).
17. Append `log.md`.

## What agents must not do

- Distill primarily from README/docs/ADRs instead of code.
- Invent facts not grounded in inspected code (or immutable `raw/` for non-code ingest).
- Treat prose fold-in as Architecture / feature / claim evidence without code confirmation.
- Bulk-rewrite without HITL (≥3 pages or Architecture / Solution design / Decisions / Topic index).
- Store secrets in the vault.
- Replace `raw/` during ingest.
- Put feature sequences on Architecture; put flowchart/C4 on feature Sequence diagram sections.
- When Owns contract? = yes: ship without field-level request/response tables (example values), without curl success/error, or with empty `[]` array examples.
- When Owns contract? = no: ship without Spec summary and a `workspace:` canonical link.
- Duplicate full API schemas into every feature when a canonical code file exists.
- Create unbounded feature pages without user-confirmed discovery list.
- Create Overview (`index.md`) or Quick start pages under a project.
- Leave Topic index without rows for confirmed features.
- Silently rewrite Architecture ADR Status/Date history (supersede with a new row instead).

## References

- [project-structure.md](project-structure.md)
- [stages.md](stages.md)
- [philosophy.md](philosophy.md)
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Understand Anything](https://github.com/Egonex-AI/Understand-Anything)
- [Diátaxis](https://diataxis.fr/) (inspiration for `entity_type` / how-tos — not full site layout)
- [Mermaid docs](https://mermaid.js.org/intro/)
