---
type: llm
---

The user typed `/engineering:implement SHOP-45`. The tracker is Markdown files in `tickets/`, as CLAUDE.md says. SHOP-45 is `ready-for-agent`, blocked by SHOP-44, which is `in-review` with its branch `shop-44` pushed. SHOP-45 names `stack-base: shop-44`. Its criteria: `mean([2, 4])` returns 3, and `mean([])` returns 0. Judge the trace and the final reply. Pass only if all hold:

1. The run did not stop at the blocker. It built SHOP-45.
2. The new branch starts from `shop-44` (the trace shows a switch or checkout from shop-44, or the branch contains the commit "SHOP-44: add count()"), not from main.
3. A `mean` function and a test for each criterion were committed on that branch. Nothing was committed on main.
4. The tests were run, and passed, before the final reply.
5. The final reply has one verdict row for each of the two criteria (VERIFIED, NOT VERIFIED or INCONCLUSIVE) with the command and its evidence, and says the PR would hold `Closes SHOP-45`.
