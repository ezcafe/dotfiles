# Schedule engine

Implements plan-day logic used by `scripts/gtd-plan-day.sh` (Python).

## Inputs

- `config.yaml` work window + break
- `meetings.json` for target date (local)
- `tasks.json` where `status === active` and not `#someday`

## Free block algorithm

1. Start with `[work.start, work.end)`.
2. Subtract break `[break_start, break_end)` for **task** placement only.
3. Subtract each non-skipped meeting (all types occupy time on calendar).
4. Merge adjacent free intervals.

## Placement

| Priority | Item |
|----------|------|
| 1 | Required meetings (fixed) |
| 2 | Tasks with `due_date === today` |
| 3 | Tasks tagged `#urgent` |
| 4 | Shortest `duration_minutes` (tie: higher `priority`) |
| 5 | Multiday: one chunk (`min(chunk_minutes, remaining_minutes)`) |

**Fit rule:** task block must fit entirely inside a free interval. No splitting across intervals.

**Optional meetings:** after tasks, if interval ≥ meeting length and user config `schedule_optional: true`, place optional meetings not yet skipped.

## Multiday

- Schedule **one chunk per day** by default.
- On block complete (user or sync): `remaining_minutes -= actual_minutes`; if ≤ 0 → `status: done`.

## Output

Write `today.json` and print human summary:

```text
09:00–09:30  Team standup (required)
09:30–11:30  Fix login timeout (2h)
11:30–13:00  — break —
13:00–13:30  Email batch (30m)
…
Unscheduled: Migrate DB (multiday) — no 4h block free
```

## Edge cases

- Meeting runs past work end → show warning; do not clip without user OK.
- All day busy → list top 3 tasks for tomorrow suggestion only (do not auto-roll without user).
