# Lazy setup (~15 minutes)

Goal: morning `plan-day` works with **one command** and almost no typing.

Primary tool: **`gtd-setup-ui.sh`** — creates local workspace, GitHub Project (fields + views), and Apple Reminders lists.

## 0. Prerequisites

```bash
# Optional but recommended (config patch + hours)
python3 -m pip install --user pyyaml

# GitHub UI (if you use Projects)
gh auth login
gh auth refresh -s project   # if project scope missing
```

Without PyYAML, scripts still run with built-in work hours (09:30–17:00 task blocks; 09:00–09:30 GTD plan; lunch 11:30–1).

## 1. Install skill in Cursor

```bash
/Users/ptquang86/dotfiles/AI/sync-cursor.sh
```

In Cursor: invoke **my-gtd-flow** or say `run my-gtd-flow setup`.

## 2. Run gtd-setup-ui.sh (main step)

Interactive by default. It asks, then **remembers** answers in `~/.my-gtd/config.yaml` (`choices.*` + adapter flags). Later runs of `.gtd-pull`, `.gtd-sync`, and setup reuse them.

```bash
SCRIPTS=/Users/ptquang86/dotfiles/AI/skills/my-gtd-flow/scripts
$SCRIPTS/gtd-setup-ui.sh
```

You will be asked:

1. **Task UI:** GitHub only / Apple Reminders only / Both / None  
2. **Calendar (read-only pulls):** Apple Calendar / Microsoft Outlook / Both / None  

Then it runs the matching setup scripts (GitHub fields/views and/or Reminders lists).

Non-interactive / flags:

```bash
$SCRIPTS/gtd-setup-ui.sh --task-ui both --calendar apple --yes
$SCRIPTS/gtd-setup-ui.sh --github --calendar outlook
$SCRIPTS/gtd-setup-ui.sh --reask          # change remembered choices
$SCRIPTS/gtd-setup-ui.sh --help
```

Show saved choices:

```bash
python3 $SCRIPTS/gtd_prefs.py ~/.my-gtd/config.yaml show
```

| Env | Default | Meaning |
|-----|---------|---------|
| `GTD_HOME` | `~/.my-gtd` | State + `config.yaml` |
| `GTD_GITHUB_OWNER` | `@me` | Project owner |
| `GTD_PROJECT_TITLE` | `GTD` | Project title (reuse if exists) |
| `GTD_REMINDERS_PREFIX` | `GTD` | List names: `{prefix} Inbox`, … |

**Requires PyYAML** to save choices: `python3 -m pip install --user pyyaml`

### What GitHub gets

Creates or reuses Project **GTD**, then ensures:

| Kind | Values |
|------|--------|
| **Status** | Inbox, Today, Next, Waiting, Someday, Done |
| **Duration** | 5m, 30m, 1h, 2h, 4h |
| **Context** | computer, phone, errands |
| **Chunk** | 1h, 2h, 4h (multiday blocks) |
| **Due** | date field |
| **Views** | **Board** (board); **Inbox / Today / Next / Waiting / Someday** (table + `status:` filter) |

Writes `adapters.github` in `~/.my-gtd/config.yaml` (`enabled`, `owner`, `project_number`, `inbox_status: Inbox`).

Open: `gh project view <N> --owner @me --web`

### What Reminders gets

| List | Role |
|------|------|
| `GTD Inbox` | Captures |
| `GTD Today` | Today’s plan (default `list_name` for sync) |
| `GTD Next` | Next actions |
| `GTD Waiting` | Waiting-for |
| `GTD Someday` | Someday/maybe |

Grant **System Settings → Privacy & Security → Reminders** if Terminal/Cursor is blocked (script times out after ~20s per list).

### What it does *not* touch

- **Outlook / Apple Calendar events** — never created/edited (pull only). Your calendar *choice* is saved so `.gtd-pull` / hourly cron know what to read.

### Remembered config shape

```yaml
choices:
  task_ui: both              # github | reminders | both | none
  calendar_source: apple     # apple | outlook | both | none
adapters:
  github:
    enabled: true
  reminders:
    enabled: true
  calendar:
    enabled: true
    apple: true
    outlook: false
    source: apple
    calendars: ["Calendar"]  # Apple Calendar.app name
```

## 3. PATH + aliases (optional)

```bash
echo 'export PATH="$HOME/.my-gtd/bin:$PATH"' >> ~/.zshrc
mkdir -p ~/.my-gtd/bin
ln -sf /Users/ptquang86/dotfiles/AI/skills/my-gtd-flow/scripts/gtd-*.sh ~/.my-gtd/bin/
cat /Users/ptquang86/dotfiles/AI/skills/my-gtd-flow/aliases >> ~/.zshrc
```

Useful aliases (all start with `.gtd`): `.gtd-setup`, `.gtd-morning` / `.gtd-mor`, `.gtd-capture` / `.gtd-cap`, `.gtd-plan`, `.gtd-sprint` / `.gtd-spr`, `.gtd-pull`, `.gtd-sync`, `.gtd-review` / `.gtd-rev`, … See [aliases](aliases).

Agent model: prefer **inherit** (`GTD_AGENT_MODEL=inherit`); fallback fast via `GTD_AGENT_FAST=composer-2.5-fast`.

## 4. Automation (recommended)

| File | Use |
|------|-----|
| [automation/cron.example](automation/cron.example) | **Hourly** Apple Calendar pull (09–17 weekdays) |
| [automation/agent-cron.example](automation/agent-cron.example) | Hourly Apple + Outlook (lowest model) |
| [automation/n8n-gtd-morning.json](automation/n8n-gtd-morning.json) | n8n import (optional) |

Daily human command: **`.gtd-morning`** (plan → sprint → ask sync).  
Pull is automated hourly; keep `.gtd-pull` for manual. **Sync only when you type `y`** (`.gtd-sync` also asks — no silent sync).

Details: [automation/README.md](automation/README.md).

## 5. Smoke test

```bash
gtd-capture.sh "Test task 5m #setup"
gtd-clarify.sh
gtd-plan-day.sh
```

You should see GTD plan 09:00–09:30, then task blocks 09:30–17:00 with lunch gap. Delete the test task from `~/.my-gtd/tasks.json` when done.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `gh: not found` | Install [GitHub CLI](https://cli.github.com/) |
| `project` scope missing | `gh auth refresh -s project` |
| Setup partial fail | Re-run `gtd-setup-ui.sh --github` or `--reminders`; each side is idempotent |
| Reminders timeout | Privacy → Reminders → allow Terminal/Cursor; re-run `--reminders` |
| Empty calendar | Set `calendars:` name; run `gtd-pull-calendar.sh` (read-only) |
| Outlook empty | Log in via browser; `.gtd-pull --outlook` (hourly cron if installed) |
| Sync always skipped | Morning/plan ask needs a TTY; or answer `y`; or `.gtd-sync` |

Done. Read [DAILY-LAZY.md](DAILY-LAZY.md) for daily use.
