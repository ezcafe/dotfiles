#!/usr/bin/env bash
# Sync only the skills and rules that live in this repo to the global Cursor dirs.
# Skills/rules present in ~/.cursor but missing from this repo are left alone.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_SKILLS="${SCRIPT_DIR}/skills"
SRC_RULES="${SCRIPT_DIR}/rules"
DEST_CURSOR="${HOME}/.cursor"
DEST_SKILLS="${DEST_CURSOR}/skills"

if [[ ! -d "${SRC_SKILLS}" ]]; then
  echo "error: missing skills dir: ${SRC_SKILLS}" >&2
  exit 1
fi

if [[ ! -d "${SRC_RULES}" ]]; then
  echo "error: missing rules dir: ${SRC_RULES}" >&2
  exit 1
fi

mkdir -p "${DEST_SKILLS}"

skill_count=0
echo "Syncing repo skills → ${DEST_SKILLS}"
shopt -s nullglob
for skill_dir in "${SRC_SKILLS}"/*/; do
  name="$(basename "${skill_dir}")"
  echo "  skill: ${name}"
  # Mirror this skill's contents only; do not touch sibling skills in DEST.
  rsync -a --delete --exclude '.DS_Store' "${skill_dir}" "${DEST_SKILLS}/${name}/"
  skill_count=$((skill_count + 1))
done

rule_count=0
echo "Syncing repo rules → ${DEST_CURSOR}"
for rule_file in "${SRC_RULES}"/*; do
  [[ -f "${rule_file}" ]] || continue
  name="$(basename "${rule_file}")"
  [[ "${name}" == .DS_Store ]] && continue
  echo "  rule: ${name}"
  cp "${rule_file}" "${DEST_CURSOR}/${name}"
  rule_count=$((rule_count + 1))
done
shopt -u nullglob

echo "Done. Updated ${skill_count} skill(s) and ${rule_count} rule file(s) from this repo."
echo "Other skills/rules already in ${DEST_CURSOR} were left unchanged."
if [[ -f "${DEST_CURSOR}/global-user-rules.md" ]]; then
  echo "Note: paste User Rules from ${DEST_CURSOR}/global-user-rules.md into Cursor Settings → Rules if needed."
fi
