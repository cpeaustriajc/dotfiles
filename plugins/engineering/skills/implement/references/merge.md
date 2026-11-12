# Until merged

Read only when `until-merged` is passed. The user has gone; the PR merges without them.
Mechanics: the harness adapter, section "Until merged".

## Grant

`until-merged` lets the run, for this ticket only:

- merge through the repo's auto-merge once the gate below holds;
- force-push its own branch with `--force-with-lease` after a rebase;
- use a test method that the project says to ask about first (browser, simulator, dev server,
  screenshots), when it is the method that proves a criterion. Rules on how to test still hold.

It grants nothing under "Ask". A harness approval prompt still applies.

## Watch

1. Hand CI failures and review comments to the harness's PR watcher. Never poll the PR in a
   loop: each wake re-reads the conversation and spends tokens on a PR that has not changed.
2. A base-branch conflict sends no event; rebase once before turning on auto-merge.
3. Budget: at most 3 fix pushes after the PR opens. Each fix runs only the checks that cover it,
   not a full `review-loop`. A fourth failure goes to Ask.

## Gate

The code host checks required CI and branch protection. Turn on its auto-merge only when these
also hold on the latest commit:

- the proof in the PR covers every changed file;
- each review-bot finding is fixed, or answered on the PR with a reason;
- no human review requests changes.

Never bypass branch protection (`--admin` or the like).

## Ask

Ask with the harness's question tool, never in a plain message: a plain question makes the
thread look finished. Put the PR link, the blocker and the options, recommended first, in it.
Ask only when a criterion cannot be proven, the gate cannot pass, the fix budget is spent, or the
next step deletes data, touches production or changes anything outside the repo. No answer:
leave the PR open and unmerged, and start the report with the question.
