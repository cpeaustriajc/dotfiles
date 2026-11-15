# Shaping a spec

## Where each part of a spec lands

| Spec section | Destination |
| --- | --- |
| Product goal, business value, customer value | The goal (usually already there) |
| Epic, objective | Project Why and What |
| Feature 1, Feature 2 | Product features in `vision`, or spec Requirements when they are one project |
| User story N | One or more Requirements; a build item cites them once the spec is Confirmed |
| Acceptance criteria | Requirements, verbatim; quoted into items |
| Acceptance considerations: UI behaviour, ordering | Item acceptance criteria |
| Acceptance considerations: performance | Project How |
| Dependencies on another system | Project How; on other work, a "blocked by" relation |
| Assumptions | Project Not in scope, or a decision |
| Risks | Project Risks, only those that change the build |
| Example values | A verifier's example under the item, generalised |
| Anything naming infrastructure, a vendor API, an endpoint or a sub-second budget | The engineering document, or a decision when it applies to every project; never items |

## A spec filed as a ticket

1. Create the spec document in the project with the author's text verbatim, status Draft.
2. Move the ticket back to the backlog, or keep it as the first build slice once the spec is
   Confirmed. Never cancel it: a cancel reads as a verdict on the author.
3. Put the project in Demo and add the approval item.

## Translating an old epic, brief or plan

An old source is evidence of the problem, not a technical spec: its architecture, services,
estimates and criteria are hypotheses until current code, tests, contracts or a newer decision
confirm them, and those outrank it.

- Keep its key or link as provenance, recover the intent, and draft from the present state.
- Sources that conflict on a product choice go to the product owner; a technical question the
  code or a contract already answers does not.
- Account for every source item: translated into a project, merged, split into several projects,
  kept as goal or reference context, or held for a product decision.
- Merge old items that describe one outcome today, listing every contributing key.
