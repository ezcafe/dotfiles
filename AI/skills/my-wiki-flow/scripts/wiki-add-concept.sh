#!/usr/bin/env bash
# Add a cross-project evergreen concept page.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SKILL_DIR/assets/project-pages/concept.md"
TOPIC_TEMPLATE="$SKILL_DIR/assets/project-pages/concepts-topic-index.md"

CONCEPT="${1:-}"

if [[ -z "$CONCEPT" ]]; then
  echo "Usage: wiki-add-concept.sh <concept-slug>"
  exit 1
fi

CONCEPT="$(echo "$CONCEPT" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
DEST_DIR="$ROOT/concepts"
OUT="$DEST_DIR/$CONCEPT.md"
TODAY="$(date +%Y-%m-%d)"
TITLE="$(python3 "$SCRIPT_DIR/_wiki_config.py" title "$CONCEPT")"

mkdir -p "$DEST_DIR"

if [[ ! -f "$DEST_DIR/topic-index.md" ]]; then
  sed -e "s/YYYY-MM-DD/$TODAY/g" "$TOPIC_TEMPLATE" > "$DEST_DIR/topic-index.md"
  echo "created: $DEST_DIR/topic-index.md"
fi

if [[ -f "$OUT" ]]; then
  echo "skip (exists): $OUT"
  exit 0
fi

escape_sed() { printf '%s' "$1" | sed -e 's/[&|\\]/\\&/g'; }

sed \
  -e "s/CONCEPT_TITLE/$(escape_sed "$TITLE")/g" \
  -e "s/YYYY-MM-DD/$TODAY/g" \
  "$TEMPLATE" > "$OUT"

TOPIC="$DEST_DIR/topic-index.md"
if [[ -f "$TOPIC" ]] && ! grep -q "concepts/$CONCEPT" "$TOPIC" 2>/dev/null; then
  printf '\n| %s | [[concepts/%s]] | |\n' "$TITLE" "$CONCEPT" >> "$TOPIC"
fi

if [[ -f "$ROOT/log.md" ]]; then
  echo "" >> "$ROOT/log.md"
  echo "## [$TODAY] distill | add concept [[concepts/$CONCEPT]]" >> "$ROOT/log.md"
fi

echo "created: $OUT"
echo "Fill in your words, set confidence/reviewed, then: wiki-build.sh && wiki-lint.py --maintain"
