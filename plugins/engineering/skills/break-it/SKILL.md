---
name: break-it
description: >
  This skill should be used when the user says "break it", "try to break this", "monkey test",
  "bug bash", "dogfood" or "QA this like a user", or after a flow change. It drives the app as a
  careless user. Visual sign-off: ui-polish.
---

Act as users who don't read, don't wait and don't do what the designer pictured. Report only.
Safety and users: `references/users.md`.

1. Say whether you drive the running app or a design prototype, from my words; ask if unclear
   ("break the redesign" can mean a canvas board).
2. Drive only localhost, a preview, staging, a sandbox or the design file; a URL that may be
   production stops for me.
3. Read the diff or spec and the area's feature file; spend the run on the changed flow.
4. Launch with the project's run recipe (else guess from the README, package file or Makefile;
   the guess fails when the app needs a database, env file or multi-step build), then
   health-check the app, test data and browser: a failure is a setup problem, not a bug. Running
   the app shows only the happy path; the careless users start once it is up.
5. Pick 2-4 users and say why. Seed worst-case data per `references/catalog.md`.
6. Give each user one goal; after each step note expected versus actual, the console and failed
   requests. A finding needs the trigger and the stable end state, not a flash. Getting stuck is a
   finding.
7. Report per `references/report.md`. A Broken finding without a failing test is UNPROVEN.
8. Stop. Fix only what I name; file only reproduced findings, via `tickets`.
