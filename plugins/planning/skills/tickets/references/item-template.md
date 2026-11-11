# Writing an item

Read this before you write an item. Step 5 of `SKILL.md` says when.

Use the project's own work-item template and section names, read fresh as `top-down.md` says.
With none, propose this one once and use it. The rules below hold under any section names.

```markdown
## Context

<Why this exists now, the evidence, and the links that stop someone rediscovering it.>

## Outcome

<The concrete state that is true when this is done. One sentence.>

## Checks

- [ ] R3: <the requirement, quoted word for word>
- [ ] You see: <the screen, message or state that proves it>. Reach it with: <the account, data, switch or payment method that sets up that state>. (test | eye | engineer)
- [ ] <Any finer condition the verifier needs.>

## Out of Scope

- <Only the boundaries that prevent a likely misunderstanding. Omit the section if none.>

## Budget

Estimate: <low–high>k of <budget>k, driven by <the largest part>. Proof: <pages, widths, crops>, at most <n> fix rounds. Stop: past <limit>k, commit what passes, write a hand-over note on this item, and stop.
```

- **Context:** 2–4 sentences plus links. Probe data and architecture go in the pull request or
  the engineering document; link them.
- **Outcome:** from the user's side.
- **Checks:** 3–5, each an observable end state, with at least one **You see** line.
- **Checkboxes.** Write each check as `- [ ]`. Use a numbered list instead when the adapter's
  Checklist row says the tracker drops checkboxes, or the read-back shows them lost; say so once.
- **Each check is reachable.** It names what puts the app in its starting state: the account type,
  the kind of data ("a cart with a premium name", not "a domain"), the test switch, the payment
  method ("bank transfer, left unpaid"). If the state needs a trigger the reader would not guess,
  name the trigger. A verifier who must ask how to reach a state cannot test it.
- **A control's state is one exact word.** A check about a button, link or section says who sees
  it and gives one state: `visible`, `visible, refuses` (quote the message), `disabled` or
  `hidden`. Never "offers nothing", "does nothing", "unavailable" or "blocked": each reads as
  any of the four. Failure: "the panel offers nothing" meant `visible, refuses`; QA passed it as
  "hidden", and agents later treated both as true.
- **Each check names who proves it.** Hand testing, by a person or an agent clicking through, is
  the exception. `test` (the default): an end-to-end test drives it and records a video; the pull
  request gives the one command and where the video and report land. The verifier watches the
  video, so look and wording checks are `test` too. `eye`: no automation can reach it (a real
  device, a third-party inbox); say why. `engineer`: it needs access
  the verifier lacks (a database, a server setting, a burst of requests, a secret key), so the
  engineer runs it and attaches the command and its evidence; the verifier reviews that evidence.
- **Each check has an oracle the verifier can see.** Not "matches what the vendor does" without
  the exact text or state; not a count the screen does not show. A setting that persists says
  where it holds: this tab, this browser, any device.
- **A value on several pages agrees.** When the item shows one value (a price, a total, a count)
  on more than one page, one check names those pages and says each shows the same value for the
  same input: "the same name shows the same price on the shortlist, in the cart and at checkout".
- **Bounded reads.** The item states the measured facts it needs (sizes, colours, copy). It
  links a large reference only as a narrow crop or excerpt.
- **Whole body:** under about 1,500 characters, a quick sign only; the estimate decides the size.
  Longer means split it. Quoted requirement lines do not count; the tree check subtracts them.
- **Behaviour, not file paths or code**: paths go stale. A prototype's snippet that pins a
  decision may be inlined, marked as from a prototype.
- **An item is self-contained**: someone who never saw the conversation can pick it up from the
  item and the spec it links. It settles every design call, so a cheaper builder does not make one
  and the result loses no quality.
- **No "As a … I want … so that" line** unless the product owner asks for it. That sentence is
  where mechanism and timing tend to sneak in.

