---
name: implement-stacked-builds
runs: 2
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep, Bash, Edit, Write, Agent]
append_system_prompt: "Non-interactive run: nobody answers questions. gh is not installed, so no PR can be opened: push the branch and report what the PR body would hold."
---

/engineering:implement SHOP-45
