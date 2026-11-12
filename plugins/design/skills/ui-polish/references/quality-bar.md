# Quality bar

Rules for any web app's designs, prototypes and screens. The project's own design system and
decision records win where they say more.

**Taste references.** Where the design says nothing, compare with shipped products from Cosign's
"High taste companies" list (Apple, Linear, A24, Notion, Stripe, Figma, Ramp, Mercury, Cursor,
Airbnb and others). Name the product and screen; never copy its brand.

**Artboards and pages**
- One artboard is one page in one viewport and one state: `<Page> / <Viewport> / <State>`. Never two
  screens or states in one; an overlay, panel or sign-in step gets its own.
- Each page at 375, 768 and 1440 px, light and dark if the app has both, and each state that
  applies (default, loading, empty, error, offline, signed out/in, long value, minimum data, hover,
  focus, pressed).
- An artboard at rest shows the finished state. Motion starts only on Play, never from a timer.
- A new screen is a proposal: current design beside option A and B. A retired design moves to a
  Deprecated page marked "Do not build from these."
- Copy layout and measurements from the design 1:1; never estimate from a picture of a board.

**Scope**
- Do the request at the smallest scope; never redesign a part it does not name (shared header,
  footer). A treatment the design system does not describe is new: show it as an option first.

**Grid.** One column grid, one gutter, one row gap; 8-point vertical, 4-point inside components. Grid
rows have fixed height; no masonry.

**Layers.** Content people return to or share gets a page with its own address, not an overlay. A
layer shows feedback; a destination is a page. A scrim only behind a modal.

**States.** Hover never carries information. Each state has two cues (WCAG 1.4.1). No heavy
borders or edge rails; no same-hue glow shadows under coloured buttons.

**Components.** Use the project's kit; never hand-draw a button, chip, card or menu. A part the kit
lacks goes into the kit first. Open each menu, select and popover on the board. A ported prototype
keeps its behaviour exactly; changes are a separate option.

**Recording a design decision.** An approved decision gets a case study with these sections:
summary; the problem with measured values and numbered requirements; the first attempt and why it
failed; what the research says (source, what it says, what it means for us); options and the
decision; rejected options with pictures; iteration (what was seen, the cause, the fix); the
decision with approval date, numbered rules and a "Do not" list; what changed; open items; sources
with the date opened. Write the new rule into the design system in the same change. When a later
decision replaces part of it, add a dated "Superseded in part" banner and keep the old text.

**Definition of done**
1. Open each changed artboard or page in a browser; code and style strings are not enough. Screenshots
   are large enough to show the grid guides.
2. Measure, do not eyeball: columns and rows against the guides, each touch target at 44x44 or more
   (`interaction.md`), contrast. A clipped glyph is measured before the font is blamed.
3. Keyboard, focus ring, zoom, forced colours, reduced motion.
4. Hand over: what changed, which artboards, which rules applied, which treatments are new, what was
   not checked.
