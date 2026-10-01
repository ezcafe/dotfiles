# Clean-minimal checklist

Copy and tick before finishing a UI change:

```
- [ ] Spacing on 8px grid (8/16/24/32/48/64)
- [ ] ≤3 chrome colors (neutrals + one accent); no rainbow gradients
- [ ] Body ≥16px; metadata ≥14px (no text-xs for UI copy)
- [ ] Clear type hierarchy (weight/size, not decoration)
- [ ] Interactive: hover, active, disabled, focus-visible
- [ ] Empty / loading / error / success planned; empty ≠ error
- [ ] Feedback scale matches stakes (inline / toast / banner / modal)
- [ ] Shadows subtle; cards border-only (no border+shadow)
- [ ] Radius: outer 8px / nested 6px; tables sharp OK
- [ ] Touch targets ≥44×44pt / 48dp (`fx-hit-40`); touch manipulation enabled (no tap delay)
- [ ] Mobile inputMode (`decimal`, `numeric`, `email`) applied on fields; inputs ≥16px (no iOS auto-zoom)
- [ ] Safe-area insets respected on mobile (`env(safe-area-inset-*)`)
- [ ] Tablet (`md`/`lg`) and desktop (`xl`) layouts preserved without regression
- [ ] Contrast ≥4.5:1 for text; accent focus rings
- [ ] No transition: all — list properties
- [ ] Light + dark verified (if both exist)
- [ ] Hex only in token sources; feature code uses tokens/primitives
```

## my-apps extras

```
- [ ] Composed from components/ui/*
- [ ] Charts via colorByIndex(resolved, i, style)
- [ ] Layout uses auto-fit / container queries (no content breakpoints)
- [ ] prefers-reduced-motion respected for fx-*
- [ ] Feedback via Field error / Alert / useNotify / Modal; toUserFacingMessage for errors
- [ ] Nested pages: location breadcrumbs from section origin
- [ ] docs/DESIGN_GUIDE.md updated if tokens/primitives or interaction patterns changed
```
