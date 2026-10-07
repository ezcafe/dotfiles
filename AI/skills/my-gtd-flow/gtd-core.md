# GTD core (lazy profile)

Based on [Getting Things Done](https://gettingthingsdone.com/) — trimmed for daily friction.

## Lists (where things live)

| List | Meaning | GitHub Status / view | Reminders list |
|------|---------|----------------------|----------------|
| **Inbox** | Unprocessed captures — do not trust for scheduling | Inbox | `GTD Inbox` |
| **Today** | Committed for today | Today | `GTD Today` |
| **Next actions** | Clarified tasks with duration | Next | `GTD Next` |
| **Calendar** | Hard landscape: meetings (**read-only** — never write Outlook/Apple Calendar) | — | — |
| **Waiting** | Blocked on someone else (`#waiting`) | Waiting | `GTD Waiting` |
| **Someday** | `#someday` — excluded from plan-day unless asked | Someday | `GTD Someday` |
| **Done** | Finished | Done | (complete reminder) |

Created by `gtd-setup-ui.sh` — see [SETUP-LAZY.md](SETUP-LAZY.md).

## Meeting types

| Type | Planning |
|------|----------|
| `required` | Always on calendar; tasks never overlap |
| `optional` | Show in plan; skip if day is full — user can mark `skipped` |
| `info_only` | No prep block; OK to miss; listed for awareness |

## Task durations

| Token | Minutes | Use |
|-------|---------|-----|
| `5m` | 5 | Quick calls, email batch |
| `30m` | 30 | Default when unknown |
| `1h` | 60 | Standard focus |
| `2h` | 120 | Deep work default for multiday chunks |
| `4h` | 240 | Half-day focus |
| `multiday` | `remaining_minutes` | Split until `done` |

**Multiday:** set `chunk_minutes` to **60, 120, or 240**. Each completed block reduces `remaining_minutes`. Plan-day schedules at most **one chunk per day** unless user sets `daily_chunks: 2`.

## Working hours

- **Work:** 09:00–17:00 (local timezone in `config.yaml`)
- **Break:** 11:30–13:00 — no new task blocks; meetings may still appear (user choice in config: `allow_meetings_during_break`, default `true`)

## Lazy capture grammar

One line:

```text
<title> [duration] [req|opt|info] [#tag] [@context]
```

Examples:

```text
Fix login timeout 2h #work
Standup prep 5m
Read RFC — info only
Migrate DB multiday chunk 4h #deep
Call vendor 30m @phone
```

Parser rules:

1. Trailing duration token wins (`5m`, `30m`, `1h`, `2h`, `4h`, or `multiday`).
2. `req` / `required` → meeting type or must-do; `opt` / `optional`; `info` / `info only` → `info_only`.
3. If line matches calendar import shape, route to meetings not tasks.

## Clarify (minimal questions)

Ask **only if** planning would fail:

| Situation | Default if silent |
|-----------|-------------------|
| No duration | `30m` |
| Meeting, no type | `optional` |
| Multiday, no chunk | `chunk_minutes: 120` |
| Title only | task on `@computer` |

## Engage order (plan-day)

1. Place **required** meetings.
2. Fill gaps with **next actions** — sort: due today → `#urgent` → shortest duration first (quick wins) → longer blocks.
3. Offer **one** optional meeting if free block ≥ duration.
4. Leave 15m buffer at end of day unless `config.no_buffer: true`.

## Done definition

- **Task:** `status: done` — remove from next pass or archive in `tasks.json` history.
- **Multiday block:** `last_block_completed_at` updated; not `done` until `remaining_minutes <= 0`.
