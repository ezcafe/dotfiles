# Wiki schema — AGENTS.md

This file is the **schema layer** for this vault (Karpathy LLM wiki pattern).
Agents that ingest, distill, query, or lint the wiki must read this first, then
skill docs: `content-contract.md` and `project-structure.md`.

## Vault layout

- `raw/` — immutable sources (read only)
- `projects/{slug}/` — Architecture, Solution design, Glossary
- `projects/{slug}/solution-design/` — one page per confirmed feature
- `projects/{slug}/references/` — overflow only (`article.template.md`)
- `inbox/` — uncategorized captures
- `index.md` — master catalog (`##` + `[[wikilinks]]`)
- `log.md` — append-only timeline
- `config.yaml` — `projects.{slug}.workspace`
- `ai/INDEX.md`, `ai/CONTEXT.md` — agent routing
- `site/` — generated HTML (do not edit)

## Canonical project pages

1. `architecture.md` — Building block (`C4Container`/`C4Component`) + Interaction (`C4Dynamic` with `UpdateLayoutConfig` 1/row + C4 palette); quality goals, communication table, risks, ADR-lite decisions
2. `solution-design.md` + `solution-design/{feature}.md` — **`sequenceDiagram`** with `alt`/`opt`; Business requirements; progressive API (full tables + curl only when Owns=yes); Cross-cutting deltas
3. `glossary.md`

No Overview, Quick start, tips-and-tricks, or design-guide pages.

Required H2s: project-structure.md. Scaffold / features: skill scripts.

## Operations

### Ingest

1. Store originals under `raw/` (or URL in frontmatter).
2. Map to `projects/{slug}/`; register workspace in `config.yaml`.
3. Append `log.md`.

### Distill / Update

1. Resolve workspace from config; capture git SHA.
2. **Update:** diff `{old-sha}..HEAD` → touch only affected pages.
3. Fill pages from **code** only. Confirm feature list before adding pages.
4. Architecture: Building block + Interaction diagrams; features: `sequenceDiagram` + progressive API + complex-logic cite.
5. Content-first pages: do not paste AGENTS instructions into distilled Markdown. Prefer tables with `workspace:` cites.
6. Set `validated_against`. HITL on bulk changes. Append `log.md`.
7. Run `wiki-lint.py`.

### Query

1. Read `index.md` / `ai/INDEX.md` → relevant pages.
2. Prefer `summary`, then body. Cite paths.
3. File valuable answers under `references/` only if user agrees.

### Lint

`wiki-lint.py` — missing pages/H2s/diagrams, docs-only claims, stale SHA,
broken links, orphans, obsolete pages.

### Sync

`wiki-sync-github.sh` dry-run; `--push` only after explicit approval. Never force-push.

## Compatibility

- **Understand Anything:** `/understand-knowledge` at this vault root.
- **my-wiki-flow:** `wiki-build.sh` after Markdown changes.
