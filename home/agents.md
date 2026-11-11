# Global guidance

## Terms
- "I" and "me" mean the user.
- Subagent: a helper agent that only reads, researches or reviews.
- Chat output: tool output I see in the chat, not a file.

## Verify
- Never claim what you haven't checked this session: "done", "works", a cause, a version.
  Check it at the source (run it, read the code, `git log`, the docs, the live system), then
  name the check: "unit tests pass; app not driven". Can't check it? Call it a guess. I act on
  what you claim.
- Prove a feature in the real app, as a user. Unit-test only a part that must work alone: tests
  first, one per way it can fail. A project's test policy replaces these two rules.
- Give each run's exact command in the chat. Save its output where the project's verify skill
  says, or else in the harness's temp folder, and give the path. Add no file to the repo just
  to hold a proof.
- For a change someone can see: same steps on the base branch, then on the change. Show only
  the change, slow enough to follow.

## Scope
- Do only what I asked. Report other problems; don't fix them.
- Before you write in a repo, tracker, wiki or channel, read its existing items and match them.
- Name a doc section by its title, not its number.
- A fix far past its asked size (one line grown past about 100)? Stop and ask.

## Questions
- Ask only for a sign-in, a secret, a taste or business call, or an approval the project or
  these rules require. Do the rest with your tools.
- Give each question a concrete case and what each answer does to it.
- My answer is final. Don't ask it again in new words.
- After my go, do every step I named without asking again.
- Put a draft I must approve in the chat, not in a file.

## Commits, pushes and PRs
- Commit each finished slice once its check passes, without asking, unless the project wants a
  sign-off first.
- Push and open the PR without asking, unless the project says to wait for approval. Then show
  the draft in the chat and wait for my go.
- Ship one project's build tickets as a PR stack in blocked-by order, each branch off the last,
  unless the project sets its own branching. Branch other work off main. A restack costs more
  than the build.
- A build keeps failing review? Rebuild it from the spec; don't patch it.

## Long commands
- Run anything longer than a few seconds in the background, with output in the chat:
  `cmd 2>&1 | tee <log>`.
- Say a tool prints no progress only after you read its output or source. Say it once, at the
  start.

## Error handling
- Use the project's error-handling style. None? Ask me before the first handler. These rules
  hold under any style:
- Send every error to a handler that acts on it, or up to the caller with its cause, even when
  no caller waits. A log alone isn't handling.
- Retry only a known temporary error, with growing random delays and a limit.
- Log where the platform collects logs, so the log survives the crash.
- A guard is a guess until a test fails without it.

## Code review
- Give reviewers the change's purpose, not just the diff. Diff-only reviewers missed a bug that
  broke the purpose.
- Take who counts as a user from the project, not from the request.
- Pick reviewers with different blind spots who know the purpose but not the history.
- Ask for every spec gap and user-facing defect, no style, ranked by user impact. A reviewer
  told to hold back reports less; one asked for style always finds some.
- Prove a finding on the user's path when you can. Run-time bugs pass read-only reviews.
- Report each kind of bug once, with its instances.
- Stop when a pass finds nothing a user would hit. Findings keep coming? Question the design.

## Delegation
- Before parallel attempts at one task, tell me how you'll pick the winner.
- Subagents write no code and ask no questions.
- A subagent result without evidence gets one more try. A second miss is a gap, not a pass.

## Instruction files
- Put rules, preferences and pointers to sources here. Put a decision, finding or status in the
  tracker or the commit: here it goes stale unseen.
- Fix or delete a wrong line; don't add a newer one beside it.
- Keep a line only if the agent errs without it. Write its scope and exception into the rule.
- Load knowledge only when needed: a rule scoped to its files, a procedure in a skill.
- Where a check can enforce a rule, write the check and point to it here.
