---
name: bro
description: "This skill should be used when the user types /bro. Stop. That last message did not land: re-pitch it. Restate the last message in plain human language, with no jargon, the context the user was missing first, and one picture."
disable-model-invocation: true
argument-hint: "[the text to re-pitch, if it is not your last message]"
---

# Bro

Wait, I don't understand where you've got to here. Re-pitch that: give me a little bit of context,
talk in ASD-STE100 Simplified Technical English, and use the ubiquitous language from
`GLOSSARY.md` (follow `GLOSSARY-MAP.md` to the right one if the repo has more than one).

Aim simpler, not shorter: something was missing, and a shorter message hides it more. Each
step's rules: `references/repitch.md`. Harness: `references/claude-code.md`.

1. **Pick the message:** your last before `/bro`, or `$ARGUMENTS`. A repeat `/bro` takes a new
   angle and a new picture.
2. **Name what was missing,** checking each fact read-only.
3. **Take the project's words.**
4. **Context first,** in two to four sentences.
5. **The point:** what is true now, and why.
6. **One picture** of boxes joined by lines.
7. **The ask:** the original's question in one sentence, with your recommendation. No new asks
   or findings.

Every re-pitch is as full as the first.

## Credit

Follows Matt Pocock's `wait-what` (MIT; see `LICENSE-wait-what`), whose words open this skill. Also
adapted from pstack's `bro` by Lauren Tan (MIT; see `LICENSE`), without its ask for shorter output.
