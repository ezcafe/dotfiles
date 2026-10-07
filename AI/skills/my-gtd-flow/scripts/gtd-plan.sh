#!/usr/bin/env bash
# Clarify + plan + sprint + ask sync (daytime replan without full morning banner).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${SCRIPT_DIR}/gtd-clarify.sh"
"${SCRIPT_DIR}/gtd-plan-day.sh"
"${SCRIPT_DIR}/gtd-sprint.sh"
"${SCRIPT_DIR}/gtd-ask-sync.sh"
