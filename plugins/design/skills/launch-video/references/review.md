# Review loop

Steps 5 and 9 of `SKILL.md`. The person reviews by watching and listening, so make each round
instant and small.

- **Open every render for them**, with the player commands linked from `SKILL.md`.
- **Audition, don't argue.** For a voice, a line read or a music choice, render the candidates
  into one file back to back (`scripts/audition.py`), say the order and the timestamps, and let
  them pick by ear. Save any take they like ("keep take C just in case") in a named file before
  generating more.
- **Change one thing per round**, and say what changed and what did not. A mid-turn note ("the
  dots are off-centre", "the yellow dot jumps a bit") is a bug report: measure it in the rendered
  frames, fix the cause, and name the cause.
- **Verify from the output, not the source.** Pull frames from the MP4 at the moments that
  matter. Track a moving element frame by frame when someone reports a twitch. A snapshot of the
  composition does not prove the encode.

## Before each handover

In every shape:

- Every element that should appear does, at its time (a time-shift or re-layout silently drops
  entrances).
- No text sits under another element, under platform UI (top 10%, bottom 18% of 9:16), or off
  the canvas.
- Lines and dots that should align are measured, not eyeballed.
- The voice is one person, says the brand and domain right, and every line ends before the next
  starts.
- Music sits under the voice; the mix peaks below 0 dB.
- Every claim, on screen or spoken, passes the project's copy rules.
- Files are where the person asked for them, not only in scratch.
