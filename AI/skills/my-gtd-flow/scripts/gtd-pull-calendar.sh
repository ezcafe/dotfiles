#!/usr/bin/env bash
# Read-only: pull Apple Calendar events into meetings.json. Never create/edit Calendar events.
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
CONFIG="${GTD_HOME}/config.yaml"
MEETINGS="${GTD_HOME}/meetings.json"

if [[ ! -f "${CONFIG}" ]]; then
  echo "Missing ${CONFIG}. Run gtd-init.sh first." >&2
  exit 1
fi

enabled="$(python3 - <<PY
import sys
try:
    import yaml
except ImportError:
    print("false")
    sys.exit(0)
cfg = yaml.safe_load(open("${CONFIG}"))
print(str((cfg.get("adapters") or {}).get("calendar", {}).get("enabled", False)).lower())
PY
)"

if [[ "${enabled}" != "true" ]]; then
  echo "Calendar adapter disabled in config."
  exit 0
fi

mkdir -p "${GTD_HOME}"
[[ -f "${MEETINGS}" ]] || echo '{"version":1,"meetings":[]}' > "${MEETINGS}"

python3 - "${GTD_HOME}" <<'PY'
import json
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

home = Path(__import__("sys").argv[1])
meetings_path = home / "meetings.json"
data = json.loads(meetings_path.read_text())

script = '''
tell application "Calendar"
    set out to ""
    set todayStart to current date
    set hours of todayStart to 0
    set minutes of todayStart to 0
    set seconds of todayStart to 0
    set todayEnd to todayStart + (1 * days)
    repeat with cal in calendars
        repeat with ev in (every event of cal whose start date ≥ todayStart and start date < todayEnd)
            set out to out & (summary of ev) & "|" & (start date of ev as string) & "|" & (end date of ev as string) & linefeed
        end repeat
    end repeat
    return out
end tell
'''
try:
    raw = subprocess.check_output(["osascript", "-e", script], text=True)
except subprocess.CalledProcessError as e:
    print("Calendar osascript failed:", e, sep="\n")
    raise SystemExit(1)

existing = {(m.get("title"), m.get("start")) for m in data.get("meetings", [])}
added = 0
for line in raw.strip().splitlines():
    if not line.strip():
        continue
    parts = line.split("|")
    if len(parts) < 3:
        continue
    title, start_s, end_s = parts[0], parts[1], parts[2]
    # AppleScript date strings vary; store raw-ish ISO best-effort
    key = (title, start_s)
    if key in existing:
        continue
    data.setdefault("meetings", []).append({
        "id": str(uuid.uuid4()),
        "title": title,
        "start": start_s,
        "end": end_s,
        "type": "optional",
        "source": "apple",
        "location": None,
        "skipped": False,
    })
    added += 1

meetings_path.write_text(json.dumps(data, indent=2) + "\n")
print(f"Calendar: added {added} meeting(s).")
PY
