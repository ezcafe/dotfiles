#!/usr/bin/env bash
# Export projects/**/*.md to a GitHub wiki clone (flat names). Never force-push.
# Default is dry-run. Pass --push after explicit user approval.
set -euo pipefail

ROOT="${WIKI_ROOT:-$HOME/Documents/my-wiki}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DO_PUSH=0
CLONE_DIR=""

usage() {
  echo "Usage: wiki-sync-github.sh [--push] [--clone-dir DIR]"
  echo "  Reads github_wiki.repo / github_wiki.remote from config.yaml"
  echo "  Default: dry-run. --push clones/updates and commits (no force)."
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --push) DO_PUSH=1; shift ;;
    --clone-dir) CLONE_DIR="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1" >&2; usage ;;
  esac
done

if [[ ! -f "$ROOT/config.yaml" ]]; then
  echo "Missing config.yaml at $ROOT" >&2
  exit 1
fi

IFS=$'\t' read -r REPO REMOTE < <(python3 "$SCRIPT_DIR/_wiki_config.py" github-wiki "$ROOT/config.yaml")

if [[ -z "$REMOTE" ]]; then
  if [[ -z "$REPO" ]]; then
    echo "github_wiki.repo / remote unset — ask the user for owner/repo." >&2
    exit 1
  fi
  REMOTE="https://github.com/${REPO}.wiki.git"
fi

CLONE_DIR="${CLONE_DIR:-$ROOT/.build/github-wiki}"
MAP_FILE="$ROOT/ai/github-wiki-map.md"

echo "GitHub wiki remote: $REMOTE"
echo "Clone dir: $CLONE_DIR"
echo "Mode: $([[ $DO_PUSH -eq 1 ]] && echo PUSH || echo DRY-RUN)"

python3 - "$ROOT" "$MAP_FILE" "$CLONE_DIR" "$DO_PUSH" "$REMOTE" <<'PY'
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

root = Path(sys.argv[1])
map_file = Path(sys.argv[2])
clone_dir = Path(sys.argv[3])
do_push = sys.argv[4] == "1"
remote = sys.argv[5]
projects = root / "projects"

def wiki_name(rel: Path) -> str:
    parts = rel.parts  # projects, slug, ...
    slug = parts[1]
    stem = rel.stem
    def cap(s: str) -> str:
        return "".join(p.capitalize() for p in s.replace("_", "-").split("-") if p)
    project = cap(slug)
    if stem == "index":
        return project
    if "solution-design" in parts and stem != "solution-design":
        return f"{project}-SolutionDesign-{cap(stem)}"
    return f"{project}-{cap(stem)}"

rows = []
if projects.is_dir():
    for md in sorted(projects.rglob("*.md")):
        if md.name == "README.md":
            continue
        rel = md.relative_to(root)
        rows.append((rel.as_posix(), wiki_name(rel), md))

map_file.parent.mkdir(parents=True, exist_ok=True)
lines = [
    "# GitHub wiki export map",
    "",
    f"Generated {date.today().isoformat()}. Local vault remains source of truth.",
    "",
    "| Local path | Wiki page |",
    "|------------|-----------|",
]
for local, wiki, _ in rows:
    lines.append(f"| `{local}` | {wiki} |")
    print(f"  {local}  →  {wiki}.md")
map_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

if not do_push:
    print(f"\nDry-run complete. Map → {map_file}")
    print("Re-run with --push after explicit user approval.")
    raise SystemExit(0)

clone_dir.parent.mkdir(parents=True, exist_ok=True)
if not (clone_dir / ".git").is_dir():
    subprocess.check_call(["git", "clone", remote, str(clone_dir)])
else:
    try:
        subprocess.check_call(["git", "-C", str(clone_dir), "pull", "--ff-only"])
    except subprocess.CalledProcessError:
        print("Pull failed — resolve manually. Never force-push.", file=sys.stderr)
        raise SystemExit(1)

for local, wiki, src in rows:
    shutil.copy2(src, clone_dir / f"{wiki}.md")

if not (clone_dir / "Home.md").is_file() and rows:
    shutil.copy2(rows[0][2], clone_dir / "Home.md")

subprocess.check_call(["git", "-C", str(clone_dir), "add", "-A"])
st = subprocess.call(["git", "-C", str(clone_dir), "diff", "--cached", "--quiet"])
if st == 0:
    print("No changes to push.")
    raise SystemExit(0)

msg = f"Sync from my-wiki vault {date.today().isoformat()}"
subprocess.check_call(["git", "-C", str(clone_dir), "commit", "-m", msg])
subprocess.check_call(["git", "-C", str(clone_dir), "push"])
print(f"Pushed to {remote}")
print(f"Map → {map_file}")

log = root / "log.md"
if log.is_file():
    with log.open("a", encoding="utf-8") as f:
        f.write(f"\n## [{date.today().isoformat()}] sync-github | pushed to {remote}\n")
PY
