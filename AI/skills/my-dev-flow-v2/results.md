# Result first-line tokens

```
Result: <token>
```

Optional note: `Result: blocked — Gate B veto`. Parent reads first ~40 lines.

| Domain | Tokens | Advance when |
|--------|--------|--------------|
| Verify | `verify-pass` \| `verify-fail` | `verify-pass` |
| Blocked | `blocked — <reason>` | settle reason first |
| Design review (`03a*`) | `clean` \| `needs update` \| `skipped` | overall `clean` |
| Gate A (`01a`) | `ok` \| `needs update` \| `escalate` | `ok` |
| Grill (`02b`) | `frontier-empty` \| `needs-round` \| `skipped` | `frontier-empty` or `skipped` |
| Skim | `done` \| `skipped` | either |
| TDD (`04a`) | `clean` \| `needs more tests` | `clean` or Notes skip |
| Code review (`05*`) | `clean` \| `needs fix` | `clean` |
| Test / Smoke (`06`) | `success` \| `failure` \| `smoke-pass` \| `smoke-fail` | `success` / `smoke-pass` |
| Merge | `success` \| `aborted` | `success` and `merge` ∈ Gate C approved |

**Clean** = zero open Critical/Major ([severity.md](severity.md)).

## Parent habit

1. Read Result first line.
2. Update card + Last Verify when Verify applies.
3. Advance only per table.
4. Max 3 attempts → Decision N ([decisions.md](decisions.md)).
