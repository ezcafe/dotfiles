# Skills path resolution

Task prompts use **`{skill-name}`** placeholders (e.g. `{my-dev-flow}`, `{myplan}`).

**Source of truth:** when this repo has `AI/skills/`, that tree is canonical.  
**Single SoT sync script:** `AI/skills/sync-to-cursor.sh` (copies into `~/.cursor/skills` for discovery). Do not use a second skills sync path for my-dev-flow*.

Before launching a Task, resolve each placeholder to the **absolute path** of that skill directory:

1. `<repo>/AI/skills/<skill-name>/` if it exists (**preferred — source of truth**)
2. else `<repo>/.cursor/skills/<skill-name>/` if it exists
3. else `~/.cursor/skills/<skill-name>/`
4. For Cursor built-ins only: `~/.cursor/skills-cursor/<skill-name>/` (e.g. `review-security`)

In the Task prompt, replace `{my-dev-flow}` with the resolved path, then reference files under it (e.g. `{my-dev-flow}/handoffs.md` → `/path/to/my-dev-flow/handoffs.md`).

Do **not** hardcode `~/.cursor/skills/...` in prompts when `AI/skills/<skill-name>` exists.

**Sync (required after SoT edits) — Step 0 hard stop:**

1. Edit SoT under `AI/skills/` (this tree).
2. When `AI/skills/my-dev-flow` exists: before classify, run `./AI/skills/sync-to-cursor.sh --check` (or full sync). Drift → **hard stop**; do not classify until fixed.
3. After SoT edits: run `./AI/skills/sync-to-cursor.sh` so `~/.cursor/skills` matches; re-`--check` if unsure.
4. Do **not** treat Cursor discovery as SoT until sync ran / `--check` is clean.

Also noted in [SKILL.md](SKILL.md) Start, [stages.md](stages.md) Step 0, [invariants.md](invariants.md) checklist item 10, and [examples/anti-patterns.md](examples/anti-patterns.md).

**Stage-id drift check (optional after editing handoffs / parent-next / stages):**  
`python3 scripts/lint-run.py . --check-stage-ids` (fails on registry drift).

**myplan:** When Step 0 Decision N chooses framing first, resolve `{myplan}` with the same rules above.
