#!/usr/bin/env bash
# Create/reuse GitHub Project "GTD" with required fields + views; patch config.
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${GTD_HOME}/config.yaml"
export GTD_GITHUB_OWNER="${GTD_GITHUB_OWNER:-@me}"
export GTD_PROJECT_TITLE="${GTD_PROJECT_TITLE:-GTD}"

if [[ ! -f "${CONFIG}" ]]; then
  "${SCRIPT_DIR}/gtd-init.sh"
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "error: gh CLI not found. Install: https://cli.github.com/" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "error: not logged in. Run: gh auth login" >&2
  exit 1
fi

if ! gh auth status 2>&1 | grep -qiE 'project'; then
  echo "Refreshing token with project scope…"
  gh auth refresh -s project,read:project || true
fi

summary="$(python3 "${SCRIPT_DIR}/gtd_setup_github.py")"

eval "$(printf '%s' "${summary}" | python3 -c '
import json, sys, shlex
d = json.load(sys.stdin)
print("login=" + shlex.quote(str(d["owner"])))
print("proj_number=" + shlex.quote(str(d["project_number"])))
print("proj_url=" + shlex.quote(str(d.get("url") or "NONE")))
')"

python3 "${SCRIPT_DIR}/gtd_config_patch.py" "${CONFIG}" \
  adapters.github.enabled true \
  adapters.github.owner "${login}" \
  adapters.github.project_number "${proj_number}" \
  adapters.github.status_field Status \
  adapters.github.inbox_status Inbox

echo "GitHub GTD project ready: #${proj_number}"
[[ "${proj_url}" != "NONE" && -n "${proj_url}" ]] && echo "  URL: ${proj_url}"
echo "  Fields: Status (Inbox/Today/Next/Waiting/Someday/Done), Duration, Context, Chunk, Due"
echo "  Views: Board, Inbox, Today, Next, Waiting, Someday"
echo "  Config: ${CONFIG}"
echo "  Tip: gh project view ${proj_number} --owner ${GTD_GITHUB_OWNER} --web"
