# Scale and space

Use typical sizes for buildings, streets and plants; replace with a canon or survey source when one
exists, and say which.

## One scale per depth plane

- Each plane gets a px-per-metre named constant; everything in it is drawn at that scale.
  Touching or adjacent objects share a plane and a scale.
- Anchor to a canon size, derive the rest: a 300 m tower at 4.3 m per floor has 70 floors. The
  window grid matches the floor pitch, or a skyscraper reads as ten storeys.
- A building that grows over time widens too, or it becomes a needle.

## Bridging two scales

An empty middle ground reads as a gap and strands the far plane. Fill it with in-between rows
(each lower and larger toward the viewer), close it with telephoto compression, or put water there.

## Ground and order

- Ground contact sets depth: place by the base, then size for that depth. Painter's algorithm,
  y-sorted by ground contact; check a mover's draw order against each object at both ends of its
  path.
- Moving the horizon, camera or layout moves everything placed against it; re-check labels, props,
  clips and overlaps.
- A rendered figure needs a shadow catcher, or it floats.
- Wrong draw order leaves stray lines, smoothed closed curves overshoot their points: clip to the
  region.
- Roadside trees stand on the verge, in front of the traffic.

## Reflections

A reflection needs a reflective surface; dry ground and grass reflect nothing. On wet asphalt only
bright sources and strong shapes reflect; the rest is sheen.
