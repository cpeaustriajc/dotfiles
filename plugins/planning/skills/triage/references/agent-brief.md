# Agent brief and triage notes

The brief is the contract; the issue body and comments are context. It must stay true when files
move: name behaviour, types, commands, routes and config keys, no file paths or line numbers; say
what the system does when done, not how; each check pass or fail by one person or agent.

## Agent brief

```markdown
## Agent brief

**Category:** bug | enhancement
**Summary:** <one line>

**Now:** <what happens today; for a bug, the broken behaviour and the reproduce steps>

**After:** <what happens when the work is done, with edge cases and errors>

**Key interfaces:**
- `<type, command, route or config key>`: <what changes>

**Checks:**
- [ ] <a check with an input and the result you see>

**Out of scope:**
- <a near feature this item does not touch>
```

For a PR, **Now** describes the diff as it is, and **After** says what is left: gaps, failed
checks, review points.

## Needs a person

Add this section to the brief for `ready-for-human`:

```markdown
**Needs a person:**
- <check>: <why an agent cannot prove it, for example "needs the merge to main first">
```

## Triage notes (needs-info)

```markdown
## Triage notes

**Settled so far:**
- <fact or decision>

**We need from @<reporter>:**
- <one specific question, with the example that shows why it matters>
```

## Wontfix

Built already: link where it lives, then close. Rejected: give the reason, then close, and record
the decision in `dossier` if it is installed.
