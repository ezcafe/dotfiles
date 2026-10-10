# my-wiki-flow stages

Run only the stages the user asked for. Default full cycle:
**Init → Ingest → Distill → Lint → Build → (optional Serve) → (optional Sync)**.

Modes: `init` | `ingest` | `distill` | `update` | `query` | `lint` | `build` |
`serve` | `sync-github`.

## Stage 0 — Resolve storage

1. Default root: `~/Documents/my-wiki` (`WIKI_ROOT` / `config.yaml` `root` may override).
2. If user asks for **GitHub wiki**:
   - Read `config.yaml` → `github_wiki.remote` / `github_wiki.repo`.
   - If unset → **ask** for `owner/repo` or wiki clone URL. Stop until answered.
3. If local root missing **or** empty (no `config.yaml` and no `projects/`) → Stage 1 Init.

## Stage 1 — Init

Run: `wiki-init.sh` (or create tree per [structure.md](structure.md)).

Creates: `config.yaml` (with empty `projects: {}`), `README.md`, `inbox/`,
`projects/`, `raw/`, `ai/`, `AGENTS.md`, `index.md`, `log.md`, `site/`, assets CSS.

Tell the user the root path in one line.

## Stage 2 — Ingest

**Goal:** Capture raw material as Markdown. Organize lightly by **project**.

### Inputs

| Source | How |
|--------|-----|
| Current workspace | Map repo → `projects/{slug}/`. Distill from **code**. Skip `node_modules`, build dirs, secrets. Register `projects.{slug}.workspace` in config. |
| GitHub branch | See **GitHub branch ingest** below. |
| Confluence URL | See **Confluence ingest** below. |
| Online document | `wiki-ingest-url.py URL` → `raw/` or `inbox/{date}-{slug}.md`. |

### GitHub branch ingest (concrete)

1. Ask for `owner/repo@branch` and optional subdirectory.
2. `gh api repos/{owner}/{repo}/contents/{path}?ref={branch}` **or**
   `git clone --depth 1 --branch {branch} --filter=blob:none` into a temp dir.
3. Copy immutable originals under `raw/github/{owner}-{repo}-{branch}/` (do not rewrite).
4. Distill into `projects/{slug}/` from **code in that tree**, not from README.
5. Frontmatter `source: https://github.com/{owner}/{repo}/tree/{branch}`.
6. Log: `## [date] ingest | github {owner}/{repo}@{branch}`.

### Confluence ingest (concrete)

1. Ask for page URL (and confirm auth if private).
2. Fetch with browser MCP **or** Confluence export (HTML/Markdown).
3. Save immutable HTML/Markdown under `raw/confluence/{space}-{pageId}.html`.
4. Draft convertible Markdown in `inbox/{date}-{slug}.md` with `source: {url}`.
5. After HITL distill, move synthesized facts into the right project pages (do **not**
   treat Confluence as code evidence for workspace projects).
6. Log: `## [date] ingest | confluence {url}`.

### Frontmatter (required on new pages)

```yaml
---
title: Human title
project: project-slug
tags: [tag1, tag2]
source: https://... or workspace:path
updated: YYYY-MM-DD
summary: One-line AI-readable summary
---
```

### Rules

- One topic per page when possible; link with `[[wiki-links]]`.
- New uncategorized captures → `inbox/` first.
- Never overwrite silently: show a clear diff summary for the user.

## Stage 3 — Distill (HITL)

AI proposes; user owns the result. Follow [project-structure.md](project-structure.md)
and [content-contract.md](content-contract.md).

1. Resolve workspace from `config.yaml` → `projects.{slug}.workspace` (ask if missing).
2. Record `git rev-parse --short HEAD`.
3. Choose profile: `lite` (Overview + Quick start) or `full` (five pages). Ask if unclear.
4. If pages missing → `wiki-scaffold-project.sh {slug} {workspace} [--lite|--full]`.
5. **Feature discovery** (full profile only) — see project-structure; **confirm the
   feature list with the user** before writing pages. Then
   `wiki-add-feature.sh {slug} {feature} [master]`.
6. Validate against **real code**; fill required H2 sections.
7. Remove obsolete `tips-and-tricks.md` / `design-guide.md` if present.
8. Set `source`, `validated_against`, `updated`, `summary`, `claims`.
9. Update root `index.md` and `ai/INDEX.md`; append `log.md`.
10. Show paths + bullets + SHA. **Wait for approval** on bulk rewrites
    (≥3 pages rewritten or any Architecture / Solution design rewrite).

## Stage 3b — Update (incremental)

When the vault already has content for `{slug}`:

1. Read `validated_against` SHA and `projects.{slug}.workspace`.
2. `git -C {workspace} diff --name-only {old-sha}..HEAD` (or `git status` if unknown).
3. Map changed paths → affected wiki pages (entrypoint → Overview/Architecture;
   routes/handlers → feature pages; package scripts → Quick start; schemas →
   contracts on feature pages).
4. Update **only** those pages; bump `validated_against` + `updated`.
5. Show a short diff summary (paths + bullets). HITL if ≥3 pages or diagram changes.
6. Run **lint**, then **build**.
7. Log: `## [date] update | {slug} {old} → {new}`.

## Stage 3c — Query

Answer from the wiki (do not rebuild unless asked):

1. Read `AGENTS.md`, `ai/CONTEXT.md`, root `index.md`, `ai/INDEX.md`.
2. Open only relevant `projects/{slug}/` pages; prefer `summary` frontmatter.
3. Cite wiki paths. If missing, say so — do not invent.
4. File valuable non-trivial answers under `projects/{slug}/references/` or a
   feature page + log entry (optional, ask first).

## Stage 3d — Lint

Run: `wiki-lint.py [--project slug]`

Checks: canonical pages for profile, required H2s, Mermaid types, complex-logic
citations, docs-only claims, stale SHA, broken wikilinks, orphans, obsolete pages.
Appends `log.md`. Fix errors before treating distill as done.

## Stage 4 — Build

Run: `wiki-build.sh` from vault root (or pass `WIKI_ROOT`).

1. `wiki-build.py` → `site/**/*.html`.
2. Pagefind indexes `site/` → `site/pagefind/`.
3. Fail if Pagefind missing: install via `npx pagefind`.

## Stage 5 — Serve (optional)

`wiki-serve.sh` — default port 8765. On macOS, `open` the URL when sensible.

## Stage 6 — Sync GitHub wiki (optional, approval required)

1. Confirm `github_wiki` config (ask if empty).
2. `wiki-sync-github.sh` — dry-run; show map.
3. Only after **explicit yes**: `wiki-sync-github.sh --push`.
4. Never force-push.

## Abort

User says stop / rejects a gate → Status stopped; do not sync or bulk-overwrite.
