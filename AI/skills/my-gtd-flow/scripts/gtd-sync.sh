#!/usr/bin/env bash
# Manual sync entrypoint — always goes through approval prompt (gtd-ask-sync.sh).
# Low-level scripts gtd-sync-github.sh / gtd-sync-reminders.sh remain for debugging only.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/gtd-ask-sync.sh"
