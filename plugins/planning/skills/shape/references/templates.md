# Templates

Contents: Spec · Project (the project check, properties, description, internal tool) · Status
update.

Proposals, not a standard. The project's own templates and section names win. Where the project
has none, propose these shapes once and use them; where its template lacks a section below, add
the section's content under the project's nearest heading.

## Spec

Written from decisions already made (`grill`), never to make new ones. A section with nothing
real to say is left out rather than filled.

```markdown
Status: Draft | Confirmed (<date>, <approver>)
Feature: <the product feature this serves, quoted>

## Problem

<Whose problem, in their words, and the evidence.>

## Done

<The observable outcome: who does what, and what they see. One or two sentences.>

## Requirements

R1. <Who> <does what> and <sees what>.
R2. <An empty, error or edge state, stated the same way.>

## Testing seams

- <Where the feature is proven, highest first. One is ideal.>

## Approaches considered

- <The approach not taken, in one line, and why.>

## Out of scope

- <What was asked for or obvious, and deliberately left out. Not empty once Confirmed.>

## Open questions

- <Empty once Confirmed.>
```

`scripts/check_tree.py` rejects a Confirmed spec that breaks either.

- **Requirements are statements, not tasks.** Each says who does what and what they see, for
  the empty, error, slow and edge states too. None names a data source, vendor, endpoint, model
  or timing budget: the product owner must be able to confirm it, and mechanism buries intent.
  Mechanism goes in one line of the project How.
- **Feasibility gate.** A requirement that needs a system the team neither owns nor has a
  contract for gets a probe of that system first; the answer often removes the dependency.
- **Requirements** are numbered once and never renumbered; a dropped one is struck through, so
  work items that cite it still resolve. A long list is fine: it should cover the feature.
- No file paths or code (`top-down.md`, Text others read). A prototype's snippet that pins a
  decision (a state machine, a schema) may be inlined, marked as from a prototype.

## Project

Before you draft or audit one, check it is a project at all: one outcome with an end and several
work items. Flag a single ticket dressed up as a project, a permanent category posing as one, or
two outcomes in one; say so rather than repair it silently.

Return the properties separately from the description, because the properties go in the tracker's
own fields:

```markdown
Name:
Summary:          <one sentence: the user or business outcome>
Lead:
Team(s):
Product:
Status:
Start:
Target:
Dependencies:

Description:
```

The description is evergreen: a neutral present tense ("Buyers save names to a shortlist", not
"will let") and no status narration, completed work, dated updates, migration history,
temporary blockers or next steps; those go in status updates or native fields.

```markdown
## Why

The enduring problem, who it hurts, and the evidence.

## What

- Three to five capabilities or changes a user can see.
- Behaviour, not implementation. No work-item acceptance criteria.

## How

The product and technical decisions that define how it works, plus any open decision. Only
constraints that shape the project; detailed plans go in the engineering document.

## Not in scope

The nearest problems this project deliberately leaves alone.

## Success

The one condition, measure or observation that says it worked. A guardrail only when needed.

## Risks

Only risks that change what gets built. Omit if none.

## Open questions

| Question | Owner | Needed by |
| --- | --- | --- |
```

Leave Owner blank unless someone named the owner; a role guessed from the question's topic is an invented owner.

Omit Open questions once the scope is settled. Revise the description only when the intended
behaviour or boundary changes.

A project for an **internal tool** (one only the team uses: a test harness, a mock of another
team's system, a QA panel) uses the same sections, and its How also says:

- whose behaviour it copies, if it stands in for another team's system, and where it deliberately
  differs, with the decision that allowed each difference;
- whether one person's use affects anyone else's, because testers share these tools.

If buyers or end users will ever see the result, it is a product project, even when the team uses
it first.

**Keep out of the description**, in the tracker's native fields instead: lead, members and teams;
product and status; priority and dates; phases; dependencies; links and resources; health.

## Status update

```markdown
Health: on track | at risk | off track

Progress:
Risks:
Next:
```

Health is the project lead's judgement: propose one and say it needs their confirmation. Rate it
only when an update was asked for. Read what changed since the previous update first, and report
changed scope, dates, lead, dependencies or phases. Finished-item counts do not replace the lead's
judgement: most items done can still be at risk if the remaining one is blocked on another team.
