#!/usr/bin/env bash
# Print today's sprint blocks from today.json (after plan-day).
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
TODAY="${GTD_HOME}/today.json"

if [[ ! -f "${TODAY}" ]]; then
  echo "No today.json — run gtd-plan-day.sh or gtd-morning.sh first." >&2
  exit 1
fi

python3 - "${TODAY}" <<'PY'
import json, sys
from datetime import datetime

path = sys.argv[1]
data = json.load(open(path))
date = data.get("date", "?")
blocks = data.get("blocks") or []
unsched = data.get("unscheduled") or []

print(f"=== Sprint {date} ===")
if not blocks:
    print("(no blocks)")
else:
    for b in blocks:
        try:
            s = datetime.fromisoformat(b["start"]).strftime("%H:%M")
            e = datetime.fromisoformat(b["end"]).strftime("%H:%M")
        except Exception:
            s, e = "?", "?"
        kind = b.get("kind", "?")
        title = b.get("title") or ""
        note = b.get("note") or ""
        extra = f" · {note}" if note else ""
        print(f"  {s}–{e}  [{kind}]  {title}{extra}")

if unsched:
    print("Unscheduled:")
    for u in unsched:
        print(f"  - {u.get('title')} ({u.get('reason', '')})")
print("=== End sprint ===")
PY
