# Levels, documents and cycles

| Level | Owner | Holds |
|---|---|---|
| Product | Product owner | Destination and features (`vision`). Projects link to it rather than repeat it. |
| Project | Product owner writes intent, engineering the structure | One feature with an end: Why, What, How, Not in scope, Success. |
| Spec | Product owner writes, engineering formats | The spec template (`templates.md`). |
| Engineering document | Engineering | At most one per project; see Documents. |
| Phase | Engineering | A fixed phase as a milestone, ended by its exit check, not a progress bar. |
| Work item | Engineering writes, product owner approves the checks | See `tickets`. |
| Done | Verifier | Only the verifier sets it, not a merge, closed issue or integration, unless the team agrees. Only a defect against the quoted requirements reopens it; a new ask is a new item. |
| Accepted | Product owner | The released feature checked against the spec's requirements. |

## Documents

Besides the spec, a project has at most one engineering document at a time, chosen by its reader:

- **Proposal**: a change another team must accept. Draft, Agreed, Shipped; once Agreed, its
  interface moves into an API contract that replaces it.
- **API contract**: an interface one side builds and another consumes, so both build at once.
- **Technical design**: work inside one codebase.

A small project with nothing to agree has none; the project How carries the mechanism. "Spec" is
the product side only, so none of these is a tech spec or PRD.

**Decisions** don't count toward that limit. `dossier`, if installed, owns them; otherwise one
document per decision, `Decision: <Topic>`, in its project. Superseding changes only the old one's
status line.

## Cycles

Cycles choose what matters next; they are not project containers or release promises. Assign them
to work items, not projects; unfinished items roll forward.
