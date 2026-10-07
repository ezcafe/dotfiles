# Design: my-gtd-flow

## What ships

- Cursor skill `AI/skills/my-gtd-flow/` (orchestrator + contracts + integration guides)
- Lazy setup doc `SETUP-LAZY.md` and daily doc `DAILY-LAZY.md`
- Local state dir `~/.my-gtd/` (config + JSON state; not committed)
- Scripts: init, capture, plan-day, sync GitHub Projects, optional Reminders/Calendar
- Agent flows: Outlook via Playwright MCP in OS default browser; n8n/cron templates in `automation/`

## Architecture

```text
Capture (1 line) → inbox.json
       ↓ clarify (defaults / rules) → tasks.json + meetings.json
       ↓ plan-day (9–17, skip 11:30–13:00) → today.json
       ↓ adapters → GitHub Project v2 | Apple Reminders (optional)
Meetings ← Apple Calendar (icalBuddy/osascript) | Outlook (Playwright export)
```

## Defaults (lazy)

- Unknown duration → 30m; unknown meeting type → `optional`
- Multiday tasks: `remaining_minutes`, default chunk 2h until done
- `@context` tags optional; energy not required
- Morning: `gtd-plan-day`; evening: agent runs 5-min review from skill

## Has API

Skill `io-contract.md` — task, meeting, day-plan schemas; adapter boundaries.

## Out of scope v1

- Mobile app; team GTD; bi-directional GitHub webhook (manual/cron sync only)
