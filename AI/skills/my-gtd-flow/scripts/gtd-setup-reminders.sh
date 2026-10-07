#!/usr/bin/env bash
# Create Apple Reminders GTD lists (Inbox/Today/Next/Waiting/Someday) + enable adapter.
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${GTD_HOME}/config.yaml"
PREFIX="${GTD_REMINDERS_PREFIX:-GTD}"

# Required GTD lists → display names
LIST_INBOX="${PREFIX} Inbox"
LIST_TODAY="${PREFIX} Today"
LIST_NEXT="${PREFIX} Next"
LIST_WAITING="${PREFIX} Waiting"
LIST_SOMEDAY="${PREFIX} Someday"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "error: Apple Reminders setup requires macOS." >&2
  exit 1
fi

if [[ ! -f "${CONFIG}" ]]; then
  "${SCRIPT_DIR}/gtd-init.sh"
fi

ensure_list() {
  local name="$1"
  local escaped="${name//\\/\\\\}"
  escaped="${escaped//\"/\\\"}"
  local script
  script="$(mktemp)"
  cat >"${script}" <<OSA
tell application "Reminders"
  if not (exists list "${escaped}") then
    make new list with properties {name:"${escaped}"}
  end if
  return name of list "${escaped}"
end tell
OSA
  # Timeout: Reminders may block on Privacy prompt
  if ! perl -e 'alarm shift; exec @ARGV' 20 osascript "${script}"; then
    rm -f "${script}"
    echo "error: Reminders timed out or failed for list '${name}'." >&2
    echo "  Grant access: System Settings → Privacy & Security → Reminders." >&2
    return 1
  fi
  rm -f "${script}"
}

echo "Ensuring Reminders GTD lists (prefix '${PREFIX}')…"
for name in "${LIST_INBOX}" "${LIST_TODAY}" "${LIST_NEXT}" "${LIST_WAITING}" "${LIST_SOMEDAY}"; do
  echo "  → ${name}"
  ensure_list "${name}" >/dev/null
done

# Patch scalar keys; write lists map with Python (PyYAML or embedded block)
python3 "${SCRIPT_DIR}/gtd_config_patch.py" "${CONFIG}" \
  adapters.reminders.enabled true \
  adapters.reminders.list_name "${LIST_TODAY}"

python3 - "${CONFIG}" "${LIST_INBOX}" "${LIST_TODAY}" "${LIST_NEXT}" "${LIST_WAITING}" "${LIST_SOMEDAY}" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
inbox, today, nxt, waiting, someday = sys.argv[2:7]
lists = {
    "inbox": inbox,
    "today": today,
    "next": nxt,
    "waiting": waiting,
    "someday": someday,
}
try:
    import yaml  # type: ignore

    data = yaml.safe_load(path.read_text()) or {}
    rem = data.setdefault("adapters", {}).setdefault("reminders", {})
    rem["enabled"] = True
    rem["list_name"] = today
    rem["lists"] = lists
    path.write_text(yaml.safe_dump(data, default_flow_style=False, sort_keys=False))
except ImportError:
    # Append / replace a markers block at end of file
    text = path.read_text()
    marker_start = "# BEGIN gtd-reminders-lists"
    marker_end = "# END gtd-reminders-lists"
    block = (
        f"{marker_start}\n"
        f"# lists (install PyYAML for structured config):\n"
        f"#   inbox: {inbox}\n"
        f"#   today: {today}\n"
        f"#   next: {nxt}\n"
        f"#   waiting: {waiting}\n"
        f"#   someday: {someday}\n"
        f"{marker_end}\n"
    )
    if marker_start in text:
        pre, rest = text.split(marker_start, 1)
        _, post = rest.split(marker_end, 1)
        text = pre + block + post.lstrip("\n")
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text)
print(f"Updated reminders lists in {path}")
PY

echo "Reminders GTD lists ready:"
echo "  ${LIST_INBOX}, ${LIST_TODAY}, ${LIST_NEXT}, ${LIST_WAITING}, ${LIST_SOMEDAY}"
echo "  Default sync list (list_name): ${LIST_TODAY}"
echo "  Config: ${CONFIG}"
echo "  If osascript failed: System Settings → Privacy & Security → Reminders → allow Terminal/Cursor."
