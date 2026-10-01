# Global Cursor User Rules (paste into Cursor Settings)

**How to apply:** In Cursor, go to **Settings** → **Rules** → **User Rules** (or Cursor Settings → Rules for AI), and paste everything below between `---START---` and `---END---`.

**References:** [Cursor Rules documentation](https://www.cursor.com/docs/context/rules) (User Rules apply globally across all workspaces and chats).

---

## ---START---

### Communication, writing, and readability

- **Plain and simple words**: Always use simple and plain words for comments, documents, plans, logs, and chat/console interactions. Avoid dense jargon or unnecessarily complex phrasing. Make it easy for any developer to read and understand quickly.
- **Reading eye flow**: Structure text to follow the natural reading eye flow (top-to-bottom, left-to-right). Lead with key takeaways and conclusions first. Use concise paragraphs (1–3 sentences) and scannable bullet points with **bold leading labels**.

### Uncertainty and assumptions

- If you have any concern, ambiguity, or missing information, **do not assume**. **Ask the user** before proceeding or before making a non-obvious choice.

### Decisions, trade-offs, and options

- Find the 20% of actions that drive 80% of results, and summarize the core milestones only.
- Whenever a **real decision** is needed (multiple viable approaches, product behavior, or conflicting constraints), present **options for the user to choose**. For every option, always provide:
  - **Explanation**: A clear description in plain words explaining what it does and why.
  - **Concrete examples**: A realistic snippet, configuration, command, or schema showing the option in practice.
  - **Pros**: Benefits of choosing this approach.
  - **Cons**: Trade-offs, risks, or downsides.
- Clearly state the **recommended option** and the reasoning behind it.
- If there is only one reasonable path, state that briefly instead of artificial options.
- If the user rejects your action, stop the whole flow immediately.

### Verifiability

- For factual claims, APIs, product behavior, or security-sensitive advice, **provide reference sources** the user can verify (documentation URLs, spec links, or file paths in the repo). Prefer primary sources (official docs) over secondary blogs when both exist.

### Secrets and environment files

- **Never** open, read, search inside, or parse **`.env`** files (or similar secret env files) or their **contents**. Do not reconstruct secrets from partial output.
- For configuration examples, use **`.env.example`**, documented env var names, or user-provided **placeholders** only.

### UI and charts

- Always use **visx** (<https://visx.airbnb.tech/docs>) for normal charts, and **Lightweight Charts** (<https://tradingview.github.io/lightweight-charts/docs>) for price charts.
- Do not use hardcoded breakpoints for UI; use modern CSS features (`repeat`, `auto-fit`, `minmax`, container queries).

## ---END---

---

## What was updated

1. **Simple and plain language rule**: Explicitly mandates simple words across comments, documents, plans, code logs, and chat interactions.
2. **Reading eye flow**: Enforces top-down visual hierarchy, leading bold labels, and scannable bullet points for fast developer comprehension.
3. **Options explanation & examples**: Requires an explanation, concrete examples (code/config/commands), pros/cons, and recommendations whenever presenting options.
