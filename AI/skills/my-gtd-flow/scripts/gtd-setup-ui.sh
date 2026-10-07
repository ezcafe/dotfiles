#!/usr/bin/env bash
# Interactive (or flagged) setup: pick task UI + calendar, remember choices, run B scripts.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
CONFIG="${GTD_HOME}/config.yaml"

usage() {
  cat <<EOF
Usage: gtd-setup-ui.sh [options]

Interactive (default on a TTY): ask task UI + calendar, save to config, run setup.

Task UI:
  --task-ui github|reminders|both|none
  --github | --reminders | --all | --none-ui

Calendar (read-only pulls):
  --calendar apple|outlook|both|none

Other:
  --reask     Ask again (ignore remembered defaults as auto-keep)
  --yes       Non-interactive: flags or remembered only
  -h, --help

Choices saved under choices.* and adapters.*.enabled in ~/.my-gtd/config.yaml
EOF
}

task_ui=""
calendar_source=""
task_from_flag=false
cal_from_flag=false
reask=false
force_yes=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --task-ui)
      task_ui="$2"
      task_from_flag=true
      shift 2
      ;;
    --calendar)
      calendar_source="$2"
      cal_from_flag=true
      shift 2
      ;;
    --github) task_ui=github; task_from_flag=true; shift ;;
    --reminders) task_ui=reminders; task_from_flag=true; shift ;;
    --all) task_ui=both; task_from_flag=true; shift ;;
    --none-ui) task_ui=none; task_from_flag=true; shift ;;
    --reask) reask=true; shift ;;
    --yes) force_yes=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

"${SCRIPT_DIR}/gtd-init.sh"

ask_menu() {
  local prompt="$1"
  shift
  local options=("$@")
  local i choice
  echo "" >&2
  echo "$prompt" >&2
  for i in "${!options[@]}"; do
    printf "  %d) %s\n" $((i + 1)) "${options[$i]}" >&2
  done
  while true; do
    read -r -p "Choice [1-${#options[@]}]: " choice || choice=""
    if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#options[@]} )); then
      echo "${options[$((choice - 1))]}"
      return
    fi
    echo "Enter a number 1-${#options[@]}." >&2
  done
}

normalize_task() {
  case "$1" in
    github|Github|GITHUB|"GitHub only") echo github ;;
    reminders|Reminders|"Apple Reminders only") echo reminders ;;
    both|Both|BOTH|"Both GitHub and Reminders") echo both ;;
    none|None|NONE|"None") echo none ;;
    *) echo "" ;;
  esac
}

normalize_cal() {
  case "$1" in
    apple|Apple|APPLE|"Apple Calendar") echo apple ;;
    outlook|Outlook|OUTLOOK|microsoft|"Microsoft Outlook") echo outlook ;;
    both|Both|BOTH|"Both Apple Calendar and Outlook") echo both ;;
    none|None|NONE|"None") echo none ;;
    *) echo "" ;;
  esac
}

remembered_task="none"
remembered_cal="none"
if [[ -f "${CONFIG}" ]]; then
  eval "$(
    python3 "${SCRIPT_DIR}/gtd_prefs.py" "${CONFIG}" get | python3 -c '
import json,sys,shlex
d=json.load(sys.stdin)
print("remembered_task="+shlex.quote(d.get("task_ui") or "none"))
print("remembered_cal="+shlex.quote(d.get("calendar_source") or "none"))
'
  )"
fi

resolve_task() {
  if [[ "${task_from_flag}" == true ]]; then
    task_ui="$(normalize_task "${task_ui}")"
    return
  fi
  if [[ "${reask}" != true && "${remembered_task}" != "none" ]]; then
    if [[ -t 0 && "${force_yes}" != true ]]; then
      echo "Remembered task UI: ${remembered_task}" >&2
      read -r -p "Keep it? [Y/n] " keep || keep=Y
      case "${keep}" in
        n|N|no|NO) ;;
        *) task_ui="${remembered_task}"; return ;;
      esac
    else
      task_ui="${remembered_task}"
      return
    fi
  fi
  if [[ -t 0 && "${force_yes}" != true ]]; then
    pick="$(ask_menu "Task UI — where should tasks live?" \
      "GitHub only" \
      "Apple Reminders only" \
      "Both GitHub and Reminders" \
      "None")"
    task_ui="$(normalize_task "${pick}")"
  else
    task_ui="${remembered_task}"
    echo "Non-interactive: task_ui=${task_ui}" >&2
  fi
}

resolve_cal() {
  if [[ "${cal_from_flag}" == true ]]; then
    calendar_source="$(normalize_cal "${calendar_source}")"
    return
  fi
  if [[ "${reask}" != true && "${remembered_cal}" != "none" ]]; then
    if [[ -t 0 && "${force_yes}" != true ]]; then
      echo "Remembered calendar: ${remembered_cal}" >&2
      read -r -p "Keep it? [Y/n] " keepc || keepc=Y
      case "${keepc}" in
        n|N|no|NO) ;;
        *) calendar_source="${remembered_cal}"; return ;;
      esac
    else
      calendar_source="${remembered_cal}"
      return
    fi
  fi
  if [[ -t 0 && "${force_yes}" != true ]]; then
    pick="$(ask_menu "Meetings — which calendar to pull (read-only)?" \
      "Apple Calendar" \
      "Microsoft Outlook" \
      "Both Apple Calendar and Outlook" \
      "None")"
    calendar_source="$(normalize_cal "${pick}")"
  else
    calendar_source="${remembered_cal}"
    echo "Non-interactive: calendar_source=${calendar_source}" >&2
  fi
}

resolve_task
resolve_cal

task_ui="$(normalize_task "${task_ui}")"
calendar_source="$(normalize_cal "${calendar_source}")"
[[ -n "${task_ui}" ]] || { echo "invalid task_ui" >&2; exit 2; }
[[ -n "${calendar_source}" ]] || { echo "invalid calendar_source" >&2; exit 2; }

echo ""
echo "Saving choices: task_ui=${task_ui} calendar_source=${calendar_source}"
python3 "${SCRIPT_DIR}/gtd_prefs.py" "${CONFIG}" set "${task_ui}" "${calendar_source}"

status=0

if [[ "${task_ui}" == "github" || "${task_ui}" == "both" ]]; then
  echo "=== GitHub Projects (fields + views) ==="
  if "${SCRIPT_DIR}/gtd-setup-github.sh"; then
    echo "=== GitHub: ok ==="
  else
    echo "=== GitHub: failed ===" >&2
    status=1
  fi
else
  echo "=== GitHub: skipped ==="
fi

if [[ "${task_ui}" == "reminders" || "${task_ui}" == "both" ]]; then
  echo "=== Apple Reminders (GTD lists) ==="
  if "${SCRIPT_DIR}/gtd-setup-reminders.sh"; then
    echo "=== Reminders: ok ==="
  else
    echo "=== Reminders: failed ===" >&2
    status=1
  fi
else
  echo "=== Reminders: skipped ==="
fi

# Re-apply choices after B scripts so adapter flags stay consistent
python3 "${SCRIPT_DIR}/gtd_prefs.py" "${CONFIG}" set "${task_ui}" "${calendar_source}" >/dev/null

echo ""
echo "Calendar pulls (.gtd-pull / hourly cron) will use: ${calendar_source}"
python3 "${SCRIPT_DIR}/gtd_prefs.py" "${CONFIG}" show
echo "Done. Re-run with --reask to change choices."
exit "${status}"
