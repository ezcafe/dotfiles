# my-wiki-flow stages

Run only the stages the user asked for. Default full cycle:
**Init → Ingest → Analyze → Distill → Lint → Build → (optional Serve) → (optional Sync)**.

Modes: `init` | `ingest` | `analyze` | `distill` | `update` | `query` | `maintain` |
`lint` | `build` | `serve` | `sync-github`.

## Stage 0 — Resolve storage

1. Default root: `~/Documents/my-wiki` (`WIKI_ROOT` / `config.yaml` `root` may override).
2. If user asks for **GitHub wiki**:
   - Read `config.yaml` → `github_wiki.remote` / `github_wiki.repo`.
   - If unset → **ask** for `owner/repo` or wiki clone URL. Stop until answered.
3. If local root missing **or** empty (no `config.yaml` and no `projects/`) → Stage 1 Init.

## Stage 1 — Init

Run: `wiki-init.sh` (or create tree per [structure.md](structure.md)).

Creates: `config.yaml` (with empty `projects: {}`), `README.md`, `inbox/`,
`projects/`, `concepts/`, `raw/`, `ai/`, `AGENTS.md`, `index.md`, `log.md`, `site/`,
assets CSS.

Optional: `WIKI_GIT=1` → `git init` the vault (docs-as-code history).  
Optional: `WIKI_PARA=1` → `areas/`, `resources/`, `archives/` (**not** in HTML nav;
personal overflow only — prefer `projects/` + `concepts/` for wiki content).

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
5. After HITL, fold into `references/` / Glossary / Decisions / concepts candidates only — do **not**
   treat Confluence as code evidence for Architecture or feature pages.
6. Log: `## [date] ingest | confluence {url}`.

### Frontmatter (required on new pages)

```yaml
---
title: Human title
project: project-slug
tags: [tag1, tag2]
entity_type: explanation
source: https://... or workspace:path
updated: YYYY-MM-DD
summary: One-line AI-readable summary
---
```

### Rules

- One topic per page when possible; link with `[[wiki-links]]`.
- New uncategorized captures → `inbox/` first.
- Never overwrite silently: show a clear diff summary for the user.

## Stage 3a — Analyze (preview; optional before Distill)

**Trigger:** user says `analyze`, “preview distill”, or “review before writing pages”.

**Do not write or overwrite project pages.** Produce a short report, then stop for HITL:

1. Resolve workspace; record `git rev-parse --short HEAD`.
2. Propose **feature list** (cap 8) with code evidence paths.
3. Draft **Topic map** rows (topic → intended page).
4. Draft **decision / anti-pattern / trade-off** candidates (each with tentative `workspace:`).
5. Optionally propose **how-to** tasks and **concept** notes.
6. Estimate pages to create/update (canonical + features + how-tos).
7. Log: `## [date] analyze | {slug} @ {sha}` (optional).

After approval → Stage 3 Distill (or generate-from-analysis: skip rediscovery, fill pages).

## Stage 3 — Distill (HITL)

AI proposes; user owns the result. Follow [project-structure.md](project-structure.md)
and [content-contract.md](content-contract.md).

1. Resolve workspace from `config.yaml` → `projects.{slug}.workspace` (ask if missing).
2. Record `git rev-parse --short HEAD`.
3. If pages missing → `wiki-scaffold-project.sh {slug} {workspace}`.
4. **Feature discovery** — see project-structure; **confirm the feature list with the
   user** before writing pages (skip if Analyze already approved the list). Then
   `wiki-add-feature.sh {slug} {feature} [master]`.
5. Confirm optional how-tos → `wiki-add-howto.sh`; concepts → `wiki-add-concept.sh`.
6. Validate against **real code**; fill required H2 sections (incl. Topic index + Decisions).
7. Remove obsolete `index.md` / `quick-start.md` / `tips-and-tricks.md` /
   `design-guide.md` if present under the project.
