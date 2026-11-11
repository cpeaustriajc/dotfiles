# Agree

Step 3 of `SKILL.md`. Always stop here, before any code is written.

Show the two candidates side by side, each in these sections, in this order:

1. **Usage**: the caller's usage first, as in the rationale's "Usage (caller's view)".
2. **Public surface**: the types and signatures a caller sees.
3. **Internals**: what the surface hides, with `not implemented` bodies and pseudocode.
4. **Red flags**: each flag from `design-red-flags.md` the candidate trips, or "none", one line
   each.
5. **Tradeoff**: one sentence, "We accept X for Y.", with no second sentence.

Add one line under each that names the model that wrote it. If both runners returned the same
shape, show both and say they converged. Recommend one, with one line why. Then end the turn and
wait for the owner: `Pick A`, `Pick B`, or `Push back on A|B: <reason>`. Where no inline view is
available, print the same sections as text blocks, candidate A then candidate B, and still wait.

A logic re-architecture, which reshapes code that exists today, shows **Today** above the two
candidates: today's public surface as excerpts with file and line, and each red flag it trips,
marked at the line that trips it, or "none". A new design skips Today. A layout task shows the
sections in `layout.md` instead.
