---
name: cleanup
description: >
  This skill should be used when the user says "cleanup", "clean up after yourself", "tear down
  the dev server", "archive this session" or "clean up stale branches". It removes what a session
  left once safe. Not code tidying.
---

"Clean up" is the go: remove each proven item without asking; ask only in the repo sweep.
Commands: `references/git.md`, `references/shell.md`; harness: `references/claude-desktop.md`
or `references/claude-code.md`. `/cleanup repo`: `references/repo-sweep.md` with
`references/checks.md`.

1. **Inventory** what this session made, per `references/checks.md`. An item you cannot tie to
   this session is Keep: another session may own it.
2. **Prove** each item with a live check from `references/checks.md`, never from memory.
3. **Remove** in the order in `references/checks.md`, processes by PID. Never force a delete.
4. **Keep** each item that failed, with a one-line reason: unpushed commits (count), uncommitted
   edits, an open PR, not this session's.
5. **Report** before archiving: Removed (each with the output that proves it, and size freed),
   Kept, Run yourself (exact commands).
6. **Archive** only on "archive" or "close", as the last call: it ends the session. Kept
   unpushed work blocks it; say so.
