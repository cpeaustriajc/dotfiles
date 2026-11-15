# Templates

Spec · Project · Status update. The project's own templates and section names win. With none,
propose these once and use them; content for a section its template lacks goes under its nearest
heading.

## Spec

Written from decisions already made (`grill`), never to make new ones. Leave out a section with
nothing real to say.

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
- <Asked for or obvious, and deliberately left out. Not empty once Confirmed.>

## Open questions
- <Empty once Confirmed.>
```

`scripts/check_tree.py` rejects a Confirmed spec with Out of scope empty or Open questions left.

- **Requirements are statements, not tasks**: who does what and what they see, for empty, error,
  slow and edge states too. None names a data source, vendor, endpoint, model or timing budget:
  the product owner must be able to confirm it. Mechanism goes in one line of the project How.
- **Feasibility gate**: a requirement needing a system the team neither owns nor has a contract
  for gets a probe of that system first; the answer often removes the dependency.
- Number requirements once and never renumber; strike a dropped one through so items citing it
  still resolve. A long list is fine if it covers the feature.
- No file paths or code. A prototype's snippet that pins a decision (a state machine, a schema)
  may be inlined, marked as from a prototype.

## Project

First check it is a project: one outcome with an end and several work items. Flag a single ticket
dressed as a project, a permanent category, or two outcomes in one, rather than repair it
silently.

Return the properties apart from the description; they go in the tracker's own fields:

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

The description is evergreen: neutral present tense ("Buyers save names to a shortlist", not
"will let"), with no status narration, completed work, dated updates, migration history,
temporary blockers or next steps. Those go in status updates or native fields, as do lead,
members, teams, product, status, priority, dates, phases, dependencies, links and health.

```markdown
## Why
The enduring problem, who it hurts, and the evidence.

## What
- Three to five capabilities or changes a user can see. Behaviour, not implementation.

## How
The product and technical decisions that define how it works, and any open decision. Only
constraints that shape the project; detailed plans go in the engineering document.

## Not in scope
The nearest problems this project leaves alone.

## Success
The one condition, measure or observation that says it worked. A guardrail only when needed.

## Risks
Only risks that change what gets built. Omit if none.

## Open questions
| Question | Owner | Needed by |
| --- | --- | --- |
```

Leave Owner blank unless someone was named; a role guessed from the topic is an invented owner.
Drop Open questions once scope is settled. Revise the description only when behaviour or boundary
changes.

An **internal tool** (only the team uses it: a test harness, a mock of another team's system, a QA
panel) has the same sections; its How also says whose behaviour it copies and where it differs,
with the decision behind each difference, and whether one person's use affects others. If buyers
or end users will ever see it, it is a product project.

## Status update

```markdown
Health: on track | at risk | off track

Progress:
Risks:
Next:
```

Health is the lead's judgement: propose one and say it needs their confirmation; rate it only
when an update was asked for. Read what changed since the last update first, and report changed
scope, dates, lead, dependencies or phases. Item counts don't set health: most items done is still
at risk if the last one is blocked on another team.