8. Set `source`, `validated_against`, `updated`, `summary`, `claims`, `confidence`.
9. Architecture ADR rows: Status + Date; supersede instead of rewriting history.
10. Update root `index.md` and `ai/INDEX.md`; append `log.md`.
11. Show paths + bullets + SHA. **Wait for approval** on bulk rewrites
    (≥3 pages rewritten or any Architecture / Solution design / Decisions /
    Topic index rewrite).

## Stage 3b — Update (incremental)

When the vault already has content for `{slug}`:

1. Read `validated_against` SHA and `projects.{slug}.workspace`.
2. `git -C {workspace} diff --name-only {old-sha}..HEAD` (or `git status` if unknown).
3. Map changed paths → affected wiki pages (entrypoint / deployables → Architecture;
   routes/handlers → feature pages; schemas → contracts on feature pages;
   domain names → Glossary; trade-off / branching policy → Decisions;
   new/renamed features → Topic index; ops scripts → how-tos).
4. Update **only** those pages; bump `validated_against` + `updated`.
5. Show a short diff summary (paths + bullets). HITL if ≥3 pages or diagram changes.
6. Run **lint**, then **build**.
7. Log: `## [date] update | {slug} {old} → {new}`.

## Stage 3c — Query

Answer from the wiki (do not rebuild unless asked):

1. Read `AGENTS.md`, `ai/CONTEXT.md`, root `index.md`, `ai/INDEX.md`.
2. Open `projects/{slug}/topic-index.md` or `concepts/topic-index.md`; match topic → open **one** primary page.
3. Prefer `summary` frontmatter before full body.
4. **Two-hop:** if the primary page is not Decisions, also skim Decisions for use-when / avoid.
   Open at most **one** additional See also / Related link. Cite wiki paths.
5. If missing, say so — do not invent.
6. File valuable non-trivial answers under `projects/{slug}/references/` or a
   feature/how-to/concept page + log entry (optional, ask first).

## Stage 3d — Lint

Run: `wiki-lint.py [--project slug]`

Checks: canonical pages (incl. topic-index + decisions), required H2s, Mermaid types,
complex-logic citations, docs-only claims, stale SHA, broken wikilinks, orphans,
obsolete pages, how-to H2s, aliases.
Appends `log.md`. Fix errors before treating distill as done.

## Stage 3e — Prose fold-in (code stays primary)

**Trigger:** user asks to fold papers / Confluence / books / brand docs into a project.

1. Keep originals under `raw/` (immutable).
2. Synthesize into `projects/{slug}/references/` (`article.template.md`) or `concepts/`.
3. Set `confidence: low` and `reviewed:` until code-confirmed.
4. Optionally merge terms into Glossary and **candidate** Decision rules — each still
   needs a `workspace:` cite before it becomes a high-confidence claim.
5. **Never** treat prose as evidence for Architecture diagrams, feature sequences,
   API contracts, or Key claims without code confirmation.
6. Update Topic index only if a new reference/how-to/concept page should be routable.
7. HITL; lint; build. Log: `## [date] fold-in | {slug} {source}`.

## Stage 3f — Maintain (vault hygiene)

**Trigger:** user says `maintain`, “inbox zero”, “wiki hygiene”, or weekly review.

Run: `wiki-lint.py --maintain` (implies coverage report). Then act on findings:

1. **Inbox to zero** — promote to project/concepts/references, or delete (warn if age > 14 days).
2. **Orphan sweep** — link or remove.
3. **Stale SHA** — run `update` for affected projects.
4. **Stale prose** — concepts/references/`reviewed` older than 90 days → re-review or mark low confidence.
5. **Empty stubs** — fill or remove required H2 placeholders after distill.
6. **Duplicates** — merge glossary/concept collisions.
7. Show **coverage summary** (projects, features, how-tos, concepts, fresh vs stale, inbox depth).
8. Lint → build if pages changed. Log: `## [date] maintain | …`.

## Stage 4 — Build

Run: `wiki-build.sh` from vault root (or pass `WIKI_ROOT`).

1. `wiki-build.py` → `site/**/*.html` (backlinks, alias redirects, source path footer).
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
