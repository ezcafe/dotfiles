#!/usr/bin/env bash
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
INBOX="${GTD_HOME}/inbox.json"

if [[ $# -lt 1 ]]; then
  echo "Usage: gtd-capture.sh \"one line task or note\"" >&2
  exit 1
fi

raw="$*"
id="$(uuidgen | tr '[:upper:]' '[:lower:]')"
ts="$(date -Iseconds)"

mkdir -p "${GTD_HOME}"
[[ -f "${INBOX}" ]] || echo '{"version":1,"items":[]}' > "${INBOX}"

python3 - "${INBOX}" "${id}" "${ts}" "${raw}" <<'PY'
import json, sys
path, uid, ts, raw = sys.argv[1:5]
with open(path) as f:
    data = json.load(f)
data.setdefault("items", []).append({
    "id": uid,
    "raw": raw,
    "captured_at": ts,
    "source": "cli",
})
with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"Captured: {raw}")
PY
