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

## Setup

When the project's own skills folder has no copy of this skill:

1. Find the tracker (`references/top-down.md`), then the tools that reach it (connected tools,
   the CLI's `--help`), and read the team's work types, templates, required fields and workflows.
2. Write a project copy of this skill there: this file without its Setup section, the
   files its other steps name and the files those name (one outside this skill's folder goes
   beside the copy, with its path rewritten), and a description that keeps only the triggers
   the copy serves. Add a Tracker section: the table below filled in with the
   tracker's objects and commands. Put `# <plugin> <version>`, from the marketplace manifest or
   the version folder in this skill's path, on the line after the opening `---`. Commit it on
   its own, following the project's branch rules and commit hooks, else on a new branch with the
   hooks on.
3. Run the copy from its Steps section, not this file.

| Level | Map to | Fallback |
|---|---|---|
| Product | Top-level goal, initiative or portfolio | A pinned page the projects link to |
| Project | Project, epic or parent item | A parent item with child items |
| Spec, engineering document, decision | A tracker or wiki document linked from the project, editable by the product owner; never a ticket | A wiki page |
| Phase | Milestone | A `Phase` field, status or label |
| Work item, sub-item | Item, child item | none |
| Work type | Item type or template | A `Task`, `Bug` or `Chore` label |
| Dependency | Native "blocked by" | A link line in the item's Context |
| Cycle | The tracker's iteration | none |
| Checklist | Native checkboxes | A numbered list |
| Status update | The tracker's update, with health | A comment on the project |

- A level the tool can't create: say so and hand over the text to paste; never fake it with a
  comment or an unrelated object. Read back what may store differently (checklists, rich text).
- A Markdown-file tracker: a heading per project, the spec linked, phases as subheadings, work
  items as checkboxes (the Outcome as the line, its checks nested).
- Fill a template's headings in the body; upload a private tool's file where its readers sign in.
- Use the method's terms for sprint language (Success, chosen items); leave estimates blank unless
  the team estimates. Read a workflow's transitions before moving an item. Batch changes to one
  item: every write notifies.
- Closing on merge is not the verifier's Done: say so, and mark "verified" with a label or status.

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
