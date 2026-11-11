# Evidence rules

Every verify run, audit and PR verdict follows these.

## Evidence

- Read the runner's own exit code. Use `set -o pipefail` and read `${PIPESTATUS[0]}`, or a report
  file. Never trust `tail`.
- Count the tests. Zero tests run is NOT VERIFIED.
- A timeout, a missing prerequisite or a skipped check is BLOCKED. Name the missing item.
- Each step pairs an action with a user-visible end state. A toast alone is not proof. An
  attribute a person cannot see, such as an `aria-label` or a `data-*` value, is not a
  user-visible end state.
- An exact check (text, value or state) decides the result. An agent's opinion of a screen,
  the capture reviewer's included, can only add a gate on top of it.
- Use the real environment the feature file names. A mock counts only at a boundary the project
  already isolates.
- Write one result line per feature: `VERIFIED`, `NOT VERIFIED` or `BLOCKED`, plus the command.
- Save the report, screenshots or trace in a path the reviewer can open. Print the path.
- Each capture gets a reviewer before you write its result line. A capture is a screenshot, a
  video end frame or saved output. The reviewer is a new read-only agent on the smallest model
  tier. An agent that has read the log or the steps is not fresh, and that includes a PR
  verifier. The reviewer call is in the adapter. Give the reviewer only the capture and the
  end state that the claim names. It answers one question: does the capture show that state? For
  a repro, that is the broken state; for a fix, the fixed state. VERIFIED needs its "yes"; "no"
  or "cannot tell" makes the line NOT VERIFIED. A new capture gets a new reviewer; never ask
  again about the same capture.

## Fake tests

Reject a test that passes without proving the feature. Reject these patterns:

- `toBeTruthy`, `toBeDefined` or `not.toThrow` as the only assertion.
- Mocks of internal modules of the code under test.
- Snapshot tests that accept any output.
- A test that asserts on its own fixture.
- Expected values computed by the code under test.
- A claim about what the screen shows, asserted only on an attribute a person cannot see.

Delete or rewrite a test that would still pass if the code under test returned `undefined`.
Never edit a test to match wrong code.

Add a lint rule only after it fails on the real existing test that it targets. The rule's message
names the fix.
