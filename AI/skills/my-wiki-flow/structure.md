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
  projects/             # PRIMARY nav grouping
    {project-slug}/
      architecture.md       # 1 Architecture
      solution-design.md    # 2 Solution design hub
      solution-design/      #    one page per feature
      glossary.md           # 3 Glossary
      references/           # overflow only (use article.template.md)
  ai/
    INDEX.md            # machine + human catalog (project → pages)
    CONTEXT.md          # how agents should load this wiki
    glossary.md         # global terms
    github-wiki-map.md  # written by wiki-sync-github.sh
  assets/
    wiki.css            # copied from skill on init; customize locally
  site/                 # GENERATED — do not hand-edit
    index.html
    projects/...
    pagefind/           # Pagefind output
  .build/               # build cache / github-wiki clone
```

Optional PARA dirs (`areas/`, `resources/`, `archives/`) are **not** created by
default. Set `WIKI_PARA=1` when running `wiki-init.sh` if you want them. They are
not in HTML nav.

## Project slug rules

- Lowercase, hyphens, short: `dotfiles`, `trading-desk`, `qan-app`.
- One active project folder = one sidebar group.
- Workspace ingest: default slug = repo name (kebab), unless user names one.

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
projects:
  my-app:
    workspace: /absolute/path/to/my-app
```

`wiki-scaffold-project.sh` upserts `projects.{slug}`. Lint and incremental update
resolve the workspace from this map.

## Canonical project pages

Every project has: **Architecture**, **Solution design** (+ feature pages), **Glossary**.
No Overview or Quick start pages.

## GitHub wiki layout note

GitHub wikis are a separate git repo (`*.wiki.git`) with mostly flat Markdown.
Use `wiki-sync-github.sh` (dry-run first; `--push` only after explicit approval):

- Keep local vault as source of truth (nested `projects/`).
- Export flattened names; mapping written to `ai/github-wiki-map.md`.
