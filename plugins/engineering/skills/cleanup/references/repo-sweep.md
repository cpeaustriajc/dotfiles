# Repo sweep (`/cleanup repo`)

For branches and worktrees from many sessions.

1. List every worktree, local branch, remote branch and PR.
2. Classify each branch and worktree with the checks of `references/checks.md`, in one table:
   Remove, Keep (reason) or Ask (no PR and unique commits: say what the commits change).
3. Leave alone a worktree a live session uses (the harness adapter lists them), a dirty
   worktree, and a remote branch whose PR someone else authored.
4. Before any delete, save every branch tip to remove in a bundle with a restore script.
5. Show the table and ask once (Claude Code: `AskUserQuestion`): remove all, remove all but Ask
   rows, or pick. Then leave each approved branch if it is checked out, delete it local first
   and remote second, and remove each approved worktree unforced.
6. Report the counts, the bundle path and the Kept rows.

- Find merged branches with `gh pr list --state all --limit 500 --json
  number,state,headRefName,headRefOid,author`, not `git branch --merged`: it misses squash merges.
- The bundle goes in `$(git rev-parse --git-common-dir)/cleanup/<date>.bundle`, with a `restore.sh`
  beside it of one `git branch <name> <sha>` line per branch. It must outlive the session, so not
  the scratchpad.
- Never `git worktree remove --force`.
