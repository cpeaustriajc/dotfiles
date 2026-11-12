# Method

Adapted from pstack's `blast-radius` (Lauren Tan, MIT; see `LICENSE`). Take from it: the one fact a
change is safe because of, proven by running real code.

## Proof levels

Take each fact the change's safety rests on as far down this list as is cheap, and say where it
stopped.

1. You said so. Worthless on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You showed the bad case can't happen: you walked the failure step by step and it doesn't reach.
4. You ran it: a script or test that calls the real code and fails loud if you're wrong.
5. You reproduced it in the running app.

Level 4 is usually one small script that imports the library the app ships and calls the exact
function you're worried about. Paste its output.

Keep the risks you confirmed; list the ones you checked and cleared separately. A search that
finds nothing is still an answer.
