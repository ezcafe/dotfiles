#!/usr/bin/env bash
# Add a project how-to / runbook page from the skill template.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SKILL_DIR/assets/project-pages/how-to.md"

SLUG="${1:-}"
TASK="${2:-}"
REPO_PATH="${3:-}"

if [[ -z "$SLUG" || -z "$TASK" ]]; then
  echo "Usage: wiki-add-howto.sh <project-slug> <task-slug> [workspace-path]"
  exit 1
fi

SLUG="$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
TASK="$(echo "$TASK" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
DEST_DIR="$ROOT/projects/$SLUG/how-to"
OUT="$DEST_DIR/$TASK.md"

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
TITLE="$(python3 "$SCRIPT_DIR/_wiki_config.py" title "$TASK")"

mkdir -p "$DEST_DIR"
if [[ -f "$OUT" ]]; then
  echo "skip (exists): $OUT"
  exit 0
fi

escape_sed() { printf '%s' "$1" | sed -e 's/[&|\\]/\\&/g'; }

sed \
  -e "s/PROJECT_SLUG/$(escape_sed "$SLUG")/g" \
  -e "s|REPO_PATH|$(escape_sed "$REPO_PATH")|g" \
  -e "s/GIT_SHA/$(escape_sed "$GIT_SHA")/g" \
  -e "s/YYYY-MM-DD/$TODAY/g" \
  -e "s/HOWTO_TITLE/$(escape_sed "$TITLE")/g" \
  "$TEMPLATE" > "$OUT"

TOPIC="$ROOT/projects/$SLUG/topic-index.md"
if [[ -f "$TOPIC" ]] && ! grep -q "how-to/$TASK" "$TOPIC" 2>/dev/null; then
  ROW="| How to ${TITLE} | [[projects/${SLUG}/how-to/${TASK}]] | Ops |"
  python3 - "$TOPIC" "$ROW" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
row = sys.argv[2]
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
out: list[str] = []
in_topic = False
in_table = False
inserted = False
for i, ln in enumerate(lines):
    if ln.startswith("## Topic map"):
        in_topic = True
        in_table = False
    elif in_topic and ln.startswith("## "):
        if in_table and not inserted:
            out.append(row + "\n")
            inserted = True
        in_topic = False
        in_table = False
    if in_topic and ln.strip().startswith("|"):
        in_table = True
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        out.append(ln)
        if in_table and not nxt.startswith("|") and not inserted:
            out.append(row + "\n")
            inserted = True
        continue
    out.append(ln)
if in_table and not inserted:
    out.append(row + "\n")
elif not inserted:
    out.append("\n" + row + "\n")
path.write_text("".join(out), encoding="utf-8")
PY
fi

if [[ -f "$ROOT/log.md" ]]; then
  echo "" >> "$ROOT/log.md"
  echo "## [$TODAY] distill | add how-to [[projects/$SLUG/how-to/$TASK]] against $GIT_SHA" >> "$ROOT/log.md"
fi

echo "created: $OUT"
echo "Fill from real tooling, then: wiki-build.sh && wiki-lint.py --project $SLUG"
