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
2. On the default branch: branch by the project's rule. An open blocker PR: stack on it
   (`references/stacking.md`).
3. Commit loose changes in small slices, in the repo's commit style. Keep existing commits.
4. A fresh reader on the cheapest model lists each added comment except one-line trap warnings
   (the repo's comment rule wins). Cut each in its own commit; the list is final.
5. Run the repo's fast checks. Red: stop.
6. Push. PR already open: report its URL.
7. Open the PR against the given base, or the pushed branch it was cut from. Body from
   `references/pr-body.md`; evidence per `references/evidence.md`; then rewrite hits from
   `references/plain-prose.md`.

Report the URL and anything skipped.
