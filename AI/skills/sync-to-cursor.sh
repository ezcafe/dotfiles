#!/usr/bin/env bash
# Sync AI/skills (source of truth) → ~/.cursor/skills for Cursor discovery.
# Does not delete unrelated skills already in ~/.cursor/skills.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${HOME}/.cursor/skills"
mkdir -p "$DEST"

count=0
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  [[ -f "${d}SKILL.md" ]] || continue
  rsync -a "${d%/}/" "${DEST}/${name}/"
  count=$((count + 1))
  echo "synced ${name}"
done

echo "Done: ${count} skill(s) from ${SRC} → ${DEST}"
echo "Source of truth remains: ${SRC}"
