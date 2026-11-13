# Stop points

The word after the ticket sets how far one run goes. Each includes the ones before it. The user
has gone, so reaching the stop point is the end; a turn that ends sooner ends the run.

| Word | The run ends when |
|---|---|
| `commit` | review-loop passes on local commits; nothing is pushed |
| `pr` (default) | the PR is open |
| `ready` | the gate below passes; the PR stays open and unmerged |
| `merged` | the gate passes and the code host's auto-merge is on, or the PR merged |

## Grant

`ready` and `merged` let the run, for this ticket only:

- force-push its own branch with `--force-with-lease` after a rebase;
- use a test method that the project says to ask about first (browser, simulator, dev server,
  screenshots), when it is the method that proves a criterion. Rules on how to test still hold;
- with `merged` only, turn on the code host's auto-merge once the gate passes, with the merge
  method of the repo's recent merged PRs. If the repo does not allow auto-merge, go to Ask.

`ready` turns off auto-merge that is already on, so the PR stays unmerged. Neither grants anything under "Ask". A harness
approval prompt still applies.

## Watch

1. Hand CI failures and review comments to the harness's PR watcher. Never poll the PR in a
   loop: each wake re-reads the conversation and spends tokens on a PR that has not changed.
2. A base-branch conflict sends no event; rebase once the checks are green.
3. While checks run at `ready`, wait in the foreground until they finish: a turn that ends while
   CI runs ends the run.
4. Budget: at most 3 fix pushes after the PR opens. Each fix runs only the checks that cover it,
   not a full `review-loop`. A fourth failure goes to Ask.

## Gate

The code host checks required CI and branch protection. The gate also needs, on the latest commit:

- the proof in the PR covers every changed file;
- each review-bot finding is fixed, or answered on the PR with a reason;
- no human review requests changes, and the PR is not a draft.

Never bypass branch protection (`--admin` or the like): the gate rests on it.

## Ask

Ask with the harness's question tool, never in a plain message: a plain question makes the
thread look finished. Put the PR link, the blocker and the options, recommended first, in it.
Ask only when a criterion cannot be proven, the gate cannot pass, the fix budget is spent, or the
next step deletes data, touches production or changes anything outside the repo. No answer:
leave the PR open and unmerged, and start the report with the question.

## Report

Add the stop point reached, the final head and, for `merged`, the merge commit or the auto-merge
state.
