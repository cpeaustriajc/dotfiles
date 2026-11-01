# Claude Code adapter

Mechanics checked against https://code.claude.com/docs/en/claude-projects.md and
https://code.claude.com/docs/en/commands in November 2026. Check again when a detail matters.

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

## Thread briefs

- **The brief starts with `/implement`.** A skill name after other text does not run the skill,
  and `disable-model-invocation: true` stops Claude from starting it. A brief that starts "Run
  /implement" builds with no gate and no close-out. Source: https://code.claude.com/docs/en/skills,
  section "Where you write the skill's name".
- **Cloud sandboxes can be lost between turns.** A thread commits and pushes work in progress.

## Work with no tickets

`/batch <instruction>` researches the code, splits the work into 5 to 30 independent units and
shows a plan. After approval it starts one background subagent per unit, each in its own
worktree; each one builds its unit, runs the tests and publishes its change. It reads no
tracker, keeps no blocked-by order and closes no ticket, so use it only when no unit blocks
another. Source: https://code.claude.com/docs/en/commands (`/batch`).
