# I/O contract

## Inputs

| Kind | Agent accepts | Notes |
|------|---------------|-------|
| Workspace | Current cwd / named paths | Skip secrets, binaries, `node_modules`; register in `config.yaml` |
| GitHub branch | `owner/repo@branch` + optional path | `gh` / shallow clone → `raw/` then distill (see stages) |
| Confluence | Page URL | Export → `raw/confluence/` + inbox draft (see stages) |
| Online doc | HTTP(S) URL | `wiki-ingest-url.py` → inbox/raw |
| Prose cluster | `raw/` / inbox papers | Fold-in → `references/` / `concepts/` (+ Glossary/Decisions candidates); code still primary |
| Existing vault | `~/Documents/my-wiki` | Analyze / update / query / maintain / lint path |

## Outputs

| Artifact | Location | Role |
|----------|----------|------|
| Markdown pages | `projects/{slug}/*.md`, `concepts/`, `inbox/` | Canonical knowledge |
| AI catalog | `ai/INDEX.md`, `ai/CONTEXT.md` | Agent context entrypoints |
| Static site | `site/**/*.html` | Browser read (+ backlinks, alias redirects) |
| Search index | `site/pagefind/` | Fast client search (~10k pages) |
| Lint / maintain report | stdout + `log.md` | `wiki-lint.py` / `--maintain` |
| Coverage summary | lint stdout | Fresh vs stale SHA, inbox depth, page counts |
| GitHub wiki map | `ai/github-wiki-map.md` | Written by sync dry-run/push |
| GitHub wiki (optional) | configured remote | Mirror after approval |

## Page Markdown shape

Rules: [content-contract.md](content-contract.md) and [project-structure.md](project-structure.md).

Frontmatter must include `validated_against: workspace:…@SHA` after distill/update
on project pages. Claims cite code paths (`confidence: high`) or are marked low.
Architecture: Building block (`C4Container`/`C4Component`) + Interaction (`C4Dynamic`).
Features: `sequenceDiagram`. API: Spec summary always; full field tables + **curl**
success/error when Owns contract? = yes (arrays ≥1 item).
How-tos: Prerequisites / Steps / Verify. Concepts: Definition / When to use / Related.

Optional: `aliases: […]` for renames; `reviewed:` for prose; `entity_type` for intent.

## HTML page contract

Every generated page includes:

1. **Search** (Pagefind) in the header.
2. **Nav** — Concepts group + projects as groups; canonical page order; nested features / how-tos.
3. **In-page TOC** from `h2`/`h3`.
4. **Article** with tables + zoomable Mermaid; optional `entity_type` badge.
5. **Backlinks** (“Linked from”) when other pages wikilink here.
6. **Source footer** — vault-relative Markdown path (edit path).
7. Link to project Architecture (or Concepts index) and site home.
8. Alias redirect HTML stubs when `aliases:` lists former paths/stems.

## Performance targets

| Concern | Approach |
|---------|----------|
| 10k pages | Static HTML; no runtime DB |
| Fast load | Shared CSS; no heavy frameworks; Pagefind |
| AI context | `ai/INDEX.md` + topic-index + one page (+ 2-hop) — not whole-site paste |

## Errors

| Case | Behavior |
|------|----------|
| Missing Pagefind | Fail build with `npx --yes pagefind --version` hint |
| GitHub wiki unset | Ask; do not guess |
| Secret-looking file | Skip + warn |
| Lint errors | Fix before treating distill/update as done |
| Sync without approval | Dry-run only; never `--push` |
