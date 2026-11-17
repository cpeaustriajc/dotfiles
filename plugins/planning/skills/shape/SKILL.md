---
name: shape
description: >
  This skill should be used when the user says "shape this", "write the spec", "put this in a doc"
  or "set a milestone", when a spec sits in one ticket or direction changes after a demo, and for
  a project audit or status update.
---

Read `references/top-down.md`; owners, documents and cycles are in `references/levels.md`.
Failures to prevent: a spec filed as a ticket gets built unconfirmed, requirements name
endpoints, a project never ends.

Paths are relative to this skill's folder.

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

1. Quote the product feature served; Done delivers it.
2. Carry the product's answers in as Settled and `grill` only the rest; many open questions: offer
   `vision`. Invent nothing to fill a section.
3. Agree the testing seams with me first: existing ones, the highest that works, ideally one
   (each extra seam is test code to keep in step).
4. Write the Draft spec, then the project description (`references/templates.md`).
5. Set milestones (`references/phases.md`). A product project starts in Demo, where a prototype
   settles an unknown instead of a question for me. Personal software uses the internal tool
   phases, and I confirm everything myself.
6. Check the tree (`references/tree-outline.md`) and hand back. `tickets` cuts only after the
   approver confirms the spec, so a change of direction edits one page.

A spec in a ticket or an old epic: `references/spec-mapping.md`. A project draft, audit or status
update: `references/templates.md`.
