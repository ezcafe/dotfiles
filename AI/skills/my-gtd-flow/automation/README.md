# Automation

## Model

Prefer **inherit**; otherwise a **fast** model:

```bash
export GTD_AGENT_MODEL=inherit              # default — no --model
export GTD_AGENT_FAST=composer-2.5-fast     # fallback if inherit fails
```

`gtd-agent.sh` and aliases honor this.

## Sync policy

**Never auto-sync.** Morning/plan call `gtd-ask-sync.sh`, which runs sync **only after you type `y`**.  
Do not put `gtd-sync-github.sh` in cron/n8n without an interactive approval step.

## Hourly meeting pull

| File | What |
|------|------|
| [cron.example](cron.example) | Hourly `gtd-pull.sh` from remembered calendar choice |
| [agent-cron.example](agent-cron.example) | Same (Outlook uses inherit→fast agent) |

```bash
crontab -e
```

Manual: `.gtd-pull`

## Morning (human)

```bash
.gtd-morning
# clarify → plan → sprint → ask sync (y to approve)
```
