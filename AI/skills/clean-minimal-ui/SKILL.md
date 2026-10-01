---
name: clean-minimal-ui
description: >-
  Apply modern clean-minimal UI: teal accent, Inter, off-white/neutral-dark
  tokens, 8px spacing, hairline cards, subtle motion. Use when designing or
  refactoring UI, building pages/components, styling forms/buttons/cards,
  theming light/dark, or when the user mentions clean-minimal, Quiet Ink
  replacement, teal accent, or modern minimal design.
---

# Clean-minimal UI

Clarity, consistency, professionalism. Every element earns its place.

## Project override

If the repo has [`docs/DESIGN_GUIDE.md`](docs/DESIGN_GUIDE.md) (e.g. **my-apps**):

1. **Read that guide first** — it is the source of truth for tokens, primitives, and IA.
2. Prefer semantic tokens (`bg-accent`, `text-foreground`) over raw hex in feature code.
3. Compose from `components/ui/*`; do not reinvent Button/Card/Input/Modal.
4. Apply the rules below only where the guide is silent.

Elsewhere (greenfield or other apps), implement this skill via CSS variables + primitives as below. Hex belongs in token files only.

## Core rules

| Rule | Do |
|------|-----|
| **Whitespace** | Generous padding/margins; group related UI; 3–7 items per section. Whitespace is functional structure. |
| **One accent** | Grays + **one** accent (default teal `#0D9488`). No purple/rainbow gradients. |
| **8px grid** | Margins/padding/gaps: 8 / 16 / 24 / 32 / 48 / 64 only. |
| **Type** | Max 2 families (Inter + mono). Body ≥16px (avoids mobile viewport zoom); metadata ≥14px; H1 ~32px, `-0.02em`. |
| **Geometry** | Subtly rounded: `--radius-md` 8px outer / `--radius-sm` 6px nested. Organic, modern, friendly. |
| **Cards** | Border **or** shadow — never both. Prefer border-only cards (`border-border`). |
| **Tables** | Sharp corners OK; hairline row dividers; no zebra. Mobile viewports switch to card lists (`@md:hidden`). |
| **Motion** | Short CSS transitions; list properties (`transition-[opacity,transform]`). Never `transition: all`. |
| **Touch & Mobile** | Hit area ≥44×44pt / 48dp floor (`fx-hit-40`). `touch-action: manipulation` for instant taps. Design for thumb reach. |
| **Mobile Inputs** | Explicit `inputMode` (`decimal`, `numeric`, `email`), `enterKeyHint`, quick-pickers over raw text, and safe-area insets. |
| **Layout** | Mobile-first; preserve tablet and desktop UI using `repeat(auto-fit, minmax(...))` + container queries (`@container`). |

## Default palette (token values)

**Light:** bg `#FAFAFA` · surface `#FFFFFF` · muted-surface `#F5F5F5` · text `#1A1A1A` · muted `#6B6B6B` · border `#E5E5E5` · accent `#0D9488` / hover `#0F766E` · destructive `#DC2626`

**Dark:** bg `#171717` · surface `#1A1A1A` · muted-surface `#262626` · text `#FAFAFA` · muted `#A0A0A0` · border `#404040` · accent `#2DD4BF`

**Shape:** radius outer 8px · nested 6px · shadows: light `0 1px 3px rgba(0,0,0,.12), 0 1px 2px rgba(0,0,0,.06)` · medium `0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.05)`

Map to CSS vars (`--background`, `--surface`, `--accent`, …) and consume via utilities. See [tokens.md](tokens.md).

## Component patterns

### Button (primary)

- Default: accent fill, white text, `padding: 12px 24px`, radius 6–8px, light shadow
- Hover: darker accent, slightly stronger shadow, `translateY(-1px)`
- Active: reset translate; Disabled: muted gray, no lift, `cursor: not-allowed`
- One primary CTA per view region; secondary/ghost for the rest

### Card

- White/surface bg, `1px` light border, radius 8px, padding 24px
- Hover: border color only (not a second shadow)
- Use for metrics, charts, entity tiles — not full-page forms or tables

### Form fields

- Label: 14px medium; input: 16px, `padding: 12px 16px`, 1px border
- Focus: 2px accent border + subtle accent glow/ring
- Error: destructive border + message below; hint: muted 14px below
- Validate after blur-with-value and on submit (all errors at once); never while typing; clear when fixed

### Links

- Default: accent, no underline · Hover: underline, slightly darker · Visited: same as default

## Interaction quality

A UI is a conversation: every action needs a visible reaction. Missing feedback reads as broken. Match the **scale** of the response to how often the action happens and how high-stakes it is.

