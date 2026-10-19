# Failure playbook (hard-stop chat)

| Stop | Chat |
|------|------|
| Skills sync drift | Sync SoT then re-check; do not classify |
| Invent *what* without framing | Offer myplan vs Mode full Ideation |
| Gate A escalate | Decision N — never invent Result `ok` |
| Design not clean before Build | Finish design-review / design-verify |
| Gate B unsettled | Ask / arm Build; do not launch Build |
| verify-fail ×3 | Decision N ([decisions.md](decisions.md)) |
| Max-round hit | Decision N |
| skip-review + Has API/DB/auth/PII/schema yes | Drop skip-review; reclassify if needed |
| Gate C without named yes | Ask commit/push/PR/merge; do not invent |
| Task wrote consent fields | Revert; parent re-writes after user yes |
| Secrets in commit path | Refuse; remove from stage |

Do not invent approval, override, or waive tokens to unblock.
