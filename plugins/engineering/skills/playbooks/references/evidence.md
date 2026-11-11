# Evidence

What counts as proof in every playbook (step 3 of `SKILL.md`).

Evidence means driving the real app and leaving a command that reruns the check, plus its trace,
screenshots or video. Read the project's feature file for the area first, if it has one
(`feature-files`).

- A recorded run with exact checks is the proof. An AI agent that clicks through the app explores
  or reproduces; its "looks right" is never the proof.
- Give an agent one case or one goal per run, never a whole checklist in one thread: each call
  resends the thread, and one question stops every case behind it.
- Name concrete inputs and the property they test ("the total equals the sum of the lines for any
  cart of 1-30 items"), never only a technique ("use property tests").
