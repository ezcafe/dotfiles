# Wiki schema — AGENTS.md

This file is the **schema layer** for this vault (Karpathy LLM wiki pattern).
Agents that ingest, distill, query, maintain, or lint the wiki must read this first, then
skill docs: `content-contract.md` and `project-structure.md`.

**Identity:** code-validated project wiki + optional `concepts/` evergreen notes.
Diátaxis informs `entity_type` / how-tos only — not a four-mode doc site.

## Vault layout

- `raw/` — immutable sources (read only)
- `projects/{slug}/` — Architecture, Topic index, Solution design, Decisions, Glossary
- `projects/{slug}/solution-design/` — one page per confirmed feature
- `projects/{slug}/how-to/` — optional task / runbook pages
- `projects/{slug}/references/` — overflow / prose fold-in (`article.template.md`)
- `concepts/` — cross-project evergreen notes (+ optional `topic-index.md`)
- `inbox/` — uncategorized captures (process via `maintain`)
- `index.md` — master catalog (`##` + `[[wikilinks]]`)
- `log.md` — append-only timeline
- `config.yaml` — `projects.{slug}.workspace`, optional `maintain.*` ages
- `ai/INDEX.md`, `ai/CONTEXT.md` — agent routing
- `site/` — generated HTML (do not edit)

## Canonical project pages

1. `architecture.md` — Building block (`C4Container`/`C4Component`) + Interaction (`C4Dynamic` with `UpdateLayoutConfig` 1/row + C4 palette); quality goals, communication table, risks, ADR-lite (Status/Date append-only)
2. `topic-index.md` — Topic map table (topic → `[[page]]`); load before full pages
3. `solution-design.md` + `solution-design/{feature}.md` — **`sequenceDiagram`** with `alt`/`opt`; Business requirements; progressive API (full tables + curl only when Owns=yes); Cross-cutting deltas
4. `decisions.md` — Use-when rules, anti-patterns, trade-offs (`workspace:` cites); links ADR-lite on Architecture
5. `glossary.md`
6. Optional `how-to/{task}.md` — Prerequisites / Steps / Verify

No Overview, Quick start, tips-and-tricks, or design-guide pages.

Required H2s: project-structure.md. Scaffold / features / how-tos / concepts: skill scripts.

## Frontmatter highlights

- `entity_type`: `tutorial` | `how-to` | `reference` | `explanation`
- `confidence`: `high` (code) | `medium` | `low` (literature)
- `aliases`: former titles/paths for redirects
- `reviewed`: required for concepts/references after fold-in
- `validated_against`: mandatory after distill/update on project pages

## Operations

### Ingest

1. Store originals under `raw/` (or URL in frontmatter).
2. Map to `projects/{slug}/` or leave in `inbox/`; register workspace in `config.yaml`.
3. Append `log.md`.

### Analyze

1. Preview feature list, Topic map draft, Decisions candidates, optional how-tos/concepts, page estimate.
2. Stop for HITL — do not write pages until approved.

### Distill / Update

1. Resolve workspace from config; capture git SHA.
2. **Update:** diff `{old-sha}..HEAD` → touch only affected pages.
3. Fill pages from **code** only. Confirm feature list before adding pages.
4. Fill Topic index + Decisions; Architecture diagrams; features: `sequenceDiagram` + progressive API + complex-logic cite.
5. Content-first pages: do not paste AGENTS instructions into distilled Markdown. Prefer tables with `workspace:` cites.
6. Set `validated_against` / `confidence`. Supersede ADR rows; do not rewrite history. HITL on bulk changes. Append `log.md`.
7. Run `wiki-lint.py`.

### Prose fold-in

1. Keep sources in `raw/`; synthesize into `references/` or `concepts/`.
2. Set `confidence: low` + `reviewed:` until code-confirmed.
3. Never use prose alone as Architecture / feature / high-confidence Key claims evidence.

### Query

1. Read `index.md` / `ai/INDEX.md` → topic-index → one primary page.
2. Two-hop: Decisions (if needed) + at most one See also.
3. Prefer `summary`, then body. Cite paths.
4. File valuable answers under `references/` / concepts only if user agrees.

### Maintain

`wiki-lint.py --maintain` — inbox age, orphans, stale SHA, reviewed age, coverage.
Process inbox; fix or schedule `update`; then build if needed.

### Lint

`wiki-lint.py` — missing pages/H2s/diagrams, topic map, decisions tables, how-tos,
docs-only claims, stale SHA, broken links, orphans, obsolete pages, aliases.

### Sync

`wiki-sync-github.sh` dry-run; `--push` only after explicit approval. Never force-push.

## Compatibility

- **Understand Anything:** `/understand-knowledge` at this vault root.
- **my-wiki-flow:** `wiki-build.sh` after Markdown changes.
