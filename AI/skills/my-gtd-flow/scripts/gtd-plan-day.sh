#!/usr/bin/env bash
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "${SCRIPT_DIR}/gtd_plan_day.py" "${GTD_HOME}"
