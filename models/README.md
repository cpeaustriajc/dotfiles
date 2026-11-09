# Models

Which model does what in this stack, from my Claude Code transcripts (July–October 2026), T3 Code
delegations and Codex reviews on GitHub. Re-check when a new model ships or a tool changes; the picks below are
dated by the models they name. T3 Code is retired, so GPT work now runs in Codex directly and the
T3 counts below are history.

## Who does what

```
            implement            review                 scout / research
 Codex      GPT-6 luna (Codex) ──▶ Codex · GPT-6.1 sol ──▶ fix ──▶ merge
            Opus 5.5 (main)      on every PR
 no Codex   Opus 5.5 (main)  ──▶ interrogate: fresh Claude reviewers (no GPT sub)
 any day    builder: Haiku 5.5 → Sonnet 5.5 → Opus 5.5 after failed reviews
            researcher: Sonnet 5.5 · Explore: Haiku 5.5 · Fable: hardest calls only
```

| Model | Where I lean on it | Evidence |
|---|---|---|
| Opus 5 → 5.5 | the main session, nearly always | ~71k of ~85k main-session turns; Opus 5.5 took over in September |
| Fable 5 / 5.1 | switched to for the hardest work, never as a subagent | ~9.5k turns; 19 of the named `/model` switches |
| Fable 5.2 | the hardest work, at `high` effort | system card, FrontierCode 2.0: `high` 45.3% at $6.72 per task, against Opus 5.5 at `max` 45.5% at $12.82; `xhigh` 49.1% at $14.19 |
| Sonnet 5.5 | subagents: research, browser runs, builder retries | "use sonnet 5.5, it's new, more intelligent and faster" (Sept 29) |
| Haiku 5.5 | swarms, scouts, builder default | "Make sure the swarms are haiku 5.5 trust in that model" (Oct 10); 5.9k turns in October alone |
| GPT-6 luna | bulk implementation, the only GPT model on fast mode | 116 of 194 delegations while T3 Code was in use |
| GPT-6 / 6.1 sol | the reviewer, at high effort; some implementation | 14 review delegations, 36 builds |
| GPT-6 astra | not used for routine work; no fast mode | "no fast mode on gpt 6 or 6.1 sol, especially astra" |

## Cross-vendor review is the one constant

Where I have Codex, every PR gets a Codex review, because sol catches what Opus misses. Of the last 60
PRs in one project, 39 got a Codex review. 38 were written by Claude (one by T3), and all
39 had at least one finding: 162 findings in total, with 32 on #401 alone.

The catch: it needs a GPT subscription, which I don't have everywhere. Without it, review
falls back to `interrogate` with fresh Claude reviewers.

## Picks

| Task | Model |
|---|---|
| Plan, spec, decide | Opus 5.5 (main session); when Opus stalls, Fable 5.2 at `high` before Opus at `max`; `xhigh` only for long unattended runs |
| Mechanical or well-specced code | Haiku 5.5 builder, or GPT-6 luna with Codex |
| Code that needs design calls | Sonnet 5.5 or Opus 5.5 builder |
| Find files and call sites | Haiku 5.5 (Explore) |
| Read the web and weigh sources | Sonnet 5.5 (researcher) |
| Final PR review | GPT-6.1 sol with Codex; Claude-only `interrogate` otherwise |

Subagents run at `medium` effort (`CLAUDE_CODE_SUBAGENT_EFFORT`); an adapter asks for `high` only
where the job needs it, as `bug-hunt` does. Failure: `high` on every subagent cost about 1.4× for a
few points (Opus 5.5 on SWE-bench Pro: medium is ~2.5 points under high at ~70% of the cost).
`ANTHROPIC_DEFAULT_HAIKU_MODEL` pins `haiku` to Haiku 5.5. Failure: on Bedrock, Google Cloud,
Foundry, Claude Platform on AWS or Claude Code before v2.1.293, the alias still means Haiku 4.5.

### Where the picks depart from Anthropic's guide

Anthropic's guide (claude.dev, "Which Claude model should you build with?", Nov 9 2026) agrees on
the main session, Explore on Haiku and Sonnet subagents. Two picks differ; re-measure them, don't
just defer:

- **Fable 5.2 starts at `high`.** The guide escalates: self-check first, then one effort level,
  then the next model at a *lower* effort (Opus `high` → Fable `medium`). I keep `high` on the
  FrontierCode 2.0 numbers above. Drop to `medium` if a score-vs-spend run on my tickets shows no gap.
- **Haiku 5.5 as the default builder.** The guide keeps code edits on the main model or Sonnet and
  says small models do worse in long agentic loops. My transcripts back Haiku for well-specced
  slices; the failure to watch is a misread that sends the main model to the wrong file. Compare
  Haiku and Sonnet builders on a few real tickets by cost per finished task.

Evidence: the guide's SWE-bench Pro, FrontierCode 2.0 and Terminal-Bench 3.0 figures, and its Claude
Code docs on the `haiku` alias and Explore.

## Cache-friendly subagents

Each call reads the whole context again. Cached input is cheap, but it is not free.

- In a subagent brief, put the stable part first and the variable part last. Then parallel agents of
  the same type share a cached prefix up to the first difference.
- To start new work, start a fresh thread with a short spec. Do not revive a long thread: each of
  its calls reads all of its history again.
- A thread that waits on a background run ends its turn once. A turn that only reports progress
  reads the whole context again and does no work.
- Use one subagent per independent concern, not many small ones. Each subagent loads its own system
  prompt and tools again.
- Switch models at a natural break: run `/compact` first, or start fresh with a short plan. The
  cache belongs to the model that wrote it, so the first turn on the new model pays the cache-write
  price on the whole conversation. Opus 5.5 → Fable 5.2 keeps the earlier thinking; Fable 5.2 → any
  other model drops it.
- Where outcomes check themselves (tests, builds), run at `low` and re-run only the failures at
  `high`: Opus 5.5 did that at ~97% for $0.17 a task, against 95.3% for $0.29 with every task at `high`.
