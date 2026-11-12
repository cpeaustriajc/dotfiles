# Prompts

Paste one into a session, with the code or decision it should look at. Each engineering prompt is one
rule turned into a search; the last two rewrite a message. Ask the agent to name the rule that changed each decision.

## Model the Domain

```text
Find all implicit state machines, booleans kept in sync, and branch chains that one table or union would replace.
```

## Foundational Thinking

```text
Find logic written before its data shapes, and one capability spread as special cases across callers.
```

## Type System Discipline

```text
Find interchangeable primitives, hand-copied schema types, casts on external data and non-exhaustive variants.
```

## Boundary Discipline

```text
Find checks inside the system that belong at its boundary, and logic that cannot run without the framework.
```

## Make Operations Idempotent

```text
Find steps that break when they run twice or after a crash at any point.
```

## Separate Before Serializing Shared State

```text
Find two writers on one file, key or branch. Give each its own target before you add a lock.
```

## Laziness Protocol

```text
Find DRY violations and tramp data.
```

## Subtract Before You Add

```text
Find YAGNI violations: dead code, stubs and guards.
```

## Minimize Reader Load

```text
Find wrappers with one caller, and state wider than it needs to be.
```

## Redesign From First Principles

```text
Find a new flag beside an old path. Say what you would build from zero with this requirement.
```

## Outcome-Oriented Execution

```text
Find shims that exist only to keep a middle step green.
```

## Exhaust the Design Space

```text
This has no precedent. Build 2 or 3 small prototypes and compare them before you pick one.
```

## Experience First

```text
Find options added because they were easy, and reports that list files instead of effects.
```

## Build the Lever

```text
Find hand edits that a script could do and prove.
```

## Fix Root Causes

```text
Find guards for states that must never exist, and sibling copies of the same bug.
```

## Attack the Premise

```text
Find fixes that share one untested premise. Test the premise before the next fix.
```

## Prove It Works

```text
Find "done" that rests on a proxy: a cache, an old build or a self-report.
```

## Test Behavior, Not Implementation

```text
Find tests that pass when behavior breaks, or fail on a refactor.
```

## Explain the Number

```text
Find numbers with no named limiter: the core, lock, disk or network that capped them.
```

## Sequence Verifiable Units

```text
Find checks against a stale base, and commit orders that prove nothing.
```

## Find Implicit Invariants

```text
List every invariant this code assumes but never enforces. Show the path that breaks each one.
```

## Follow the Dependencies

```text
Map what depends on what. Find Dependency Rule violations (adapters, flags, special cases that exist only to make them work), and say the simpler shape the dependencies already imply.
```

## Re-pitch

```text
That last message did not land. Say it again in plain words, in the project's own terms: first the context I was missing, then what is true now and why, then one diagram of boxes and lines, then your one question with your recommendation. Aim simpler, not shorter.
```

## Unslop

```text
Rewrite this text without AI slop (the tells in plugins/engineering/skills/blast-radius/references/ai-tells.md). Keep every claim and the tone. Return only the text.
```

Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, under
the MIT licence: [PROMPTS.LICENSE](PROMPTS.LICENSE).
