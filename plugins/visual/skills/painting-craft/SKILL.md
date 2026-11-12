---
name: painting-craft
description: >
  This skill should be used whenever a picture is drawn, painted, illustrated or animated in code
  (SVG, canvas, numpy, Blender): scenes, figures, creatures, vehicles, buildings, landscapes. Also
  when reference art is pasted, a picture looks off, flat, floating or out of proportion, or
  costume, armour or vehicle research is needed. It paints to a gallery standard with a screenshot
  review loop. Not for UI icons, charts or diagrams.
---

# Painting craft

Parts fail at 2× zoom while the composition passes. Read first: taste
(`references/taste.md`); `references/recipes.md` for foliage, grass, metal, cloth, faces,
windows, lights or water; `references/code-techniques.md` before coding. Claude Code: look at
fetched references, studies and crops with the Read tool (it shows images); brief research (step 2)
to a subagent on a cheaper model; use the session's scratchpad directory for the review shots. Skip
only inapplicable steps, and say so.

1. **Tradition:** two or three named works, plus one reference per hero element
   (`scripts/refs.py`). An era names a subject, not a style (`references/aesthetic.md`).
2. **Research** canon, history and real sizes, with sources; mark guesses UNVERIFIED
   (`references/armour.md`).
3. **Space and light:** horizon, camera, px per metre per depth plane (`references/scale.md`);
   one light, its colour and fill (recipes, last section).
4. **Masses** and a value plan; screenshot it. A weak thumbnail fails at any detail.
5. **Hero studies** alone at 2×, from their recipe, `references/anatomy.md` and
   `references/render3d.md`, compared with `scripts/compare.py` until no structural gap remains.
6. **Compose** the studies at their depth planes; the rest from recipes, less detailed.
7. **Ground:** contact, shadows, depth order.
8. **Unify:** one light, one medium pass, rendered at 2×.
9. **Review zoomed in:** `references/review.md`.

Commit message: proxies, UNVERIFIED items, review commands.
