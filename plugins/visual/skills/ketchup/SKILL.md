---
name: ketchup
description: "This skill should be used when the user types /ketchup. Catch the user up on what changed in this chat since their last message, in a few plain sentences and small visuals. Give each action item just enough context to make the call. Use for /ketchup."
disable-model-invocation: true
---

# Ketchup

Catch the user up on what changed since their last message before `/ketchup`; notifications and
subagent results are not theirs. Assume they remember nothing after it. Use
[`/bro`](../bro/SKILL.md)'s voice. Each step's rules: `references/reply.md`. Harness:
`references/claude-code.md`.

1. **Gather, read-only:** your work, subagent reports, others' messages, and the live state of
   each PR, CI run or agent this chat touched. Check each number against its source.
2. **Find the action items:** calls only the user can make.
3. **Open** with how many things need the user. Nothing happened and nothing waits: say so, stop.
4. **Show** the work's screenshots and videos, then any diagram that explains a change.
5. **Summarise:** one spoken bullet per thing asked, with its state.
6. **Action items:** each call with your recommendation, why, and what happens with no answer.
7. **Choices** after the list.

Keep the text well under 150 words, visuals aside. Give each fact once. Short of words: cut
history before action items.

## Credit

Adapted from pstack's `ketchup` by Lauren Tan (MIT; see `LICENSE`).
