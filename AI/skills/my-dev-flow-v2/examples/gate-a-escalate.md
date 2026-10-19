# Golden: Gate A escalate → Decision N

**Ask:** Mode full feature with UI — Gate A returns Result **escalate**.  
**Classify:** Mode full; profile full or lite. Status **`paused`**; card Next = `gate-a`.

## Path

| # | Action | Result |
|---|--------|--------|
| 1 | `ideation` | `01-idea.md` |
| 2 | `gate-a` | `01a-gate-a.md` Result **escalate** |
| 3 | Parent | Pause; Next=`gate-a`; **Decision N** ([decisions.md](../decisions.md)): re-run Gate A · human override Result **ok** + Notes **only after explicit user yes** · Stop |
| 4a | Re-run | User picks re-run → parent bumps **Round** on `01a` → launch `gate-a` again |
| 4b | Override | Explicit yes (e.g. `yes override Gate A to ok after escalate`) → **parent** sets Result **ok** + Notes → continue **skim** |
| 4c | Stop | Status **`stopped`**; freeze stage |

## Do not

- Invent Result **ok** without Decision N + explicit user yes
- Auto-continue to skim while Result is **escalate**

SoT: [failure.md](../failure.md) · [results.md](../results.md) · [gate-a.md](../../my-dev-flow-v2-design/stages/gate-a.md).
