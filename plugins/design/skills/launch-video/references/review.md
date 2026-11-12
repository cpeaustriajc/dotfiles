# Review loop

Steps 5 and 9 of `SKILL.md`. The person reviews by watching and listening: make each round small.

- Open every render for them (`quicktime.md`).
- Audition, don't argue: render candidates back to back into one file (`scripts/audition.py`), say
  the order and timestamps, let them pick by ear. Save a liked take in a named file before
  generating more.
- One change per round; say what changed and what did not. A mid-turn note ("the yellow dot jumps")
  is a bug report: measure it in the rendered frames, fix the cause, name it.
- Verify from the MP4, not the source: pull frames at the key moments, track a moving element frame
  by frame for a twitch. A composition snapshot does not prove the encode.

## Before each handover

In every shape:

- Every element appears at its time (a time-shift or re-layout silently drops entrances).
- No text under another element, off canvas, or outside the safe zones (top 10%, bottom 18% of 9:16).
- Alignments measured, not eyeballed.
- One voice, brand and domain pronounced right, every line ends before the next starts.
- Music under the voice; the mix peaks below 0 dB (`music.md` step 3).
- Every claim, on screen or spoken, passes the project's copy rules.
- Files are where the person asked, not only in scratch.
