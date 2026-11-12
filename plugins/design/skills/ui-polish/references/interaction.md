# Interaction rules

A row names the rule it breaks. Follow Vercel's Web Interface Guidelines
(https://github.com/vercel-labs/web-interface-guidelines), Rauno Freiberg's "Interaction design"
(https://rauno.me/craft/interaction-design), Emil Kowalski's mobile-native skill
(https://github.com/emilkowalski/skill), Apple HIG and WWDC18 "Designing Fluid Interfaces"
(https://developer.apple.com/videos/play/wwdc2018/803/), and WCAG 2.2 (https://www.w3.org/TR/WCAG22/)
for press and release, drag and hover, loading, focus, forms, navigation and accessible text.

Our choices:
- Hit targets are 44x44 CSS px at every viewport, not only on touch. A row a person selects is at
  least 44 tall. Below 24x24 also fails WCAG 2.2 SC 2.5.8 unless an exception applies; name which in
  the row.
- Draw the control at its full target size: no invisible hit area (at a card edge it covers a
  neighbour).
- Destructive actions get a confirmation or an undo window.
- Loading: no spinner under 1s; show after 500ms, keep at least 200ms; over 10s a percent bar and
  Cancel.

Mobile web gotchas:
- `100dvh` for app shells, `100svh` for full-screen heroes, never `100vh`.
- `viewport-fit=cover` wherever `env(safe-area-inset-*)` is used; without it the insets are 0. Add
  `interactive-widget=resizes-content` when inputs sit at the bottom (Android keyboard).
- A `theme-color` meta per colour scheme (`media` attribute); a `color-scheme` meta or property.
- A horizontal carousel sets `touch-action: pan-y`; `touch-action: none` only where the element owns
  every axis.
- `user-select: none`, `-webkit-touch-callout: none` and `-webkit-tap-highlight-color: transparent`
  only on controls (the last only with a visible pressed state), never on content.
- Check on a real phone, not only a narrow desktop window.
