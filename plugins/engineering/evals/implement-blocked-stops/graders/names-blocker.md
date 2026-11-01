---
type: llm
---

The user typed `/engineering:implement SHOP-42`. The project's CLAUDE.md names the tracker: Markdown files in `tickets/`. SHOP-42 is `ready-for-agent` but is blocked by SHOP-41, which is `in-progress` and has no stack base or pushed branch. Judge the trace and the final reply. Pass only if all hold:

1. The run read `tickets/SHOP-42.md` and `tickets/SHOP-41.md` (or otherwise read SHOP-41's state).
2. The final reply says the build stopped because SHOP-41 is an open blocker.
3. No `mean` function was written, and no branch with a commit was made.
