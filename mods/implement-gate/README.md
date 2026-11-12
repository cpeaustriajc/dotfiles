# implement-gate

A mod (a plugin that adds a hook to Claude Code) that holds an `/implement` run to the stop point you typed. Claude cannot merge or push past it, and cannot end the run before it.

## Why

An unattended agent that decides how far to go can merge a pull request you wanted to review. It can also stop while CI still runs, and nobody prompts it again.

The `implement` skill takes a stop point word: `commit`, `pr`, `ready` or `merged`. The skill text alone can drift. This mod checks each Bash command and each turn's end against the word.

## Install

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install implement-gate@dotfiles
```

To see that it is on, run `claude plugin list` and look for `implement-gate`. The mod is optional: `engineering` does not install it.

## Example

1. You type `/implement SHOP-42 ready` and leave.
2. Claude opens the pull request and tries to end the turn while CI runs.
3. The hook runs `gh pr view`, sees a running check, and blocks the stop. Claude reads "checks are still running".
4. Claude waits on `gh pr checks --watch`. The checks go green.
5. Claude runs `gh pr merge 7 --squash`. The hook denies it, because `ready` leaves the pull request unmerged.
6. The turn ends. The pull request is open and ready for you.

## What it does

| Event | Case | Decision |
|---|---|---|
| Prompt | You type `/implement` | Saves the last word of the line as the stop point, and shows it in a toast. Any other last word means `pr`. |
| Command | You type `/implement-gate off` | Ends the run: the hooks stop checking. `/implement-gate` alone shows the stop point. |
| Turn end | You interrupt the run | Ends the run. |
| Bash | `gh pr merge --admin`, at any stop point | Deny. |
| Bash | `gh pr merge`, a merge through `gh api`, or `git push` to the default branch, below `merged` | Deny. `gh pr merge --disable-auto` passes. |
| Bash | The words are only text, such as a commit message | Deny too. The text tells Claude to pass the text in a file. |
| MCP | A merge tool such as `merge_pull_request`, below `merged` | Deny. |
| MCP | A push tool such as `push_files`, at `commit` | Deny. |
| Bash | `git push` or `gh pr create`, at `commit` | Deny. |
| Bash | The hook fails | Deny with "could not check". |
| Stop | At `pr`: no pull request is open for the branch | Block. |
| Stop | At `ready`: a draft, a running or failed check, a change request, a conflict, or auto-merge on | Block. |
| Stop | At `merged`: a draft, a failed check, a change request or a conflict, or auto-merge off | Block. |
| Stop | The current branch is the default branch, or HEAD is detached | Pass, and end the run. |
| Stop | The stop point is reached, or the stop point is `commit` | Pass, and end the run. |
| Stop | It blocked 3 times for the same head commit | Pass and write a log line. The Bash and MCP denies stay. |
| Stop | `git` or `gh` fails or takes over 20 seconds | Pass this stop, keep the gate, and write a log line. |

Each block names what is missing and tells Claude to ask with `AskUserQuestion` if it cannot go on alone.

## Settings

No settings. The block limit is `MAX_BLOCKS` in [hooks/register.ts](hooks/register.ts).

To turn the mod off, run `claude plugin disable implement-gate@dotfiles`.

## Limits

- It reads Bash commands as text. A merge from a script file passes.
- It reads the default branch from `origin/HEAD`, else it uses `main` and `master`. A bare `git push` while on the default branch passes.
- It checks the pull request for the current branch only.
- A block re-prompts Claude, which costs a turn. The limit of 3 for each head commit caps that cost. While CI runs, Claude waits in a foreground command, which spends no tokens.
- The gate parts that `gh` cannot see, such as proof for every file, rest on the skill text.

## More

- [hooks/register.ts](hooks/register.ts): the hook source.
- [hooks/register.test.ts](hooks/register.test.ts): the tests.
- [implement](../../plugins/engineering/skills/implement/references/stop-points.md): the stop points the mod holds.
- [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/main/skills): the prior art. Its `full-send` and `full-stop` skills ask the model to stop at merge or at ready; this mod checks it.
