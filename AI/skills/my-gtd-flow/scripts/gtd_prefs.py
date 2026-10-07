#!/usr/bin/env python3
"""Read/write remembered GTD setup choices in ~/.my-gtd/config.yaml."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VALID_TASK_UI = ("github", "reminders", "both", "none")
VALID_CALENDAR = ("apple", "outlook", "both", "none")


def load_data(path: Path) -> dict:
    if not path.exists():
        example = Path(__file__).with_name("config.example.yaml")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(example.read_text())
    text = path.read_text()
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
        return data if isinstance(data, dict) else {}
    except ImportError:
        return {"_raw": text}


def dump_data(path: Path, data: dict) -> None:
    if "_raw" in data:
        raise SystemExit("Cannot dump without PyYAML when config was loaded raw")
    try:
        import yaml  # type: ignore

        path.write_text(yaml.safe_dump(data, default_flow_style=False, sort_keys=False))
    except ImportError:
        raise SystemExit(
            "PyYAML required to save choices. Install: python3 -m pip install --user pyyaml"
        )


def apply_choices(data: dict, task_ui: str, calendar_source: str) -> dict:
    if task_ui not in VALID_TASK_UI:
        raise SystemExit(f"invalid task_ui: {task_ui}")
    if calendar_source not in VALID_CALENDAR:
        raise SystemExit(f"invalid calendar_source: {calendar_source}")

    data.setdefault("choices", {})
    data["choices"]["task_ui"] = task_ui
    data["choices"]["calendar_source"] = calendar_source

    adapters = data.setdefault("adapters", {})
    gh = adapters.setdefault("github", {})
    rem = adapters.setdefault("reminders", {})
    cal = adapters.setdefault("calendar", {})

    gh["enabled"] = task_ui in ("github", "both")
    rem["enabled"] = task_ui in ("reminders", "both")

    cal["enabled"] = calendar_source != "none"
    cal["apple"] = calendar_source in ("apple", "both")
    cal["outlook"] = calendar_source in ("outlook", "both")
    if calendar_source == "both":
        cal["source"] = "both"
    elif calendar_source == "outlook":
        cal["source"] = "outlook"
    elif calendar_source == "apple":
        cal["source"] = "apple"
    else:
        cal["source"] = "none"

    return data


def get_choices(path: Path) -> tuple[str, str]:
    data = load_data(path)
    if "_raw" in data:
        text = data["_raw"]
        task = "none"
        cal = "none"
        m = re.search(r"task_ui:\s*(\w+)", text)
        if m:
            task = m.group(1)
        m = re.search(r"calendar_source:\s*(\w+)", text)
        if m:
            cal = m.group(1)
        # fallback from adapters.enabled
        if task == "none":
            gh = bool(re.search(r"github:\n(?:.*\n)*?    enabled:\s*true", text))
            rem = bool(re.search(r"reminders:\n(?:.*\n)*?    enabled:\s*true", text))
            if gh and rem:
                task = "both"
            elif gh:
                task = "github"
            elif rem:
                task = "reminders"
        return task, cal

    choices = data.get("choices") or {}
    task = str(choices.get("task_ui") or "none")
    cal = str(choices.get("calendar_source") or "none")
    if task == "none" and not choices:
        gh = bool(((data.get("adapters") or {}).get("github") or {}).get("enabled"))
        rem = bool(((data.get("adapters") or {}).get("reminders") or {}).get("enabled"))
        if gh and rem:
            task = "both"
        elif gh:
            task = "github"
        elif rem:
            task = "reminders"
        cal_ad = (data.get("adapters") or {}).get("calendar") or {}
        if cal_ad.get("outlook") and cal_ad.get("apple"):
            cal = "both"
        elif cal_ad.get("outlook"):
            cal = "outlook"
        elif cal_ad.get("apple") or (
            cal_ad.get("enabled") and cal_ad.get("source") in (None, "apple")
        ):
            cal = "apple"
        elif cal_ad.get("enabled") and cal_ad.get("source") == "outlook":
            cal = "outlook"
    return task, cal


def cmd_get(path: Path) -> None:
    task, cal = get_choices(path)
    print(json.dumps({"task_ui": task, "calendar_source": cal}))


def cmd_set(path: Path, task_ui: str, calendar_source: str) -> None:
    data = load_data(path)
    if "_raw" in data:
        # bootstrap from example then apply
        example = Path(__file__).with_name("config.example.yaml")
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(example.read_text()) or {}
        except ImportError:
            raise SystemExit(
                "PyYAML required to save choices. Install: python3 -m pip install --user pyyaml"
            )
    apply_choices(data, task_ui, calendar_source)
    dump_data(path, data)
    print(f"Saved choices: task_ui={task_ui} calendar_source={calendar_source} → {path}")


def cmd_show(path: Path) -> None:
    task, cal = get_choices(path)
    print(f"task_ui={task}")
    print(f"calendar_source={cal}")


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Usage:\n"
            "  gtd_prefs.py <config.yaml> get\n"
            "  gtd_prefs.py <config.yaml> show\n"
            "  gtd_prefs.py <config.yaml> set <task_ui> <calendar_source>",
            file=sys.stderr,
        )
        raise SystemExit(2)
    path = Path(sys.argv[1])
    cmd = sys.argv[2]
    if cmd == "get":
        cmd_get(path)
    elif cmd == "show":
        cmd_show(path)
    elif cmd == "set":
        if len(sys.argv) != 5:
            raise SystemExit("set requires <task_ui> <calendar_source>")
        cmd_set(path, sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
