---
name: commit
description: >
  This skill should be used when the user asks to commit their work: "commit", "commit and push",
  "make commits in the repo's style" or "split these changes into commits". It commits the
  uncommitted changes in small logical slices with messages in the repo's style, then pushes the
  current branch ("local" skips the push). The terminal version of the desktop Commit and push
  button. Not for PR bodies or reviews.
disable-model-invocation: true
argument-hint: "[local]"
---

Arguments: `$ARGUMENTS`. `local` skips the push. Commands: `references/git.md`.

1. Read the status, the full uncommitted diff and the last 10 subjects; match their style.
2. Commit one concern per commit. Stage by path; leave out `.env`, credentials and ignored files.
   Add no AI attribution or co-author trailers.
3. On the default branch: branch first, by the project's rule, else the tracker's branch name
   for the issue, else a short topic. Add no prefix: the harness and the tracker set their own.
4. Push and set the upstream, unless `local`. If the remote moved, rebase only when it applies
   cleanly; on a conflict, stop and tell me.

Report each commit as `<sha> <subject>`, the branch, and whether it was pushed.
