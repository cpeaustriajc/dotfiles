# Claude Code adapter

Mechanics checked against https://code.claude.com/docs/en/claude-projects.md and
https://code.claude.com/docs/en/commands in November 2026. Check again when a detail matters.

## Tracker

Use the tracker's MCP server or CLI for every read and write in this run.

## Workers: Projects

A worker in `references/orchestrate.md` is a Projects thread (claude.ai/code, the desktop Code tab
or mobile; plans and setup: the docs above). Run `/implement <spec>` in the project conversation as
the coordinator. Put the base branch and these rules in the project instructions, and set the
thread cap to 3: more threads use up the plan limits faster than you can check the PRs. A stacked
item's brief names its base; the thread resets onto it and opens its PR against it.

## Stop points

Checked against https://code.claude.com/docs/en/claude-code-on-the-web.md ("Auto-fix pull
requests") and https://code.claude.com/docs/en/desktop.md ("Monitor pull request status") in
November 2026.

- **Watch**: auto-fix (`/autofix-pr` on the PR branch; it needs the Claude GitHub App). No GitHub
  App: wait as in **Wait** below, not `/loop`.
- **Merge**: on the desktop app, "Merge when ready" turns on GitHub auto-merge. On the web or
  CLI, `gh pr merge <pr> --auto` with the repo's method (`--squash`, `--merge` or `--rebase`,
  from recent merged PRs). Auto-merge must be allowed in the repo settings; if it is not, ask.
- **Ready**: `gh pr merge <pr> --disable-auto` turns off auto-merge that is already on.
- **Ask**: `AskUserQuestion`.
- **Wait**: while checks run at `ready`, wait in the foreground with `gh pr checks <pr> --watch`
  (Bash timeout 600000). A turn that ends while CI runs ends the run.
- **Hold**: the optional `implement-gate` mod denies a merge or push past the stop point and
  blocks the turn's end before it. Without the mod, the stop point rests on this text alone.

## Thread briefs

- **The brief starts with `/implement`.** A skill name after other text does not run the skill,
  and `disable-model-invocation: true` stops Claude from starting it. A brief that starts "Run
  /implement" builds with no gate and no close-out. Source: https://code.claude.com/docs/en/skills,
  section "Where you write the skill's name".
- **Cloud sandboxes can be lost between turns.** A thread commits and pushes work in progress.

## Work with no tickets

`/batch <instruction>` (https://code.claude.com/docs/en/commands) fans out background subagents,
one per unit. It reads no tracker, keeps no blocked-by order and closes no ticket, so use it only
when no unit blocks another.
