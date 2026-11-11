# Git and GitHub

Commands for the branch, stash and config steps of `SKILL.md`.

## Prove (step 2)

- Branch with a PR: `gh pr view <branch> --json state,headRefOid` is MERGED or CLOSED, and the
  branch tip (`git rev-parse <branch>`) equals `headRefOid`.
- Branch with no PR: `git cherry origin/main <branch>` prints no `+` line.
- Remote branch: the same checks, and the PR `author` is me.
- Config edit: `git diff -- <file>` shows only this session's change.

## Remove (step 3)

1. `git stash drop <sha>` for each own stash, found again by its tag.
2. Restore config edits by path: `git restore -- <file>`.
3. Leave the branch: `git switch --detach origin/main`.
4. Delete the local branch with `git branch -d <branch>` while its remote branch still exists:
   git allows `-d` for a branch merged into its upstream, so a squash merge passes.
5. Then `git push origin --delete <branch>`. If GitHub already deleted the remote branch and
   `-d` refuses, put `git branch -D <branch>` under Run yourself; never force it.
