#!/usr/bin/env python3
"""Patch nested keys in ~/.my-gtd/config.yaml (PyYAML preferred; line editor fallback)."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def coerce(value: str):
    if value in ("true", "True"):
        return True
    if value in ("false", "False"):
        return False
    if value.isdigit():
        return int(value)
    return value


def yaml_quote(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    s = str(value)
    if any(c in s for c in ":#{}[]&*!|>%@`'\""):
        return json.dumps(s)
    return s


def patch_with_yaml(path: Path, pairs: list[tuple[str, str]]) -> None:
    import yaml  # type: ignore

    data = yaml.safe_load(path.read_text()) if path.exists() else {}
    data = data or {}
    if not isinstance(data, dict):
        data = {}

    for dotted, raw in pairs:
        keys = dotted.split(".")
        cur = data
        for k in keys[:-1]:
            nxt = cur.get(k)
            if not isinstance(nxt, dict):
                nxt = {}
                cur[k] = nxt
            cur = nxt
        cur[keys[-1]] = coerce(raw)

    path.write_text(yaml.safe_dump(data, default_flow_style=False, sort_keys=False))


def patch_line_editor(path: Path, pairs: list[tuple[str, str]]) -> None:
    """Replace or insert adapters.<name>.<key> lines (2-space YAML indent)."""
    if not path.exists():
        example = Path(__file__).with_name("config.example.yaml")
        path.write_text(example.read_text())

    updates: dict[tuple[str, str], object] = {}
    for dotted, raw in pairs:
        parts = dotted.split(".")
        if len(parts) != 3 or parts[0] != "adapters":
            raise SystemExit(
                f"Without PyYAML only adapters.<name>.<key> is supported (got {dotted}). "
                "Install: python3 -m pip install --user pyyaml"
            )
        updates[(parts[1], parts[2])] = coerce(raw)

    lines = path.read_text().splitlines(keepends=True)
    out: list[str] = []
    current: str | None = None
    seen_keys: set[tuple[str, str]] = set()

    for line in lines:
        stripped = line.lstrip("\n\r")
        # normalize: compute indent from spaces only
        body = line.rstrip("\n\r")
        indent = len(body) - len(body.lstrip(" "))
        content = body.lstrip(" ")
        nl = "\n" if line.endswith("\n") else ""

        if indent == 2 and content.endswith(":") and not content.startswith("#"):
            # Flush? no — entering new adapter
            current = content[:-1].strip()
            out.append(line if line.endswith("\n") else line + "\n")
            continue

        if indent == 0 and content and not content.startswith("#"):
            current = None

        if current and indent == 4 and ":" in content and not content.startswith("#"):
            key = content.split(":", 1)[0].strip()
            pair = (current, key)
            if pair in updates:
                out.append(f"    {key}: {yaml_quote(updates[pair])}{nl or chr(10)}")
                seen_keys.add(pair)
                continue

        out.append(line if line.endswith("\n") else line + "\n")

    # Insert keys that were not present
    missing = {k: v for k, v in updates.items() if k not in seen_keys}
    if missing:
        text = "".join(out)
        for (adapter, key), val in missing.items():
            needle = f"  {adapter}:\n"
            if needle not in text:
                raise SystemExit(f"adapter block '{adapter}' missing in {path}")
            insert_at = text.index(needle) + len(needle)
            text = text[:insert_at] + f"    {key}: {yaml_quote(val)}\n" + text[insert_at:]
        path.write_text(text)
    else:
        path.write_text("".join(out))


def main() -> None:
    if len(sys.argv) < 3 or (len(sys.argv) - 2) % 2 != 0:
        print(
            "Usage: gtd_config_patch.py <config.yaml> <key.path> <value> [...]",
            file=sys.stderr,
        )
        raise SystemExit(2)

    path = Path(sys.argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    args = sys.argv[2:]
    pairs = [(args[i], args[i + 1]) for i in range(0, len(args), 2)]

    if not path.exists():
        example = Path(__file__).with_name("config.example.yaml")
        path.write_text(example.read_text())

    try:
        import yaml  # noqa: F401

        patch_with_yaml(path, pairs)
    except ImportError:
        patch_line_editor(path, pairs)

    print(f"Updated {path}")


if __name__ == "__main__":
    main()
