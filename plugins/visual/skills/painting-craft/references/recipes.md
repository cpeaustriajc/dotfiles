# Recipes for the parts that fail at 2× zoom

A reviewer reads structure at zoom, not colour. Build each hero element as a study at its zoomed
size. Use standard craft for cloth, small faces and hands, glow and lamps, atmosphere and light
direction (one key, written down before shading).

## Foliage and tree crowns

Fails as coin dabs (camouflage), blobs with blob holes (clip art), branches stopping at the crown.
- Seeded branch skeleton (trunk, 3–6 limbs, secondaries); clumps hang on the tips.
- Each clump in three values, underside darker and cooler; inner, lower clumps darker still.
- Noise-displaced silhouette, 2–3 octaves (`feTurbulence` + `feDisplacementMap`); leaf marks past
  the lit edge; branches and irregular sky holes show between clumps.
- Lost edges between same-value clumps, found edges against sky. Mark = leaf cluster.
- Far trees as hedgerows and copses with hidden bases, never lollipops.

## Grass and ground cover

Fails as even strokes of one length and colour, or a flat slab. Value bands first, then tufts of
5–15 blades from one base varied in length and lean, at the plane's scale; a few blades overlap a
resting object's lower edge.

## Polished metal and plate armour

Fails as grey tubes with scribbles, lit like plastic.
- Environment-mapped bands following form (sky, dark horizon band, ground), one specular streak,
  rolled edges, each lame casting onto the plate below, rivets with highlight and shadow.
- Articulated pieces (cop, wings, lames, finger lames) drawn separately, each banded.
- A figure whose pose foreshortens goes to `render3d.md`.

## Mail and other fine repeating texture

- Under about 4 px per ring at zoom, paint mail as value: a mid-dark mass, a lit band, a dark
  overlap edge. Above it, rows that follow the form, highlights on the lit side only.
- Bricks, tiles and window grids too: resolved at viewing zoom or painted as value, never
  half-resolved.

## Windows and lit facades

Night windows sparse and clustered, many dark, whole floors dark; each pane reflects what faces it,
never one stamped diagonal.

## Dark passages

Fails as one muddy value that the paint pass turns to mud. At least two value steps and one
low-contrast structure (bark furrows, clump edges, tufts); coloured shadows; the darkest dark small
and placed.
