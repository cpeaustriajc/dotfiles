---
name: ui-polish
description: >
  This skill should be used when the user asks to review a UI against its design, polish spacing,
  type, colour or motion, or sign off a visual change. It compares the screen with the design and
  gives a Before/After/Why table.
---

# UI polish

Review the UI against its design. Change nothing until I name the rows to fix.

1. Find the design: a mockup, Figma frame, export, my screenshot, an approved plan, else the
   closest screen in the app. The design beats your taste. None: say so, and judge against the
   existing screens and `references/quality-bar.md`.
2. Look at the running UI at its width and at 375px, in light and dark if both exist. Code alone misses what
   renders.
3. Check `references/layout.md` always, plus `references/motion.md` for motion,
   `references/interaction.md` for controls, forms, loading or navigation,
   `references/app-ui.md` for dense app screens, and `references/quality-bar.md` for a design
   or prototype.
4. Report one Before/After/Why table and a verdict per `references/verdict.md`.
5. Fix only the rows I name. "Run until clean" names every row: fix all, then repeat steps 1–4.
   Ask for sign-off once, after a pass with no rows.
