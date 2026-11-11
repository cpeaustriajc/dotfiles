# Between rounds and the final report

Steps 3 and 4 of `SKILL.md`. The main session does this; hunters do not.

## Between rounds (step 3)

- **Coverage**: every shard file has a line in the reply. A missing file goes into the next
  round. Keep a count: files read over files in scope, as a percent.
- **Verify** each fix yourself: read the diff, run the new test. A diff that fails your review
  twice goes back with a hunter one model tier up.
- **Route** each out-of-shard bug to the hunter that owns that file next round.
- **Ledger** in the ignored work folder: each bug as verified-fixed, unproven, or rejected with
  one line why.
- **Prevention**: for each verified bug, one proposal (a lint rule, test, hook or instruction
  change) in the strongest layer that can hold it, as in `hone`. A proposed lint or test must
  fail on the original bug code first; show that failure in the proposal.
- **Suite**: run the full test suite. A red suite is the next round's first bug.
- **Commit** each verified fix as its own atomic commit, if the project lets you commit.

## Report (step 4)

Run the full suite as the project's verify skill says. Then report:

- coverage percent and rounds run;
- **verified bugs**, fixed, each with its commit and test;
- **unproven bugs**, kept apart from the verified ones, with why no failing test exists;
- **rejected findings**, one line each, so I can override;
- **Prevention**, one group: the proposal for each verified bug, with its failing check;
- the exact E2E command and where its trace or report is;
- where the ledger and every hunter reply are in the work folder.
