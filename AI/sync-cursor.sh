#!/usr/bin/env bash
# Sync AI skills and rules from this repo to the global Cursor directories.
# Source of truth: AI/skills and AI/rules
# Targets:       ~/.cursor/skills and ~/.cursor/global-user-rules.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_SKILLS="${SCRIPT_DIR}/skills"
SRC_RULES="${SCRIPT_DIR}/rules"
DEST_CURSOR="${HOME}/.cursor"
DEST_SKILLS="${DEST_CURSOR}/skills"
DEST_RULES_FILE="${DEST_CURSOR}/global-user-rules.md"
SRC_RULES_FILE="${SRC_RULES}/global-user-rules.md"

if [[ ! -d "${SRC_SKILLS}" ]]; then
  echo "error: missing skills dir: ${SRC_SKILLS}" >&2
  exit 1
fi

if [[ ! -f "${SRC_RULES_FILE}" ]]; then
  echo "error: missing rules file: ${SRC_RULES_FILE}" >&2
  exit 1
fi

mkdir -p "${DEST_SKILLS}"

echo "Syncing skills → ${DEST_SKILLS}"
rsync -a --delete --exclude '.DS_Store' "${SRC_SKILLS}/" "${DEST_SKILLS}/"

echo "Syncing rules  → ${DEST_RULES_FILE}"
cp "${SRC_RULES_FILE}" "${DEST_RULES_FILE}"

skill_count="$(find "${DEST_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
echo "Done. ${skill_count} skill folders synced; global-user-rules.md updated."
echo "Note: paste User Rules from ${DEST_RULES_FILE} into Cursor Settings → Rules if needed."
