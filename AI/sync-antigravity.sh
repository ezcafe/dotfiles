#!/usr/bin/env bash
# Sync repo AI/rules + skills to global Antigravity config:
#   - Skills → ~/.gemini/config/skills/<skill_name>/
#   - Rules  → ~/.gemini/config/rules/<rule_file> and ~/.gemini/GEMINI.md
#
# Usage:
#   ./sync-antigravity.sh           # sync all skills and rules
#   ./sync-antigravity.sh --check   # check drift between SoT and global config

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_SKILLS="${SCRIPT_DIR}/skills"
SRC_RULES="${SCRIPT_DIR}/rules"

DEST_GEMINI_DIR="${HOME}/.gemini"
DEST_CONFIG_DIR="${DEST_GEMINI_DIR}/config"
DEST_SKILLS="${DEST_CONFIG_DIR}/skills"
DEST_RULES="${DEST_CONFIG_DIR}/rules"
DEST_GLOBAL_MD="${DEST_GEMINI_DIR}/GEMINI.md"

CHECK_ONLY=0
if [[ "${1:-}" == "--check" ]]; then
  CHECK_ONLY=1
elif [[ -n "${1:-}" ]]; then
  echo "usage: $0 [--check]" >&2
  exit 2
fi

if [[ ! -d "${SRC_SKILLS}" ]]; then
  echo "error: missing skills dir: ${SRC_SKILLS}" >&2
  exit 1
fi

if [[ ! -d "${SRC_RULES}" ]]; then
  echo "error: missing rules dir: ${SRC_RULES}" >&2
  exit 1
fi

mkdir -p "${DEST_SKILLS}" "${DEST_RULES}"

# --- Check Mode ---
if [[ "${CHECK_ONLY}" -eq 1 ]]; then
  drift=0
  echo "Checking drift: ${SRC_SKILLS} ↔ ${DEST_SKILLS}"
  shopt -s nullglob
  for d in "${SRC_SKILLS}"/*/; do
    [[ -d "$d" ]] || continue
    name="$(basename "${d%/}")"
    [[ "${name}" == "_archive" ]] && continue
    [[ -f "${d%/}/SKILL.md" ]] || continue
    dest_dir="${DEST_SKILLS}/${name}"
    if [[ ! -d "$dest_dir" ]]; then
      echo "missing in Antigravity config: ${name}"
      drift=1
      continue
    fi
    if ! diff -qr \
      --exclude '.DS_Store' \
      --exclude '__pycache__' \
      --exclude '*.pyc' \
      "${d%/}" "$dest_dir" >/tmp/sync-antigravity-check.$$.txt 2>&1; then
      echo "drift: ${name}"
      cat /tmp/sync-antigravity-check.$$.txt
      drift=1
    else
      echo "ok: ${name}"
    fi
    rm -f /tmp/sync-antigravity-check.$$.txt
  done
  shopt -u nullglob

  if [[ "$drift" -ne 0 ]]; then
    echo "FAIL: skills SoT ↔ Antigravity config drift — run: $0" >&2
    exit 1
  fi
  echo "ok: all skills in Antigravity config match SoT"
  exit 0
fi

# --- Sync Skills ---
echo "Syncing skills → ${DEST_SKILLS}"
skill_count=0
shopt -s nullglob
for d in "${SRC_SKILLS}"/*/; do
  name="$(basename "${d%/}")"
  [[ "${name}" == "_archive" ]] && continue
  [[ -f "${d}SKILL.md" ]] || continue
  rsync -a "${d%/}/" "${DEST_SKILLS}/${name}/"
  skill_count=$((skill_count + 1))
  echo "  skill: ${name}"
done
shopt -u nullglob

# --- Sync Rules ---
echo "Syncing rules → ${DEST_RULES} and ${DEST_GLOBAL_MD}"
rule_count=0
shopt -s nullglob
for rule_file in "${SRC_RULES}"/*; do
  [[ -f "${rule_file}" ]] || continue
  name="$(basename "${rule_file}")"
  [[ "${name}" == .DS_Store ]] && continue

  echo "  rule: ${name}"
  cp "${rule_file}" "${DEST_RULES}/${name}"
  rule_count=$((rule_count + 1))

  # If this is global-user-rules.md, also populate ~/.gemini/GEMINI.md
  if [[ "${name}" == "global-user-rules.md" ]]; then
    if grep -q "## ---START---" "${rule_file}" && grep -q "## ---END---" "${rule_file}"; then
      # Extract between markers
      sed -n '/## ---START---/,/## ---END---/p' "${rule_file}" \
        | sed '1d;$d' > "${DEST_GLOBAL_MD}"
    else
      cp "${rule_file}" "${DEST_GLOBAL_MD}"
    fi
    echo "  global instructions: updated ${DEST_GLOBAL_MD}"
  fi
done
shopt -u nullglob

echo "Done. Synced ${skill_count} skill(s) and ${rule_count} rule(s) to Antigravity global config."
echo "Skills: ${DEST_SKILLS}"
echo "Rules:  ${DEST_RULES} and ${DEST_GLOBAL_MD}"
