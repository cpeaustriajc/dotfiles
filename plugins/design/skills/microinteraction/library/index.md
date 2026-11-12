# Motion example library

Each effect is named by its term in Emil Kowalski's animation-vocabulary skill (<https://github.com/emilkowalski/skills>) and has a good and a
bad version. For each version:

- `<version>.html`: the demo page. Its CSS is the recipe.
- `<version>.gif`: the motion as it plays, for the owner. Claude sees only its first frame.
- `<version>-frames.png`: for Claude. Twelve frames evenly spaced in time, each labelled with its
  time, above a plot of the planned curve (line) and the measured progress (dots).
- `<version>-samples.json`: the measured progress at every frame.

| Term | Good | Bad |
|---|---|---|
| Scale in | [good](scale-in/good.html): a popover grows from its trigger, `scale(0.95)` and opacity, 200ms `cubic-bezier(0.23, 1, 0.32, 1)` | [bad](scale-in/bad.html): grows from `scale(0)` at its own centre, 400ms `ease-in` |
| Slide in | [good](slide-in/good.html): a toast rises from the bottom edge with opacity, 400ms `cubic-bezier(0.23, 1, 0.32, 1)` | [bad](slide-in/bad.html): the same path on 500ms `ease-in`, so it starts slow, then stops abruptly |

## Re-make

```
bash plugins/design/skills/microinteraction/library/remake.sh [effect ...]
```

It re-records every demo (or the effects named) and fails when a GIF is wider than 480px or larger
than 150 KB. Needs and options: the header of `remake.sh`.

## Add an effect

1. Make a folder named after the animation-vocabulary term, in lower case with dashes.
2. Write `good.html` and `bad.html` at 480x270. Copy a demo here as the start.
3. Mark up the demo as the header of `record.cjs` says.
4. Run `remake.sh <folder>` and add a row to the table above.
