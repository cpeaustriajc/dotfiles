---
name: implement
description: >
  This skill should be used when the user types "/implement" with a ticket or a spec. It builds
  one ready ticket without supervision: it gets the ticket from the tracker, trusts its answers,
  builds it with the feature playbook, reviews after the commit and opens a PR that closes it.
  With a spec or several tickets, it starts one Claude Code Projects thread per ready ticket.
disable-model-invocation: true
argument-hint: "<ticket | spec>"
---

# Implement

Arguments: `$ARGUMENTS`.

Build work that is already decided. The ticket holds the answers. Never reopen the plan. End with
proof that the user checks later, never with a question.

A criterion is one line of the ticket that says when the work is done. Use the project's own
name for it in everything you write.

Tool mechanics: `references/claude-code.md`.

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
3. Every item that blocks it is closed.

If the item is `ready-for-human`, build only the part an agent can prove. Put the rest under
Needs you.

Branch from a fresh trunk. Skip this only if the current branch is already for this item. Never
build on the trunk.

## 4. Trust the ticket

Do not run `grill`. Do not propose a different approach. For each question the ticket does not
answer:

| The answer is | Do |
|---|---|
| Easy to undo | Follow the closest existing pattern. Add it to Decided. |
| Costly to undo, or against the spec or a recorded decision | Stop. Post triage notes on the item, move it to `needs-info`, report. |

A criterion that cannot be met as written is a costly question.

## 5. Build

1. Run the feature playbook (`playbooks`, `references/feature.md`) from its step 2. The ticket
   settled step 1. A Bug item runs the bug playbook instead.
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

This session coordinates. Each ticket gets its own Claude Code Projects thread, which runs steps
1 to 7 and opens its own PR (`references/claude-code.md`). This session never builds a ticket.

1. **Frame.** Read the spec and its items. Build the graph from the blocked-by links.
2. **Frontier.** The frontier is every `ready-for-agent` item whose blockers are closed. List each
   item that is not ready as a gate.
3. **Start.** Start one thread per frontier item. The brief's first line is `/implement <item
   link>`.
4. **Check.** A thread's report is a claim. Read its PR's verdict table. Rerun one check on its
   branch.
5. **Advance.** When a PR merges, recompute the frontier and start its new items. Never start an
   item whose blocker is open: it builds on code that is not there yet.
6. **Gates.** Collect each `needs-info` item. Bring them to the user in one batch, not one at a
   time.
7. **Report.** Give each item with its PR and verdict, the open gates, and each abandoned item
   with the reason.

A thread that stops with no PR: read its branch, not its report. Start one fresh thread with the
remaining work. If that one fails too, abandon the item and add a gate.
