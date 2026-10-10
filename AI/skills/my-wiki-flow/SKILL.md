---
name: my-wiki-flow
description: >-
  Builds or updates a personal AI knowledge wiki from the current workspace,
  GitHub branches, Confluence links, or online documents. Stores Markdown
  under ~/Documents/my-wiki (local-first) or a GitHub wiki; generates
  ArchWiki-style static HTML with project-grouped navigation and Pagefind
  search. Supports init, ingest, distill, incremental update, query, lint,
  build, serve, and sync-github. Use when the user says run my-wiki-flow,
  wiki flow, build knowledge base, update my wiki, query the wiki, lint wiki,
  second brain wiki, or ingest docs into the wiki.
disable-model-invocation: false
argument-hint: "init | ingest | distill | update | query | lint | build | serve | sync-github"
---

# my-wiki-flow

Personal knowledge wiki: **capture → organize by project → distill → lint → static HTML**.
Local-first at `~/Documents/my-wiki`. Optional GitHub wiki sync.

Inspired by CODE (Capture / Organize / Distill / Express) and progressive AI
second-brain levels. Human stays in the loop on distill/update.

| Doc | Use |
|-----|-----|
| [stages.md](stages.md) | Canonical stage order (incl. update / query / lint) |
| [structure.md](structure.md) | Vault + site layout + config `projects` map |
| [io-contract.md](io-contract.md) | Inputs, outputs, config |
| [ui-archwiki.md](ui-archwiki.md) | ArchWiki-style UI rules |
| [ai-context.md](ai-context.md) | How agents load / query wiki context |
| [philosophy.md](philosophy.md) | Condensed second-brain principles |
| [content-contract.md](content-contract.md) | Frontmatter, claims, lint rules |
| [project-structure.md](project-structure.md) | Pages, H2s, feature discovery |
| [aliases](aliases) | `.wiki-*` shell aliases |

**Scripts:** `{skill}/scripts/`

## When to run

| User says | Do |
|-----------|-----|
| `init` / first run | Ensure vault exists; create structure if missing/empty |
| `ingest` / add sources | Workspace, GitHub branch, Confluence, or URL → Markdown |
| `distill` | Fill/update pages from code; **HITL** on bulk changes |
| `update` | Incremental: diff since `validated_against` → touch affected pages |
| `query` | Answer from wiki with citations (no rebuild unless asked) |
| `lint` | `wiki-lint.py` — structure, diagrams, claims, SHA, links |
| `build` | Regenerate HTML + Pagefind |
| `serve` | Local preview of `site/` |
| `sync-github` | Dry-run then `--push` **only after explicit yes** |
| workspace → wiki | Scaffold + distill current repo into a project |

## Non-negotiables

1. **Local-first:** default root `~/Documents/my-wiki`.
2. **GitHub wiki optional:** ask for owner/repo if unset. Never invent a remote.
3. **Canonical source = Markdown** under `projects/`. HTML is generated only.
4. **Search = Pagefind** after every build.
5. **Nav grouped by project**; TOC like ArchWiki.
6. **UI follows ArchWiki** ([ui-archwiki.md](ui-archwiki.md)).
7. **HITL distill/update:** approve bulk rewrites (≥3 pages or Architecture/Solution design).
8. **No secrets** in vault pages.
9. **Sync / push only on explicit approval** (`wiki-sync-github.sh`).
10. **Organize for AI context** ([ai-context.md](ai-context.md)).
11. **Content contract:** [content-contract.md](content-contract.md) + [project-structure.md](project-structure.md). Distill from **real code**, not README/docs. Validate against workspace SHA. Register `projects.{slug}.workspace` in config.
12. **Lint before done:** run `wiki-lint.py` after distill/update; fix errors.

## Agent workflow (summary)

1. Read `~/Documents/my-wiki/config.yaml` if present; else **init**.
2. Resolve storage: local vs GitHub wiki (ask if needed).
3. Follow [stages.md](stages.md) for the requested mode.
4. Prefer scripts in `scripts/` over ad-hoc generation.
5. After ingest/distill/update: **lint** → **build**.
6. Keep chat short; point to vault paths.

## Package map

| Path | Role |
|------|------|
| `scripts/wiki-init.sh` | Vault skeleton + config |
| `scripts/wiki-build.py` / `.sh` | Markdown → HTML + Pagefind |
| `scripts/wiki-serve.sh` | Serve `site/` |
| `scripts/wiki-ingest-url.py` | URL → inbox/raw draft |
| `scripts/wiki-scaffold-project.sh` | Canonical pages (Architecture, Solution design, Glossary) |
| `scripts/wiki-add-feature.sh` | Feature solution-design page |
| `scripts/wiki-lint.py` | Structure / diagram / claims / SHA lint |
| `scripts/wiki-sync-github.sh` | Dry-run / `--push` GitHub wiki export |
| `scripts/_wiki_config.py` | Shared config helpers |
| `assets/wiki.css` | ArchWiki-like stylesheet |
| `assets/page.template.html` | HTML shell |
| `assets/project-pages/` | Page templates |
| `assets/article.template.md` | Overflow / `references/` only |

## Related

- `my-guide-flow` — teaching lessons (not the long-term wiki).
- `my-gtd-flow` — tasks/schedule; do not dump GTD JSON into wiki unless asked.
