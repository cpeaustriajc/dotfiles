# implement

`implement` builds a ready ticket with no help from you. It ends with a pull request that closes the ticket and shows the proof for each check.

## When to use it

Use it when a ticket is planned and an agent can prove it done. Without it, an agent redesigns settled work or says "done" with no proof.

- To build one `ready-for-agent` ticket, type `/implement <ticket link>`.
- To build all ready tickets of a spec, type `/implement <spec link>`. In Claude Code, type it in a [project](https://code.claude.com/docs/en/claude-projects).

If an idea still has open questions, use `grill`. If nobody has checked the ticket, use `triage` first. If a change has no tickets and splits into independent parts, run the built-in `/batch` command. A migration across the codebase is one example.

## Example

You type `/implement SHOP-42`.

1. Claude finds the tracker that the project uses, reads SHOP-42 and says its title.
2. Claude checks that the ticket is `ready-for-agent` and that its blockers are closed.
3. Claude builds the ticket in slices and commits each slice with its check.
4. Claude runs `review-loop` on the commits and fixes what it finds.
5. Claude opens a pull request that closes SHOP-42 when you merge it.

You get the pull request. It has a verdict and evidence for each criterion of the ticket.

## Install

The `engineering` plugin ships this skill. Add the marketplace, then install the plugin.

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install engineering@dotfiles
```

The skill then loads as `/engineering:implement`.

## What it does

- It reads the ticket from the tracker that the project names. If the project names none, Claude finds it.
- It never reads the ticket from a list in the conversation.
- It asks you no design questions. An easy choice follows the closest pattern in the code, and the pull request lists it.
- A costly question stops the run. Claude moves the ticket to `needs-info` and adds a note.
- `review-loop` checks the commits: verify, code review and simplify.
- For a spec or several tickets, one parallel worker builds each ready ticket. Each worker opens its own pull request.
- It starts a ticket only after each blocker is closed, or is pushed as the base of its stack.

## Limits

- It runs only when you type it. Claude never starts it alone.
- A stop point word after the ticket sets how far it goes: `commit`, `pr` (the default), `ready` or `merged`.
- It merges a pull request only when you type `merged`. Otherwise you merge it.
- With `ready` or `merged`, Claude Code's auto-fix handles CI failures and review comments. `references/stop-points.md` sets the fix budget.
- The `implement-gate` mod limits the run to its stop point. It denies a merge or push past it and blocks an early stop.
- It turns on GitHub auto-merge only when its proof covers every changed file and each bot finding has an answer.
- It never closes a ticket by hand. The merge closes the ticket.
- A spec or several tickets need a harness that runs parallel workers. In Claude Code, this is Projects. `references/claude-code.md` lists the plans that have it.

## More

- [SKILL.md](SKILL.md) is the method that Claude follows.
- [references/orchestrate.md](references/orchestrate.md) is the coordinator method for a spec or several tickets.
- [references/stop-points.md](references/stop-points.md) is the stop point method: the grant, the fix budget, the merge gate and when to ask.
- [references/claude-code.md](references/claude-code.md) covers the Projects setup, auto-fix and merging, the thread briefs and `/batch`.
- `ready` and `merged` come from the `full-stop` and `full-send` skills in [t3dotgg/tstack](https://github.com/t3dotgg/tstack/tree/main/skills), read in November 2026. Those skills show no measured results.
- Claude Code's auto-fix and GitHub auto-merge replace its `babysit-pr` watcher here.
- The fix budget is new here. It stops an unattended run from spending tokens on a pull request that keeps failing.
