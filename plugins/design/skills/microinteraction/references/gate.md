# The gate

Step 3 of `SKILL.md`. A candidate must pass all four questions, in order. Record each answer for
the report.

## 1. Frequency: how often does a user see this?

| Frequency | Verdict |
| --- | --- |
| 100+ times a day (keyboard shortcuts, command palette, core navigation) | Reject. No animation. |
| Tens of times a day (hover states, list navigation, frequent toggles) | Reject, or only fast, subtle motion |
| Occasional (modals, drawers, toasts, settings) | Eligible: standard animation |
| Rare or first-time (onboarding, empty states, success, celebration) | Eligible: the delight budget lives here |

A keyboard-initiated action (command palette, shortcut, focus jump) is a disqualifier. Repeated
hundreds of times a day, animation makes it feel slow and disconnected. Raycast has no open or
close animation, and that is the best experience.

## 2. Purpose: why does this animate?

Name one of these:

- **Feedback:** the interface heard the user (press scale, hold-to-confirm fill).
- **Spatial consistency:** where something came from or went (a toast enters and exits the same
  edge; a panel grows from its trigger).
- **State indication:** a state change made legible (a morphing button, an expanding accordion).
- **Preventing a jarring change:** content that teleports, appears or vanishes with no bridge.
- **Explanation:** motion that shows how a feature works (marketing or onboarding only).
- **Delight:** only at the rare or first-time frequency.

A candidate with no purpose from this list is rejected.

## 3. Speed: does it fit the budget?

UI motion stays under 300ms:

| Element | Duration |
| --- | --- |
| Press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| Marketing, explanation | Can be longer |

A moment that works only as a slow, showy animation fails.

## 4. Function: does motion help or hinder here?

Decoration hinders functional, dense UI. A mouse-tracking effect suits a marketing page; on a
banking app's graph, no animation is better. Data the user reads or acts on does not move for
style.
