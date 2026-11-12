# Claude Code

## Proof scripts

- Write each proof script in the session's scratchpad directory, never beside the code. Run it
  from the project root so it imports the code the app ships.
- Paste the script, the command, its exit code and its output in the writeup. The OS empties the
  scratchpad, so the writeup is the copy the owner runs again.
- Never edit the change's own files to prove a fact.

## Risk map

- Call `mcp__visualize__read_me` once with `modules: ["interactive"]`, then
  `mcp__visualize__show_widget` with an HTML map.
- The change sits in the middle: one box with its one-line summary, and the safety fact under it,
  marked proven (with its proof level) or unproven.
- Around it, one box per confirmed risk: how it breaks, its `file:line`, its likelihood and cost,
  and its proof level, joined to the change by a line.
- The cleared risks sit apart in a muted group, labelled Cleared, each with its `file:line` and the
  reason it is fine.
- A click on a risk box calls `sendPrompt("How do I check <file:line>: <how it breaks>?")`. A click
  on a cleared box calls `sendPrompt("Why is <file:line> cleared?")`.
- Without the visualize tools (terminal, headless evals), print a mermaid `flowchart LR` block:
  a `change` node, one node per risk with its `file:line` and level joined to it, and a
  `subgraph Cleared` with no line to the change.
