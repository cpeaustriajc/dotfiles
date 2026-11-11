---
name: feature-files
description: >
  This skill should be used when writing or updating a feature file, when an E2E check needs to
  know how to reach and drive an area of the app, or when a UI change makes a feature file wrong.
  Not for writing the test code.
---

One small file per feature, so a check reads only its area instead of rediscovering the app.

- **Where**: the project's folder, else `references/features/` in its verify skill. Name each
  file as a user calls the feature (`checkout.md`); a `README.md` table lists them.
- **Write** per `references/template.md`, only for features the next change touches.
- **Launch steps** stay in the harness's run recipe, so two recipes cannot drift:
  `references/claude-code.md`.

To verify a change:

1. **Find** the 1 or 2 files whose **Code** or **Tests** lines match the changed paths. Read only
   those.
2. **Run** the **Check** in the real app, and each **Path to cover** the change could affect.
   Save the evidence; say where, with the command that reruns it.
3. **Fix** a file the app no longer matches, in the same change: a wrong feature file is worse
   than none.
4. **Add** a bug the file did not predict to **What tends to break**.
