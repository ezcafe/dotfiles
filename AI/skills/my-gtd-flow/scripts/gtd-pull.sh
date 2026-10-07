#!/usr/bin/env bash
# Manual / hourly pull: Apple Calendar and/or Outlook from remembered choices.
# Calendars are READ-ONLY — never create/edit/delete events.
# Flags override config; with no flags, use adapters.calendar.apple / .outlook.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
CONFIG="${GTD_HOME}/config.yaml"
mkdir -p "${GTD_HOME}/logs"

do_apple=""
do_outlook=""
from_flags=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --outlook)
      do_outlook=true
      from_flags=true
      shift
      ;;
    --apple-only)
      do_apple=true
      do_outlook=false
      from_flags=true
      shift
      ;;
    --outlook-only)
      do_apple=false
      do_outlook=true
      from_flags=true
      shift
      ;;
    --both)
      do_apple=true
      do_outlook=true
      from_flags=true
      shift
      ;;
    -h|--help)
      echo "Usage: gtd-pull.sh [--apple-only|--outlook|--outlook-only|--both]"
      echo "  Default: use remembered choices from config (gtd-setup-ui.sh)."
      echo "  Env: GTD_PULL_OUTLOOK=1, GTD_AGENT_MODEL=inherit|fast-slug"
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 2
      ;;
  esac
done

if [[ "${from_flags}" != true ]]; then
  if [[ -f "${CONFIG}" ]]; then
    do_apple="$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" calendar apple)"
    do_outlook="$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" calendar outlook)"
    enabled="$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" calendar enabled)"
    if [[ "${enabled}" == "true" && "${do_apple}" != "true" && "${do_outlook}" != "true" ]]; then
      src="$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" calendar source)"
      case "${src}" in
        apple|both|"") do_apple=true ;;
      esac
      case "${src}" in
        outlook|both) do_outlook=true ;;
      esac
    fi
  else
    do_apple=true
    do_outlook=false
  fi
fi

if [[ "${GTD_PULL_OUTLOOK:-0}" == "1" ]]; then
  do_outlook=true
fi

status=0

if [[ "${do_apple}" != "true" && "${do_outlook}" != "true" ]]; then
  echo "No calendar source enabled (choices.calendar_source=none). Skipping pull."
  echo "  Change with: gtd-setup-ui.sh --reask"
  exit 0
fi

if [[ "${do_apple}" == "true" ]]; then
  echo "Pull Apple Calendar (read-only)…"
  if ! "${SCRIPT_DIR}/gtd-pull-calendar.sh"; then
    echo "warn: Apple Calendar pull failed" >&2
    status=1
  fi
fi

if [[ "${do_outlook}" == "true" ]]; then
  echo "Pull Outlook (read-only, model=${GTD_AGENT_MODEL:-inherit})…"
  if ! "${SCRIPT_DIR}/gtd-agent.sh" -p --force --approve-mcps -- \
    "Read skill my-gtd-flow. Pull Outlook calendar for today into ~/.my-gtd/meetings.json per outlook-playwright.md. READ-ONLY: never create/edit/delete/RSVP Outlook or Apple Calendar events. Do not plan or sync. Ask only if login is required."; then
    echo "warn: Outlook pull failed" >&2
    status=1
  fi
fi

exit "${status}"
