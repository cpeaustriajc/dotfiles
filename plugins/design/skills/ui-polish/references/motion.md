# Motion rules

A row names the rule it breaks. A tradeoff the code or design documents (a comment on a
deliberately slow transition) is mentioned in its row, not flagged.

Principles: Lasseter, "Principles of Traditional Animation Applied to 3D Computer Animation",
SIGGRAPH 1987 (https://doi.org/10.1145/37402.37407); Thomas and Johnston, "The Illusion of Life:
Disney Animation", 1981. Practice: Emil Kowalski's "Great Animations"
(https://emilkowal.ski/ui/great-animations) and his skills `review-animations`,
`animation-performance` and `apple-design` (https://github.com/emilkowalski/skills); Apple WWDC18
"Designing Fluid Interfaces" and WWDC23 "Animate with springs"
(https://developer.apple.com/videos/play/wwdc2023/10158/); Josh Comeau, "An Interactive Guide to CSS
Transitions" (https://www.joshwcomeau.com/animation/css-transitions/); Paco Coursey, "Disable
transitions on theme toggle" (https://paco.me/writing/disable-theme-transitions).

Our choices:
- Fix order: delete the animation, shorten it, fix the easing, fix the origin, make it
  interruptible, then move it to `transform` and `opacity`.
- Default curves when the design says none: ease-out `cubic-bezier(0.23, 1, 0.32, 1)`, ease-in-out
  `cubic-bezier(0.77, 0, 0.175, 1)`, drawers and sheets `cubic-bezier(0.32, 0.72, 0, 1)`. Flag the
  built-in `ease-out` keyword only when the motion feels weak.
- Bounce defaults to 0, may reach about 0.3, never passes 0.4.
- A crossfade that shows both states gets about 2px blur, never near 20px.
- The theme toggle switches instantly, transitions suppressed.
- Check at 2-5x slow motion in DevTools, not at full speed. Read durations and curves from the CSS
  or `document.getAnimations()`, not by eye.
