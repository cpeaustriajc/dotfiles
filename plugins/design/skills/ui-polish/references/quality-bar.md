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
rows have fixed height; no masonry. Measure against the guides, never by eye.

**Layers.** Content people return to or share gets a page with its own address, not an overlay. A
layer shows feedback; a destination is a page. A scrim only behind a modal.

**States.** Hover never carries information. Each state has two cues (WCAG 1.4.1).

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
1. Open each changed artboard or page in a browser; code and style strings are not enough.
2. Light and dark at 375, 768 and 1440 px.
3. Grid guides on; measure against columns and rows.
4. Each touch target 44x44 or more.
5. Open each menu, select and popover.
6. Accessibility: contrast, keyboard, focus ring, zoom, forced colours, reduced motion.
7. Hand over: what changed, which artboards, which rules applied, which treatments are new, what was
   not checked.

**Known failures**
- Several screens or states in one artboard; a larger redesign than asked for.
- Hand-drawn components, or colours and materials the design system does not specify.
- "Done" reported before the board was opened; screenshots too small to show the guides.
- Boards empty at rest because they draw from timers; a prototype port that changed the design.
- A lesson left in a case study and not written into the design system.
- Heavy borders or edge rails; same-hue glow shadows under coloured buttons.
- A clipped glyph blamed on the font before anyone measured it.
