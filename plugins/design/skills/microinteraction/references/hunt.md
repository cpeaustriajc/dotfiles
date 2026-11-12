# Where to hunt

Step 2 of `SKILL.md`. Sweep these seams, with recipes from Emil Kowalski's skills
(https://github.com/emilkowalski/skill); take values from the project's tokens first.

- Feedback gaps: pressables with no `:active`; destructive plain clicks (hold-to-confirm).
- Teleporting state: conditional renders, route content, accordions that snap, list adds and
  removes (CSS transitions, not keyframes, so rapid triggers retarget).
- Missing spatial story: popovers with no link to their trigger; toasts and sheets that exit
  differently from how they entered.
- Group entrances on an occasional page (a short stagger, never blocking input).
- Gesture seams: draggable or swipeable elements that snap with no physics.
- The delight budget: first run, empty state, success, celebration rendered flat.

Searches: `{isOpen &&`, `display: none` toggles, `onClick` with no `:active` or transition, `details`
and accordion markup, drag handlers, `.map(` renders of entering lists, empty-state and success
components.
