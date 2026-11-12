# Git and GitHub

- Branch with a PR: `gh pr view <branch> --json state,headRefOid` is MERGED or CLOSED and
  `git rev-parse <branch>` equals `headRefOid`. With no PR: `git cherry origin/main <branch>`
  prints no `+` line. A remote branch also needs the PR `author` to be me.
- Leave the branch with `git switch --detach origin/main`.
- Delete the local branch with `git branch -d` while its remote branch still exists: git allows
  `-d` for a branch merged into its upstream, so a squash merge passes. Then
  `git push origin --delete <branch>`. If GitHub already deleted the remote branch and `-d`
  refuses, put `git branch -D <branch>` under Run yourself; never force it.
