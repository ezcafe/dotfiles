#!/usr/bin/env bash
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
CONFIG="${GTD_HOME}/config.yaml"
TODAY="${GTD_HOME}/today.json"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
enabled="$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" reminders enabled)"
list_name="$(python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" reminders list_name)"
[[ -n "${list_name}" ]] || list_name="GTD Today"

if [[ "${enabled}" != "true" ]]; then
  echo "Reminders adapter disabled."
  exit 0
fi

if [[ ! -f "${TODAY}" ]]; then
  echo "Run gtd-plan-day.sh first." >&2
  exit 1
fi

python3 - "${TODAY}" "${list_name}" <<'PY'
import json, subprocess, sys
today_path, list_name = sys.argv[1], sys.argv[2]
plan = json.load(open(today_path))
for b in plan.get("blocks", []):
    if b.get("kind") != "task":
        continue
    title = b["title"]
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    script = f'''
    tell application "Reminders"
        tell list "{list_name}"
            make new reminder with properties {{name:"{safe_title}"}}
        end tell
    end tell
    '''
    try:
        subprocess.check_call(["osascript", "-e", script])
        print(f"Reminder: {title}")
    except subprocess.CalledProcessError:
        print(f"Failed reminder: {title}", file=sys.stderr)
PY

echo "Reminders sync pass complete."
