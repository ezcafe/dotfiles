# Parent-next — Open 1–2

After derive Expected Next, open **at most two** files:

| Next | Open |
|------|------|
| `gate-b` / `gate-c` | That gate file only (parent-only) |
| Named stage | Subflow `stages/<id>.md` + artifact path from handoff |
| `lens-*` | Expand via handoffs description map → specific lens stage |
| `api\|db` | Both api-contract-review + db-design-review prompts; Pending parallel |

Do not open full handoffs or orchestrator SKILL.
