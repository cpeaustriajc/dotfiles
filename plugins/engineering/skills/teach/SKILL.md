---
name: teach
description: "This skill should be used when the user types /teach with a subject: explain a body of work plainly so a person actually understands it. Runs the `how` and `why` skills and weaves what they find into one clear explanation. Use for 'teach me this', 'help me really understand X', 'explain this change or subsystem to me'."
disable-model-invocation: true
argument-hint: "<subject: subsystem, change, file or question>"
---

Explain `$ARGUMENTS`, what it is, how it works and why, at the person's pace. Change no file.
Adapters: `references/claude-code.md`, `../how/references/claude-code.md`. Detail per step:
`references/teaching.md`.

1. Pick the few things they should leave understanding, from why they ask and what they know.
2. Read the code, then follow `../how/SKILL.md` and `../why/SKILL.md` in parallel. Take their
   findings, not their layout. Keep `why` narrow unless the reasons are the point.
3. Open with a plain definition and its common name, then tie it to this case.
4. Give the smallest complete answer first, one or two sentences, then offer to go deeper or move
   on, and follow their lead.
5. Three or more moving parts: a build-up diagram series. One all-at-once diagram is reference.
6. Keep `why`'s tier words and hedges as written: they are findings.
7. Write through `../../../writing/skills/unslop/SKILL.md`.

Reply with the explanation and the threads worth chasing with `how` or `why`, never a report of
what you did.

## Credit

Adapted from pstack's `teach` by Lauren Tan (MIT; see `LICENSE`).
