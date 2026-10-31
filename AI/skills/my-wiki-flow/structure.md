# Vault structure

Default root: `~/Documents/my-wiki`

```text
~/Documents/my-wiki/
  config.yaml           # root, github_wiki, build, projects.{slug}.workspace
  README.md             # human overview
  AGENTS.md             # schema layer (Karpathy); from skill template on init
  index.md              # master catalog (## + [[wikilinks]]); regenerated on build
  log.md                # append-only operations log
  raw/                  # immutable sources (Karpathy layer 1)
  inbox/                # uncategorized captures (CODE Capture)
  concepts/             # cross-project evergreen notes
    topic-index.md      # optional vault-wide concept map
    {concept}.md
  projects/             # PRIMARY nav grouping
    {project-slug}/
      architecture.md       # 1 Architecture
      topic-index.md        # 2 Topic index (agent routing)
      solution-design.md    # 3 Solution design hub
      solution-design/      #    one page per feature
      decisions.md          # 4 Decisions (judgment layer)
      glossary.md           # 5 Glossary
      how-to/               #    optional task guides
      references/           # overflow / prose fold-in (article.template.md)
  ai/
    INDEX.md            # machine + human catalog (project → pages)
    CONTEXT.md          # how agents should load this wiki
    glossary.md         # global terms (short); prefer concepts/ for evergreen depth
    github-wiki-map.md  # written by wiki-sync-github.sh
  assets/
    wiki.css            # copied from skill on init; customize locally
  site/                 # GENERATED — do not hand-edit
    index.html
    projects/...
    concepts/...
    pagefind/           # Pagefind output
  .build/               # build cache / github-wiki clone
```

Optional PARA dirs (`areas/`, `resources/`, `archives/`) are **not** created by
default and are **not** in HTML nav. Set `WIKI_PARA=1` when running `wiki-init.sh`
only for personal overflow outside the wiki model. Prefer `projects/` + `concepts/`.

Optional vault git: `WIKI_GIT=1 wiki-init.sh` runs `git init` so the vault has
docs-as-code history (HITL diffs). Does not invent remotes.

## Project slug rules

- Lowercase, hyphens, short: `dotfiles`, `trading-desk`, `qan-app`.
- One active project folder = one sidebar group.
- Workspace ingest: default slug = repo name (kebab), unless user names one.
- Concepts use the same slug rules under `concepts/`.

## Empty / missing root

Treat as empty if:

- path does not exist, **or**
- exists but has no `config.yaml` and no `projects/` directory.

Then run init and create the tree above.

## config.yaml (minimal)

```yaml
root: ~/Documents/my-wiki
title: My Wiki
storage: local   # local | github_wiki
github_wiki:
  repo: ""       # owner/repo — asked when storage is github_wiki and empty
  remote: ""     # optional explicit wiki.git URL
build:
  site_dir: site
  pagefind: true
nav:
  group_by: project
maintain:
  inbox_max_age_days: 14
  reviewed_max_age_days: 90
projects:
  my-app:
    workspace: /absolute/path/to/my-app
```

`wiki-scaffold-project.sh` upserts `projects.{slug}`. Lint and incremental update
resolve the workspace from this map.

## Canonical project pages

Every project has: **Architecture**, **Topic index**, **Solution design** (+ feature
pages), **Decisions**, **Glossary**. Optional: **how-to/**. No Overview or Quick start.

Cross-project: **concepts/** evergreen notes.

## GitHub wiki layout note

GitHub wikis are a separate git repo (`*.wiki.git`) with mostly flat Markdown.
Use `wiki-sync-github.sh` (dry-run first; `--push` only after explicit approval):

- Keep local vault as source of truth (nested `projects/` + `concepts/`).
- Export flattened names; mapping written to `ai/github-wiki-map.md`.
