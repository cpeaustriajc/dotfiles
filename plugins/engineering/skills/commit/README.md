# commit

A skill that commits your uncommitted changes as atomic commits, in the repo's message style, then pushes the branch. It is the terminal version of the desktop Commit and push button.

## When to use it

Type `/commit` when you want your work saved as clean commits. The skill sets `disable-model-invocation`, so it runs only when you type the command. Claude never starts it alone.

To open a pull request, use `create-pr`. To review changes, use `review-loop`.

## Example

You type: `/commit`

1. Claude reads the diff and the recent commit messages, as Claude Code does for any commit.
2. Claude splits the changes into one commit for each concern.
3. Claude pushes the current branch.

You get the `git log --oneline` lines of the new commits and the `git status -sb` line, which shows the branch and whether it is pushed. Type `/commit local` to skip the push.

## Install

The `engineering` plugin ships this skill. Add the marketplace, then install the plugin:

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install engineering@dotfiles
```

To turn the plugin off, run `claude plugin disable engineering@dotfiles`. This also turns off every other skill in `engineering`.

## What it does

- Staging and secrets follow Claude Code's own commit rules: it stages by path and leaves out `.env` and credentials.
- AI attribution follows Claude Code's `attribution` setting.
- If you are on the default branch, it creates a branch first. The name follows the project's rule, else the tracker's branch name for the issue, else a short topic.
- It pushes with `-u`, unless you pass `local`.
- If the remote moved and the push fails, it pulls with rebase only when the rebase applies cleanly.

## Limits

- On any rebase conflict, it stops and tells you. It does not resolve the conflict.
- It does not open a pull request or write a PR body.
- It does not review the code it commits.
- It has no settings. The only argument is `local`.

## More

- [SKILL.md](SKILL.md): the method Claude follows.
