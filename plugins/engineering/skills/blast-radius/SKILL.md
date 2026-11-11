---
name: blast-radius
description: "This skill should be used when the user types /blast-radius on a change: find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust."
disable-model-invocation: true
argument-hint: "<change: PR, branch, commit or diff>"
---

Find what `$ARGUMENTS` breaks outside its diff (empty: the branch against its base, plus
uncommitted edits). Callers are one grep away; find the breakage grep won't show. Detail per step:
`references/method.md`. Writeup: `references/writeup.md`. Adapter:
`references/claude-code.md`.

1. Read the change and what it now does that the diff doesn't spell out. Pull its PR and commits
   by the Seed anchor step of `../why/SKILL.md`.
2. Find the one fact it's safe because of; most risks clear when it holds.
3. Look where grep stops: library source, run timing, data formats, flags.
4. Rate each risk by real chance and cost. Cite real lines; never invent a caller or an API.
5. Prove the fact by running real code: a writeup that sounds right reads the same whether or not
   it is true.
6. A big or wide change also gets `interrogate`.

Reply with the writeup, the fact proven or marked unproven, then the risk map.

## Credit

Adapted from pstack's `blast-radius` by Lauren Tan (MIT; see `LICENSE`).
