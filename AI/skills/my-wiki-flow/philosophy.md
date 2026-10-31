# Philosophy (condensed)

Sources:

- [Building Your AI Second Brain — Ron Forbes](https://www.ronforbes.com/blog/building-your-ai-second-brain)
- [How to Build an AI Second Brain: Five Levels — MindStudio](https://www.mindstudio.ai/blog/how-to-build-ai-second-brain-five-levels)
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Understand Anything](https://github.com/Egonex-AI/Understand-Anything) — knowledge graph over Karpathy wikis
- [Trail of Bits skills](https://github.com/trailofbits/skills) — progressive disclosure for entry vs reference pages
- [book-to-skill](https://github.com/virgiliojr94/book-to-skill) — topic index + decision layer; structure over dumps
- [Diátaxis](https://diataxis.fr/) — reader-intent inspiration only (see Identity below)
- [ADS](https://archstandard.org/v1/standard/overview/) — architecture page shape

## Identity (what this skill is)

**my-wiki-flow is a code-validated, project-scoped LLM wiki** for systems you maintain.

| It is | It is not |
|-------|-----------|
| Markdown vault + ArchWiki-style HTML | A full Diátaxis doc site |
| Progressive disclosure (Topic index → one page) | Atomic Zettelkasten for every feature |
| Architecture / Decisions / how-tos grounded in code | README rewrites |
| Optional cross-project `concepts/` evergreen notes | A dump of your entire digital life |

**Diátaxis:** use as a compass for *optional* how-to / concept pages (`entity_type`). Do **not** force tutorials or split every feature into four modes. Feature solution-design pages intentionally mix explanation + reference because agents need one routable design surface.

**Evergreen notes:** put recurring ideas in `concepts/`; keep long feature templates under `projects/{slug}/`.

## CODE with AI

| Stage | Human | AI |
|-------|-------|----|
| Capture | Dump freely; inbox OK | Transcribe / fetch / draft Markdown |
| Organize | Guide project structure | Categorize, tag, link |
| Distill | Judgment, nuance, approval | Summaries, patterns, indexes |
| Express | Own the published page | First draft of wiki HTML-ready Markdown |
| Maintain | Skim hygiene report | Inbox / orphan / stale / coverage lint |

## Principles this skill enforces

1. **File over app** — plain Markdown you own; HTML is a view.
2. **Organize for AI context** — project folders beat perfect taxonomy.
3. **Links over deep nesting** — connect pages; keep nav shallow.
4. **Stay in the loop** — AI drafts; you approve distill/update on meaningful changes.
5. **Do not outsource understanding** — wiki pages teach *you*; summaries are not a substitute for judgment.
6. **Code over repo docs** — distill from sources/handlers/schemas/config/tests, not README or `docs/**`.
7. **Start at a level you will maintain** — Architecture + Topic index + Solution design + Decisions + Glossary; optional how-tos + concepts.
8. **Capture first, perfect later** — inbox is valid; structure emerges; run `maintain` so inbox does not rot.
9. **Lint and incremental update** — `wiki-lint.py`; refresh from git diffs (`update`) instead of rewriting everything.
10. **Claims have a lifecycle** — status, confidence, and review dates for fold-in vs code-backed facts.

## What not to do

- Spend a session designing folders with no pages.
- Import entire digital life before first useful project wiki.
- Accept bulk AI rewrites without skim.
- Put secrets in the vault.
- Claim full Diátaxis coverage while shipping mixed-purpose feature pages.
- Treat prose fold-in as Architecture / sequence / Key claims evidence without code confirmation.
