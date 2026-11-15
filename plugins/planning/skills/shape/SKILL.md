---
name: shape
description: >
  This skill should be used when the user says "shape this", "write the spec", "put this in a doc"
  or "set a milestone", when a spec sits in one ticket or direction changes after a demo, and for
  a project audit or status update.
---

Read `references/top-down.md`. Owners, documents and cycles: `references/levels.md`. Failures: a
spec filed as a ticket is built unconfirmed, requirements name endpoints, a project never ends.

## Setup

When the project has no copy of this skill among its own project skills (the folder where this
harness loads a repo's skills), set up first:

1. Find the tracker as `references/top-down.md` says, then what reaches it: the connected tools'
   lists, the CLI's `--help`. Read the team's work types, templates, required fields and
   workflows.
2. Write a project copy of this skill in that folder with no Setup section, and copy `references/`
   and `scripts/` beside it. Add a Tracker section: the table below filled in with the tracker's
   own objects and commands. Stamp this skill's version or commit in the copy's first line.
3. Run the copy, not this file.

| Level | Map to | Fallback |
|---|---|---|
| Product | A top-level goal, initiative or portfolio | A pinned page the projects link to |
| Project | A project, epic or parent item | A parent item with child items |
| Spec, engineering document, decision | A document in the tracker or its wiki, linked from the project; not a ticket, not a repo file the product owner can't edit | A page in the team's wiki |
| Phase | A milestone | A `Phase` field, a status or a label per phase |
| Work item, sub-item | An item, a child item | none |
| Work type | An item type or template | A `Task`, `Bug` or `Chore` label |
| Dependency | A native "blocked by" | A link line in the item's Context |
| Cycle | The tracker's iteration | none |
| Checklist | Native checkboxes | A numbered list |
| Status update | The tracker's update, with its health | A comment on the project |

- A tool that cannot create a level: say what is missing and hand over the text to paste. Never
  fake it through a comment or an unrelated object.
- Read back what a tool may store differently (a checklist, rich text) after the first write.
- A tracker that is a Markdown file: one heading per project, the spec linked, phases as
  subheadings, work items as checkboxes with the Outcome as the line and its checks nested.
- A template or form fills its headings in the body. A file a private tool hosts is uploaded
  where its readers sign in.
- Translate sprint language into the method's terms (Success, chosen items); leave estimates
  blank unless the facts say the team estimates. Read a workflow's transitions before moving an
  item. Every write notifies: batch changes to one item.
- An item that closes on merge is not the verifier's Done: say so in the facts, and use a label
  or status for "verified".

1. Quote the product feature served; Done delivers it.
2. Carry the product's answers in as Settled; `grill` only the rest. Many open questions: offer
   `vision`. Invent nothing to fill a section.
3. Agree the testing seams with me first: existing, the highest that works, ideally one (each
   extra seam is test code to keep in step).
4. Write the Draft spec, then the project description, per `references/templates.md`.
5. Set milestones per `references/phases.md`. A product project starts in Demo, where a
   prototype settles an unknown instead of a question for me. Personal software uses the
   internal tool phases: I confirm everything myself.
6. Check the tree per `references/tree-outline.md`, then hand back. `tickets` cuts after the
   approver confirms the spec; until then a change of direction edits one page.

Other runs: a spec in a ticket or an old epic, `references/spec-mapping.md`; a project draft,
audit or status update, `references/templates.md`.
