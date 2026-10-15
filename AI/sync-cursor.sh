#!/usr/bin/env bash
# Sync repo AI/rules (+ skills via the single SoT skills sync script).
# Skills SoT sync: AI/skills/sync-to-cursor.sh (do not duplicate rsync here).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_SKILLS="${SCRIPT_DIR}/skills"
SRC_RULES="${SCRIPT_DIR}/rules"
DEST_CURSOR="${HOME}/.cursor"
SKILLS_SYNC="${SRC_SKILLS}/sync-to-cursor.sh"

if [[ ! -d "${SRC_SKILLS}" ]]; then
  echo "error: missing skills dir: ${SRC_SKILLS}" >&2
  exit 1
fi

if [[ ! -f "${SKILLS_SYNC}" ]]; then
  echo "error: missing skills sync SoT: ${SKILLS_SYNC}" >&2
  exit 1
fi

if [[ ! -d "${SRC_RULES}" ]]; then
  echo "error: missing rules dir: ${SRC_RULES}" >&2
  exit 1
fi

echo "Skills (SoT): ${SKILLS_SYNC}"
"${SKILLS_SYNC}"

rule_count=0
echo "Syncing repo rules → ${DEST_CURSOR}"
shopt -s nullglob
for rule_file in "${SRC_RULES}"/*; do
  [[ -f "${rule_file}" ]] || continue
  name="$(basename "${rule_file}")"
  [[ "${name}" == .DS_Store ]] && continue
  echo "  rule: ${name}"
  cp "${rule_file}" "${DEST_CURSOR}/${name}"
  rule_count=$((rule_count + 1))
done
shopt -u nullglob

echo "Done. Updated rules (${rule_count} file(s)). Skills via sync-to-cursor.sh."
echo "Other skills/rules already in ${DEST_CURSOR} were left unchanged."
if [[ -f "${DEST_CURSOR}/global-user-rules.md" ]]; then
  echo "Note: paste User Rules from ${DEST_CURSOR}/global-user-rules.md into Cursor Settings → Rules if needed."
fi
