# Review loop and checklist

Step 9 of SKILL.md. Look at the picture the way the user will: in the real page, on desktop and on
a phone, at full size and zoomed in.

1. Set up once per session in a scratch folder:
   `mkdir -p <scratch>/shot && cd <scratch>/shot && npm i playwright && npx playwright install chromium`.
   Run the scripts from that folder by their path in this skill; `shoot.mjs` loads Playwright from
   the current directory.
2. Serve the page on a free port and shoot it with `scripts/shoot.mjs --url <url> --out <prefix>`.
   It shoots each `--size` (default `1600x1000` and `390x844`) at device pixel ratio 2.
   `--section '#id' --at 0..1` scrolls through a sticky section, `--y` scrolls to a pixel, and
   `--repeat N --every ms` catches moving parts. A page error it prints means the picture is not
   the one you think.
3. Judge the whole frame first: tradition, value plan, space.
4. Cut 2× crops of every element: `uv run --with pillow python scripts/crop.py SHOT OUT x,y,w,h:name ...`
   (boxes in CSS pixels). Answer the checklist for each crop.
5. Fix, re-shoot, and compare with the previous shots. Keep before and after shots and the exact
   commands for the commit message.

## Checklist

- **Proportion.** Do figures, animals, vehicles, props and buildings match their measurements? Does
  every pose's reach work?
- **Pose and mood.** Does each body carry its weight the way the reference does?
- **Grounding.** Does everything touch its support, with a contact accent? Is anything hovering a
  few pixels off?
- **Depth order.** Does each object overlap the way its ground contact says, and does every moving
  object stay in order along its whole path?
- **Space.** Do the horizon and scale with distance agree? Is there an empty gap between two
  scales? Are any edges unintended?
- **Light.** Do shadows and highlights come from one source? Do reflections sit on a surface that
  can reflect?
- **Tradition.** Would this sit beside the reference works, or does any part read as clip-art?
- **Structure at zoom.** Does every 2× crop of a hero element show built structure (branches inside
  crowns, plate edges and environment bands, grass in tufts) and at least three value steps?
- **Medium.** Did fine detail survive the stylisation? Is any repeating texture cut, smeared or
  evenly spread?
- **States.** In every era, time of day and viewport, does each object belong, and do the
  in-between frames hold?
- **Accuracy.** Does each costume piece, building, colour and canon detail match a source? Are
  proxies and UNVERIFIED items named?
