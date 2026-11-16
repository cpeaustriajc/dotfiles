---
name: create-pr
description: >
  This skill should be used when the user asks to open a pull request: "open a PR", "make a PR for
  this branch", "create a draft PR" or "PR this against develop". It commits, runs the fast
  checks, pushes and opens the PR.
argument-hint: "[draft] [base-branch]"
---

Arguments: the text after the skill name (`$ARGUMENTS` where the harness fills it in). `draft` opens a draft; any other word is the base.

Paths are relative to this skill's folder.

## Setup

When the project has no copy of this skill among its own project skills (the folder where this
harness loads a repo's skills), set up first:

1. Find the code host and its tool: the remote's host, the CLI's `--help`. Read how it attaches
   an image or video to a PR (a flag, an upload call), and its size limit for a video.
2. Write a project copy of this skill there: this file without its Setup section, the
   files its other steps name and the files those use (one outside this skill's folder goes
   into the copy's folder, with its path rewritten), and a description that keeps only the triggers
   the copy serves. Fill in the commands for opening a PR from a body file with its
   base, for reading a PR's state, and for attaching evidence, with the upload limit. Put
   `# <plugin> <version>`, from the marketplace manifest or the version folder in this skill's
   path, on the line after the opening `---`. Commit it on its own, following the project's
   branch rules and commit hooks, else on a new branch with the hooks on.
3. Run the copy from its Steps section, not this file.

## Steps

Evidence uploads: reference each file in the body by its path relative to the body file. Check a
video against the limit with `scripts/check-video.sh <file> <MB>`. When one upload fails, the PR
may still exist with the others: check the exit code and the rendered body, then attach the
missing file. A tool that reads a browser session to upload: ask me first. Pass the base when
one was given, or the branch was cut from one that exists on the remote.

1. No remote: offer to create the matching repo, private or public.
2. Branch and commit per steps 1 and 2 of `../commit/SKILL.md`; keep existing commits. An open
   blocker PR: stack on it (`references/stacking.md`).
3. A fresh reader on the cheapest model reads only added or changed comments. Hand it the
   output of `git diff <base>...HEAD` and the comment rule in its prompt, so it needs no tools
   and sees nothing of this session; the harness's code review and simplify checks do not
   replace it. A comment stays
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
