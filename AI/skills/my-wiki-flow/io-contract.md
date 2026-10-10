# I/O contract

## Inputs

| Kind | Agent accepts | Notes |
|------|---------------|-------|
| Workspace | Current cwd / named paths | Skip secrets, binaries, `node_modules`; register in `config.yaml` |
| GitHub branch | `owner/repo@branch` + optional path | `gh` / shallow clone → `raw/` then distill (see stages) |
| Confluence | Page URL | Export → `raw/confluence/` + inbox draft (see stages) |
| Online doc | HTTP(S) URL | `wiki-ingest-url.py` → inbox/raw |
| Existing vault | `~/Documents/my-wiki` | Update / query / lint path |

## Outputs

| Artifact | Location | Role |
|----------|----------|------|
| Markdown pages | `projects/{slug}/*.md`, `inbox/` | Canonical knowledge |
| AI catalog | `ai/INDEX.md`, `ai/CONTEXT.md` | Agent context entrypoints |
| Static site | `site/**/*.html` | Browser read |
| Search index | `site/pagefind/` | Fast client search (~10k pages) |
| Lint report | stdout + `log.md` | `wiki-lint.py` |
| GitHub wiki map | `ai/github-wiki-map.md` | Written by sync dry-run/push |
| GitHub wiki (optional) | configured remote | Mirror after approval |

## Page Markdown shape

Rules: [content-contract.md](content-contract.md) and [project-structure.md](project-structure.md).

Frontmatter must include `validated_against: workspace:…@SHA` after distill/update.
Claims cite code paths. Architecture: Interaction diagram (`C4Dynamic`). Features: `sequenceDiagram`. API contracts include spec, **curl** requests, and success/error responses (arrays show ≥1 item).

## HTML page contract

Every generated page includes:

1. **Search** (Pagefind) in the header.
2. **Nav** — projects as groups; canonical page order; nested features.
3. **In-page TOC** from `h2`/`h3`.
4. **Article** with tables + zoomable Mermaid.
5. Link to project overview and site home.

## Performance targets

| Concern | Approach |
|---------|----------|
| 10k pages | Static HTML; no runtime DB |
| Fast load | Shared CSS; no heavy frameworks; Pagefind |
| AI context | `ai/INDEX.md` + project folder + `summary` — not whole-site paste |

## Errors

| Case | Behavior |
|------|----------|
| Missing Pagefind | Fail build with `npx --yes pagefind --version` hint |
| GitHub wiki unset | Ask; do not guess |
| Secret-looking file | Skip + warn |
| Lint errors | Fix before treating distill/update as done |
| Sync without approval | Dry-run only; never `--push` |
