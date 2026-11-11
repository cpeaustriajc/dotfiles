# Report

Step 7 of `SKILL.md`.

## Run folder

Write `break-it-<date>-<flow>/` in a folder the project ignores, with `report.md`, numbered
screenshots and the video. `report.md` opens with the exact URL, the commit and the users run, so
someone else can run it again.

## Chat report

Plain words, no internal jargon:

1. **What broke**, in three tiers. **Broken**: wrong data, a crash, lost input, or a flow that
   can't finish. **Ugly**: works but looks wrong (overflow, clipping, misaligned layout).
   **Fragile**: works now but breaks under a plausible change (a longer name, another locale).
   Each gets a one-line title, the user who found it, numbered repro steps, expected versus
   actual, the screenshot or video timestamp, and any side effect checked (stored value, request
   sent, file written).
   Each Broken finding also gets an end-to-end test in the project's suite that drives the repro
   and asserts the expected result. It is a bug only when that test fails for the stated reason;
   otherwise mark it UNPROVEN. Keep the test out of the merge gate (the suite's skip or tag) until
   the fix; then it stays as a regression test. A filed Bug links its test.
2. **Decisions for me**: behaviour that is odd but matches the spec, or whose fix is a product
   call. Each gets a recommended answer.
3. **What held up**: one line listing the attacks that did nothing.
4. **Not tested**: each user, board or attack not run, each UNPROVEN finding, and each finding not
   re-run after its fix. Never call a run clean or ask for sign-off while a Broken finding is
   open or untested. A finding blamed on setup or another branch stays open until a rerun
   proves it.

When I say to file, file each finding reproduced in the running app as a Bug via `tickets`,
never an UNPROVEN one. A finding only in a design prototype goes to the design's fix list, not the tracker: its readers
would think the app is broken.
