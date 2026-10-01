---
name: dev-decision-routing
description: Inspects Work/Dev/{HTML|CSS|Js} in the qan project for reference knowledge before implementing web features. Use when coding HTML, CSS, JavaScript, or TypeScript, or when the user asks to implement or build a front-end feature. Routes to local knowledge first, then online sources if needed.
---

# Dev Decision Routing

Before implementing any HTML, CSS, or JavaScript/TypeScript feature, run the decision routing workflow below. Local knowledge takes precedence; fall back to online sources only when nothing relevant is found.

## Tool requirement

**Use context-mode MCP (user-context-mode) for all lookup and research in this workflow.** Do not use Read, Grep, or WebSearch. Use these instead:

| Task | Use context-mode | Do NOT use |
|------|------------------|------------|
| List/read files in Work/Dev/* | `execute_file` or `batch_execute` | Read, Glob |
| Search for patterns in files | `search` on indexed content | Grep |
| Look up docs/specs online | `fetch_and_index` + `search` | WebSearch |
| Run discovery commands | `batch_execute` or `execute` | Bash/Shell |

## Path constant

```
QAN_PATH = /Users/ptquang86/ws/syncthing/pi4-jotty/data/notes/qan
```

Update this path in this skill file if the qan project moves.

## Routing table

| Prompt keywords / context | Route to folder |
|---------------------------|-----------------|
| HTML, markup, semantic, structure, elements | `{QAN_PATH}/Work/Dev/HTML` |
| CSS, styling, layout, grid, flexbox | `{QAN_PATH}/Work/Dev/CSS` |
| JavaScript, TypeScript, JS, TS, logic, interactivity | `{QAN_PATH}/Work/Dev/Js` |

If the prompt spans multiple languages, check each relevant folder once in a single pass.

## Workflow

1. **Detect language** from the user prompt:
   - HTML: markup, structure, elements, semantic
   - CSS: styling, layout, design, grid, flex
   - JS/TS: JavaScript, TypeScript, logic, interactivity, scripting

2. **Resolve lookup path** using the table above.

3. **Local lookup** — Use context-mode MCP:
   - `batch_execute` with commands to list/read files in the resolved Work/Dev path
   - Or `execute_file` to read `.md`/`.mdc` files in that folder
   - Use `search` for pattern discovery if content is already indexed

4. **Apply or fallback**:
   - If relevant local knowledge exists: apply it and proceed
   - If folder is empty or nothing matches: use `fetch_and_index` + `search` (context-mode) for docs/specs, then proceed
   - Do not use WebSearch

5. **Proceed** with implementation using the gathered context.

## Efficiency rules

- One lookup pass per language — no redundant reads
- Use `batch_execute`/`execute_file` for broad discovery; use `search` for targeted search
- Do not re-read the same file within the same workflow
- If the folder has no files beyond README.md, treat as "no local knowledge" and fallback
