#!/usr/bin/env bash
# Markdown → HTML, then Pagefind index.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="${WIKI_SITE_DIR:-site}"

if [[ ! -d "$ROOT" ]]; then
  echo "Wiki root missing: $ROOT — run wiki-init.sh first." >&2
  exit 1
fi

python3 "$SCRIPT_DIR/wiki-build.py" --root "$ROOT"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx not found; HTML built but Pagefind skipped. Install Node.js to enable search." >&2
  exit 0
fi

# Ensure pagefind binary available via npx
if ! npx --yes pagefind --version >/dev/null 2>&1; then
  echo "Pagefind could not run via npx. HTML is ready at $ROOT/$SITE_DIR" >&2
  exit 1
fi

npx --yes pagefind --site "$ROOT/$SITE_DIR"
echo "Pagefind index → $ROOT/$SITE_DIR/pagefind/"
echo "Preview: wiki-serve.sh"
