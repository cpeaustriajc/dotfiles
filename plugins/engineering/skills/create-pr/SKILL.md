---
name: create-pr
description: >
  This skill should be used when the user asks to open a pull request: "open a PR", "make a PR for
  this branch", "create a draft PR" or "PR this against develop". It commits, runs the fast
  checks, pushes and opens the PR.
argument-hint: "[draft] [base-branch]"
---

Arguments: `$ARGUMENTS`. `draft` opens a draft; any other word is the base. Commands: the code
host's adapter (`references/github.md`) and the harness's (`references/claude-code.md`).

1. No remote: offer to create the matching repo, private or public.
2. Branch and commit per steps 1 and 2 of `../commit/SKILL.md`; keep existing commits. An open
   blocker PR: stack on it (`references/stacking.md`).
3. A fresh reader on the cheapest model reads only added or changed comments. A comment stays
   when it names a trap (what breaks if the next reader edits blindly) in at most two sentences
   and about 20 words; the repo's comment rule wins. It lists every other one with file:line and
   why. Cut or shorten each, in one commit; the list is final.
4. Run the repo's fast checks and `python3 -I ../review-loop/scripts/tests_kept.py --base <base>`.
   Red: stop. A `tests_kept.py` finding passes only when the owner allowed that test change.
5. Push. Read the PR's state on the code host first: already open or merged, report its URL and
   leave its state.
6. Open the PR against the given base, else the pushed branch it was cut from, with the body per
   `references/pr-body.md` and the evidence per `references/evidence.md`.

Report the URL and anything skipped.
