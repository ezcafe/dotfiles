# Using the wiki as AI context

## Load order (agents)

When the user asks to use or **query** the wiki:

1. Read `{root}/AGENTS.md` and skill [content-contract](content-contract.md) if shaping pages.
2. Read `{root}/ai/CONTEXT.md`.
3. Read root `index.md` and `ai/INDEX.md` for the project map.
4. Open only the **relevant project folder** (and linked pages), not the entire vault.
5. Prefer page `summary` frontmatter before full body.
6. Cite wiki paths. If missing, say so — do not invent.
7. For site UX questions, skim generated HTML only if Markdown is missing.

For **Understand Anything**, point `/understand-knowledge` at the vault root after `wiki-build.sh`.

## Query vs rebuild

| Intent | Mode |
|--------|------|
| Answer a question from existing pages | `query` — no scaffold/build unless asked |
| Code moved; refresh stale pages | `update` then lint + build |
| New project / empty stubs | `distill` then lint + build |

## CONTEXT.md template (maintained by distill/build)

```markdown
# AI context — My Wiki

- **Root:** ~/Documents/my-wiki
- **Canonical:** Markdown under projects/
- **Do not:** paste all of site/ into the prompt

## How to answer from this wiki

1. Pick project(s) from INDEX.md
2. Read Architecture + Solution design + Glossary as needed
3. Cite page paths when stating facts from the wiki
4. If missing, say so — do not invent wiki content
```

## INDEX.md shape

```markdown
# Wiki index

## project-slug — Title

- [Page title](../projects/project-slug/page.md) — summary
- …

## inbox

- …
```

## Second-brain levels (this skill’s default)

| Level | Support in my-wiki-flow |
|-------|-------------------------|
| 1 Routing | `inbox/` → `projects/` by project |
| 2 Metadata | frontmatter tags + summaries |
| 3 Fast search | Pagefind on HTML |
| 4 RAG-ready | Agents retrieve via INDEX + project folders + summaries |
| 5 Knowledge graph | Out of scope unless user asks later |

Start maintainable: Levels 1–2 + Pagefind + disciplined load order + **lint**.
Do not build a vector DB unless requested.

## Organize for context windows

Keep all notes for one effort under `projects/{slug}/` so an agent can be pointed
at a single directory. Register the code root in `config.yaml` →
`projects.{slug}.workspace`.
