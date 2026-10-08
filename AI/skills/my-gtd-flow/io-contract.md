# I/O contract

All files under `~/.my-gtd/`. UTF-8 JSON. Validate before write.

## config.yaml (sketch)

```yaml
timezone: America/Los_Angeles  # example — use local
work:
  plan_start: "09:00"   # GTD morning plan window
  plan_end: "09:30"
  start: "09:30"        # task blocks begin here
  end: "17:00"
  break_start: "11:30"
  break_end: "13:00"
  allow_meetings_during_break: true
adapters:
  github:
    enabled: false
    owner: YOUR_ORG
    project_number: 1
    status_field: Status
    inbox_status: Inbox
  reminders:
    enabled: false
    list_name: GTD
  calendar:
    enabled: false
    source: apple  # apple | outlook_file
    calendars: ["Work"]
planning:
  default_duration_minutes: 30
  multiday_default_chunk_minutes: 120
  end_of_day_buffer_minutes: 15
rules:
  meeting_title_patterns:
    - match: "(?i)optional"
      type: optional
    - match: "(?i)FYI|info only"
      type: info_only
```

## inbox.json

```json
{
  "version": 1,
  "items": [
    {
      "id": "uuid",
      "raw": "Fix bug 2h #work",
      "captured_at": "2025-10-07T09:00:00-07:00",
      "source": "cli|agent|github|reminders"
    }
  ]
}
```

## tasks.json

```json
{
  "version": 1,
  "tasks": [
    {
      "id": "uuid",
      "title": "Fix login timeout",
      "status": "active|done|someday|waiting",
      "duration_minutes": 120,
      "multiday": false,
      "remaining_minutes": null,
      "chunk_minutes": null,
      "due_date": null,
      "tags": ["work"],
      "context": "computer",
      "priority": 0,
      "github_issue": null,
      "reminder_id": null,
      "updated_at": "ISO8601"
    }
  ]
}
```

**Multiday:** `multiday: true`, `remaining_minutes` > 0, `chunk_minutes` ∈ {60, 120, 240}.

## meetings.json

```json
{
  "version": 1,
  "meetings": [
    {
      "id": "uuid",
      "title": "Team sync",
      "start": "ISO8601",
      "end": "ISO8601",
      "type": "required|optional|info_only",
      "source": "apple|outlook|manual",
      "location": null,
      "skipped": false
    }
  ]
}
```

## today.json (plan-day output)

```json
{
  "version": 1,
  "date": "2025-10-07",
  "generated_at": "ISO8601",
  "blocks": [
    {
      "kind": "meeting|task|buffer",
      "ref_id": "uuid",
      "title": "string",
      "start": "ISO8601",
      "end": "ISO8601",
      "note": null
    }
  ],
  "unscheduled": [
    { "ref_id": "uuid", "title": "string", "reason": "no_free_block" }
  ]
}
```

## Agent validation rules

1. IDs: UUID v4 or stable slug; never reuse across types.
2. `start` < `end`; meetings/tasks must not overlap **required** items.
3. Task blocks only inside work hours and outside break unless config overrides.
4. Do not delete inbox items until promoted to tasks/meetings or user confirms trash.
