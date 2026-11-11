# Output and preview

Steps 4 and 5 of `SKILL.md`. The harness mechanics are in `claude-code.md`.

If nothing survives the gate, say so plainly in Part 1; Parts 2 and 3 still follow.

## Part 1: Opportunities

At most 5–7 proposals for a whole app; fewer for one view, and fewer and subtler for a crisp
dashboard than for a playful consumer app. One row per proposal, ordered by leverage:

| # | Location | Today | Purpose | Frequency | Suggested motion |
| --- | --- | --- | --- | --- | --- |
| 1 | `Toast.tsx:41` | New toasts appear at once | Preventing a jarring change | Occasional | Enter via `@starting-style`: `opacity: 0; translateY(100%)` to settled, `transition: 400ms ease`, exit by the same edge |
| 2 | `Button.tsx:18` | No press feedback | Feedback | Tens a day | `:active { transform: scale(0.97) }`, `transition: transform 160ms ease-out`, subtle enough for its frequency |

- Each "Suggested motion" cell gives exact values: curve, duration, properties. Take curves from
  the project's tokens, else from these: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`,
  `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`, `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`.
- Animate `transform` and `opacity` only.
- Give a reduced-motion version: gentler, not zero.
- Put hover motion behind `@media (hover: hover) and (pointer: fine)`.
- Name each effect with its term from `animation-vocabulary.md` (Scale in, Stagger, Press / Tap
  feedback).

## Part 2: Rejected candidates (required)

2–5 places considered and not proposed, each with the gate question that rejected it:

- `CommandMenu.tsx:12`, command palette open and close. **Rejected: keyboard-initiated, 100+ a
  day.**
- `Chart.tsx:88`, animated line drawing on the analytics graph. **Rejected: data the user is
  reading; decoration hinders.**

This part keeps the output a filter instead of a wishlist.

## Part 3: Verdict

One short paragraph: how much motion the interface needs, whether it is already close, and the
one proposal with the most leverage. End by asking the owner to pick.

## Preview

The owner judges motion by watching it. One inline view holds one card per proposal, in table
order:

- **Stage:** a stand-in copy of the element in plain HTML and CSS that looks like the real one
  (size, colours, radius, text). It plays the motion with the table's exact values on load and on
  a Replay button. The real source stays untouched.
- **Beside the stage:** the number, the glossary term, the location, the purpose and the values
  (property, duration, curve).
- **Pick and Skip** on each card, and one button that sends the choices.

The view is self-contained: no network, no build step. With no inline view, use the fallback in
`claude-code.md`.
