---
name: commit
description: >
  Use this skill whenever the user wants their working-tree changes turned into commits: "commit it", "commit this", "lgtm, commit", "commit and push", "push it", "ship it to the branch", "save this to git", or a request to split edits (all of them, or those in named files or folders) into atomic commits. It often comes right after a fix works, tests pass or a review is approved. It branches off the default branch if needed, writes atomic commits in the repo's style, and pushes them; the `local` argument skips the push. Do not use it to only draft a commit message the user will commit themselves, to explain hook failures, to set up hooks, or to undo, cherry-pick or rewrite commits or history.
argument-hint: "[local]"
---

Arguments: the text after the skill name (`$ARGUMENTS` where the harness fills it in). `local` skips the push.

1. On the default branch: branch first, by the project's rule, else the tracker's branch name
   for the issue, else a short topic. Add no prefix: the harness and the tracker set their own.
2. Make atomic commits of the uncommitted changes.
3. Push and set the upstream, unless `local`. If the remote moved, rebase only when it applies
   cleanly; on a conflict, stop and tell me.

Report the output of `git log --oneline --no-decorate <first new commit>~1..HEAD` and
`git status -sb`.
