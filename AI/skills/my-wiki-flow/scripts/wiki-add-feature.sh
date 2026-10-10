#!/usr/bin/env bash
# Add a solution-design feature page from the skill template.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SKILL_DIR/assets/project-pages/solution-design-feature.md"

SLUG="${1:-}"
FEATURE="${2:-}"
MASTER="${3:-}"
REPO_PATH="${4:-}"

if [[ -z "$SLUG" || -z "$FEATURE" ]]; then
  echo "Usage: wiki-add-feature.sh <project-slug> <feature-slug> [master-feature-name] [workspace-path]"
  exit 1
fi

SLUG="$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
FEATURE="$(echo "$FEATURE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
DEST_DIR="$ROOT/projects/$SLUG/solution-design"
OUT="$DEST_DIR/$FEATURE.md"

if [[ ! -d "$ROOT/projects/$SLUG" ]]; then
  echo "Project missing: $ROOT/projects/$SLUG — run wiki-scaffold-project.sh first." >&2
  exit 1
fi

if [[ -z "$REPO_PATH" ]]; then
  REPO_PATH="$(python3 "$SCRIPT_DIR/_wiki_config.py" workspace "$ROOT/config.yaml" "$SLUG")"
fi
REPO_PATH="${REPO_PATH:-.}"

GIT_SHA="unknown"
if git -C "$REPO_PATH" rev-parse --short HEAD >/dev/null 2>&1; then
  GIT_SHA="$(git -C "$REPO_PATH" rev-parse --short HEAD)"
fi
TODAY="$(date +%Y-%m-%d)"
TITLE="$(python3 "$SCRIPT_DIR/_wiki_config.py" title "$FEATURE")"
MASTER_NAME="${MASTER:-ungrouped}"

mkdir -p "$DEST_DIR"
if [[ -f "$OUT" ]]; then
  echo "skip (exists): $OUT"
  exit 0
fi

# Escape sed replacements that may contain &
escape_sed() { printf '%s' "$1" | sed -e 's/[&|\\]/\\&/g'; }

sed \
  -e "s/PROJECT_SLUG/$(escape_sed "$SLUG")/g" \
  -e "s|REPO_PATH|$(escape_sed "$REPO_PATH")|g" \
  -e "s/GIT_SHA/$(escape_sed "$GIT_SHA")/g" \
  -e "s/YYYY-MM-DD/$TODAY/g" \
  -e "s/FEATURE_TITLE/$(escape_sed "$TITLE")/g" \
  -e "s/MASTER_FEATURE_NAME/$(escape_sed "$MASTER_NAME")/g" \
  "$TEMPLATE" > "$OUT"

HUB="$ROOT/projects/$SLUG/solution-design.md"
if [[ -f "$HUB" ]] && ! grep -q "solution-design/$FEATURE" "$HUB" 2>/dev/null; then
  printf '\n- [[projects/%s/solution-design/%s|%s]]\n' "$SLUG" "$FEATURE" "$TITLE" >> "$HUB"
fi

if [[ -f "$ROOT/log.md" ]]; then
  echo "" >> "$ROOT/log.md"
  echo "## [$TODAY] distill | add feature [[projects/$SLUG/solution-design/$FEATURE]] against $GIT_SHA" >> "$ROOT/log.md"
fi

echo "created: $OUT"
echo "Fill from real code, then: wiki-build.sh && wiki-lint.py --project $SLUG"
