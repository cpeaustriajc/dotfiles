# Trail audit

Step 7 of `SKILL.md`. One fresh agent that did none of the work, on the model the adapter names,
gets the log, the plan and the transcript paths of every session the run used. It edits nothing
and flags:

- **Unsupported**: a log row the transcript does not show happening (the change, the check run,
  the keep or revert), or an evidence pointer that does not resolve (no such commit or file).
- **Unlogged**: an action in the transcript the log leaves out: a kept or reverted change, a
  change of approach, an edit to the check or its tests, a skipped step.
- **No artifact**: a "done", "passes" or "fixed" claim, in the log or the transcript, with no
  check output, commit or file behind it.

Each flag is one Attention line: the item, the evidence (log or transcript line, quoted), and what
I must check. The list opens the report as the auditor wrote it. No flags: "Attention: nothing to
check", with no padding and no cap on the count. An audit that could not read a transcript is an
Attention line, not a clean list.

Step 6's reviewer judges the diff against the predicate; this audit judges whether the log tells
what happened.
