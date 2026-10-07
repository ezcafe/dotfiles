#!/usr/bin/env python3
"""Promote inbox lines to tasks.json using lazy defaults."""
from __future__ import annotations

import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

DURATIONS = {
    "5m": 5,
    "30m": 30,
    "1h": 60,
    "2h": 120,
    "4h": 240,
}


def load_json(path: Path, default: dict) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    path.write_text(json.dumps(default, indent=2) + "\n")
    return default


def parse_line(raw: str, default_min: int, default_chunk: int) -> dict:
    title = raw.strip()
    tags = re.findall(r"#(\w+)", title)
    title = re.sub(r"#\w+", "", title).strip()
    ctx = None
    m = re.search(r"@(\w+)", title)
    if m:
        ctx = m.group(1)
        title = re.sub(r"@\w+", "", title).strip()

    meeting_type = "optional"
    if re.search(r"\b(req|required)\b", raw, re.I):
        meeting_type = "required"
    elif re.search(r"\b(info|info only)\b", raw, re.I):
        meeting_type = "info_only"
    elif re.search(r"\b(opt|optional)\b", raw, re.I):
        meeting_type = "optional"

    multiday = bool(re.search(r"\bmultiday\b", raw, re.I))
    chunk = default_chunk
    cm = re.search(r"chunk\s+(1h|2h|4h)", raw, re.I)
    if cm:
        chunk = {"1h": 60, "2h": 120, "4h": 240}[cm.group(1).lower()]

    duration = default_min
    for token, mins in DURATIONS.items():
        if re.search(rf"\b{re.escape(token)}\b", raw, re.I):
            duration = mins
            break

    status = "someday" if "someday" in tags else "active"
    if "waiting" in tags:
        status = "waiting"

    task = {
        "id": str(uuid.uuid4()),
        "title": title or raw.strip(),
        "status": status,
        "duration_minutes": duration,
        "multiday": multiday,
        "remaining_minutes": (duration * 8 if multiday else None),
        "chunk_minutes": chunk if multiday else None,
        "due_date": None,
        "tags": tags,
        "context": ctx or "computer",
        "priority": 1 if "urgent" in tags else 0,
        "github_issue": None,
        "reminder_id": None,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "_meeting_type_hint": meeting_type,
    }
    return task


def main() -> None:
    home = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / ".my-gtd")
    config_path = home / "config.yaml"
    default_min, default_chunk = 30, 120
    if config_path.exists():
        try:
            import yaml  # type: ignore

            cfg = yaml.safe_load(config_path.read_text()) or {}
            planning = cfg.get("planning") or {}
            default_min = int(planning.get("default_duration_minutes", 30))
            default_chunk = int(planning.get("multiday_default_chunk_minutes", 120))
        except ImportError:
            pass

    inbox_path = home / "inbox.json"
    tasks_path = home / "tasks.json"
    inbox = load_json(inbox_path, {"version": 1, "items": []})
    tasks = load_json(tasks_path, {"version": 1, "tasks": []})

    promoted = []
    remaining = []
    for item in inbox.get("items", []):
        raw = item.get("raw", "")
        if not raw.strip():
            continue
        task = parse_line(raw, default_min, default_chunk)
        tasks.setdefault("tasks", []).append({k: v for k, v in task.items() if not k.startswith("_")})
        promoted.append(task["title"])
        remaining.append(item)

    inbox["items"] = [] if promoted else inbox.get("items", [])
    tasks_path.write_text(json.dumps(tasks, indent=2) + "\n")
    inbox_path.write_text(json.dumps(inbox, indent=2) + "\n")

    if promoted:
        print("Clarified → tasks:", ", ".join(promoted))
    else:
        print("Inbox empty — nothing to clarify.")


if __name__ == "__main__":
    main()
