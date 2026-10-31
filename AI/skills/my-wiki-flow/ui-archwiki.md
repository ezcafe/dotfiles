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
│ ▸ Concepts   │ lead paragraph                           │
│ ▸ Project A  │ ## Section                               │
│   · page     │ body…                                    │
│   · how-to   │ **Note** box                             │
│ ▸ Project B  │ ### Subsection                           │
│              │ Linked from · Source: path.md            │
└──────────────┴──────────────────────────────────────────┘
```

- Left (or collapsible) **nav grouped by project**; **Concepts** is a top-level group when present.
- Within a project: canonical pages flat (Architecture → Topic index → Solution design → Decisions → Glossary); **feature solution designs nest under Solution design**; **how-tos nest under a How-to parent** (optional `nav_group` / `master_feature` subgroups for features).
- Main column: TOC → title → article → backlinks → footer with vault Markdown path.
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
| Note / Tip / Warning | ArchWiki boxes: Note blue, Tip green, Warning amber |
| Nav | Compact list; current page gray left bar; Vector expand chevron |
| Tables | Header `#eaecf0` |
| Color rule | Chrome/diagrams stay grayscale; color only for attention (callouts, search marks) |
| Mermaid | Neutral gray theme |
| Nav | Collapse/expand projects, Solution design, How-to, and feature groups (persisted) |
| Badges | Page kind + optional `entity_type` (how-to / explanation / reference / tutorial) |
| Backlinks | Compact “Linked from” list above footer |
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
3. Link related pages instead of duplicating (prefer inline contextual wikilinks).
4. Lead with a plain-language summary under the title.
5. Code/commands in `<pre><code>` with light background.
6. Footer always shows the vault-relative `.md` path so humans can edit the source.

## Do not

- Card grids, stat strips, or marketing heroes.
- Heavy client frameworks.
- Inline critical CSS duplicates — one `wiki.css`.
- Hide search behind a menu on desktop.
