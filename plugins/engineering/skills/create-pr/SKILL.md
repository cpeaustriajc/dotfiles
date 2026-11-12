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

1. Not signed in to the code host: stop. No remote: offer the matching repo, a private or a
   public one.
2. On the default branch: branch by the project's rule, else the tracker's branch name for the
   issue, else a short topic, with no prefix. An open blocker PR: stack on it
   (`references/stacking.md`).
3. Commit loose changes in small slices, in the repo's commit style, with no secrets.
   Keep existing commits.
4. A fresh reader on the cheapest model reads only added or changed comments. A comment stays
   when it names a trap (what breaks if the next reader edits blindly) in at most two sentences
   and about 20 words; the repo's comment rule wins. It lists every other one with file:line and
   why. Cut or shorten each, in one commit; the list is final.
5. Run the repo's fast checks. Red: stop.
6. Push. PR already open: report its URL, and leave its draft or ready state.
7. Open the PR against the given base, else the pushed branch it was cut from: body per
   `references/pr-body.md`, evidence per `references/evidence.md`, prose per
   `references/plain-prose.md`.

Report the URL and anything skipped.
