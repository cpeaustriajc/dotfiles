# Levels, documents and cycles

Read this when you set up a project's structure, write an engineering document or a decision,
or place a cycle. The steps are in `SKILL.md`.

## Levels in the tracker

| Level | Owner | Holds |
|---|---|---|
| Product | Product owner | Destination and features; see `vision`. Projects link to it rather than repeat it. |
| Project | Product owner writes intent, engineering the structure | One feature with an end: Why, What, How, Not in scope, Success. |
| Spec | Product owner writes, engineering formats | The spec template, with a status line: Draft, or Confirmed (date, by whom). |
| Engineering document | Engineering | At most one per project; see Documents. |
| Phase | Engineering | One of the fixed phases, as a milestone. Its exit check, not a progress bar, ends it. |
| Work item | Engineering writes, product owner approves the checks | See `tickets`. |
| Done | Verifier | Only a defect against the quoted requirements reopens it. A new ask is a new item. |
| Accepted | Product owner | The released feature checked against the spec's requirements. |

## Documents

Besides the spec, a project has at most one engineering document at a time, chosen by who reads
it:

- **Proposal**: a change another team must accept. Draft, Agreed, Shipped; once Agreed, its
  interface moves into an API contract that replaces it.
- **API contract**: an interface one side builds and another consumes, so both build at once.
- **Technical design**: work that stays inside one codebase.

A small project with nothing to agree skips it; the project How carries the mechanism. "Spec"
means the product side only, so none of these is called a tech spec or PRD.

**Decisions** don't count toward that limit. If `project-knowledge` is installed, it owns them.
Otherwise file one document per decision titled `Decision: <Topic>` in its project; superseding
changes only the old one's status line.

## Cycles

Cycles or sprints choose what matters next; they are not project containers or release
promises. Assign them to work items, not to project descriptions, and let unfinished items roll
forward.
