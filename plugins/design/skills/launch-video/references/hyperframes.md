# HyperFrames: composing and rendering

Install it as a Claude Code plugin (`claude plugin marketplace add heygen-com/hyperframes`, then
`claude plugin install hyperframes@hyperframes`) and read its `hyperframes-core` skill and
`hyperframes/references/plugin-installation.md` before writing a composition. `hf` below is that
file's launcher, `node <PLUGIN_ROOT>/skills/hyperframes/scripts/plugin-cli.mjs`, never `npx`:

```sh
hf init videos/<project> --non-interactive --example=blank --skill=product-launch-video
hf check · hf snapshot --at 2.4,8.1,12.6 · hf render --quality high --output renders/<name>.mp4
```

Spine: its `product-launch-video` workflow; `hf capture <url> -o ./capture --json` for brand
tokens, fonts, text and screenshots. Its audio script only retrieves music, never generates: use
`music.md` and `voice.md`. `check` runs lint first; fix what it reports (hidden-state, `fromTo`,
`<audio>` id and root-composition errors are all lint codes).

## One composition, one timeline

One monolithic `index.html`, one paused timeline at `window.__timelines["main"]`, shot as a oner: a
`#world` element carries the frames and a virtual camera moves between them. Ignore lint's "nested
sections need sub-compositions" (it is about Studio's timeline view). Match cuts and morphs, not
fades; one playful spring at most.

## Traps that cost a render each

- Include `opacity: 0` with any `yPercent` hide (`check` counts moved text as visible).
- Text that changes over time is a pure function of a tweened proxy (`onUpdate` reading
  `proxy.v`), never `tl.call(...)`: calls do not undo when the renderer seeks backwards.
- `tl.shiftChildren(amount, false, after)` moves every earlier-authored tween that starts after
  `after`. Add tweens that keep their times after the shift. A retime once dropped three of five
  cards; the snapshot caught it.
- Opaque children hide lines drawn behind them (a route line read as dashed under white rows).
- A round line cap shows as a dot at full dash offset: keep the path at `opacity: 0` until drawn.
- A spring that travels reads as a twitch: pop in place (scale from 0, damping >= 0.9).
- Compute centres; a dot at x=155 on a line at x=155-161 is 3 px off and visible.
- `check` reports intentional overlaps (a drawer over a list): fix the real ones, say which you left.

## Format-aware master (9:16, 1:1, 16:9 from one source)

One master `index.html` at 1080x1920; the other shapes are generated, so every edit reaches all three.

1. Root carries `data-format="9x16"`; the world sits in `#frame-world`.
2. The script applies a static view transform per shape; anything outside the world that points at
   something inside it is computed from `VIEW`, not hard-coded:
   ```js
   const FORMAT = document.getElementById("root").dataset.format || "9x16";
   const VIEW = { "9x16": { tx: 0, ty: 0, s: 1 }, "1x1": { tx: 151, ty: -104, s: 0.72 },
                  "16x9": { tx: 881, ty: -352, s: 0.85 } }[FORMAT];
   document.getElementById("frame-world").style.transform =
     `translate(${VIEW.tx}px, ${VIEW.ty}px) scale(${VIEW.s})`;
   ```
3. Per-shape layout in CSS keyed on the attribute (`#root[data-format="16x9"] .headline`); wide:
   words left, world right. Choreography that depends on space gets a per-format table.
4. Generate siblings with `scripts/build_formats.sh` (copies the project minus renders, snapshots,
   capture; rewrites root size, `data-format`, body size, viewport). Backups
   count as root compositions: keep none in the folder.
5. Snapshot each shape at the moments that matter before rendering it.
