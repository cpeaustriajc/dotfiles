# Stacked PRs

Read this when the work's issue has a blocker whose PR is still open. Step 2 of `SKILL.md` says
when.

Build items of one project ship as one stack in blocked-by order. Branch off the blocker's
branch, and open the PR against it; an item with no open blocker branches off the trunk. A stack
of parallel branches off the trunk costs a restack later: every PR rebases and loses its verify
verdict. The PR base is the record every tool shares, so a fresh session finds the base there.
Land the stack bottom first. A builder rebases only its own branch; the coordinator restacks
after a merge, bottom up.

Use the tool the project already uses; with none, plain git and the PR base. Check each command
with `--help` before its first use in a project: these tools change often.

| Step | Plain git + `gh` | `gh stack` | Graphite (`gt`) | git-town |
|---|---|---|---|---|
| Start the bottom item | `git switch -c <branch> <trunk>` | `gh stack init <branch>` | `gt create <branch>` on the trunk | `git town hack <branch>` |
| Start the next item on the one below | `git switch -c <branch> <base>` | `gh stack add <branch>` from the top branch | `gt create <branch>` from the top branch | `git town append <branch>` from the top branch |
| Open the PRs | `gh pr create --base <base>` per item | `gh stack submit` | `gt submit --stack` | `git town propose --stack` |
| After the bottom PR merges | `git rebase --onto <trunk> <old base> <branch>`, then `gh pr edit <pr> --base <trunk>`; repeat up the stack | `gh stack sync` | `gt sync` | `git town sync --stack` |
| Fix a wrong parent | `gh pr edit <pr> --base <base>` | see `gh stack --help` | see `gt --help` | `git town set-parent` |

Sources: `github/gh-stack` README; graphite.com/docs/cheatsheet; git-town.com/stacked-changes
and its command pages; the autopilot-stack playbook in `cursor/plugins` (pstack), which keeps one
linear stack and records the parent only as the PR base.