If the repo has `docs/DESIGN_GUIDE.md`, follow its **Feedback**, **Empty & loading**, **Search**, **Page headings & breadcrumbs**, and **Dashboard layout** sections. They map these patterns onto app primitives.

Elsewhere, apply:

| Pattern | Do |
|---------|----|
| **Error** | What happened + why + next step. Inline for fields; banner for blocked pages; toast for failed mutations; modal for destructive confirms. No jargon, humour, or raw stack traces. Clear the error when the value is fixed. Validate on blur-with-value and on submit (all errors at once) — not while typing. |
| **Success** | Name the object (“Transaction added”). Routine → toast or inline; critical → allow a larger pause **and** a next action. Never a full-page party for frequent tasks. |
| **Empty** | Informative + one next action. Empty ≠ error chrome. |
| **Loading** | Feedback in the region that will change; duration-appropriate (skeleton vs progress vs “done” toast). |
| **Search** | Only if the list is long enough. Placeholder names the corpus. Find-in-list, not a nav crutch. Empty hits explained. |
| **Breadcrumbs** | Location in the hierarchy, not click history. Omit on top-level. Origin = section, not Home when chrome already shows the app. Last item is current (not a link). |
| **Dashboard** | Metrics first, then optional chart, then table. Don’t show a viz just because the data exists. Deltas + words, not color alone. |

Control states on every interactive piece: **default, hover, focus-visible, disabled, active**.

## Modern Minimal UI tenets (Diana Malewicz)

1. **Whitespace as layout:** Generous negative space establishes visual hierarchy, reduces cognitive load, and highlights core actions.
2. **Subtly rounded geometry:** Soft concentric rounding (`8px` outer / `6px` nested) creates organic, modern surfaces.
3. **High-contrast accessible typography:** Clear Inter weight scales; body ≥16px (no mobile zoom), metadata ≥14px, tabular numerals.
4. **Restrained color architecture:** Clean neutral surfaces, 1 primary teal accent, muted secondary, and clear semantic alerts.
5. **Hairline structure:** Border-only cards; subtle shadow elevation reserved for popovers and dialog overlays.

## 2026 Mobile UX essentials (UXCam)

- **Thumb Zone ergonomics:** Keep frequent actions and primary CTAs within one-handed thumb reach; reserve corners for navigation.
- **Touch target minimums:** Interactive targets ≥44×44pt / 48dp (`fx-hit-40`) to prevent mis-taps and rage taps.
- **Input friction reduction:** Mobile keyboard hints (`inputMode="decimal"|"numeric"|"email"`), quick-pickers, and autofill.
- **Instant touch feedback:** `touch-action: manipulation` and `fx-press` (`scale(0.98)`) for tactile responsiveness without double-tap delay.
- **Safe-area insets:** Handle edge-to-edge mobile screens via `env(safe-area-inset-*)`.
- **Responsive preservation:** Retain tablet and desktop layouts unchanged while optimizing narrow phone viewports with container queries.

## Anti-patterns

- Purple-blue / rainbow / multi-color gradients
- Text &lt; 14px for UI copy (chart ticks only exception)
- Random spacing off the 8px grid
- Heavy dramatic shadows; glow theater; over-animation
- Mixing filled + outlined button styles randomly
- Hard-coded hex/fonts/radii in feature JSX when a token system exists
- Content layouts driven by 768/1024 breakpoints when auto-fit works
- Generic “Success” / “Error occurred” copy; raw system errors in the UI
- Treating empty as an error; search as a substitute for navigation
- Full-page success for routine, high-frequency actions

## Workflow

When building or refactoring UI:

1. Confirm tokens exist (or add them to the token source file only).
2. Compose primitives; match spacing to 8px grid.
3. Wire hover / active / disabled / focus for every control. Plan empty, loading, error, and success — not only the happy path.
4. Verify **light and dark** if the app has both.
5. Run the checklist in [checklist.md](checklist.md).

## Related

- Full token table + CSS snippets: [tokens.md](tokens.md)
- Pre-ship checklist: [checklist.md](checklist.md)
- Pattern sources: [error](https://www.pencilandpaper.io/articles/ux-pattern-analysis-error-feedback), [success](https://www.pencilandpaper.io/articles/success-ux), [search](https://www.pencilandpaper.io/articles/search-ux), [breadcrumbs](https://www.pencilandpaper.io/articles/breadcrumbs-ux), [dashboards](https://www.pencilandpaper.io/articles/ux-pattern-analysis-data-dashboards), [interaction patterns](https://www.pencilandpaper.io/articles/microinteractions-ux-interaction-patterns)
