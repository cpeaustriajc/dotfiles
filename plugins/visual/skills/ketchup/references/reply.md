# Reply rules

The rules for each step of SKILL.md, in order.

## Contents
- Voice
- Gather (step 1)
- Action items (steps 2 and 6)
- Summary (step 5)
- Visuals (step 4)
- Choices (step 7)

## Voice

- Say what changed for the user, not how: "the tests pass", not "CI is green".
- Leave out hashes, paths, commands, build numbers and test counts unless the user needs one to
  act. Name each PR, branch or agent as the user knows it.
- A fact that needs missing context gets the context or goes.

## Gather (step 1)

- Change no code, start nothing, post nothing.
- Say so when you correct a number.

## Action items (steps 2 and 6)

- An action item is a call only the user can make: a product choice, an approval, an irreversible
  action, access you lack. Include ones raised before their last message.
- Work you can still do is not one. Invent none to fill the reply.
- An unasked step the work does not need counts only if it is irreversible and waiting on the
  user: one line, no visual, no "what happens if you do not answer".
- List them as plain bullets, never a diagram or box, two lines each: the call the user owns
  (merge, approve, pick) with your recommendation and why, including any step you would take
  first, what must happen first and what cannot be undone; then what happens with no answer.
- Write "unknown" for a part you do not know. Link to the detail.

## Summary (step 5)

- One bullet per thing the user asked for: what came of it, and done, running, failed or not
  checked. Write it as spoken: "Search was slow from a missing index", not "Search review: done"
  or "Slow search: missing index".
- Name any bug found and fixed on the way. Each line stays true read alone.
- Never mark done what still waits on the user; leave out what the action items say.
- Then at most three short lines that change what the user knows or must do, and one line of work
  left that you can do yourself.
- Leave out work that changed nothing for the user.

## Visuals (step 4)

- A visual is a screenshot, a video, a Mermaid diagram, an inline chart or diagram, or a generated
  image. A Markdown table is not one, even with before and after columns.
- Draw what is easier to grasp as a picture: how a design or system works, a PR stack or
  dependency chain with each PR's state, a before and after of a fix, options side by side. A
  status list, or boxes with nothing connecting them, is not worth drawing.
- At most six boxes, at most eight words each, labelled in words a person would say, not tags
  like "Tests: pass". A fact that needs a sentence goes in the text, or nowhere.
- Embed screenshots and videos inline when the change is visible. A visible change with none
  gets "No screenshot yet," on its summary line, with what changed on screen.
- A diagram shows how things connect; a chart shows numbers. Draw only from facts you have: never
  invent a number or draw a screen you did not capture. Link only artifacts that exist.

## Choices (step 7)

- Give every option the work weighed, each with what it gets the user and what it costs. Keep
  them out of the rest of the reply.
- If screenshots above already show the options, write each one's gain and cost under its
  screenshot. Otherwise compare the options side by side, with the current state when there is
  one.
