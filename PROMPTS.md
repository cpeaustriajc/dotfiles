# Prompts

Paste one into a session, with the code or decision it should look at. Each is one engineering
rule written as a hunt. Name the rule in the agent's reply, so you can see which one changed a
decision.

1. **Model the Domain**: Find all implicit state machines, booleans kept in sync, and branch
   chains that one table or union would replace.
2. **Foundational Thinking**: Find logic written before its data shapes, and one capability
   spread as special cases across callers.
3. **Type System Discipline**: Find interchangeable primitives, hand-copied schema types, casts
   on external data and non-exhaustive variants.
4. **Boundary Discipline**: Find checks inside the system that belong at its boundary, and
   logic that cannot run without the framework.
5. **Make Operations Idempotent**: Find steps that break when they run twice or after a crash at
   any point.
6. **Separate Before Serializing Shared State**: Find two writers on one file, key or branch.
   Give each its own target before you add a lock.
7. **Laziness Protocol**: Find one decision made in two places, and parameters passed through
   untouched.
8. **Subtract Before You Add**: Find dead code, stubs and guards that no spec or use needs.
9. **Minimize Reader Load**: Find wrappers with one caller, and state wider than it needs to be.
10. **Redesign From First Principles**: Find a new flag beside an old path. Say what you would
    build from zero with this requirement.
11. **Outcome-Oriented Execution**: Find shims that exist only to keep a middle step green.
12. **Exhaust the Design Space**: This has no precedent. Build 2 or 3 small prototypes and
    compare them before you pick one.
13. **Experience First**: Find options added because they were easy, and reports that list files
    instead of effects.
14. **Build the Lever**: Find hand edits that a script could do and prove.
15. **Fix Root Causes**: Find guards for states that must never exist, and sibling copies of the
    same bug.
16. **Attack the Premise**: Find fixes that share one untested premise. Test the premise before
    the next fix.
17. **Prove It Works**: Find "done" that rests on a proxy: a cache, an old build or a
    self-report.
18. **Test Behavior, Not Implementation**: Find tests that pass when behavior breaks, or fail on
    a refactor.
19. **Explain the Number**: Find numbers with no named limiter: the core, lock, disk or network
    that capped them.
20. **Sequence Verifiable Units**: Find checks against a stale base, and commit orders that
    prove nothing.
21. **Find Implicit Invariants**: List every invariant this code assumes but never enforces.
    Show the path that breaks each one.
22. **Follow the Dependencies**: Map what depends on what. Find code bolted on against that
    direction (adapters, flags, special cases that exist only to make it work), and say the
    simpler shape the dependencies already imply.

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, under
the MIT licence: [PROMPTS.LICENSE](PROMPTS.LICENSE).
