# The project verify skill and the hand-off

Steps 6 and 8 of `SKILL.md`.

## Verify skill (step 6)

Write a project skill, with frontmatter, in the project's repo. It tells a cold agent:

- when a change touches the covered code;
- the one command to run;
- how to tell a bug from a model error;
- how to update the model for an intended change;
- for a TLA+ check: TLC stops at the first broken rule, so remove it and rerun until none
  breaks, and tell each trace as steps in the code's words.

Record the covered files and functions, the bounds and the sync commit. Move the sync commit
forward only after you confirm the model matches the code there. No placeholders.

## Hand off (step 8)

Report what you verified, the tool and why, the bounds, each finding as steps, the run command,
and what is out of scope. A pass covers the model, not the system.
