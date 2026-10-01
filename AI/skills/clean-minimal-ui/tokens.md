# Clean-minimal tokens

Use these when creating or updating a design-token file. Do **not** paste hex into feature components.

## CSS variables (example)

```css
:root {
  --radius: 0.5rem;
  --radius-inner: 0.375rem;
  --shadow-sm: 0 1px 3px rgb(0 0 0 / 0.12), 0 1px 2px rgb(0 0 0 / 0.06);
  --shadow-md: 0 4px 6px rgb(0 0 0 / 0.07), 0 2px 4px rgb(0 0 0 / 0.05);
  --space-step: 0.5rem;

  --background: #fafafa;
  --foreground: #1a1a1a;
  --muted: #6b6b6b;
  --surface: #ffffff;
  --border: #e5e5e5;
  --muted-surface: #f5f5f5;

  --accent: #0d9488;
  --accent-hover: #0f766e;
  --accent-foreground: #ffffff;
  --ring: #0d9488;

  --secondary: #f5f5f5;
  --secondary-hover: #ebebeb;
  --secondary-foreground: #2d2d2d;

  --destructive: #dc2626;
  --destructive-foreground: #ffffff;
}

.dark {
  --background: #171717;
  --foreground: #fafafa;
  --muted: #a0a0a0;
  --surface: #1a1a1a;
  --border: #404040;
  --muted-surface: #262626;

  --accent: #2dd4bf;
  --accent-hover: #5eead4;
  --accent-foreground: #171717;
  --ring: #2dd4bf;

  --secondary: #262626;
  --secondary-hover: #333333;
  --secondary-foreground: #fafafa;

  --destructive: #f87171;
  --destructive-foreground: #171717;
}
```

## Typography

- UI + headings: Inter (400 / 500 / 600 / 700)
- Code: IBM Plex Mono or `ui-monospace`
- Body: `1rem` / `line-height: 1.5`
- H1: ~32px, `letter-spacing: -0.02em`
- Metadata: `0.875rem` (14px) minimum for UI chrome

## Chart series (restrained)

Teal + gray + semantic amber/red only. Example light series:

`#0d9488`, `#0f766e`, `#f59e0b`, `#059669`, `#737373`, `#dc2626`, `#a0a0a0`, `#2d2d2d`

No violet / cyan / sky chrome series.

## Spacing map

| px | Common Tailwind |
|----|-----------------|
| 8  | `p-2` `gap-2` |
| 16 | `p-4` `gap-4` |
| 24 | `p-6` `gap-6` |
| 32 | `p-8` `gap-8` |
| 48 | `p-12` `gap-12` |
| 64 | `p-16` `gap-16` |

## my-apps mapping

| Role | Utility / token |
|------|-----------------|
| Page bg | `bg-background` |
| Card | `bg-surface border-border` (no shadow) |
| Text | `text-foreground` / `text-muted` |
| CTA | `bg-accent text-accent-foreground` |
| Focus | `ring-ring` |
| Outer radius | `rounded-[var(--radius-md)]` |
| Nested radius | `rounded-[var(--radius-sm)]` |
| Modal/popover elevation | `shadow-[var(--shadow-md)]` |
| Hit target floor | `fx-hit-40` (≥44×44pt / 48dp) |
| Mobile safe area | `.safe-bottom`, `.safe-top`, `.safe-area-pad` |
| Instant touch | `touch-action: manipulation;`, `.fx-press` |
