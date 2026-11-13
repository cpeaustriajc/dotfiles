# Briefing a Claude model

Read the section for the model you are about to prompt, and "All models". Source: Anthropic's
prompting pages, fetched 2026-11-13 as markdown from
`platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md`
and `.../prompting-claude-<model>.md` (the index is `platform.claude.com/llms.txt`). Fetch them
again when a model ships. Brackets name the page section.

## All models

- Give goal, reasons and what done looks like; skip the steps. [Add context; Leverage thinking] Seen here: a brief dictated a design from an unchecked reading of an API, and the worker redid it.
- Say what to do, not what to avoid. [Control the format]
- Ask for the action: "Change this function", not "Can you suggest changes". [Tool usage]
- Examples: three to five, varied, in <example> tags. [Use examples effectively] Seen here: a single draft text was copied word for word.
- Long material first, the ask last. [Long context prompting]
- Ask for a check before it reports done. [Leverage thinking]
- Don't ask for its reasoning in the reply; refusals on Fable, Opus, Sonnet. Ask for a short explanation. [Safeguard refusals]
- "Answer directly" does not reduce thinking on Haiku, Sonnet or Fable; lower effort does. [Calibrate effort]

## Haiku 5.5

- Low effort or a long prompt: it stops early and skips checks. Add: "Keep working until everything asked is done; stop to ask only when you can't go on or before a risky step. When done and checked, report; mention extra features, docs or refactors instead of doing them." [Prevent early stopping]
- Code: "Run a real check that exercises the change before reporting done; a syntax check does not count; if none can run, say which." [Tell coding agents to verify]
- Search: give today's date. "Search regardless of confidence" made half of no-search prompts search. [Accurate search results]

## Sonnet 5.5

- Low and medium effort: it checks in early. Use the Haiku "Keep working" text; without its second half it adds tests, docs and files. [Steer initiative and scope]
- Ideas or a plan: "Give that and stop; build only when told." [Steer initiative and scope]
- At xhigh and max: "Don't start extra review rounds or reviewer subagents unless asked" cut cost by a third. [Steer initiative and scope]
- Low effort skips checks; use the Haiku check line. [Verification on coding tasks]

## Opus 5.5

- Starts fast; on loose tasks name the sources to read first. [Explore context in multiapp workflows]
- Unattended: name the stops to avoid (a summary announcing the next step, an offer to continue, decisions that block nothing) and the stop wanted (nothing can move without the user). [Unattended agentic runs]
- Drop "think carefully" lines. [Thinking instructions in chat]

## Fable 5.2

- "Never" is taken as absolute; write the exception ("ask before deleting"). Name the steps needing approval; "messages to outsiders" held half of routine requests. [Keep caution from piling up; Approvals]
- Ownership sets structure. "You are the owner of this codebase; its design is up to you" lifted consolidation from under 10 to 75 percent of runs, with 70 to 80 percent more tokens and unasked changes; "no drive-by refactors" does not cancel it. Omit it when the user owns the code. [Say who owns the code]
- Low and medium effort stop early: "Don't stop while you owe work; diagnose ordinary obstacles; leave deliberate blockers and report them." [Finish the whole task]
- Hard style limits make prose choppy; for reports say the reader saw none of the tool calls. [Review prompts; Make reports easy to follow]
