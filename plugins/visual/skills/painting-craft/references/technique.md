# Technique

**Layers and depth**
- One layer per depth plane, drawn back to front; a mover goes into the layer at its travel depth.
- Multiply-style blending darkens every overlap: blend one layer per tint, so its shapes merge.
- A repeating pattern (windows, bricks, halftone) tiles from one global origin, with edges snapped
  to its grid, or cells split at every edge.
- Text is fitted to its measured box, not to a glyph-width guess. Labels get a placement pass:
  every item and occluder as an obstacle box, several candidate spots per anchor, first clear wins.

**Randomness and iteration**
- Seed every random choice. A new element draws from a new seeded stream, so approved ones stay
  where they are; never add or reorder draws in an old stream.

**Figures that turn toward the viewer:** build them as volumes in perspective (a 3D tool, or
boxes and cylinders drawn in perspective), never as side-view outlines; see `anatomy.md`. Paint
them under the scene's light and inside the same medium pass as the scene.

**Animated and multi-state scenes:** check the in-between frames; capture movers several times a
fraction of a second apart.

**Output**
- Render at 2× display size (3200 × 2000 for 1600 × 1000).
- Painted traditions (oil, gouache) get one shared brushwork pass over the composed picture: the
  same stroke size and direction rules everywhere, figures included. It unifies; it can't rescue a
  weak drawing. Flat-vector and graphic styles skip it.
