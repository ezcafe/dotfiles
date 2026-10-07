#!/usr/bin/env python3
"""Print adapter key values without requiring PyYAML.

Usage: gtd_read_adapter.py <config.yaml> <adapter> <key> [<key>...]
Prints space-separated values (missing → empty / false / NONE by key heuristics).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def load_adapter_block(text: str, adapter: str) -> dict[str, str]:
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
        block = (data.get("adapters") or {}).get(adapter) or {}
        return {str(k): str(v).lower() if isinstance(v, bool) else str(v) for k, v in block.items()}
    except ImportError:
        pass

    lines = text.splitlines()
    in_adapters = False
    in_block = False
    out: dict[str, str] = {}
    for line in lines:
        if re.match(r"^adapters:\s*$", line):
            in_adapters = True
            in_block = False
            continue
        if in_adapters and re.match(r"^[^\s#]", line):
            break
        if in_adapters and re.match(rf"^  {re.escape(adapter)}:\s*$", line):
            in_block = True
            continue
        if in_block and re.match(r"^  \w", line) and not line.startswith("    "):
            break
        if in_block:
            m = re.match(r"^    (\w+):\s*(.+?)\s*$", line)
            if m:
                out[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return out


def main() -> None:
    if len(sys.argv) < 4:
        print(
            "Usage: gtd_read_adapter.py <config.yaml> <adapter> <key> [<key>...]",
            file=sys.stderr,
        )
        raise SystemExit(2)
    path = Path(sys.argv[1])
    adapter = sys.argv[2]
    keys = sys.argv[3:]
    text = path.read_text() if path.exists() else ""
    block = load_adapter_block(text, adapter)
    vals = []
    for k in keys:
        v = block.get(k, "")
        if k == "enabled" and not v:
            v = "false"
        if k in ("owner",) and not v:
            v = "NONE"
        if k in ("project_number",) and not v:
            v = "0"
        vals.append(v)
    print(" ".join(vals))


if __name__ == "__main__":
    main()
