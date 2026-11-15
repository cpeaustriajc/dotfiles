---
name: commit
description: >
  This skill should be used when the user says "commit", "commit and push", "push it" or "ship it to the branch", or asks to save finished work to git. It makes atomic commits in the repo's style and pushes them; `local` skips the push.
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
