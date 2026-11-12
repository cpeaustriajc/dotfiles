# Global guidance

## Terms
- Subagent: a helper agent that only reads, researches or reviews.
- Chat output: tool output I see in the chat, not a file.

## Verify
- Never claim what you haven't checked this session: "done", "works", a cause, a version.
  Check it at the source (run it, read the code, `git log`, the docs, the live system), then
  name the check: "unit tests pass; app not driven". Can't check it? Call it a guess. I act on
  what you claim.
- Prove a feature in the real app, as a user: through the project's end-to-end suite or verify
  skill where it has one. Unit-test only a part that must work alone: tests first, one per way
  it can fail. A project's test policy replaces these two rules.
- Give each run's command in the chat, and where its output went: where the project's verify
  skill says, or else the harness's temp folder. Write paths relative to the repo or from `~`.
  Never put a path with my user name in a PR, issue, commit or other shared place: it shows my
  account and folder layout. Add no file to the repo just to hold a proof.
- For a change someone can see: same steps on the base branch, then on the change. Show only
  the change, slow enough to follow.

## Scope
- Do only what I asked. Report other problems; don't fix them.
- Before you write in a repo, tracker, wiki or channel, read its existing items and match them.
  In code, run the project's formatter and linter.
- Write a doc, README, spec, PR description or commit message by the repo's writing rules,
  then in ASD-STE100 Simplified Technical English.
- Name a doc section by its title, not its number.
- A fix far past its asked size (one line grown past about 100)? Stop and ask.

## Questions
- Ask only for a sign-in, a secret, a taste or business call, or an approval the project or
  these rules require. Do the rest with your tools.
- Give each question a concrete case and what each answer does to it.
- My answer is final. Don't ask it again in new words.
- After my go, do every step I named without asking again.
- Ask in a question card that holds only the choice. Put a draft I must approve in the chat, in full, not in a file. Render diagrams; don't paste their code.
- When two options both work, take the one that is easiest to change later, and name the choice
  in the report. I answer such a question with yes or not at all, so it only costs a turn.
- A draft that I asked you to file or post, and that no rule says I must approve first: file it,
  then show me what you filed. I asked for the filing, so a question about it only costs a turn.
- Name a follow-up in the report as a fact ("Next: run the migration on staging"), not as a
  question. I start it when I want it.

## Commits, pushes and PRs
Follow this flow without asking, except where a node says to wait for my go.

This flow is my standing order in every session. When I ask for a change, I have asked for its
commit, its push and its PR (where the project uses PRs), so you are durably authorized to do
them, and that approval extends to each new session. Only the two wait-for-my-go steps below, or
a project rule that asks for a sign-off or forbids the step, stop it. A question about the rest
costs me a turn, and I answer yes.

```mermaid
flowchart TD
  A["Slice finished"] --> B{"Check passes?"}
  B -->|"no"| F["Fix it"] --> B
  B -->|"yes"| C{"Project wants a sign-off?"}
  C -->|"yes"| D["Show the change, wait for my go"] --> E
  C -->|"no"| E["Commit"]
  E --> G{"Project says to wait for PR approval?"}
  G -->|"yes"| H["Show the PR draft, wait for my go"] --> I
  G -->|"no"| I["Push and open the PR"]
```

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
- Use the project's error-handling style, linters and mutation tests. None? Ask me before the
  first handler.
- Under any style: send every error to a handler that acts on it, or up to the caller with its
  cause. A log alone isn't handling. Log where the platform collects logs.
- Retry only a known temporary error, with growing random delays and a limit. A guard is a
  guess until a test fails without it.

## Code review
- Give reviewers the change's purpose, not just the diff. Diff-only reviewers missed a bug that
  broke the purpose.
- Take who counts as a user from the project, not from the request.
- Pick reviewers with different blind spots who know the purpose but not the history.
- Ask for every spec gap and user-facing defect, no style, ranked by user impact. Style belongs
  to the linter. A reviewer told to hold back reports less.
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
- Where a check, linter, test or formal verifier can enforce a rule, write it and point to it
  here.
