#!/usr/bin/env bash
set -euo pipefail

GTD_HOME="${GTD_HOME:-$HOME/.my-gtd}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="${SCRIPT_DIR}/config.example.yaml"

mkdir -p "${GTD_HOME}/logs" "${GTD_HOME}/bin"

if [[ ! -f "${GTD_HOME}/config.yaml" ]]; then
  cp "${TEMPLATE}" "${GTD_HOME}/config.yaml"
  echo "Created ${GTD_HOME}/config.yaml — edit adapters."
else
  echo "Config exists: ${GTD_HOME}/config.yaml"
fi

for f in inbox tasks meetings; do
  path="${GTD_HOME}/${f}.json"
  if [[ ! -f "${path}" ]]; then
    echo "{\"version\":1,\"$( [[ "$f" == "inbox" ]] && echo items || echo "$f" )\":[]}" > "${path}"
    echo "Created ${path}"
  fi
done

echo "GTD workspace ready at ${GTD_HOME}"
