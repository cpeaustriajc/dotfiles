# GitHub adapter

Commands: `gh issue`, `gh pr`, `gh label`, `gh search issues --help`.

- Open PRs with author association: `gh api 'repos/{owner}/{repo}/pulls?state=open&per_page=100'`
  (`author_association`, `user.login`). An outside author is not `OWNER`, `MEMBER` or
  `COLLABORATOR`.
- A bare `#42` can be an issue or a PR: `gh issue view <n> --json url` answers for both; the URL
  says `/pull/` or `/issues/`.
- "A reply after the last triage note": compare the last comment's date with the disclaimer's and
  the reporter's last comment.
- `gh label create` only after the person says yes. Close with `gh issue close <n> --reason "not planned"`.
- Every write notifies the watchers: labels and comment in one pass per item.
