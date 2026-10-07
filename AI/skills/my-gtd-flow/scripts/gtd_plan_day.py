#!/usr/bin/env python3
"""Build today.json from meetings + tasks (9–17, lunch 11:30–13:00)."""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import List, Tuple


def parse_hm(s: str) -> time:
    h, m = s.split(":")
    return time(int(h), int(m))


def load_yaml_config(home: Path) -> dict:
    path = home / "config.yaml"
    if not path.exists():
        return {
            "work": {
                "start": "09:00",
                "end": "17:00",
                "break_start": "11:30",
                "break_end": "13:00",
            },
            "planning": {"end_of_day_buffer_minutes": 15},
        }
    try:
        import yaml  # type: ignore

        return yaml.safe_load(path.read_text()) or {}
    except ImportError:
        return {
            "work": {
                "start": "09:00",
                "end": "17:00",
                "break_start": "11:30",
                "break_end": "13:00",
            },
            "planning": {"end_of_day_buffer_minutes": 15},
        }


def iso_local(d: date, t: time) -> str:
    return datetime.combine(d, t).isoformat()


def subtract_interval(
    free: List[Tuple[datetime, datetime]], start: datetime, end: datetime
) -> List[Tuple[datetime, datetime]]:
    out: List[Tuple[datetime, datetime]] = []
    for a, b in free:
        if end <= a or start >= b:
            out.append((a, b))
            continue
        if a < start:
            out.append((a, start))
        if end < b:
            out.append((end, b))
    return [(a, b) for a, b in out if b > a]


def merge(free: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]:
    if not free:
        return []
    free.sort()
    merged = [free[0]]
    for a, b in free[1:]:
        la, lb = merged[-1]
        if a <= lb:
            merged[-1] = (la, max(lb, b))
        else:
            merged.append((a, b))
    return merged


def main() -> None:
    home = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / ".my-gtd")
    today = date.today()
    cfg = load_yaml_config(home)
    work = cfg.get("work") or {}
    planning = cfg.get("planning") or {}
    buffer_min = int(planning.get("end_of_day_buffer_minutes", 15))

    w_start = parse_hm(work.get("start", "09:00"))
    w_end = parse_hm(work.get("end", "17:00"))
    br_start = parse_hm(work.get("break_start", "11:30"))
    br_end = parse_hm(work.get("break_end", "13:00"))

    day_start = datetime.combine(today, w_start)
    day_end = datetime.combine(today, w_end)
    break_start = datetime.combine(today, br_start)
    break_end = datetime.combine(today, br_end)

    meetings_path = home / "meetings.json"
    tasks_path = home / "tasks.json"
    meetings = json.loads(meetings_path.read_text()) if meetings_path.exists() else {"meetings": []}
    tasks = json.loads(tasks_path.read_text()) if tasks_path.exists() else {"tasks": []}

    blocks = []
    free = [(day_start, day_end)]

    for m in meetings.get("meetings", []):
        if m.get("skipped"):
            continue
        start = datetime.fromisoformat(m["start"])
        end = datetime.fromisoformat(m["end"])
        if start.date() != today and end.date() != today:
            continue
        blocks.append(
            {
                "kind": "meeting",
                "ref_id": m.get("id"),
                "title": m.get("title", "Meeting"),
                "start": start.isoformat(),
                "end": end.isoformat(),
                "note": m.get("type"),
            }
        )
        free = subtract_interval(free, start, end)

    # Task placement: exclude break from free time
    free = subtract_interval(free, break_start, break_end)
    free = merge(free)

    # Reserve end-of-day buffer
    if buffer_min > 0:
        buf_start = day_end - timedelta(minutes=buffer_min)
        free = subtract_interval(free, buf_start, day_end)

    active_tasks = [
        t
        for t in tasks.get("tasks", [])
        if t.get("status") == "active" and "someday" not in (t.get("tags") or [])
    ]
    active_tasks.sort(
        key=lambda t: (
            0 if t.get("due_date") == today.isoformat() else 1,
            0 if "urgent" in (t.get("tags") or []) else 1,
            t.get("duration_minutes", 9999),
            -t.get("priority", 0),
        )
    )

    unscheduled = []
    for t in active_tasks:
        if t.get("multiday"):
            mins = min(
                t.get("chunk_minutes") or 120,
                t.get("remaining_minutes") or t.get("chunk_minutes") or 120,
            )
        else:
            mins = t.get("duration_minutes", 30)
        need = timedelta(minutes=mins)
        placed = False
        for i, (a, b) in enumerate(free):
            if b - a >= need:
                start = a
                end = a + need
                blocks.append(
                    {
                        "kind": "task",
                        "ref_id": t.get("id"),
                        "title": t.get("title"),
                        "start": start.isoformat(),
                        "end": end.isoformat(),
                        "note": f"{mins}m",
                    }
                )
                free[i] = (end, b)
                placed = True
                break
        if not placed:
            unscheduled.append(
                {
                    "ref_id": t.get("id"),
                    "title": t.get("title"),
                    "reason": "no_free_block",
                }
            )

    blocks.sort(key=lambda b: b["start"])
    out = {
        "version": 1,
        "date": today.isoformat(),
        "generated_at": datetime.now().isoformat(),
        "blocks": blocks,
        "unscheduled": unscheduled,
    }
    out_path = home / "today.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")

    print(f"Plan for {today.isoformat()} → {out_path}")
    for b in blocks:
        s = datetime.fromisoformat(b["start"]).strftime("%H:%M")
        e = datetime.fromisoformat(b["end"]).strftime("%H:%M")
        print(f"  {s}–{e}  {b['title']} ({b['kind']})")
    if unscheduled:
        print("Unscheduled:")
        for u in unscheduled:
            print(f"  - {u['title']}")


if __name__ == "__main__":
    main()
