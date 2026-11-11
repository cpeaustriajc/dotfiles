# GitHub and git

- Reverts (step 1): `git log --grep=Revert`.
- PR review comments (step 1): `gh pr list --state all --search "<topic>"`, then
  `gh api repos/{owner}/{repo}/pulls/<n>/comments` and `gh pr view <n> --comments`.
