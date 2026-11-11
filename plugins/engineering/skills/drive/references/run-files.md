# Run files

The exit check (step 2 of `SKILL.md`), the baseline (step 3), the state each pass reads (step 4),
the brake (step 5), the reviewer (step 6) and the report (step 8).

## Exit check

Show it to me before the first pass. A ticket's checks and You see lines are its end state.

```markdown
End state: <the end state, as the check's own output: "pnpm test cart passes, 0 failing">
Check: <the exact command, and where its output goes>
Holds throughout: <what must stay true: files not to touch, the regression suite green>
Floor: <at least N passes, so an early lucky win can't end the run> (metric runs only)
Budget: <passes, hours or spend; whichever comes first ends the run>
```

## Baseline

Freezing covers the check, the tests it relies on and the data they read. Record the failing output, or a metric as the median of several runs. A check that passes too
easily is suspected before the code is. A check found broken is fixed in its own change, outside
the loop, with my say-so.

## State on disk

A pass starts from these files, not from memory, so a full context loses nothing.

- **Plan**: the units still to try. A pass changes only an item's status; it never deletes or
  rewrites items. A stale plan is regenerated once, as a logged pass.
- **Log**: one row per pass in a gitignored `drive.tsv`: time, hypothesis, change, check before,
  check after, kept or reverted, and a pointer to the evidence (commit, output file), not prose.
  Side discoveries (an unrelated bug, a helpful refactor) go here as notes for me, not into the run.
- **Resume note**: when the run pauses, the next pass, what is uncommitted, how to restart, and
  the transcript path of every session the run has used. Commit or revert before you pause.

Each pass reads the plan, the log's last rows and the history first, and skips what was tried.
A better pass is committed with its log row. A pass that does not improve the check is reverted in full; nothing is kept because it "might
help".

## Brake

- **Stuck**: several reverted passes in a row, or several with no change in the check. Change the
  kind of hypothesis once, or combine near misses; still stuck, stop and say so.
- **Out of budget**: stop, even mid-plan.
- **Dead end**: the end state needs a Holds throughout line broken. Stop and bring me the
  conflict; don't trade one for the other.
- **Not a stop**: a slow but real gain while cheap untried hypotheses remain.

A stop is a report, not a failure.

## Reviewer

For a run that matters, a fresh agent or a different model, given the predicate, the diff and the log, confirms done
before I'm told. Inconclusive is no pass.

## Report

Nothing above the Attention list but a title line: no greeting, summary or verdict. Then:

- The predicate's state, with the check's last output.
- Passes kept and reverted, and the budget used.
- Why it stopped: met, stuck, budget or dead end.
- What needs me: side discoveries, a predicate that looked wrong, anything skipped.
- The path to the log.
