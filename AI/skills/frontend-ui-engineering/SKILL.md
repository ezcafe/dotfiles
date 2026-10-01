---
name: frontend-ui-engineering
description: >-
  Builds accessible, responsive, production-quality UI structure and behavior.
  Use when creating or changing pages and components, layouts, client state,
  loading/empty/error states, or accessibility. Defers visual tokens to
  clean-minimal-ui and audits to web-design-guidelines.
---

# Frontend UI Engineering

Cursor-optimized adaptation of [addyosmani/agent-skills frontend-ui-engineering](https://github.com/addyosmani/agent-skills/tree/main/skills/frontend-ui-engineering). Structure and interaction first; look-and-feel via project design system.

## Project first

1. If `docs/DESIGN_GUIDE.md` or similar exists — **read it and follow it**
2. Visual tokens / clean-minimal look → [clean-minimal-ui](../clean-minimal-ui/SKILL.md)
3. Full UI guideline audit → [web-design-guidelines](../web-design-guidelines/SKILL.md)
4. React/Next perf rules → [vercel-react-best-practices](../vercel-react-best-practices/SKILL.md)

## Boundaries

| Tier | Rule |
|------|------|
| **Always** | Keyboard access for interactive controls. Loading, empty, and error states. Keep skeletons in sync with live layout (zero CLS). Semantic tokens from the project — no random hex in features. |
| **Ask first** | New global state libraries; new design primitives that duplicate `components/ui`. |
| **Never** | Ship purple-gradient “AI aesthetic” against the project system. Use `div` click handlers instead of buttons. Skip empty/error for “we’ll polish later.” |

## Component rules

- **Compose** — small pieces (`Card` + header/body) over mega-config props
- **One job** — presentational list vs container that loads data
- **Colocate** — component + tests + hook + local types when complexity warrants
- **Split** when a file grows past ~200 lines of mixed concerns

## State choice (simplest that works)

| Need | Tool |
|------|------|
| Local UI | `useState` |
| Shared by 2–3 siblings | Lift state |
| Theme / auth / locale | Context |
| Filters / shareable UI | URL search params |
| Remote server data | Project’s data library (Query/SWR/server components) |
| Complex app-wide client | Only if project already uses a store |

Avoid prop drilling past ~3 levels — context or restructure.

## Interaction patterns

- **Loading** — skeletons that mirror layout (order, grid, radii), not spinners for whole pages
- **Empty** — explain + one clear next action; empty ≠ error
- **Error** — human message + retry when safe; match stakes
- **Optimistic UI** — only when rollback is defined

## Accessibility (minimum)

- Real `<button>` / `<a>` for actions; `iconOnly` / `fx-hit-40` (≥44×44) for icon-only
- Labels: visible `<label>` or `aria-label` on icon-only
- Focus moves into dialogs when opened; do not trap focus incorrectly on non-modals
- Do not use color alone for state
- Heading levels in order; one `h1` per page

## Responsive layout

Prefer `repeat(auto-fit, minmax(...))` and container queries over hardcoded breakpoint sprawl. Mobile-first. Test narrow (~320) and wide.

## Anti “AI aesthetic” (short)

Avoid: purple/indigo defaults, oversized padding everywhere, stock card grids with no priority, heavy multi-layer shadows, `rounded-2xl` everywhere, lorem-only content, hero clutter. Use the project palette and spacing scale.

## Checklist

- [ ] Renders without console errors
- [ ] Keyboard path through interactive elements
- [ ] Loading / empty / error handled
- [ ] Skeleton parity with live UI
- [ ] Tokens/primitives from project (or clean-minimal-ui)
- [ ] Light and dark checked when the app supports both
- [ ] Hit targets ≥44×44 for icon-only

## Related

- [clean-minimal-ui](../clean-minimal-ui/SKILL.md)
- [web-design-guidelines](../web-design-guidelines/SKILL.md)
- [vercel-react-best-practices](../vercel-react-best-practices/SKILL.md)
- [performance-optimization](../performance-optimization/SKILL.md)
