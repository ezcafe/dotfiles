#!/usr/bin/env bash
# Morning orchestrator: clarify → plan → sprint blocks → ask sync.
# Calendar/Outlook pulls are hourly (see automation/cron.example); use gtd-pull.sh if needed.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
mkdir -p "${GTD_HOME}/logs"

echo "=== GTD morning ==="
echo "1/3 Clarify…"
"${SCRIPT_DIR}/gtd-clarify.sh"

echo "2/3 Plan day…"
"${SCRIPT_DIR}/gtd-plan-day.sh"

echo "3/3 Sprint blocks…"
"${SCRIPT_DIR}/gtd-sprint.sh"

"${SCRIPT_DIR}/gtd-ask-sync.sh"

echo "=== Morning done ==="
