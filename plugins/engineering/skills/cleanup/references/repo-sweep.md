# Repo sweep (`/cleanup repo`)

For branches and worktrees from many sessions.

1. List every worktree, local branch, remote branch and PR.
2. Classify each branch and worktree with the checks of step 2 of `SKILL.md`
   (`references/checks.md`), in one table: Remove, Keep (reason) or Ask (no PR and unique
   commits: say what the commits change).
3. Leave alone a worktree a live session uses (the harness adapter lists them), a dirty
   worktree, and a remote branch whose PR someone else authored.
4. Before any delete, save every branch tip to remove in a bundle with a restore script.
5. Show the table and ask once (Claude Code: `AskUserQuestion`): remove all, remove all but Ask
   rows, or pick. Then leave each approved branch if it is checked out, delete it local first
   and remote second, and remove each approved worktree unforced.
6. Report the counts, the bundle path and the Kept rows.

## Commands (git and GitHub)

- Worktrees: `git worktree list --porcelain`.
- PRs: `gh pr list --state all --limit 500 --json number,state,headRefName,headRefOid,author`.
  Use `gh`, not `git branch --merged`: it misses squash merges.
- Unique commits of an Ask row: `git log --oneline origin/main..<branch>`.
- Backup before a delete: `git bundle create .claude/work/cleanup/<date>.bundle <branches>`, and
  a `restore.sh` with one `git branch <name> <sha>` line per branch.
- Leave a checked-out branch: `git switch --detach origin/main`.
- Delete a branch: `git branch -d <branch>` while its remote branch exists, then
  `git push origin --delete <branch>`. If `-d` refuses, put `git branch -D <branch>` under Run
  yourself.
- Remove an approved worktree with `git worktree remove <path>`, never `--force`.
