---
name: cleanup
description: >
  This skill should be used when the user says "cleanup", "clean up after yourself", "tear down
  the dev server", "archive this session" or "clean up stale branches". It removes what a session
  left once safe. Not code tidying.
---

"Clean up" is the go: remove each proven item without asking; ask only in the repo sweep.
Commands: `references/git.md`. `/cleanup repo`: `references/repo-sweep.md` with
`references/checks.md`.

1. **Inventory** what this session made, per `references/checks.md`. After a context summary the
   inventory may miss items: grep the session transcript for background runs, `docker run`,
   `git switch -c` and `git stash push`. An item you cannot tie to
   this session is Keep: another session may own it.
2. **Prove** each item with a live check from `references/checks.md`, never from memory.
3. **Remove** in the order in `references/checks.md`, processes by PID; a background task goes
   through the harness's stop tool, then confirm its PID is gone. Never force a delete: a forced
   delete is how unpushed work gets lost. A destructive git command or a kill of a process this
   session did not start may be blocked: list it under Run yourself.
4. **Keep** each item that failed, with a one-line reason: unpushed commits (count), uncommitted
   edits, an open PR, not this session's.
5. **Report** before archiving: Removed (each with the output that proves it, and size freed),
   Kept, Run yourself (exact commands).
6. **Archive** only on "archive" or "close", as the last call: it ends the session. Kept
   unpushed work blocks it; say so. With a harness archive tool, call it for this session: it
   removes the session's worktree (never `git worktree remove` your own first; one with
   uncommitted changes stays on disk). A linked session that shares the worktree or is idle is
   archived with it; one still working blocks it, so name it under Kept. Without one, end the
   report with the command to remove this worktree from the main checkout under Run yourself:
   removing the shell's own folder breaks the shell.

In the repo sweep, a worktree whose path is the cwd of a live session is Keep; use the harness's
stale-worktree cleanup for worktrees idle 30 days or more instead of `git worktree remove`. A
setting that archives a session when its PR closes leaves processes, containers, stashes and
evidence: still clean up.
