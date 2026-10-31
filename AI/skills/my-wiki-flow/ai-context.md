# Using the wiki as AI context

## Load order (agents)

When the user asks to use or **query** the wiki:

1. Read `{root}/AGENTS.md` and skill [content-contract](content-contract.md) if shaping pages.
2. Read `{root}/ai/CONTEXT.md`.
3. Read root `index.md` and `ai/INDEX.md` for the project / concepts map.
4. Open `projects/{slug}/topic-index.md` or `concepts/topic-index.md` and match the question to one **Topic** row.
5. Open only that linked page (primary). Prefer page `summary` frontmatter before full body.
6. **Two-hop max:**
   - If the question is “when / avoid / trade-off” or the primary page is not Decisions → also open `decisions.md`.
   - Open at most **one** additional See also / Related / backlink target.
7. Respect `entity_type` when choosing among candidates (how-to for tasks, explanation/reference for concepts).
8. Cite wiki paths. If missing, say so — do not invent.
9. For site UX questions, skim generated HTML only if Markdown is missing.

For **Understand Anything**, point `/understand-knowledge` at the vault root after `wiki-build.sh`.

## Query vs rebuild

| Intent | Mode |
|--------|------|
| Answer a question from existing pages | `query` — no scaffold/build unless asked |
| Preview features / topics before writing | `analyze` — report only, then HITL |
| Code moved; refresh stale pages | `update` then lint + build |
| New project / empty stubs | `distill` then lint + build |
| Fold papers/docs into references/concepts | `fold-in` (Stage 3e) — prose ≠ code evidence |
| Inbox / orphan / stale hygiene | `maintain` then lint + build |

## CONTEXT.md template (maintained by distill/build)

```markdown
# AI context — My Wiki

- **Root:** ~/Documents/my-wiki
- **Canonical:** Markdown under projects/ and concepts/
- **Do not:** paste all of site/ into the prompt

## How to answer from this wiki

1. Pick project(s) or Concepts from INDEX.md
2. Read topic-index.md → open one linked page
3. Two-hop: Decisions (if needed) + at most one See also
4. Prefer frontmatter summary before full body
5. Cite page paths when stating facts from the wiki
6. If missing, say so — do not invent wiki content
```

## INDEX.md shape

```markdown
# Wiki index

## concepts — Concepts

- [Concept title](../concepts/…md) — summary

## project-slug — Title

- [Page title](../projects/project-slug/page.md) — summary
- …

## inbox

- …
```

## Second-brain levels (this skill’s default)

| Level | Support in my-wiki-flow |
|-------|-------------------------|
| 1 Routing | `inbox/` → `projects/` / `concepts/`; **topic-index** |
| 2 Metadata | frontmatter tags, summaries, `entity_type`, `confidence`, `aliases` |
| 3 Fast search | Pagefind on HTML + backlinks |
| 4 RAG-ready | Agents retrieve via INDEX + topic-index + one page (+ 2-hop) |
| 5 Knowledge graph | Out of scope unless user asks later |

Start maintainable: Levels 1–2 + Pagefind + disciplined load order + **lint** + **maintain**.
Do not build a vector DB unless requested.

## Organize for context windows

Keep all notes for one effort under `projects/{slug}/` so an agent can be pointed
at a single directory. Put recurring cross-project ideas under `concepts/`.
Register the code root in `config.yaml` → `projects.{slug}.workspace`.
Prefer Topic index over dumping every feature page.
