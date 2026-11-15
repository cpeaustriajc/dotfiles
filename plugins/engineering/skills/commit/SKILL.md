---
name: commit
description: >
  This skill should be used when the user wants working-tree changes turned into commits: "commit it", "commit this", "lgtm, commit", "commit and push", "push it", "ship it to the branch", "save this to git", or a request to split edits (all, or those in named files or folders) into atomic commits. It often comes right after a fix works or tests pass. It branches if needed, commits in the repo's style and pushes; `local` skips the push. Not for drafting a message only, undo or history rewrites.
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
