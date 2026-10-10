#!/usr/bin/env bash
# Create ~/Documents/my-wiki (or WIKI_ROOT) skeleton if missing/empty.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TITLE="${WIKI_TITLE:-My Wiki}"

is_empty() {
  local d="$1"
  [[ ! -d "$d" ]] && return 0
  [[ ! -f "$d/config.yaml" && ! -d "$d/projects" ]] && return 0
  return 1
}

fill_karpathy_gaps() {
  mkdir -p "$ROOT/raw" "$ROOT/site"
  if [[ -f "$SKILL_DIR/assets/AGENTS.template.md" && ! -f "$ROOT/AGENTS.md" ]]; then
    cp "$SKILL_DIR/assets/AGENTS.template.md" "$ROOT/AGENTS.md"
  fi
  if [[ ! -f "$ROOT/index.md" ]]; then
    cat > "$ROOT/index.md" <<EOF
# Wiki index

$TITLE — rebuild with \`wiki-build.sh\` to refresh catalog links.

## inbox

_Empty._
EOF
  fi
  if [[ ! -f "$ROOT/log.md" ]]; then
    cat > "$ROOT/log.md" <<EOF
# Log

## [$(date +%Y-%m-%d)] init | Karpathy layout files added
EOF
  fi
  if [[ ! -f "$ROOT/raw/README.md" ]]; then
    cat > "$ROOT/raw/README.md" <<EOF
# Raw sources

Immutable inputs. Wiki pages cite \`source: raw/...\`.
EOF
  fi
}

if ! is_empty "$ROOT"; then
  fill_karpathy_gaps
  echo "Wiki already initialized: $ROOT (Karpathy layout checked)"
  exit 0
fi

mkdir -p \
  "$ROOT/raw" \
  "$ROOT/inbox" \
  "$ROOT/projects" \
  "$ROOT/ai" \
  "$ROOT/assets" \
  "$ROOT/site"
# Optional PARA overflow (not in HTML nav): create only if WIKI_PARA=1
if [[ "${WIKI_PARA:-0}" == "1" ]]; then
  mkdir -p "$ROOT/areas" "$ROOT/resources" "$ROOT/archives"
fi

cp "$SKILL_DIR/assets/wiki.css" "$ROOT/assets/wiki.css"
if [[ -f "$SKILL_DIR/assets/AGENTS.template.md" && ! -f "$ROOT/AGENTS.md" ]]; then
  cp "$SKILL_DIR/assets/AGENTS.template.md" "$ROOT/AGENTS.md"
fi

cat > "$ROOT/config.yaml" <<EOF
root: $ROOT
title: $TITLE
storage: local
github_wiki:
  repo: ""
  remote: ""
build:
  site_dir: site
  pagefind: true
nav:
  group_by: project
# Map each project slug to its code workspace (used by distill / lint / update).
projects: {}
# Example:
# projects:
#   my-app:
#     workspace: /path/to/my-app
#     profile: full   # full | lite
EOF

cat > "$ROOT/README.md" <<EOF
# $TITLE

Personal knowledge wiki (my-wiki-flow) — Karpathy three-layer pattern.

- **Raw sources:** \`raw/\` (immutable)
- **Wiki articles:** \`projects/\`, \`inbox/\`
- **Schema:** \`AGENTS.md\`, root \`index.md\`, \`log.md\`
- **Generated site:** \`site/\` (HTML + Pagefind)
- **AI entrypoints:** \`ai/INDEX.md\`, \`ai/CONTEXT.md\`

Run \`wiki-build.sh\` after adding Markdown pages.
Compatible with [Understand Anything](https://github.com/Egonex-AI/Understand-Anything) \`/understand-knowledge\`.
EOF

if [[ ! -f "$ROOT/index.md" ]]; then
  cat > "$ROOT/index.md" <<EOF
# Wiki index

$TITLE — add projects under \`projects/{slug}/\`, then rebuild.

## inbox

_Empty._
EOF
fi

if [[ ! -f "$ROOT/log.md" ]]; then
  cat > "$ROOT/log.md" <<EOF
# Log

Append-only timeline. Format: \`## [YYYY-MM-DD] operation | Title\`

## [$(date +%Y-%m-%d)] init | Vault created
EOF
fi

cat > "$ROOT/raw/README.md" <<EOF
# Raw sources

Place immutable inputs here (exports, clips, PDFs, originals). Wiki pages cite paths as \`source: raw/...\`.
EOF

cat > "$ROOT/ai/CONTEXT.md" <<EOF
# AI context — $TITLE

- **Root:** \`$ROOT\`
- **Canonical:** Markdown under \`projects/\`
- **Do not:** paste all of \`site/\` into the prompt

## How to answer from this wiki

1. Pick project(s) from [INDEX.md](INDEX.md)
2. Read that project's \`index.md\` + matching pages
3. Prefer frontmatter \`summary\` before full body
4. Cite page paths when stating facts from the wiki
5. If missing, say so — do not invent wiki content
EOF

cat > "$ROOT/ai/INDEX.md" <<EOF
# Wiki index

_No projects yet. Ingest a workspace or add \`projects/{slug}/index.md\`._

## inbox

_Empty._
EOF

cat > "$ROOT/ai/glossary.md" <<EOF
# Glossary

| Term | Meaning |
|------|---------|
EOF

cat > "$ROOT/projects/.gitkeep" <<EOF
EOF

cat > "$ROOT/inbox/README.md" <<EOF
# Inbox

Drop uncategorized captures here. Distill into \`projects/{slug}/\` later.
EOF

echo "Initialized wiki at $ROOT"
