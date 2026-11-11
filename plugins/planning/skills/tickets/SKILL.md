---
name: tickets
description: >
  This skill should be used when the user says "break this into tickets", "cut the next slice",
  "write the issue", "file these bugs as issues" or "rewrite this ticket", or a ticket is too
  long. It writes slices, or one bug or chore.
---

Read `../shape/references/top-down.md` first; its adapter rows say where each part lands.

1. Draft spec: cut only Demo prototypes. Else list its requirements and which items cite them.
2. Read facts from the fetched trunk; search open and recent closed items. A branch
   behind the trunk files work already done.
3. Cut the next slice only:
   - vertical slices, prefactors first, blockers named, riskiest first;
   - each fits one session of its cheapest builder: `references/sizing.md`;
   - two or more code items in Implementation stack: `references/stacking.md`.
4. Show the slice: title, requirements, what I see, blockers, builder, estimate, stack base.
   Iterate until I approve. Other questions are spec gaps for `shape`.
5. Write each item per `references/item-template.md`; type, Bug or wide change per
   `references/item-kinds.md`.
6. Write blockers first, a stack bottom first. Run the tree check (`--launch` at Launch).
