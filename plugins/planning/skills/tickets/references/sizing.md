# Sizing an item for one session

The test of size is context, not length. The model that cuts the slice is not the model that
builds it. Name the builder: the cheapest model the project's model picks give that kind of work
(a mid-size model for code with design calls, a small one only for mechanical, fully specced
work). Estimate the context a fresh session of that builder uses to finish the item, and
compare the upper estimate with the budget. More than five checks, more than five test cases, a
body over about 1,500 characters and unrelated parts of the code are quick signs to split. A slice that passes all of them can still be too big.

Failure: six stacked items passed every quick sign. The user had to ask if they fit 200–400k with
exploration and proof. Measured, each item needed 140k–400k, and one did not fit 200k.

## The budget

- Use the builder's budget: the project's, when its agent rules or spec state one.
- With none, ask once, beside the slice. Until you have an answer, use 200k.
- Compare the upper estimate, not the middle. An item over the budget is split.

## The estimate

**Estimate = fixed + reading + build + proof.** Give each part as a range, and name the largest
part as the driver.

| Part | What it counts | How to count it |
|---|---|---|
| Fixed | What a fresh session loads before its first turn: system prompt, tools, skills, memory | Measure it with the harness's context view. With no measure, use 85k. |
| Reading | Code, spec, templates, designs and references the item reads before it writes | About 1 token for each 4 characters of text. Each image about 10k with its turns. |
| Build | The files it changes, read again and edited | The size of those files, times the edit rounds. |
| Proof | Test runs, screenshots, crops, and each fix round | Each image about 10k again, in every round. Long test output in full. |

- **Count every image at about 10k.** The image alone costs 1.5–2.5k; in the measured run about
  15 images came with about 150k of messages. 3 widths, a screenshot and a crop each, 3 rounds
  is 18 images, about 180k, before the fixed cost.
- **Reading is the hidden part.** One earlier thread used 17 turns reading templates, content, a
  design board, crops and a skill, and wrote no code.
- **A review loop multiplies proof.** A visual item with a screenshot-crop-fix loop (a painted
  initial) measured 250–400k.

## Make it fit

Shrink the item first. Split it when it is still over the budget.

- **Facts, not sources**, and **narrow references**: see the item template. A file with
  built-in images is never read whole: one shell print of a 3.8 MB reference filled the context.
- **A fixed proof budget** (pages, widths, crops, most fix rounds); with no limit there is no
  upper estimate.
- **Split a visual item with a review loop smaller.** One element or one page for each item, so its
  loop fits with room left.

## The stop rule

Each item names a limit below the budget, with room left to hand over (about 80% of it). Past that
limit, the thread commits what passes, writes a hand-over note on the item (what passes, what
fails, the next step) and stops. A fresh thread starts from the note, not from a full context.

## In the slice list

Each item shows its estimate and its driver, so the user does not have to ask:

```
3. Painted initial, one width (R4). Builder: mid-size. ~150–190k of 200k: fixed 85k, 2 images, 3 rounds.
```

Source: one measured run on 2026-11-07, a blog redesign cut into six stacked items. Its numbers
(fixed cost, image cost, item estimates) are above. Measure again when the harness or the model
changes its fixed cost or image cost.
