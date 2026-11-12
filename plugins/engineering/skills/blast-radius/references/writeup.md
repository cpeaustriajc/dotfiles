# Writeup

The reply of `SKILL.md`. Proof levels are the ones in the method reference. Write it through `references/ai-tells.md`, cite real
code, and strip anything private before it goes anywhere public.

- **What it does**, including the part that isn't obvious.
- **The one fact it's safe because of**: the fact, the proof level it reached, and the proof. If
  you couldn't prove it, write unproven.
- **Risks**: each names how it breaks, the `file:line`, how likely and how bad, its proof level,
  and how to check. Paste the proof for the ones that matter.
- **Cleared**: what you checked and why it's fine.
- **Before you merge**: the cheapest test or repro that catches the real bug, including the
  script you wrote.

Then the risk map: the change in the middle, one box per confirmed risk with its `file:line` and
proof level, and the cleared risks apart in their own group. A click on a risk asks how to check
it. Mechanics and the text fallback are in the adapter.
