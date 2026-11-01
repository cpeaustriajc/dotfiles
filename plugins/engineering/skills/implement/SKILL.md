---
name: implement
description: >
  This skill should be used when the user types "/implement" with a ticket or a spec. It builds
  one ready ticket without supervision: it gets the ticket from the tracker, trusts its answers,
  builds it with the feature playbook, reviews after the commit and opens a PR that closes it.
  With a spec or several tickets, it starts one parallel worker per ready ticket.
disable-model-invocation: true
argument-hint: "<ticket | spec>"
---

# Implement

Arguments: `$ARGUMENTS`.

Build work that is already decided. The ticket holds the answers. Never reopen the plan. End with
proof that the user checks later, never with a question.

A criterion is one line of the ticket that says when the work is done. Use the project's own
name for it in everything you write.

Tool mechanics: `references/<tool>.md` (Claude Code: `references/claude-code.md`).

## 0. Pick the mode

| The argument is | Mode |
|---|---|
| One ticket reference | One ticket: steps 1 to 7 |
| A spec, or two or more tickets | Orchestrate: section "Orchestrate" |

## 1. Find the tracker

1. Read the tracker the project names: `CLAUDE.md`, `AGENTS.md`, `.claude/rules/`, `CONTRIBUTING`
   or the docs.
2. If the project names none, find it. Look at the form of the reference, the connected MCP
   servers and the CLIs, and the keys in branch names and commit messages.
3. Use that tracker's MCP server or CLI for every read and write in this run.
4. If two trackers remain, stop and ask which.

## 2. Get the ticket

1. Read the item from the tracker by its reference: a URL or the tracker's key.
2. Never match a bare number against a list in this conversation or in a file. It picks the
   wrong item.
3. Write its title and link in one line.
4. If the reference matches two items (an issue and a pull request), stop and ask which.
5. If there is no reference and the plan is only in this conversation, write its criteria as
   you understood them. Wait for the user's go.

## 3. Gate

Check each line. If one fails, stop and name it.

1. The item is `ready-for-agent` (or the team's name for it). Any other state: run `triage`.
2. It has criteria, each a check that passes or fails.
3. Every item that blocks it is closed, or is its stack base with a pushed branch. Without the
   second case, a stack never builds past its first item.

If the item is `ready-for-human`, build only the part an agent can prove. Put the rest under
Needs you.

Branch from the stack base that the ticket names, else from a fresh trunk. Skip this only if the
current branch is already for this item. Never build on the trunk.

## 4. Trust the ticket

Do not run `grill`. Do not propose a different approach. For each question the ticket does not
answer:

| The answer is | Do |
|---|---|
| Easy to undo | Follow the closest existing pattern. Add it to Decided. |
| Costly to undo, or against the spec or a recorded decision | Stop. Post triage notes on the item, move it to `needs-info`, report. |

A criterion that cannot be met as written is a costly question.

## 5. Build

1. Run the feature playbook (`playbooks`, `references/feature.md`) from step 2 to step 6. The
   ticket settled step 1. Step 7 here opens the PR, after the review. A bug item runs the bug
   playbook instead, up to its report.
2. Make each criterion a check. Make each criterion that a user sees an end-to-end check in the
   running app.
3. Commit per slice. Never commit red. Save each check's command and evidence.
4. Do not touch Out of Scope items. Put a side discovery in the report.

## 6. Review after the commit

1. Run `interrogate` on `<base>...HEAD`. Its reviewers are fresh: the builder never grades its own
   work.
2. Fix each Act on row in its own commit. Rerun the checks it touches.
3. Put each Consider row in the PR.

## 7. Close out

Push and open the PR with `create-pr`. The body holds:

1. The tracker's close word or link for the item, so the merge closes it. Never close it by
   hand.
2. One row per criterion: the criterion, the command, the evidence path, and VERIFIED, NOT
   VERIFIED or INCONCLUSIVE. INCONCLUSIVE is not a pass.
3. **Decided:** each answer from step 4 that the ticket did not give.
4. **Needs you:** each line only a person can check.

Report the PR link and the same three lists.

## Orchestrate

In Orchestrate mode, read `references/orchestrate.md` first and follow it. This session
coordinates. A worker from the harness builds each ticket.
