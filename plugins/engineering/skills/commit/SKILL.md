---
name: commit
description: Trigger when the user says along the lines of 'commit'
argument-hint: "[local]"
disable-model-invocation: true
---

Arguments: `$ARGUMENTS`. `local` skips the push.

1. Read the status, the full uncommitted diff and the last 10 subjects; match their style.
2. Make atomic commits. Stage by path; leave out `.env`, credentials and ignored files.
   Add no AI attribution or co-author trailers.
3. On the default branch: branch first, by the project's rule, else the tracker's branch name
   for the issue, else a short topic. Add no prefix: the harness and the tracker set their own.
4. Push and set the upstream, unless `local`. If the remote moved, rebase only when it applies
   cleanly; on a conflict, stop and tell me.

Report each commit as `<sha> <subject>`, the branch, and whether it was pushed.
