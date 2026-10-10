# ArchWiki-style UI

Visual and structural target:
[ArchWiki Installation guide](https://wiki.archlinux.org/title/Installation_guide#Pre-installation).

## Layout

```text
┌─────────────────────────────────────────────────────────┐
│ Brand / site title          [ Search box ........ ]     │
├──────────────┬──────────────────────────────────────────┤
│ Navigation   │ Contents (TOC)                           │
│              │ # Page title                             │
│ ▸ Project A  │ lead paragraph                           │
│   · page     │ ## Section                               │
│   · page     │ body…                                    │
│ ▸ Project B  │ **Note** box                             │
│   · page     │ ### Subsection                           │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
```

- Left (or collapsible) **nav grouped by project**.
- Within a project: canonical pages flat; **feature solution designs nest under Solution design** (optional `nav_group` / `master_feature` subgroups).
- Main column: TOC → title → article.
- Search always visible in the header (Pagefind **Component UI** `pagefind-searchbox`). Results open in an overlay dropdown so the article does not shift down. Do not use legacy `pagefind-ui.js` / `PagefindUI`.

## Look and feel

Use vault `assets/wiki.css` (from skill). Match ArchWiki cues:

| Element | Treatment |
|---------|-----------|
| Background | Light gray page (`#f8f9fa`), white article surface |
| Text | Dark readable (`#202122`), system-ui / sans; code in monospace |
| Links | Near-black text + underline (no blue/purple) |
| Headings | Clear hierarchy; underline/border under `h1` |
| TOC | Bordered box, centered “Contents” |
| Note / Tip / Warning | Same neutral gray callout box (labels carry meaning) |
| Nav | Compact list; current page gray left bar; Vector expand chevron |
| Tables | Header `#eaecf0` |
| Color rule | Grayscale only — no accent fills in chrome or diagrams |
| Mermaid | Neutral gray theme |
| Nav | Collapse/expand projects, Solution design, and feature groups (persisted) |
| Chrome | Minimal; no dashboard cards, no purple gradients, no emoji clutter |

## Callout Markdown conventions

Build maps these blockquotes or paragraphs:

```markdown
> **Note** Text of the note.

> **Tip** Optional shortcut.

> **Warning** Destructive or easy-to-get-wrong step.
```

## Readability rules

1. Short sections; one idea per subsection.
2. Prefer numbered procedures for how-tos.
3. Link related pages instead of duplicating.
4. Lead with a plain-language summary under the title.
5. Code/commands in `<pre><code>` with light background.

## Do not

- Card grids, stat strips, or marketing heroes.
- Heavy client frameworks.
- Inline critical CSS duplicates — one `wiki.css`.
- Hide search behind a menu on desktop.
