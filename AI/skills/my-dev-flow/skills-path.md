# Skills path resolution

Task prompts use **`{skill-name}`** placeholders (e.g. `{my-dev-flow}`, `{myplan}`).

**Source of truth:** when this repo has `AI/skills/`, that tree is canonical. Sync to
Cursor with `AI/skills/sync-to-cursor.sh` (copies into `~/.cursor/skills` for discovery).

Before launching a Task, resolve each placeholder to the **absolute path** of that skill directory:

1. `<repo>/AI/skills/<skill-name>/` if it exists (**preferred — source of truth**)
2. else `<repo>/.cursor/skills/<skill-name>/` if it exists
3. else `~/.cursor/skills/<skill-name>/`
4. For Cursor built-ins only: `~/.cursor/skills-cursor/<skill-name>/` (e.g. `review-security`)

In the Task prompt, replace `{my-dev-flow}` with the resolved path, then reference files under it (e.g. `{my-dev-flow}/handoffs.md` → `/path/to/my-dev-flow/handoffs.md`).

Do **not** hardcode `~/.cursor/skills/...` in prompts when `AI/skills/<skill-name>` exists.
After editing skills under `AI/skills/`, run `./AI/skills/sync-to-cursor.sh` so Cursor’s skill list matches.
