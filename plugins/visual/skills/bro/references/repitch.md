# Re-pitch rules

The rules for each step of SKILL.md, in order.

## Pick the message (step 1)

- If `$ARGUMENTS` holds text, re-pitch that text instead of your last message.
- If your last message was itself a re-pitch, it did not land either. Re-pitch the same original
  again: find the premise the first re-pitch still assumed, and use a different picture.

## What was missing (step 2)

Name to yourself the premises the message took for granted:
- a term it used and never defined;
- a step it skipped, or a cause it never stated;
- a state the user did not see: a file, an error, a test result, a decision from earlier;
- why the message mattered, and what it asked the user to do.

Check each fact against the code or the chat. Read files only.

## The project's words (step 3)

Look in this order: `GLOSSARY.md` (or the one `GLOSSARY-MAP.md` points to), the terms in
`CLAUDE.md` or `AGENTS.md`, then the names in the code. Use each term as the project uses it and
define it at first use. Invent no label for a thing that already has a name.

## Context and point (steps 4 and 5)

- Context: what the thing is and how it worked before, then what went wrong.
- Point: what changed or what is true now, and why.

## One picture (step 6)

Draw the one part easiest to grasp as a picture: how the parts connect, the order of the steps,
or a before and after. Boxes joined by lines: at most six boxes, at most eight words each. A list,
a table or two columns of text is not a picture.

## Sentences (ASD-STE100)

- Full sentences with a subject, a verb and articles. No fragments, note style or arrows in place
  of verbs.
- One idea per sentence: at most 20 words for an instruction, 25 for a description. Active voice,
  present tense, common words.
- Leave out hashes, flags, line numbers and tool names unless the user needs one to act.
