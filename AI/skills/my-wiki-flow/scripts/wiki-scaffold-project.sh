#!/usr/bin/env bash
# Scaffold canonical project pages under projects/{slug}/.
# Usage: wiki-scaffold-project.sh <slug> [workspace-path] [--lite]
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES="$SKILL_DIR/assets/project-pages"

SLUG=""
REPO_PATH="."
PROFILE="full"

for arg in "$@"; do
  case "$arg" in
    --lite) PROFILE="lite" ;;
    --full) PROFILE="full" ;;
    -*)
      echo "Unknown flag: $arg" >&2
      exit 1
      ;;
    *)
      if [[ -z "$SLUG" ]]; then
        SLUG="$arg"
      elif [[ "$REPO_PATH" == "." ]]; then
        REPO_PATH="$arg"
      fi
      ;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "Usage: wiki-scaffold-project.sh <project-slug> [workspace-path] [--lite|--full]"
  echo "  --lite  Only Overview + Quick start (expand later with --full or re-scaffold)"
  exit 1
fi

SLUG="$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
DEST="$ROOT/projects/$SLUG"
GIT_SHA="unknown"
if git -C "$REPO_PATH" rev-parse --short HEAD >/dev/null 2>&1; then
  GIT_SHA="$(git -C "$REPO_PATH" rev-parse --short HEAD)"
fi
TODAY="$(date +%Y-%m-%d)"
# Absolute workspace for config
ABS_REPO="$(cd "$REPO_PATH" 2>/dev/null && pwd || echo "$REPO_PATH")"

mkdir -p "$DEST/solution-design" "$DEST/references"

if [[ "$PROFILE" == "lite" ]]; then
  PAGES=(index.md quick-start.md)
else
  PAGES=(index.md quick-start.md architecture.md solution-design.md glossary.md)
fi

for page in "${PAGES[@]}"; do
  out="$DEST/$page"
  if [[ -f "$out" ]]; then
    echo "skip (exists): $out"
    continue
  fi
  sed \
    -e "s/PROJECT_SLUG/$SLUG/g" \
    -e "s|REPO_PATH|$ABS_REPO|g" \
    -e "s/GIT_SHA/$GIT_SHA/g" \
    -e "s/YYYY-MM-DD/$TODAY/g" \
    "$TEMPLATES/$page" > "$out"
  echo "created: $out"
done

# Remove obsolete pages from older scaffolds
for obsolete in tips-and-tricks.md design-guide.md; do
  if [[ -f "$DEST/$obsolete" ]]; then
    rm -f "$DEST/$obsolete"
    echo "removed obsolete: $DEST/$obsolete"
  fi
done

python3 "$SCRIPT_DIR/_wiki_config.py" upsert-project "$ROOT/config.yaml" "$SLUG" "$ABS_REPO" "$PROFILE"

if [[ -f "$ROOT/log.md" ]]; then
  echo "" >> "$ROOT/log.md"
  echo "## [$TODAY] distill | scaffold project [[projects/$SLUG/index]] profile=$PROFILE against $GIT_SHA" >> "$ROOT/log.md"
fi

echo "Scaffolded projects/$SLUG (profile=$PROFILE) — fill from real code, then wiki-build.sh"
if [[ "$PROFILE" == "lite" ]]; then
  echo "Lite: Overview + Quick start only. Later: wiki-scaffold-project.sh $SLUG $ABS_REPO --full"
else
  echo "Feature pages: wiki-add-feature.sh $SLUG <feature-slug> [master-feature]"
fi
