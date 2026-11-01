# Global guidance

## Terms
- "Me" and "I" mean the user.
- Thread: a separate Claude session that builds code.
- Subagent: a helper agent that only reads, researches or reviews.
- Harness output: the tool output that I see in the chat, not a file.

## Precedence
- A project's test policy overrides the Testing section.
- A project's error-handling style overrides the style of the Error handling section. Its rules
  still apply.
- A project that needs a sign-off before a commit overrides the commit rule in Workflow.

## Facts
- Before you state or use a fact that can change (a package version, an API, what is installed,
  configured, tracked, deprecated or decided), check its source now: the code, upstream main,
  git log and PRs, the tracker, the vendor docs or the live system.
- If you cannot check a fact, label it a guess or ask me.
- When a CI run fails in seconds with no steps, it did not run the code. Read its annotations
  (`gh run view <run-id>`) before you change code.
- Refer to a document section by its title, not its number — numbers change.

## Scope
- Change only what I asked. Report other problems; do not fix them.
- When a fix grows far past its asked size (example: a one-line fix past about 100 lines), stop
  and ask me.

## Questions
- Ask me only for a sign-in, a secret, or a decision of taste or business. Do everything your
  tools can do.
- Give every question a concrete example: a specific person, input or situation, and what each
  answer makes happen in it.
- Treat my answer, picked or typed, as final. Never ask it again in new words.
- After my go, do every step I named with no new question.
- Put a draft that I must read or approve in the chat, not in a file.

## Workflow
- Commit each finished slice when its check passes, without asking. This overrides "commit only
  when asked".
- When a build fails review again and again, rebuild it fresh from the spec. Do not patch it.

## Long commands
- Run a command that can take longer than a few seconds in the background.
- Send its output to the harness output, never only to a file. To keep a log too, pipe it
  through `tee <file>`.
- Say that a tool prints no progress only after you read its output or its source. Say it once,
  when the command starts.

## Testing
- Prove a feature by driving the real app as a user does. Prefer these as the only tests.
- Unit-test a part only when it must be tested alone. Write its tests first: one case for each
  way it can fail.
- For a test run that I rely on, save its exact command and evidence where another person can run
  it again, and tell me where.
- For a PR or issue whose change a user, QA or caller can observe, show a before and an after of
  the same state: same steps, on the base branch and on the change. Show only the change, at a
  speed a person can follow.

## Error handling
- Where the project has no error-handling style, ask me before the first handler.
- Send every error, including one that no caller waits for, to a handler that acts on it, or up
  to the caller with its cause. A log alone is not handling.
- Retry only an error known to be temporary: growing random delays, with a limit.
- Write a log where the platform collects it, so that it survives the crash it describes.
- Treat a guard as a guess until a test fails when you remove the guard.

## Code review
- Give reviewers the purpose of the change, not only the diff — diff-only reviewers missed a bug
  that broke the purpose.
- Take who counts as a user from the project, not from the request.
- Use reviewers with different blind spots who know the purpose but not the work history.
- Ask reviewers for every finding — a reviewer told to hold back reports less, not better. Rank
  findings by user impact.
- When you can, prove a finding on the user's path — run-time bugs pass read-only reviews.
- Report each kind of bug once, with its instances.
- Stop when a pass finds nothing a user would hit. If findings continue, question the design.

## Delegation
- The session I talk to plans, writes specs, starts threads and reviews their work. Threads
  build.
- A thread shares my checkout unless another thread edits the same repo.
- Give small fixes for one repo to one thread.
- Push a thread's branch and open its PR without asking me.
- Start new work in a fresh thread, not an idle one — an idle thread reads its full history again.
- Ship the build tickets of one project as one PR stack in blocked-by order, each branch off the
  previous one. Branch other items off main. A restack costs more than the build.
- Before parallel attempts at one task, tell me how you will pick the winner.
- Subagents write no code and ask no questions.
- Put subagents on a cheaper model than yours unless a skill names an exception. Raise effort
  when one misreads or loops.
- When a subagent result has no evidence, give it one more try. A second miss is a gap, never a
  pass.

## Instruction files
- Memory and instruction files hold rules, preferences and pointers to sources. Never put a
  decision, finding or status in them — it goes stale unseen.
- Fix or delete a wrong line. Never add a newer line beside it.
- Keep a line only if Claude makes a mistake without it.
- Put knowledge where it loads only when needed: a rule scoped with `paths:` to its files, a
  procedure in a skill. An `@import` still loads in full.
- When a check can enforce a rule, write the check and keep a pointer to it in the file.
- Give a custom agent only the instructions its job needs (`omitClaudeMd: true` when it needs
  none of the project's).

<!-- Sources: https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/best-practices -->
