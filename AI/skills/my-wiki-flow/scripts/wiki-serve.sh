#!/usr/bin/env bash
# Serve generated site/ for local preview.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SITE="${ROOT}/${WIKI_SITE_DIR:-site}"
PORT="${WIKI_PORT:-8765}"

if [[ ! -d "$SITE" ]]; then
  echo "Site not found: $SITE — run wiki-build.sh first." >&2
  exit 1
fi

URL="http://127.0.0.1:${PORT}/"

port_in_use() {
  if command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1
    return
  fi
  (echo >/dev/tcp/127.0.0.1/"${PORT}") >/dev/null 2>&1
}

open_url() {
  if command -v open >/dev/null 2>&1; then
    open "$URL"
  fi
}

if port_in_use; then
  echo "Already serving at ${URL} (port ${PORT} in use)."
  open_url
  exit 0
fi

echo "Serving $SITE at $URL"
if command -v open >/dev/null 2>&1; then
  (sleep 0.4 && open_url) &
fi
exec python3 -m http.server "$PORT" --directory "$SITE"
