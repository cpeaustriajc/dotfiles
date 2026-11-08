---
name: tickets-visual-loop-size
runs: 2
max_turns: 6
allowed_tools: [Skill, Read, Glob, Grep]
append_system_prompt: "Non-interactive run: nobody answers questions and no tracker is connected. Write nothing to a tracker. End with the full proposed list of items as your final message."
---

the blog redesign spec is confirmed, cut the next slice. R1 article pages use the new type scale, R2 the first letter of each article is a painted initial that matches the design board, R3 the home page lists posts in the new card layout. the design board is design/board.html, 3.8 MB with the images built in, plus 12 crops of the painted initial. the agent that builds each item checks it by screenshot at 375, 768 and 1280 px, crops the initial, compares it to the board and fixes it until it matches. I want one ticket per requirement, each with 3 checks.
