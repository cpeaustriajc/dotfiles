# Where to hunt

Step 2 of `SKILL.md`. Each seam is a known class of real opportunity, with a starting recipe.

**Feedback gaps**
- A pressable element with no `:active` state: `transform: scale(0.97)` with
  `transition: transform 160ms ease-out` (subtle range 0.95–0.98).
- A destructive action on a plain click, where a hold-to-confirm fill would prevent slips: a
  `clip-path: inset(0 100% 0 0)` overlay, 2s linear while pressed, 200ms ease-out snap-back on
  release.

**Teleporting state**
- Content that swaps, appears or vanishes at once (conditional renders, route content, expanding
  sections): enter from `scale(0.95–0.97)` with `opacity: 0`, `ease-out`, never from `scale(0)`;
  `@starting-style` for entry without JS.
- An accordion or collapse that snaps open: a height and opacity transition.
- List items added or removed with no bridge, on a list that is not high-frequency: enter and
  exit transitions. Use CSS transitions, not keyframes, so rapid triggers retarget smoothly.

**Missing spatial story**
- A panel, popover or menu with no link to its trigger: scale in with `transform-origin` at the
  trigger (Base UI: `var(--transform-origin)`). Modals stay centred.
- A dismissable surface (toast, sheet) that exits differently from how it entered: symmetric
  paths, with percentages such as `translateY(100%)` instead of fixed pixels.

**Group entrances**
- A grid or list on an occasional page that pops in all at once: a 30–80ms stagger. It is
  decorative and never blocks input.

**Gesture seams**
- A draggable or swipeable element that snaps with no physics: a spring
  (`{ type: "spring", duration: 0.5, bounce: 0.2 }`, bounce 0.1–0.3), dismissal by velocity
  (`Math.abs(distance) / elapsedMs > ~0.11`), and rubber-banding at the edges instead of a hard
  stop.

**The delight budget**
- A rare, high-emotion moment rendered flat: first run, empty state, success, celebration. Only
  here are bounce, a generous stagger or a longer beat welcome.

## Searches

Conditional renders with no transition (`{isOpen &&`, `display: none` toggles), `onClick` on
elements with no `:active` or transition style, `details` and accordion markup, drag handlers,
`.map(` renders of entering lists, empty-state and success components.
