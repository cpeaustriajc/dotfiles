---
name: triage-unproven-bug
runs: 2
max_turns: 6
allowed_tools: [Skill, Read, Glob, Grep]
---

triage issue #318 and write the agent brief so an agent can fix it. title: "saving a draft loses the title". the reporter's steps: sign in as an editor, open any draft, rename it in the title field, press Cmd+S, then reload the page, and the old title is back. chrome 141 on macos. the steps look clear to me. the repo isn't here, so nobody has run them yet.
