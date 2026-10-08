# Daily use (lazy)

Aliases: `.gtd-capture` / `.gtd-cap`, `.gtd-morning` / `.gtd-mor`, `.gtd-plan`, `.gtd-sprint` / `.gtd-spr`, `.gtd-pull`, `.gtd-sync`, `.gtd-review` / `.gtd-rev`, plus `.gtd-setup`, `.gtd`, `.gtd-now`.

First-time: [SETUP-LAZY.md](SETUP-LAZY.md) → `.gtd-setup` (asks GitHub/Reminders/Both/None + Outlook/Apple/Both/None; remembers).  
Change later: `.gtd-setup --reask`  
Hourly meetings: [automation/cron.example](automation/cron.example) runs `.gtd-pull` using remembered calendar.  
Agent model: **inherit** by default; falls back to fast (`GTD_AGENT_FAST=composer-2.5-fast`).  
**Sync only when you type `y`** after plan / `.gtd-sync` — never automatic.

## Morning — 09:00–09:30 (GTD plan)

Run this in the plan window. Task blocks start at **09:30**.

```bash
.gtd-capture "optional brain dump 30m"
.gtd-morning
```

`gtd-morning.sh` does:

1. Clarify inbox → tasks  
2. Plan day → `today.json`  
3. Print **sprint blocks**  
4. Ask **Sync …? [y/N]** → sync **only if you approve with `y`**

Pull is hourly (if cron installed). Sync never runs unless you approve.

Manual: `.gtd-pull`, `.gtd-sync` (still asks), `gtd-pull-calendar.sh`.

Glance at sprint output, GitHub view **Today**, or Reminders **GTD Today**.

## During the day

- Capture: `.gtd-capture "…"`  
- Replan: `.gtd-plan` (sprint + ask sync again)  
- Now: `.gtd-now`  
- Force pull: `.gtd-pull` or `.gtd-pull --outlook`  
- Sync (asks first): `.gtd-sync`  

- Done: Status **Done** on GitHub / check Reminders, or `my-gtd-flow done <title>`  
- Multiday block done: `my-gtd-flow block done <title>`  
- Skip optional meeting: local only — never edit Calendar/Outlook  

## Lunch (11:30–13:00)

Break. Optional: `.gtd-capture` only.

## Evening — 5 minutes

```bash
.gtd-review
```

(Inherit → fast.) Mark done, skip optional meetings, preview tomorrow top 3. Do not sync unless you approve.

## Weekly — 10 min

- Empty Inbox  
- Scan Waiting / Someday (promote max 2)  
- Archive Done on GitHub **Board**

## Cheat sheet

| Token | Meaning |
|-------|---------|
| `5m` `30m` `1h` `2h` `4h` | Duration |
| `multiday chunk 2h` | Long task split |
| `req` / `opt` / `info` | Meeting type |
| `#tag` | Label |
| `@phone` `@computer` | Context |

Default duration **30m**. Default meeting **optional**.
