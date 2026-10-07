# Integrations

Pick **one task UI** or both. Calendar can be Apple, Outlook, or both (merge by time; dedupe by title+start).

## Calendar read-only

<a id="calendar-read-only"></a>

**Never update Outlook calendar or Apple Calendar.**

| Allowed | Forbidden |
|---------|-----------|
| Read / scrape events into `meetings.json` | Create, edit, delete, move events |
| Infer `type` / `skipped` in local JSON | Accept / decline / RSVP in the calendar UI |
| Plan around meetings in `today.json` | Write blocks or tasks back to Calendar/Outlook |

Task UIs (GitHub Projects, Apple Reminders) may still be updated. Calendars are landscape only.

## GitHub Projects (gh CLI)

**Primary sources:** [GitHub CLI manual — project](https://cli.github.com/manual/gh_project), [Projects v2 REST](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project-using-the-api).

### One-time (scripted) — prefer `gtd-setup-ui.sh`

Full walkthrough: [SETUP-LAZY.md](SETUP-LAZY.md).

```bash
gh auth login
gh auth refresh -s project   # if needed

# Recommended: both UIs
scripts/gtd-setup-ui.sh --all

# GitHub only (A → gtd-setup-github.sh → gtd_setup_github.py)
scripts/gtd-setup-ui.sh --github
```

Creates/reuses Project **GTD** with required GTD shape (GraphQL):

| Kind | Names |
|------|--------|
| Status options | Inbox, Today, Next, Waiting, Someday, Done |
| Fields | Duration (5m–4h), Context, Chunk (1h/2h/4h), Due |
| Views | Board (board); Inbox / Today / Next / Waiting / Someday (table + `status:` filter) |

Writes `owner`, `project_number`, `inbox_status: Inbox` into `config.yaml`. Idempotent — safe to re-run.

### Sync direction (lazy v1)

| Direction | Behavior |
|-----------|----------|
| GTD → GitHub | New active tasks → draft issue / project item; prefer Status **Inbox** or **Today** from plan |
| GitHub → GTD | `gh project item-list` on cron — import Inbox / Today items |

Run: `scripts/gtd-sync-github.sh`

**Field mapping (default):**

| GTD | GitHub |
|-----|--------|
| `title` | Issue / item title |
| `duration_minutes` | **Duration** field (or body `Duration: 2h`) |
| `chunk_minutes` | **Chunk** field |
| `@context` | **Context** field |
| `due_date` | **Due** field |
| `status: done` | Status **Done** |

## Apple Reminders (optional)

Requires macOS.

### One-time (scripted) — prefer `gtd-setup-ui.sh`

```bash
scripts/gtd-setup-ui.sh --reminders
# or: scripts/gtd-setup-reminders.sh
# prefix: GTD_REMINDERS_PREFIX=GTD (default)
```

| List | Role |
|------|------|
| `GTD Inbox` | Captures |
| `GTD Today` | Default sync target (`list_name`) |
| `GTD Next` | Next actions |
| `GTD Waiting` | Waiting-for |
| `GTD Someday` | Someday/maybe |

Enables `adapters.reminders` in `config.yaml`. If osascript times out (~20s): **Privacy → Reminders**.

Daily sync: `scripts/gtd-sync-reminders.sh`.

- Export: today’s task blocks → **GTD Today** (optional due time = block start).
- Import: incomplete reminders → local inbox (`source: reminders`).

No Reminders → set `adapters.reminders.enabled: false`.

## Apple Calendar (optional)

**Read-only.** `gtd-pull-calendar.sh` only reads events; it must never create or modify Calendar events.

**Option A — icalBuddy** (if installed):

```bash
icalBuddy -f eventsToday+num
```

Parse into `meetings.json` via `scripts/gtd-pull-calendar.sh`.

**Option B — osascript** (built-in): same script fallback.

Apply `config.rules.meeting_title_patterns` to set `type`.

## Microsoft Outlook (Playwright)

**Read-only.** Navigate and snapshot only — never click create/edit/delete/RSVP on events.

No password in repo. Agent uses **Playwright MCP** against the **system default browser** profile or a dedicated logged-in session.

### Flow

Detailed agent steps: [outlook-playwright.md](outlook-playwright.md).

1. Navigate to Outlook on the web calendar week view.
2. Snapshot events for target day(s) — **do not mutate the calendar**.
3. Map to `meetings.json` entries (`source: outlook`).
4. User confirms once if selectors break (store selectors in `~/.my-gtd/outlook-selectors.json`, not in git).

### Lazy tips

- Run pull once each morning via cron **after** login cookie exists.
- Mark internal meetings optional with Outlook categories → map in config if visible in DOM.

### Dedupe

When Apple + Outlook both enabled: same `start` ± 2 min and similar title → keep one, prefer `required` type if either is required.

## n8n / cron

See [automation/README.md](automation/README.md).
