---
type: llm
---

The user typed `/engineering:implement SHOP-43`. CLAUDE.md names no tracker. The tickets are Markdown files in `tickets/`, and a commit message cites SHOP-40. SHOP-43 has `state: needs-info`. Judge the trace and the final reply. Pass only if all hold:

1. The run found and read `tickets/SHOP-43.md` without asking which tracker to use.
2. The final reply says SHOP-43 is not ready to build (its state is needs-info) and points to triage or to answering its open question.
3. No `median` function was written.
