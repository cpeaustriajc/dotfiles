---
name: tickets
description: >
  This skill should be used when the user says "break this into tickets", "cut the next slice",
  "write the issue", "file these bugs as issues" or "rewrite this ticket", or a ticket is too
  long. It writes slices, or one bug or chore.
---

Read `references/top-down.md` first: the Tracker section of this skill's project copy says where each part lands, and
"Write, then check the tree" says when you may write.

## Setup

When the project's skills folder has no copy of this skill, set up first:

1. Find the tracker (`references/top-down.md`) and the tools that reach it (connected tools, the
   CLI's `--help`), and read the team's work types, templates, required fields and workflows.
2. Write the copy in that folder: this file without Setup, every file the copy uses directly or
   through another file (copied into its folder, paths rewritten), and a description with only
   the triggers it serves. Add a Tracker section: the Tracker map in `references/top-down.md`, with the
   tracker's objects and commands. Put `# <plugin> <version>` (from the marketplace manifest or
   this skill's version folder) on the line after the opening `---`. Commit it alone under the
   project's branch rules, else on a new branch, with hooks on.
3. Run the copy from its Steps section.

## Steps

1. Draft spec: cut only Demo prototypes. Else list its requirements and which items cite them.
2. Fetch the trunk and read facts from it; search open and recent closed items for
   one that already covers or supersedes this. A branch
   behind the trunk files work already done.
3. Cut the next slice only:
   - vertical slices, prefactors first, blockers named, riskiest first; a wide mechanical
     change is the exception: `references/item-kinds.md`.
   - each fits one session of its cheapest builder: `references/sizing.md`.
4. Show the slice: title, requirements, what I see, blockers, builder, estimate.
   Iterate until I approve. Other questions are spec gaps for `shape`.
5. Write each item per `references/item-template.md`; type, Bug or wide change per
   `references/item-kinds.md`.
6. Write blockers first. Run the tree check (`--launch` at Launch).

A set that an agent builds without me goes through `refine` before step 5.
