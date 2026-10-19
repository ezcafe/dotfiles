# Golden path — Gate A escalate → Decision N

Short walkthrough when Gate A returns **escalate**. SoT: [failure-playbook.md](../failure-playbook.md) · [results.md](../results.md) · [gate-a.md](../../my-dev-flow-design/stages/gate-a.md).

## Ask

> Mode full feature with UI — Gate A Task returns Result **escalate** (unsafe / unethical / too unclear without a human).

## Step 0 (abbrev)

- Mode **full**, Review profile **full** or **lite**
- Status **`paused`** after escalate; card Next = `gate-a`
- HITL Gate B **blocking** (Mode full); Gate C **blocking**

## Parent before each Task (fixed)

1. Clarity boundary + `clarity-check ok — <Next>` ([parent-next.md](../parent-next.md)).
2. `python3 {my-dev-flow}/scripts/lint-run.py <run-dir> --next --derive` (or `preflight.py`)
3. `--snapshot-consent` before launch; `--check-consent-writes` after
4. On handoff (exit 0): `python3 {my-dev-flow}/scripts/handoff-for.py <stage-id>`

## Pipeline (escalate focus)

| # | Stage / action | Result |
|---|----------------|--------|
| 1 | `ideation` | `01-idea.md` |
| 2 | `gate-a` | `01a-gate-a.md` Result **escalate** |
| 3 | Parent | Pause immediately; Next=`gate-a`; **Decision N**: re-run Gate A · human override Result **ok** + Notes **only after explicit user yes** · Stop |
| 4a | Re-run | User picks re-run → increment **Round** on `01a` → launch `gate-a` again |
| 4b | Override | User explicitly says e.g. `yes override Gate A to ok after escalate`; **parent** sets Result **ok** + Notes + Run log `parent consent write — gate-a-override` → re-snapshot → continue **skim** |
| 4c | Stop | Status **`stopped`**; freeze stage |

## Do not

- Invent Result **ok** on resume without Decision N + explicit user yes
- Auto-continue to skim while Result is **escalate**

## Anti-pattern

| Wrong | Right |
|-------|-------|
| Set `01a` Result **ok** to unblock skim | Hold; Decision N + explicit user yes, or re-run Gate A |

Index: [INDEX.md](INDEX.md).
