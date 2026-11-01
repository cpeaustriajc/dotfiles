# implement

`implement` builds a ready ticket with no help from you. It ends with a pull request that closes the ticket and shows the proof for each check.

## When to use it

Use it when a ticket is planned and an agent can prove it done. Without it, an agent redesigns settled work or says "done" with no proof.

- To build one `ready-for-agent` ticket, type `/implement <ticket link>`.
- To build all ready tickets of a spec, type `/implement <spec link>` in a [Claude Code project](https://code.claude.com/docs/en/claude-projects).

If an idea still has open questions, use `grill`. If nobody has checked the ticket, use `triage` first. If a change has no tickets and splits into independent parts, run the built-in `/batch` command. A migration across the codebase is one example.

## Example

You type `/implement SHOP-42`.

1. Claude finds the tracker that the project uses, reads SHOP-42 and says its title.
2. Claude checks that the ticket is `ready-for-agent` and that its blockers are closed.
3. Claude builds the ticket in slices and commits each slice with its check.
4. Fresh reviewers read the commits, and Claude fixes what they find.
5. Claude opens a pull request that closes SHOP-42 when you merge it.

You get the pull request. It has a verdict and evidence for each Done When line.

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
- Reviewers that did not write the code check the commits.
- For a spec or several tickets, one Claude Code Projects thread builds each ready ticket. Each thread opens its own pull request.
- It starts a ticket only after all its blockers close.

## Limits

- It runs only when you type it. Claude never starts it alone.
- It never merges a pull request. You merge it.
- It never closes a ticket by hand. The merge closes the ticket.
- A spec or several tickets need Claude Code Projects. `references/claude-code.md` lists the plans that have it.

## More

- [SKILL.md](SKILL.md) is the method that Claude follows.
- [references/claude-code.md](references/claude-code.md) covers the Projects setup, the thread briefs and `/batch`.
