# Orchestrate

Read this when the argument is a spec, or two or more tickets. One-ticket mode is in `SKILL.md`.

This session coordinates and never builds a ticket. Each ticket gets its own worker: a parallel
session from the harness, on its own branch, that runs steps 1 to 7 of `SKILL.md` and opens its
own PR. A worker start needs a brief and the item's base branch. Run at most 3 workers at a time:
more use up the plan limits faster than the PRs can be checked.

1. **Frame.** Read the spec and its items. Build the graph from the blocked-by links.
2. **Frontier.** The frontier is every `ready-for-agent` item that passes the gate in step 3 of
   `SKILL.md` (`references/ticket.md`). List each item that is not ready as a gate.
3. **Start.** Start one worker per frontier item, up to the cap. The brief's first
   line invokes the skill the way this harness runs one from a prompt (`/implement <item link>`
   where skills are slash commands): a skill named inside other text may not run, and a brief that
   starts "Run /implement" builds with no gate and no close-out. The brief names the
   item's base branch; a stacked item's worker resets onto it and opens its PR against it. A
   worker's sandbox can be lost between turns, so it pushes its work in progress to its own
   branch (except at stop point `commit`).
4. **Check.** Trust but verify: read the PR's verdict table and rerun one check on the worker's
   branch.
5. **Advance.** When a PR merges or a stack base is pushed, recompute the frontier and start its
   new items. Never start an item whose blocker has no pushed branch: it builds on code that is
   not there yet.
6. **Gates.** Collect each `needs-info` item. Bring them to the user in one batch, not one at a
   time.
7. **Report.** Give each item with its PR and verdict, the open gates, and each abandoned item
   with the reason.

A worker that stops with no PR: read its branch, not its report. Start one fresh worker with the
remaining work. If that one fails too, abandon the item and add a gate.
