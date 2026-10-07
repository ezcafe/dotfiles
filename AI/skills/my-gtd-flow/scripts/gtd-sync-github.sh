#!/usr/bin/env bash
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
CONFIG="${GTD_HOME}/config.yaml"
TASKS="${GTD_HOME}/tasks.json"
TODAY="${GTD_HOME}/today.json"

if [[ ! -f "${CONFIG}" ]]; then
  echo "Missing config. Run gtd-init.sh." >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI not installed — skip GitHub sync." >&2
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
read -r owner proj enabled < <(
  python3 "${SCRIPT_DIR}/gtd_read_adapter.py" "${CONFIG}" github owner project_number enabled
)

if [[ "${enabled}" != "true" || "${owner}" == "NONE" ]]; then
  echo "GitHub adapter disabled."
  exit 0
fi

[[ -f "${TASKS}" ]] || { echo "No tasks.json"; exit 0; }

# Export active tasks without github_issue as draft issues (lazy v1)
python3 - "${TASKS}" "${owner}" <<'PY'
import json, subprocess, sys
path, owner = sys.argv[1], sys.argv[2]
tasks = json.load(open(path))
changed = False
for t in tasks.get("tasks", []):
    if t.get("status") != "active" or t.get("github_issue"):
        continue
    title = t["title"]
    mins = t.get("duration_minutes", 30)
    body = f"Duration: {mins}m\n\nManaged by my-gtd-flow."
    try:
        cmd = ["gh", "issue", "create", "--title", title, "--body", body]
        # Prefer label when it exists; do not fail sync if missing.
        labels = subprocess.run(
            ["gh", "label", "list", "--json", "name", "-q", ".[].name"],
            capture_output=True,
            text=True,
        )
        if labels.returncode == 0 and "gtd" in labels.stdout.splitlines():
            cmd.extend(["--label", "gtd"])
        out = subprocess.check_output(cmd, text=True).strip()
        # output is URL; extract number
        num = out.rstrip("/").split("/")[-1]
        t["github_issue"] = int(num)
        changed = True
        print(f"Created issue #{num}: {title}")
    except subprocess.CalledProcessError as e:
        print(f"Skip {title}: gh failed", e, file=sys.stderr)
if changed:
    json.dump(tasks, open(path, "w"), indent=2)
    open(path, "a").write("\n")
PY

# Add today plan as issue comment on first gtd issue (optional visibility)
if [[ -f "${TODAY}" ]]; then
  echo "Today plan written to ${TODAY}; pin in Project manually or extend script."
fi

echo "GitHub sync pass complete."
