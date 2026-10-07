# Outlook calendar pull (Playwright)

Use when `adapters.calendar` does not include Apple Calendar but the user lives in Outlook on the web.

## Hard rule

**Never update Outlook calendar.** Pull events into `meetings.json` only. Do not create, edit, delete, move, or RSVP to events in the Outlook UI.

## Preconditions

- User logged into Outlook in the **OS default browser** (or profile Playwright uses).
- Playwright MCP available (`plugin-playwright-playwright` or `cursor-ide-browser`).

## Steps (agent)

1. Confirm target date (default: today, local).
2. `browser_navigate` to `https://outlook.office.com/calendar/view/day` (or org-specific URL).
3. `browser_snapshot` — locate event rows (title, start, end). Store working selectors in `~/.my-gtd/outlook-selectors.json` if DOM is stable. **Read-only interactions only** (navigate, snapshot, scroll).
4. For each event, append to `meetings.json`:
   - `source: outlook`
   - `type`: infer from title using `config.rules.meeting_title_patterns`; default `optional`
5. Run `gtd-plan-day.sh` or merge via skill workflow.

## Security

- Do not screenshot credentials or paste cookies into chat.
- Do not commit `outlook-selectors.json` if it contains org URLs with tokens.

## Failure

If login wall appears: stop and ask user to log in manually, then retry snapshot.
