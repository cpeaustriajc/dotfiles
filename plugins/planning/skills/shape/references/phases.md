# Phases

Each project gets these phases in order and no others, with empty phase descriptions (the table
is the definition) and no frontend and backend split. No target dates unless asked, and then only
on Launch: a date on every phase makes a waterfall.

## Product project

| Phase | Holds | Exit check | Decides |
| --- | --- | --- | --- |
| Demo | The spec in Draft, plus throwaway mockup or prototype items. No build items. | An approval item ("<approver> approves the <spec> after the demo") is done, and the spec is Confirmed. | Approver |
| Implementation | Items split from the Confirmed spec, the next slice only. | The verifier marked every item done. | Verifier |
| Launch | The production release, a release note, verification on production. | The product owner accepts the release against the spec. | Product owner |
| Post Launch | Bugs and small follow-ups to what shipped. | Two cycles after Launch the project completes. | Engineering |

- **Demo lasts one cycle.** Still unconfirmed after that, it goes back to the product owner as a
  question, not a second demo. Demo work is throwaway, never the start of production code.
- **A change of direction** in Demo edits the spec and closes the mockup items. After Demo it
  moves the project back to Demo: the spec returns to Draft, unstarted build items go to the
  backlog, and only the slice in progress is lost.
- **Post Launch is not a parking lot**: anything but a fix to what shipped is a new spec.

## Internal tool

No Demo: no approver gates a tool only the team uses. The spec stays short (requirements and Out
of scope, confirmed by the main user) so items still cite requirements.

| Phase | Holds | Exit check | Decides |
| --- | --- | --- | --- |
| Implementation | Build items, plus a mockup on the first item when the tool has a screen. | The verifier marked every item done (Chores: engineering, after code review). | Verifier |
| Launch | The tool live where the team uses it, and a note on how to use it. | The main user confirms they can do the job named in Success. | Main user |
| Post Launch | Bugs and small follow-ups to what shipped. | Two cycles after Launch the project completes. New asks start a new project. | Engineering |

Whoever owns visual calls approves a mockup on its item before the build; visual sign-off is not a
phase.
