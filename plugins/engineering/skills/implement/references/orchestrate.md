# Orchestrate

Read this when the argument is a spec, or two or more tickets. One-ticket mode is in `SKILL.md`.

This session coordinates and never builds a ticket. Each ticket gets its own worker: a parallel
session from the harness, on its own branch, that runs steps 1 to 7 of `SKILL.md` and opens its
own PR. The harness adapter (`references/<tool>.md`) says how to start a worker, how to name its
base branch and how many to run at a time.

1. **Frame.** Read the spec and its items. Build the graph from the blocked-by links.
2. **Frontier.** The frontier is every `ready-for-agent` item that passes the gate in step 3 of
   `SKILL.md`. List each item that is not ready as a gate.
3. **Start.** Start one worker per frontier item, up to the adapter's cap. The brief's first
   line is `/implement <item link>`. The brief names the item's base branch.
4. **Check.** A worker's report is a claim. Read its PR's verdict table. Rerun one check on its
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
