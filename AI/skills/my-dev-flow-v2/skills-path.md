# Skills path resolution

Task prompts use `{skill-name}` placeholders (e.g. `{my-dev-flow-v2}`, `{myplan}`).

**Source of truth:** when the repo has `AI/skills/`, that tree is canonical.  
Sync: `AI/skills/sync-to-cursor.sh` → `~/.cursor/skills`.

Resolve placeholders to absolute skill directories:

1. `<repo>/AI/skills/<skill-name>/` if present (**preferred**)
2. else `<repo>/.cursor/skills/<skill-name>/`
3. else `~/.cursor/skills/<skill-name>/`
4. Cursor built-ins only: `~/.cursor/skills-cursor/<skill-name>/`

Do not hardcode `~/.cursor/skills/...` when `AI/skills/<name>` exists.

**Step 0:** when `AI/skills/my-dev-flow-v2` exists, `--check` (or sync) before classify. After SoT edits: sync then re-check.
