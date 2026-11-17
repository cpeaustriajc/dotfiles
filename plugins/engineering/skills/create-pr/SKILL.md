---
name: create-pr
description: >
  This skill should be used when the user asks to open a pull request: "open a PR", "make a PR for
  this branch", "create a draft PR" or "PR this against develop". It commits, runs the fast
  checks, pushes and opens the PR.
argument-hint: "[draft] [base-branch]"
---

Arguments: the text after the skill name (`$ARGUMENTS` where the harness fills it in). `draft`
opens a draft; any other word is the base. Paths are relative to this skill's folder.

## Setup

When the project's skills folder has no copy of this skill, set up first:

1. Find the code host's tool (the remote's host, the CLI's `--help`), how it attaches an image or
   video to a PR, and its video size limit.
2. Write the copy in that folder: this file without Setup, every file the copy uses directly or
   through another file (copied into its folder, paths rewritten), and a description with only
   the triggers it serves. Fill in the commands to open a PR from a body file with its base, read
   a PR's state and attach evidence, with the limit. Put `# <plugin> <version>` (from the
   marketplace manifest or this skill's version folder) on the line after the opening `---`.
   Commit it alone under the project's branch rules, else on a new branch, with hooks on.
3. Run the copy from its Steps section.

## Steps

Evidence: reference each file in the body by its path relative to the body file, and check a
video with `scripts/check-video.sh <file> <MB>`. When one upload fails, the PR may exist with the
rest: check the exit code and the rendered body, then attach the missing file. Ask me before a
tool reads a browser session to upload.

1. No remote: offer to create the repo, private or public.
2. On the default branch, branch first: by the project's rule, else the tracker's branch name
   for the issue, else a short topic, with no prefix. Make atomic commits; keep existing commits. Stack on
   an open blocker PR (`references/stacking.md`).
3. A fresh reader on the cheapest model gets only `git diff <base>...HEAD` and the comment rule,
   so it needs no tools and sees nothing of this session; the harness's code review does not
   replace it. A comment stays when it names a trap (what breaks if the next reader edits
   blindly) in two sentences and about 20 words at most; the repo's rule wins. It lists every
   other added or changed comment with file:line and why. Cut or shorten each, in one commit;
   the list is final.
4. Run the repo's fast checks and `python3 -I scripts/tests_kept.py --base <base>`.
   Red: stop. A `tests_kept.py` finding passes only when the owner allowed that test change.
5. Push. Read the PR's state on the code host: already open or merged, report its URL and leave
   it.
6. Open the PR against the given base, else the remote branch it was cut from, with the body per
   `references/pr-body.md` and the evidence per `references/evidence.md`.

Report the URL and anything skipped.
