# Claude Code adapter

Mechanics checked against https://code.claude.com/docs/en/claude-projects.md and
https://code.claude.com/docs/en/commands in November 2026. Check again when a detail matters.

## Tracker

Use the tracker's MCP server or CLI for every read and write in this run.

## Workers: Projects

A worker in `references/orchestrate.md` is a Projects thread.

Projects is in public beta on Pro, Max and Ultra plans. Team and Enterprise plans do not have it.
It runs in the claude.ai/code sidebar, the desktop app's Code tab and the mobile apps, not in the
CLI.

1. Create a project and add the repository.
2. Put the base branch and these rules in the project instructions. Every thread starts from them.
3. Set the thread cap to 3. More threads use up the plan limits faster than you can check the PRs.
4. Run `/implement <spec>` in the project conversation. It is the coordinator.
5. Each thread is a cloud session with its own branch from the default branch. For a stacked
   item, the brief names its base. The thread resets onto that base and opens its PR against it.
6. Each thread opens its own PR. Auto-fix then handles CI failures, review comments and conflicts.

## Stop points

Checked against https://code.claude.com/docs/en/claude-code-on-the-web.md ("Auto-fix pull
requests") and https://code.claude.com/docs/en/desktop.md ("Monitor pull request status") in
November 2026.

- **Watch**: auto-fix. It needs the Claude GitHub App on the repo. Turn it on with
  `/autofix-pr` on the PR branch, or from the Changes card menu on the web. It wakes on GitHub
  events and fixes CI failures and review comments, so the session spends nothing while CI runs.
  No GitHub App: wait as in **Wait** below, not `/loop`.
- **Conflicts**: auto-fix gets no event for a base-branch conflict. Rebase yourself.
- **Merge**: on the desktop app, "Merge when ready" turns on GitHub auto-merge. On the web or
  CLI, `gh pr merge <pr> --auto` with the repo's method (`--squash`, `--merge` or `--rebase`,
  from recent merged PRs). Auto-merge must be allowed in the repo settings; if it is not, ask.
- **Ready**: `gh pr merge <pr> --disable-auto` turns off auto-merge that is already on.
- **Ask**: `AskUserQuestion`.
- **Wait**: while checks run at `ready`, wait in the foreground with `gh pr checks <pr> --watch`
  (Bash timeout 600000). A turn that ends while CI runs ends the run.
- **Hold**: the `implement-gate` mod reads the last word of the `/implement` line. Below `merged`
  it denies a merge and a push to the default branch; at `commit`, every push. At `pr` and past,
  it blocks the turn's end until `gh pr view` shows the stop point, at most 3 times. Without the
  mod, the stop point rests on this text alone. `/implement-gate off` ends its hold.

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
