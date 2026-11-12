# Claude Code

## Inline view

- Call `mcp__visualize__read_me` once with `modules: ["interactive"]`, then
  `mcp__visualize__show_widget` with one HTML view that holds every card.
- Each card is a row: stage left, text right (stacked on a narrow screen).
- The stage's motion is plain CSS (a class-toggled transition; `@keyframes` only when the suggestion
  is itself a keyframe loop). Replay removes the class, forces a reflow (`el.offsetWidth`), re-adds
  it. It also plays once on load.
- Pick and Skip are a toggle per card; nothing is chosen at the start. One Send button calls
  `sendPrompt("Pick 1, 3. Skip 2.")`; an unchosen card counts as Skip.
- After the view, end the turn. The owner's reply is the pick.

## Without the inline view

In a terminal or headless run, print the three Parts as text, then end with: "Reply with the
numbers to pick, for example Pick 1, 3. The rest are skipped." Nobody answering is not a pick.

## Files

The inline view is the only output. Never `Edit` or `Write` the project in this command.
