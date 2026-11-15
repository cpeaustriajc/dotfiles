# Top-down planning

Shared by `vision` (product: worth it, features F1…Fn, out of scope), `shape` (project: spec with
requirements R1…Rn, testing seams, milestones) and `tickets` (work item: one slice citing its
requirements). `grill` asks a project's open questions; `vision` grills the product. Each level
inherits what the one above settled, so questions thin out going down.

## Five rules

1. **Read the level above first.** A project starts from one product feature, a work item from
   the spec. No product: offer `vision` for a minimal one; a one-off internal tool may stand
   alone if I say so.
2. **Every item cites its parent**: a project its feature, a requirement the project's Done, a
   work item its requirements. An item with no parent is scope nobody asked for.
3. **Build a level only from a confirmed parent.** A Draft product gets one-line project
   placeholders at most; a Draft spec gets no build items, since it usually changes after a demo.
   A work item is ready only once engineering confirms it names only systems the team owns or
   has a contract for.
4. **Changes flow down, questions flow up.** A changed feature returns its spec to Draft; a
   changed requirement flags every item citing it. A lower level never edits a higher one: a
   requirement found wrong while building comes to me as a question.
5. **Status rolls up**: items close milestones, milestones feed the project update, project health
   feeds the product update. Nobody retypes progress.

## Find the tracker

Stop at the first hit:

1. A pointer in the project's instruction file, such as `Tracker: Linear, team ENG`, a Jira URL
   or `GitHub issues`.
2. The connected tools: a tracker's MCP server, or its CLI signed in (`acli`, `gh`).
3. Ask once and offer to add the pointer. For personal software, recommend a Markdown file in the
   repo.

Then fill the project copy's Tracker section (`SKILL.md`, Setup).

**The project's facts override these defaults**: who holds each role, the templates, which areas
can't skip QA, where older specs live. Look for a tracker section in the instruction file or a
file it points to; ask only what the task needs. On a solo project one person holds every role:

- **Product owner**: intent, priority, requirements; accepts releases.
- **Approver**: confirms direction, often after a demo; usually the product owner.
- **Verifier**: marks work done. QA if the team has it, else the product owner.
- **Engineering**: decomposition, work types, feasibility.

The tracker's own templates are the source of truth: read them fresh, never copy them into files.
Don't invent owners, dates, measurements or dependencies; leave them blank or ask.

## Write, then check the tree

Drafting, auditing or translating never authorises a write, and a PR, issue or comment is a
write: the default is a draft in chat. Before a write, state the exact item and change; after it,
read it back and report what the tracker holds. Show me the first write to a shared tracker, and
batch related changes, since many trackers notify on every save. Edit only what this run created
or I name; another person's ticket or epic is read-only, so a finding goes in a comment I approve.

**Text others read** (spec, item, update) has no file paths, code, project terms or engineering
jargon: paths go stale, and the product owner, QA and other teams lack repo access. A technical
question goes to me.

After writing, read the tree back and run the check (`tree-outline.md`) with absolute paths. Fix
every line it prints, or say why one stays.
