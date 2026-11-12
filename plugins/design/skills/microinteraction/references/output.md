# Output and preview

Steps 4 and 5 of `SKILL.md`. The harness mechanics are in `claude-code.md`.

If nothing survives the gate, say so plainly in Part 1; Parts 2 and 3 still follow.

## Part 1: Opportunities

At most 5-7 proposals for a whole app; fewer for one view, fewer and subtler for a crisp dashboard.
One row per proposal, ordered by leverage:

| # | Location | Today | Purpose | Frequency | Suggested motion |
| --- | --- | --- | --- | --- | --- |
| 1 | `Toast.tsx:41` | New toasts appear at once | Preventing a jarring change | Occasional | Enter via `@starting-style`: `opacity: 0; translateY(100%)` to settled, `transition: 400ms ease`, exit by the same edge |
| 2 | `Button.tsx:18` | No press feedback | Feedback | Tens a day | `:active { transform: scale(0.97) }`, `transition: transform 160ms ease-out`, subtle enough for its frequency |

- "Suggested motion" gives exact values (curve, duration, properties). Curves from the project's
  tokens, else Emil Kowalski's (`--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`).
- Transform and opacity only; a gentler (not zero) reduced-motion version; hover motion behind
  `@media (hover: hover) and (pointer: fine)`.
- Name each effect with its animation-vocabulary term.

## Part 2: Rejected candidates (required)

2-5 places considered and not proposed, each with the gate question that rejected it:

- `CommandMenu.tsx:12`, command palette open and close. **Rejected: keyboard-initiated, 100+ a day.**
- `Chart.tsx:88`, line drawing on the analytics graph. **Rejected: data the user is reading.**

## Part 3: Verdict

One short paragraph: how much motion the interface needs, whether it is already close, the one
proposal with most leverage. End by asking the owner to pick.

## Preview

One inline view, one card per proposal, in table order:

- **Stage:** a stand-in copy of the element in plain HTML and CSS (size, colours, radius, text)
  playing the table's exact values on load and on Replay. The real source stays untouched.
- **Beside the stage:** number, term, location, purpose, values (property, duration, curve).
- **Pick and Skip** per card, and one button that sends the choices.

Self-contained: no network, no build step. Without an inline view, use the fallback in
`claude-code.md`.
