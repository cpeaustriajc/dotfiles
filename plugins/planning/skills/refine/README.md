# refine

A skill that loops a set of drafted tickets until a fresh reader finds nothing left open. It runs
between `tickets`, which drafts them, and `triage`, which marks them ready for an agent.

## When to use it

Use it when tickets touch a contract, another team or a live system, and an agent will build
them without you. It stops an agent from meeting an unanswered behaviour halfway through a ticket.

- You say "refine these tickets", "anything still unanswered?" or "is this ready for an agent?".
- You say "keep refining until nothing is unclear" or "fact-check the drafts".

Do not use it for a product question. Use `vision`. Do not use it to ask you design questions
one by one. Use `grill`.

## Example

You say: "Refine the request-only checkout tickets."

1. Claude reads the contract, the code, every ticket's comments and your meeting notes.
2. Claude lists a dozen open behaviours, such as three unpaid orders in a chain.
3. Three read-only subagents check the code, the tracker and the vendor's test site at the same time.
4. Claude writes draft 10, with a confidence and a source for each choice.
5. A fresh subagent reads draft 10 cold and finds 25 problems. Claude fixes them as draft 11.
6. Rounds go on until a cold read finds only slips. Then Claude reports the choices and waits.

You get a local draft, each choice with its confidence, and the list of what only a person can do.

## Install

The `planning` plugin ships this skill:

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install planning@dotfiles
```

The skill then loads as `/planning:refine`.

## What it does

- Claude keeps each draft version private, in your tool's document or artifact feature, or in a temp directory outside the repo.
- Each open behaviour is checked against the sources before Claude asks you about it.
- Each choice in a draft carries a confidence and a link or command that shows it.
- Each check in a ticket names who runs it, and with which account, data or control.
- A fresh subagent, which has not seen Claude's reasoning, reads each draft as a user, QA, a builder and an attacker.
- Claude writes the decided fixes to a decision log beside the draft, so a later session can apply them.
- The loop stops when a cold read finds only slips, such as a wrong count or name.

## Limits

- It writes nothing to the tracker before you approve a draft.
- A probe that changes something outside the draft, such as a test order, waits for your go.
- It stops at a sign-in, a password, a purchase or a secret, and hands that step to you.

## More

- [SKILL.md](SKILL.md): the method Claude follows.
- [references/cold-read.md](references/cold-read.md): the cold reader's brief and findings.
- [references/claude-code.md](references/claude-code.md): the Claude Code commands.
