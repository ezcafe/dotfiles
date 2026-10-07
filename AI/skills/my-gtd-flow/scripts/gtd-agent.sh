#!/usr/bin/env bash
# Run Cursor agent with inherit model when possible, else a fast model.
# Usage: gtd-agent.sh [-p] [--force] [--approve-mcps] [--] "prompt..."
set -euo pipefail

# inherit = omit --model (use session/parent default). Override: GTD_AGENT_MODEL=composer-2.5-fast
MODEL="${GTD_AGENT_MODEL:-inherit}"
FAST_FALLBACK="${GTD_AGENT_FAST:-composer-2.5-fast}"

if ! command -v agent >/dev/null 2>&1; then
  echo "error: agent CLI not found" >&2
  exit 1
fi

args=()
print=false
force=false
approve_mcps=false
prompt=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -p|--print) print=true; shift ;;
    --force) force=true; shift ;;
    --approve-mcps) approve_mcps=true; shift ;;
    --) shift; prompt+=("$@"); break ;;
    *) prompt+=("$1"); shift ;;
  esac
done

[[ ${#prompt[@]} -gt 0 ]] || { echo "Usage: gtd-agent.sh [-p] [--force] [--approve-mcps] \"prompt\"" >&2; exit 2; }

[[ "${print}" == true ]] && args+=(-p)
[[ "${force}" == true ]] && args+=(--force)
[[ "${approve_mcps}" == true ]] && args+=(--approve-mcps)

if [[ "${MODEL}" == "inherit" || -z "${MODEL}" ]]; then
  # Prefer inherit (no --model). If agent rejects, caller may set GTD_AGENT_MODEL to a fast slug.
  :
else
  args+=(--model "${MODEL}")
fi

# If inherit fails on some installs, retry once with fast model when GTD_AGENT_INHERIT_FALLBACK=1 (default)
run_agent() {
  agent "${args[@]}" "${prompt[*]}"
}

if ! run_agent; then
  if [[ "${MODEL}" == "inherit" || -z "${MODEL}" ]] && [[ "${GTD_AGENT_INHERIT_FALLBACK:-1}" == "1" ]]; then
    echo "warn: inherit run failed — retrying with fast model ${FAST_FALLBACK}" >&2
    agent "${args[@]}" --model "${FAST_FALLBACK}" "${prompt[*]}"
  else
    exit 1
  fi
fi
