# Method

The detail behind steps 1 to 5 of `SKILL.md`.

## Proof levels

Take each fact the change's safety rests on as far down this list as is cheap, and say where it
stopped.

1. You said so. Worthless on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You showed the bad case can't happen: you walked the failure step by step and it doesn't reach.
4. You ran it: a script or test that calls the real code and fails loud if you're wrong.
5. You reproduced it in the running app.

Level 4 is usually one small script that imports the same library the app ships and calls the
exact function you're worried about. Paste its output.

## Read the change (step 1)

The diff, and the symbols it adds, changes and deletes.

## The one fact (step 2)

Most changes that look risky are safe because of a single fact, like "this call only drops
already-dead cache entries and does nothing else". Spend your time here, not on a long list of
maybes.

## Where grep stops (step 3)

- The source of the library you call, at its pinned version, and any local patch.
- When things run: microtasks, unmount and teardown, framework lifecycles (Solid versus React).
- What a symbol search misses: the JSON an API returns, a DB column, a wire format, another
  language reading the same bytes, a feature flag, code three hops downstream.

## Each risk (step 4)

Keep the risks you confirmed; list the ones you checked and cleared separately. A search that
finds nothing is still an answer.
