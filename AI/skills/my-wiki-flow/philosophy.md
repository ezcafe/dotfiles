# Philosophy (condensed)

Sources:

- [Building Your AI Second Brain — Ron Forbes](https://www.ronforbes.com/blog/building-your-ai-second-brain)
- [How to Build an AI Second Brain: Five Levels — MindStudio](https://www.mindstudio.ai/blog/how-to-build-ai-second-brain-five-levels)
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Understand Anything](https://github.com/Egonex-AI/Understand-Anything) — knowledge graph over Karpathy wikis
- [Trail of Bits skills](https://github.com/trailofbits/skills) — progressive disclosure for entry vs reference pages

## CODE with AI

| Stage | Human | AI |
|-------|-------|-----|
| Capture | Dump freely; inbox OK | Transcribe / fetch / draft Markdown |
| Organize | Guide project structure | Categorize, tag, link |
| Distill | Judgment, nuance, approval | Summaries, patterns, indexes |
| Express | Own the published page | First draft of wiki HTML-ready Markdown |

## Principles this skill enforces

1. **File over app** — plain Markdown you own; HTML is a view.
2. **Organize for AI context** — project folders beat perfect taxonomy.
3. **Links over deep nesting** — connect pages; keep nav shallow (project → pages).
4. **Stay in the loop** — AI drafts; you approve distill/update on meaningful changes.
5. **Do not outsource understanding** — wiki pages teach *you*; summaries are not a substitute for judgment.
6. **Code over repo docs** — project wiki describes what the code does; distill from sources/handlers/schemas/config/tests, not from README or `docs/**`.
7. **Start at a level you will maintain** — Architecture + Solution design + Glossary per project; RAG/graph later only if asked.
8. **Capture first, perfect later** — inbox is valid; structure emerges.
9. **Lint and incremental update** — health-check with `wiki-lint.py`; refresh from git diffs (`update`) instead of rewriting everything.

## What not to do

- Spend a session designing folders with no pages.
- Import entire digital life before first useful project wiki.
- Accept bulk AI rewrites without skim.
- Put secrets in the vault.
