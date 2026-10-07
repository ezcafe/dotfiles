#!/usr/bin/env bash
# Sync ONLY after explicit approval (y). No auto-sync env bypass.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
CONFIG="${GTD_HOME}/config.yaml"

gh_on=false
rem_on=false
if [[ -f "${CONFIG}" ]]; then
  [[ "$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" github enabled)" == "true" ]] && gh_on=true
  [[ "$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" reminders enabled)" == "true" ]] && rem_on=true
fi

if [[ "${gh_on}" != true && "${rem_on}" != true ]]; then
  echo "No task UI enabled (choices.task_ui=none). Sync skipped."
  exit 0
fi

targets=()
[[ "${gh_on}" == true ]] && targets+=("GitHub")
[[ "${rem_on}" == true ]] && targets+=("Reminders")
target_label="$(IFS=' / '; echo "${targets[*]}")"

if [[ ! -t 0 ]]; then
  # Piped stdin: require an explicit y line; empty/cron → never sync
  if ! read -r ans; then
    ans=
  fi
  if [[ -z "${ans}" ]]; then
    echo "Sync skipped (no approval). Say y interactively or pipe 'y'."
    exit 0
  fi
else
  read -r -p "Sync to ${target_label} now? [y/N] " ans || ans=n
fi

case "${ans}" in
  y|Y|yes|YES)
    echo "Approved — syncing…"
    [[ "${gh_on}" == true ]] && "${SCRIPT_DIR}/gtd-sync-github.sh" || true
    [[ "${rem_on}" == true ]] && "${SCRIPT_DIR}/gtd-sync-reminders.sh" || true
    echo "Sync done."
    ;;
  *)
    echo "Sync skipped (not approved)."
    ;;
esac
