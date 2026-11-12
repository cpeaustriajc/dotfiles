# Painting in code

**SVG**
- One group per depth plane, back to front; movers inserted at their travel depth.
- `mix-blend-mode: multiply` darkens every overlap; blend one group per tint so shapes merge.
- Tile windows, bricks or halftone with a `<pattern>` on one global origin and snap edges to its
  grid, or cells split at every edge.
- Defs live in the document that renders them; a separately rasterised layer doesn't share them.
- Fit text with `textLength` and `lengthAdjust="spacingAndGlyphs"`; glyph-width estimates overflow.
- Labels by a placement pass: obstacle boxes for every item and occluder, several candidate
  positions per anchor, first clear one wins.

**Randomness and iteration**
- Seed every random stream. New elements draw from a new seeded stream, so approved ones don't
  move; never insert calls into an old stream or reorder them.

**Animated and multi-state scenes:** test the in-between frames; shoot movers several times a
fraction of a second apart.

**Raster passes and 3D figures**
- Scene in 2D, posed figures in 3D, one stylisation pass over both. Preview a figure at final
  scale over a cached scene before the full pipeline.
- Render at 2× display size (3200 × 2000 for 1600 × 1000).
- Painted traditions (oil, gouache): `scripts/paintpass.py --help` (`--width 3200` for a 1600 × 1000 page) over the composed PNG for one
  shared brushwork. It unifies; it can't rescue a weak drawing. Flat-vector and graphic styles skip it.
