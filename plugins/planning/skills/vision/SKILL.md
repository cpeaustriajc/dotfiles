---
name: vision
description: >
  This skill should be used when the user has a product idea, asks "is this worth building" or if
  a tool can sell, says "grill me on this idea", "plan the product" or "set up the initiative" or
  wants a product update. No ideation.
---

Read `references/top-down.md` and the Product row of the Tracker section in this skill's project copy.

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

1. Grill the idea: the grill steps in `references/interview.md`, with `references/rounds.md`
   and the changes in `references/interview.md`. A `scout`
   idea's filter scores answer Real, Reach and copies; ask only what scored unknown.
2. Settle worth it first: `references/worth-it.md`; for a tool of mine that might sell,
   `references/personal-to-sellable.md`.
3. Instead of grill's step 7: once each branch is settled, out of scope or not yet specified,
   post the ledger as the draft product and ask if it is right.
4. On yes, write it per `references/product-template.md`. A test-first product stays Draft until
   the test result is in.
5. Once Confirmed, create one project per feature in the Sequence's first step, linked to
   the product and holding only its line. Hand the first to `shape`; shape the next when the
   one before reaches Launch, or when I say.
6. Launch, a feature change, an update or an audit: `references/later.md`.
