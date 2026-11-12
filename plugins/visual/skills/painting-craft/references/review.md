# Review loop

Step 9 of SKILL.md. Look the way the user will: the real page, desktop and phone, full size and
zoomed.

1. Once per session, in a scratch folder:
   `mkdir -p <scratch>/shot && cd <scratch>/shot && npm i playwright && npx playwright install chromium`.
   Run the scripts from there by their path in this skill; `shoot.mjs` loads Playwright from the
   current directory.
2. Serve the page on a free port and shoot it: `scripts/shoot.mjs --help`.
3. Whole frame first: tradition, value plan, space.
4. 2× crops of every element (`scripts/crop.py --help`, boxes in CSS pixels). Check each crop.
5. Fix, re-shoot, compare. Keep before/after shots and exact commands for the commit message.

Checklist: proportion (every reach works); pose; grounding; depth order along every mover's path;
space (no empty gap between scales); one light; tradition (no clip-art part); structure at zoom
(each hero crop shows built structure and at least three value steps); medium (no smeared or evenly
spread texture); states (every era, time, viewport, in-between frames); accuracy (proxies and
UNVERIFIED named).
