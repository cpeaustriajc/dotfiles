---
name: unslop
description: "This skill should be used when the user types /unslop with text. Cut AI tells from any writing."
disable-model-invocation: true
argument-hint: "<text>"
---

# Unslop

1. Scan the text for each numbered pattern in `references/patterns.md`.
2. Rewrite each hit. Keep every claim and the intended tone.
3. Return the rewritten text.

## Credit

Adapted from pstack's `unslop` by Lauren Tan (MIT; see `LICENSE`).
