---
name: my-wiki-flow
description: >-
  Builds or updates a personal AI knowledge wiki from the current workspace,
  GitHub branches, Confluence links, or online documents. Stores Markdown
  under ~/Documents/my-wiki (local-first) or a GitHub wiki; generates
  ArchWiki-style static HTML with project-grouped navigation and Pagefind
  search. Supports init, ingest, analyze, distill, incremental update, prose
  fold-in, query, maintain, lint, build, serve, and sync-github. Use when the
  user says run my-wiki-flow, wiki flow, build knowledge base, update my wiki,
  query the wiki, lint wiki, maintain wiki, second brain wiki, or ingest docs
  into the wiki.
disable-model-invocation: false
argument-hint: "init | ingest | analyze | distill | update | query | maintain | lint | build | serve | sync-github"
---

# my-wiki-flow

Personal knowledge wiki: **capture → organize by project → distill → maintain → lint → static HTML**.
Local-first at `~/Documents/my-wiki`. Optional GitHub wiki sync.

**Identity:** code-validated, project-scoped LLM wiki (Karpathy layers + HITL).
Diátaxis informs optional how-tos / `entity_type` — not a full four-mode doc site.
See [philosophy.md](philosophy.md).

Inspired by CODE (Capture / Organize / Distill / Express) and progressive AI
second-brain levels. Human stays in the loop on distill/update.

| Doc | Use |
|-----|-----|
| [stages.md](stages.md) | Canonical stage order (incl. update / query / maintain / lint) |
| [structure.md](structure.md) | Vault + site layout + config `projects` map |
| [io-contract.md](io-contract.md) | Inputs, outputs, config |
| [ui-archwiki.md](ui-archwiki.md) | ArchWiki-style UI rules |
| [ai-context.md](ai-context.md) | How agents load / query wiki context |
| [philosophy.md](philosophy.md) | Condensed second-brain principles + identity |
| [content-contract.md](content-contract.md) | Frontmatter, claims lifecycle, lint rules |
| [project-structure.md](project-structure.md) | Pages, H2s, feature discovery, how-tos, concepts |
| [aliases](aliases) | `.wiki-*` shell aliases |

**Scripts:** `{skill}/scripts/`

## When to run

| User says | Do |
|-----------|-----|
| `init` / first run | Ensure vault exists; create structure if missing/empty |
| `ingest` / add sources | Workspace, GitHub branch, Confluence, or URL → Markdown |
| `analyze` | Preview features / topic map / decisions; **no page writes** until HITL |
| `distill` | Fill/update pages from code; **HITL** on bulk changes |
| `update` | Incremental: diff since `validated_against` → touch affected pages |
| fold-in / papers into wiki | Stage 3e: `references/` / `concepts/` + candidates (code still primary) |
| `query` | Topic index → one page (+ 2-hop); citations (no rebuild unless asked) |
| `maintain` | Inbox / orphans / stale SHA / reviewed age / coverage |
| `lint` | `wiki-lint.py` — structure, diagrams, claims, SHA, links |
| `build` | Regenerate HTML + Pagefind (backlinks, aliases, source footer) |
| `serve` | Local preview of `site/` |
| `sync-github` | Dry-run then `--push` **only after explicit yes** |
| workspace → wiki | Scaffold + distill current repo into a project |

## Non-negotiables

1. **Local-first:** default root `~/Documents/my-wiki`.
2. **GitHub wiki optional:** ask for owner/repo if unset. Never invent a remote.
3. **Canonical source = Markdown** under `projects/` (+ `concepts/`). HTML is generated only.
4. **Search = Pagefind** after every build.
5. **Nav grouped by project** (+ Concepts group); TOC like ArchWiki.
6. **UI follows ArchWiki** ([ui-archwiki.md](ui-archwiki.md)).
7. **HITL distill/update:** approve bulk rewrites (≥3 pages or Architecture / Solution design / Decisions / Topic index).
8. **No secrets** in vault pages.
9. **Sync / push only on explicit approval** (`wiki-sync-github.sh`).
10. **Organize for AI context** ([ai-context.md](ai-context.md)) — query via Topic index + 2-hop.
11. **Content contract:** [content-contract.md](content-contract.md) + [project-structure.md](project-structure.md). Distill from **real code**, not README/docs. Prose fold-in ≠ code evidence. Validate against workspace SHA. Register `projects.{slug}.workspace` in config.
12. **Lint before done:** run `wiki-lint.py` after distill/update; fix errors. Prefer `maintain` for vault hygiene.

## Agent workflow (summary)

1. Read `~/Documents/my-wiki/config.yaml` if present; else **init**.
2. Resolve storage: local vs GitHub wiki (ask if needed).
3. Follow [stages.md](stages.md) for the requested mode.
4. Prefer scripts in `scripts/` over ad-hoc generation.
5. After ingest/distill/update/maintain: **lint** → **build**.
6. Keep chat short; point to vault paths.

## Package map

| Path | Role |
|------|------|
| `scripts/wiki-init.sh` | Vault skeleton + config |
| `scripts/wiki-build.py` / `.sh` | Markdown → HTML + Pagefind |
| `scripts/wiki-serve.sh` | Serve `site/` |
| `scripts/wiki-ingest-url.py` | URL → inbox/raw draft |
| `scripts/wiki-scaffold-project.sh` | Canonical pages (+ how-to/ dir) |
| `scripts/wiki-add-feature.sh` | Feature solution-design page |
| `scripts/wiki-add-howto.sh` | Project how-to / runbook page |
| `scripts/wiki-add-concept.sh` | Cross-project evergreen concept |
| `scripts/wiki-lint.py` | Structure / diagram / claims / SHA / maintain |
| `scripts/wiki-sync-github.sh` | Dry-run / `--push` GitHub wiki export |
| `scripts/_wiki_config.py` | Shared config helpers |
| `assets/wiki.css` | ArchWiki-like stylesheet |
| `assets/page.template.html` | HTML shell |
| `assets/project-pages/` | Page templates |
| `assets/article.template.md` | Overflow / `references/` only |

## Related

- `my-guide-flow` — teaching lessons (not the long-term wiki).
- `my-gtd-flow` — tasks/schedule; do not dump GTD JSON into wiki unless asked.
