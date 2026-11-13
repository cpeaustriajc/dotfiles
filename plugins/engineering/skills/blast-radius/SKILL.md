---
name: blast-radius
description: "This skill should be used when the user types /blast-radius on a change: find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust."
disable-model-invocation: true
argument-hint: "<change: PR, branch, commit or diff>"
---

Find what the arguments (the text after the skill name; `$ARGUMENTS` where the harness fills it in) break outside its diff (empty: the branch against its base, plus
uncommitted edits). Callers are one grep away; find the breakage grep won't show. Detail per step:
`references/method.md`. Writeup: `references/writeup.md`.

1. Read the change and what it now does that the diff doesn't spell out. Pull its PR and commits:
   `git blame` and pickaxe (`git log -S`) for its lines, then their PR and ticket IDs.
2. Find the one fact it's safe because of; most risks clear when it holds.
3. Look where grep stops: library source, run timing, data formats, flags.
4. Rate each risk by real chance and cost. Cite real lines; never invent a caller or an API.
5. Prove the fact by running real code: a writeup that sounds right reads the same whether or not
   it is true. Write the proof script in the session's scratch directory, never beside the code,
   and run it from the project root. Never edit the change's own files to prove it. Paste the
   script, command, exit code and output in the writeup: the scratch directory gets emptied.
6. A big or wide change also gets `review-loop`.

Reply with the writeup, the fact proven or marked unproven, then the risk map: the change in the
middle with its summary and the safety fact (proven with its level, or unproven); around it one
box per confirmed risk (how it breaks, `file:line`, likelihood, cost, proof level); cleared risks
in a muted group labelled Cleared, each with `file:line` and why it is fine. Draw it with the
harness's interactive widget tool when there is one, each box clickable to ask how to check it;
else a mermaid `flowchart LR` with a `subgraph Cleared` that has no line to the change.

## Credit

Adapted from pstack's `blast-radius` by Lauren Tan (MIT; see `LICENSE`).
