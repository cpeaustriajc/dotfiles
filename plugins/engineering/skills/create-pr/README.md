# create-pr

A skill that commits your work, runs the fast checks, pushes, and opens a GitHub pull request that links the issue and the evidence. It is the terminal version of the desktop Create PR button.

## When to use it

Type `/create-pr`, or ask Claude to open a PR, when a branch is ready for review. Claude also loads it on a request such as "push it and open the PR".

For commits alone, use `commit`. To review the diff, use `review-loop`.

## Example

You type: `/create-pr draft develop`

1. Claude commits any loose changes and runs the checks that your `AGENTS.md` or `CLAUDE.md` names.
2. Claude pushes the branch.
3. Claude opens a draft PR against `develop`.

You get the PR URL on its own line, plus one line on anything skipped, such as "no issue found". The word `draft` makes a draft. Any other word is the base branch.

## Install

The `engineering` plugin ships this skill. Add the marketplace, then install the plugin:

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install engineering@dotfiles
```

To turn the plugin off, run `claude plugin disable engineering@dotfiles`. This also turns off every other skill in `engineering`.

## What it does

- It needs `gh` signed in.
- If there is no GitHub remote, it asks whether to link a matching repo, create a private repo, or create a public one.
- It branches and commits as the `commit` skill does, and keeps your existing commits.
- Before the checks, a separate reader reads the diff for comments only. It keeps a comment only if the comment warns about a trap. A trap is code that breaks when the next person edits it unaware.
- Claude removes or shortens each comment that the reader lists, and commits that change as its own slice.
- It runs the fast checks that the repo's `AGENTS.md` or `CLAUDE.md` names, and `tests_kept.py` from `review-loop`, which flags a weakened, skipped or removed test. If one fails, it stops and opens no PR, unless you allowed that test change.
- If a PR is already open for the branch, it pushes and reports the URL. It does not open a duplicate.
- The PR body follows the repo's template. Without one, it follows the form of the repo's last few merged PRs. Without either, it has a short summary, an `Evidence` line, a `Merge danger` line and a `Test changes` line.
- Evidence videos and screenshots show each click and key press, play at a person's pace, and leave out sign-in and cleanup. Claude attaches them to the PR with `gh --attach`.
- It links the issue by its key. `scripts/check_pr_body.py` rejects `Closes`, `Fixes` or `Resolves`, which would close the issue on merge.
- The same check rejects headings, checklists, em dashes and arrows in the default body. Claude also rewrites AI-sounding prose, such as metaphor nouns.

## Limits

- It leaves out the `Evidence` line when no end-to-end run happened. It does not invent one.
- Reviewers, labels and the linked issue go in the PR's own fields, not the body. The issue key goes in the branch name or title.
- AI attribution follows Claude Code's own setting.
- It does not change the draft or ready state of an existing PR.
- It has no settings. The arguments are `draft` and a base branch.

## More

- [SKILL.md](SKILL.md): the method Claude follows.
- [references/pr-body.md](references/pr-body.md): the PR title, body and metadata.
- [references/stacking.md](references/stacking.md): stacked PRs on an open blocker, with commands for plain git, gh stack, Graphite and git-town.
- [references/evidence.md](references/evidence.md): the rules for screenshots and videos in the Evidence line.
- [scripts/check_pr_body.py](scripts/check_pr_body.py): the PR body check, with its tests in `scripts/test_check_pr_body.py`.
- [scripts/check-video.sh](scripts/check-video.sh): fails a video over the upload limit, with grey padding, or frozen for most of its length. Tests: `scripts/test_check_video.sh`.
- [references/github.md](references/github.md): how to upload screenshots and videos to a GitHub PR or issue.

### Sources and evidence

- Source: Matt Pocock's `writing-for-agents` skill, from `mattpocock/skills` on `main`. Its rules: cut a sentence the model obeys by default, and point to a source of truth over a copy. It gives no measured result.
- Evidence: on 2026-11-11, terse project skills in one product repo kept their exact steps in most runs. Those skills point to the tracker's templates and the repo's rules and copy none of them.
