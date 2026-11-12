# review-loop

A skill that runs verify, code review and simplify on your change in rounds. It stops when a round changes no code.

## When to use it

Use it after a build or a fix, before you mark the PR ready. Claude also loads it when you say "run the review loop" or "is this ready for review".

To open the PR, use `create-pr`.

## Example

You say: "run the review loop".

1. Claude runs the project's verify skill for the issue.
2. Claude runs a code review with the issue and the project's users as the purpose.
3. Claude fixes each finding that a user would hit, then runs a simplify pass.
4. If any step changed code, Claude runs one more round.

You get the verify lines, the review result and each finding that is not fixed.

## Install

The `engineering` plugin ships this skill. Add the marketplace, then install the plugin:

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install engineering@dotfiles
```

To turn the plugin off, run `claude plugin disable engineering@dotfiles`. This also turns off every other skill in `engineering`.

## What it does

- It reads the project's verify skill, the issue and the project's code review rule.
- It changes code in your working tree: the review fixes and the simplify fixes.
- It asks you nothing during the rounds.
- The thread that built the change runs it, because that thread knows the purpose.

## Limits

- It does not commit, push or open a PR.
- If the project has no verify skill, the verify step is blocked and the report says so.
- It has no settings and no arguments.

## More

- [SKILL.md](SKILL.md): the method Claude follows.
- [references/claude-code.md](references/claude-code.md): the commands for each step in Claude Code.

### Sources and evidence

- Source: the `review-loop` project skill in one product repo, commit `9b0998330`. It gives no measured result.
