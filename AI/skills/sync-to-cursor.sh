#!/usr/bin/env bash
# Sync AI/skills (source of truth) → ~/.cursor/skills for Cursor discovery.
# SoT for skills sync in this repo (do not maintain a second skills sync path).
# Does not delete unrelated skills already in ~/.cursor/skills.
#
# Usage:
#   ./AI/skills/sync-to-cursor.sh           # sync all skills with SKILL.md
#   ./AI/skills/sync-to-cursor.sh --check   # diff my-dev-flow* SoT ↔ discovery; exit 1 on drift
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${HOME}/.cursor/skills"
CHECK_ONLY=0

if [[ "${1:-}" == "--check" ]]; then
  CHECK_ONLY=1
elif [[ -n "${1:-}" ]]; then
  echo "usage: $0 [--check]" >&2
  exit 2
fi

mkdir -p "$DEST"

if [[ "$CHECK_ONLY" -eq 1 ]]; then
  drift=0
  shopt -s nullglob
  for d in "$SRC"/my-dev-flow "$SRC"/my-dev-flow-*/; do
    [[ -d "$d" ]] || continue
    name="$(basename "${d%/}")"
    [[ -f "${d%/}/SKILL.md" ]] || continue
    dest_dir="${DEST}/${name}"
    if [[ ! -d "$dest_dir" ]]; then
      echo "missing in discovery: ${name}"
      drift=1
      continue
    fi
    # Compare trees (exclude junk). Quiet when identical.
    if ! diff -qr \
      --exclude '.DS_Store' \
      --exclude '__pycache__' \
      --exclude '*.pyc' \
      "${d%/}" "$dest_dir" >/tmp/sync-to-cursor-check.$$.txt 2>&1; then
      echo "drift: ${name}"
      cat /tmp/sync-to-cursor-check.$$.txt
      drift=1
    else
      echo "ok: ${name}"
    fi
    rm -f /tmp/sync-to-cursor-check.$$.txt
  done
  shopt -u nullglob
  if [[ "$drift" -ne 0 ]]; then
    echo "FAIL: my-dev-flow* SoT ↔ ~/.cursor/skills drift — run: $0" >&2
    exit 1
  fi
  echo "ok: my-dev-flow* discovery matches SoT"
  exit 0
fi

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
echo "Drift check (optional): $0 --check"
