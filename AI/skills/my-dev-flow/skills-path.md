# Skills path resolution

Task prompts use **`{skill-name}`** placeholders (e.g. `{my-dev-flow}`, `{myplan}`).

Before launching a Task, resolve each placeholder to the **absolute path** of that skill directory:

1. `<repo>/.cursor/skills/<skill-name>/` if it exists  
2. else `~/.cursor/skills/<skill-name>/`  
3. For Cursor built-ins only: `~/.cursor/skills-cursor/<skill-name>/` (e.g. `review-security`)

In the Task prompt, replace `{my-dev-flow}` with the resolved path, then reference files under it (e.g. `{my-dev-flow}/handoffs.md` → `/path/to/my-dev-flow/handoffs.md`).

Do **not** hardcode `~/.cursor/skills/...` in prompts when a project skill exists.
