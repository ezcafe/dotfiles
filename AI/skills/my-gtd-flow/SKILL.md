---
name: my-gtd-flow
description: >-
  GTD task manager for lazy daily use: capture with minimal input, plan work
  blocks 9AM–5PM (lunch 11:30–1PM), sync to GitHub Projects (gh) and/or Apple
  Reminders, ingest meetings from Microsoft Outlook (Playwright in default
  browser) or Apple Calendar (read-only — never create/edit/delete calendar
  events). Multiday tasks split into 1/2/4h blocks. Use when the user says run
  my-gtd-flow, GTD, plan my day, capture task, sync projects, morning, or daily
  GTD review. Prefer inherit model; otherwise use a fast model. Sync only after
  explicit user approval.
disable-model-invocation: true
argument-hint: "capture | morning | plan-day | sync | review | setup | pull"
---

# my-gtd-flow

GTD for people who skip forms. **One inbox, smart defaults, automation first.**

| Doc | Use |
|-----|-----|
| [SETUP-LAZY.md](SETUP-LAZY.md) | One-time setup via `gtd-setup-ui.sh` |
| [DAILY-LAZY.md](DAILY-LAZY.md) | Morning `.gtd-morning` + evening review |
| [gtd-core.md](gtd-core.md) | Lists, durations, meeting types, working hours |
| [io-contract.md](io-contract.md) | JSON schemas |
| [integrations.md](integrations.md) | GitHub / Reminders / Calendar / Outlook |
| [outlook-playwright.md](outlook-playwright.md) | Outlook web pull (read-only) |
| [schedule-engine.md](schedule-engine.md) | Planner rules |
| [automation/README.md](automation/README.md) | Hourly pull cron + agent-cron |
| [aliases.example](aliases.example) | `.gtd-*` aliases |

**Scripts:** `{skill}/scripts/`

## Model (non-negotiable)

1. **Prefer `inherit`** — use the session / parent model (do not pass `--model` when possible).
2. **Otherwise use a fast model** — default fallback `composer-2.5-fast` (`GTD_AGENT_FAST`).
3. Env: `GTD_AGENT_MODEL=inherit` (default) or a fast slug; scripts use `gtd-agent.sh`.
4. Do **not** escalate to a larger model unless the user explicitly asks.

## Workspace

```text
~/.my-gtd/
  config.yaml
  inbox.json / tasks.json / meetings.json / today.json
  logs/
```

## When to run

| User says | Do |
|-----------|-----|
| setup | `gtd-setup-ui.sh` (asks GitHub/Reminders/Both/None + Outlook/Apple/Both/None; remembers) |
| morning / start day | `gtd-morning.sh` (clarify → plan → **sprint blocks** → ask sync) |
| plan / replan | `gtd-plan.sh` (same ask-sync) |
| capture | `gtd-capture.sh` or agent one-liner |
| pull meetings | Hourly cron; manual `gtd-pull.sh` / `gtd-pull-calendar.sh` |
| sync | **Only after you approve** (`y` on ask). Never silent auto-sync. |
| review | `.gtd-review` (inherit → fast) |

## Agent workflow

1. Read `~/.my-gtd/config.yaml` if present; else setup.
2. Prefer running scripts over reinventing logic.
3. **Morning:** run `gtd-morning.sh` (or clarify + plan + sprint + ask sync).
4. After any plan: **ask** to sync; run sync **only if the user approves** (`y`). Never sync unprompted. Agent must not call sync scripts unless the user said yes.
5. Calendar/Outlook: **pull only**. Never update Outlook or Apple Calendar.
6. Keep answers short; model = inherit, else fast.

## Non-negotiables

- Work **09:00–17:00**; no task blocks **11:30–13:00**.
- Durations: **5m, 30m, 1h, 2h, 4h**, or multiday chunks **1h/2h/4h**.
- Meeting types: **required** / **optional** / **info_only**.
- **Never update Outlook or Apple Calendar.**
- **Model:** inherit when possible, otherwise fast.
- **Sync only on explicit approval** (never assume yes).

## Package map

| File | Role |
|------|------|
| `scripts/gtd-morning.sh` | Morning: plan → sprint → ask sync |
| `scripts/gtd-plan.sh` | Clarify → plan → sprint → ask sync |
| `scripts/gtd-sprint.sh` | Print today’s blocks |
| `scripts/gtd-ask-sync.sh` | Ask → sync only on `y` |
| `scripts/gtd-agent.sh` | Agent wrapper: inherit → fast fallback |
| `scripts/gtd-pull.sh` | Manual/hourly calendar pull |
| `scripts/gtd-sync.sh` | Same as ask-sync (always prompts) |
| `scripts/gtd-setup-ui.sh` | Setup GitHub + Reminders |
| `automation/cron.example` | Hourly Apple pull |
| `automation/agent-cron.example` | Hourly Apple + Outlook |

## Related

- Playwright MCP for Outlook (read-only).
- `gh` for GitHub Projects.
