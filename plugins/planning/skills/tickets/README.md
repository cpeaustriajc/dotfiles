# tickets

A skill that cuts a confirmed spec into thin work items. Each item can be demoed on its own and quotes the requirements it meets.

## When to use it

Use it when a spec is confirmed and you need the next piece of work. Use it also when one ticket is too long.

- You say "break this into tickets", "cut the next slice" or "write the issue".
- You say "file these bugs as issues" or "rewrite this ticket".
- A ticket does two things and needs a split.

Do not use it to write the spec or the milestones: use `shape`. Do not use it to plan a whole product: use `vision`. Do not use it to ask questions about an approach: use `grill`. Do not use it to fix the ticket's code.

## Example

You say: "Cut the next slice from the checkout spec. R4 through R7 have no ticket yet."

1. Claude opens the spec and lists which requirements existing items already cite.
2. Claude shows the slice: title, requirements, what you see, blockers, builder and context estimate.
3. You approve the slice or change its size or order.
4. Claude writes the items, blockers first, and runs the tree check.

You get work items that each hold Context, Outcome, Checks and, if needed, Out of Scope.

## Install

The `planning` plugin ships this skill. Add the marketplace, then install the plugin:

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install planning@dotfiles
```

To turn the plugin off, run `claude plugin disable planning@dotfiles`. This also turns off every other skill in `planning`. For other agents such as Codex, run `scripts/link-skills.sh` in the repo.

## What it does

- Claude reads the spec first. If the spec is Draft, Claude cuts only prototype items for the Demo phase and says what would confirm it.
- Claude cuts the next slice only, not the whole spec. Each item is a narrow path through every layer, not one layer.
- Each item names the items that block it. Branches and stacked PRs are left to `create-pr`.
- Claude asks one question: are the size and the blocking right? Any other question goes up to `shape` as a spec change.
- Each item's checks quote the requirement with its number and has a "You see" line that says what the verifier observes.
- Each check names the account, data or switch that reaches its state.
- Each check names who proves it: a one-command test, a person's eye, or the engineer.
- Claude names the builder model for each item, from your model picks, and settles every design call so a cheaper builder loses no quality.
- Claude estimates the context each item uses in a fresh builder session: fixed session cost, reading, building and proof, with every image counted.
- Claude splits an item whose upper estimate is over the context budget. The budget is the project's, or Claude asks; the default is 200k tokens.
- Three to five checks and a body under about 1,500 characters are quick signs only. A short item with a screenshot review loop can still be too big.
- Each item names its proof budget and a stop rule: past a limit, the agent commits what passes, writes a hand-over note and stops.
- Items state the measured facts they need, and link a large reference only as a crop or an excerpt.
- Claude labels each item Task, Bug or Chore. A Chore adds a No-QA check and cites no requirement.
- A bug found after Done becomes a new item, related to the original.
- Claude writes through your tracker's adapter in `shape/references/`, then runs the tree check. Add `--launch` when the project enters Launch.

## Limits

- It cuts nothing from a Draft spec, except prototype items.
- It does not settle spec questions inside a ticket.
- Items hold no file paths and no code, because both go stale.
- It does not mark an item Done. The verifier does.
- It has no settings.

## More

- [SKILL.md](SKILL.md): the method Claude follows.
- [references/item-template.md](references/item-template.md): the parts of an item, and the rules for each check. The tracker's adapter says how each part lands.
- [references/item-kinds.md](references/item-kinds.md): work types, the Chore's No-QA check, bugs and wide mechanical changes.
- [references/sizing.md](references/sizing.md): how Claude estimates context per item, and the measured run behind the numbers.
- [../shape/references/top-down.md](../shape/references/top-down.md): the five rules and the tracker lookup.
- [../shape/references/tree-outline.md](../shape/references/tree-outline.md): the tree JSON that the check reads.

### Sources and evidence

- Source: Matt Pocock's `writing-for-agents` skill, from `mattpocock/skills` on `main`. Its rules: cut a sentence the model obeys by default, and point to a source of truth over a copy. It gives no measured result.
- Evidence: on 2026-11-11, terse project skills in one product repo kept their exact steps in most runs. Those skills point to the tracker's templates and the repo's rules and copy none of them.
