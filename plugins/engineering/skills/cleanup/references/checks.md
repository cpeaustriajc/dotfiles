# Inventory, checks and removal order

Steps 1 to 3 of `SKILL.md`, and the checks the repo sweep reuses. Commands: `references/git.md`
and `references/shell.md`, both linked from `SKILL.md`.

## Inventory (step 1)

What this session made, from this conversation: background processes and their PIDs, dev
servers, containers and volumes, local and remote branches, stashes, edits to tool config,
evidence (videos, screenshots, test output, the work folder) and temp files.

## Checks (step 2)

A live check for each item, never memory:

- **process or server**: alive, and its working folder is this checkout;
- **branch**: its PR is merged or closed and the branch tip equals the PR head; with no PR, it
  has no commits missing from the trunk;
- **remote branch**: the same, and I authored the PR;
- **stash**: its message is a tag this session wrote;
- **evidence**: the PR it proves is merged, or the file is attached to the PR or ticket;
- **config edit**: the diff shows only this session's change.

## Removal order (step 3)

In this order, so one step does not block the next:

1. Stop processes by their PID, never by name or port.
2. Remove the containers and volumes this session named.
3. Drop each own stash, found again by its tag.
4. Restore config edits by path.
5. Delete the evidence paths.
6. Leave the branch.
7. Delete the local branch while its remote branch still exists, so a squash merge passes.
8. Delete the remote branch. A delete git refuses goes under Run yourself; never force it.
