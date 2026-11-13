# Models

This page says which model does what in this stack. It draws on my Claude Code transcripts
(July–October 2026), T3 Code delegations and Codex reviews on GitHub. Re-check when a new model ships or a tool changes; the picks below are
dated by the models they name. T3 Code is retired, so GPT work now runs in Codex directly and the
T3 counts below are history.

## Who does what

```
            implement            review                 scout / research
 Codex      GPT-6 luna (Codex) ──▶ Codex · GPT-6.1 sol ──▶ fix ──▶ merge
            Opus 5.5 (main)      on every PR
 no Codex   Opus 5.5 (main)  ──▶ review-loop: Claude code review (no GPT sub)
 any day    builder by task: mechanical Haiku 5.5 · specced Sonnet 5.5 · design Opus 5.5
            researcher: Sonnet 5.5 · Explore: Haiku 5.5 · Fable: advisor
```

| Model | Where I lean on it | Evidence |
|---|---|---|
| Opus 5 → 5.5 | the main session, nearly always | ~71k of ~85k main-session turns; Opus 5.5 took over in September |
| Fable 5 / 5.1 | switched to for the hardest work, never as a subagent | ~9.5k turns; 19 of the named `/model` switches |
| Fable 5.2 | the hardest work, at `high` effort | system card, FrontierCode 2.0: `high` 45.3% at $6.72 per task, against Opus 5.5 at `max` 45.5% at $12.82; `xhigh` 49.1% at $14.19 |
| Sonnet 5.5 | subagents: research, browser runs, specced builds | "use sonnet 5.5, it's new, more intelligent and faster" (Sept 29) |
| Haiku 5.5 | swarms, scouts, mechanical builds | "Make sure the swarms are haiku 5.5 trust in that model" (Oct 10); 5.9k turns in October alone |
| GPT-6 luna | bulk implementation, the only GPT model on fast mode | 116 of 194 delegations while T3 Code was in use |
| GPT-6 / 6.1 sol | the reviewer, at high effort; some implementation | 14 review delegations, 36 builds |
| GPT-6 astra | not used for routine work; no fast mode | "no fast mode on gpt 6 or 6.1 sol, especially astra" |

## Cross-vendor review is the one constant

Where I have Codex, every PR gets a Codex review, because sol catches what Opus misses. Of the last 60
PRs in one project, 39 got a Codex review. 38 were written by Claude (one by T3), and all
39 had at least one finding. In total there were 162 findings, with 32 on #401 alone.

The catch is that it needs a GPT subscription, which I don't have everywhere. Without it, review
falls back to `review-loop` with Claude code review.

## Picks

| Task | Model |
|---|---|
| Plan, spec, decide | Opus 5.5 (main session), with Fable 5.2 as advisor; a Fable session only to coordinate a planned orchestration |
| Mechanical code | Haiku 5.5 builder, or GPT-6 luna with Codex |
| Specced code | Sonnet 5.5 builder |
| Code that needs design calls | Opus 5.5 builder |
| Find files and call sites | Haiku 5.5 (Explore) |
| Read the web and weigh sources | Sonnet 5.5 (researcher) |
| Final PR review | GPT-6.1 sol with Codex; Claude-only `review-loop` otherwise |

Split a task that proves bigger than its brief. Do not move it to a bigger model.

Subagents run at `medium` effort (`CLAUDE_CODE_SUBAGENT_EFFORT`); an adapter asks for `high` only
where the job needs it. Failure: `high` on every subagent cost about 1.4× for a
few points (Opus 5.5 on SWE-bench Pro: medium is ~2.5 points under high at ~70% of the cost).
`ANTHROPIC_DEFAULT_HAIKU_MODEL` pins `haiku` to Haiku 5.5. Failure: on Bedrock, Google Cloud,
Foundry, Claude Platform on AWS or Claude Code before v2.1.293, the alias still means Haiku 4.5.

### Where the picks depart from Anthropic's guide

Anthropic's guide (claude.dev, "Which Claude model should you build with?", Nov 9 2026) agrees on
the main session, Explore on Haiku and Sonnet subagents. One pick differs; re-measure it, don't
just defer:

- **Fable 5.2 starts at `high`.** The guide escalates: self-check first, then one effort level,
  then the next model at a *lower* effort (Opus `high` → Fable `medium`). I keep `high` on the
  FrontierCode 2.0 numbers above. Drop to `medium` if a score-vs-spend run on my tickets shows no gap.

The evidence is the guide's SWE-bench Pro, FrontierCode 2.0 and Terminal-Bench 3.0 figures, and its Claude
Code docs on the `haiku` alias and Explore.

### Picking a thread's model by complexity (Nov 12 2026)

A thread gets the cheapest model that fits its task: mechanical work on Haiku 5.5, specced work on
Sonnet 5.5, design on Opus 5.5. A Fable 5.2 session runs only on my word; Fable advises any
session (see below). Evidence:

- Prices per million tokens, input/output (platform.claude.com/docs/en/about-claude/pricing):
  Haiku 5.5 $0.10/$0.50 for a prompt up to 100,000 tokens and $0.50/$2.50 over it; Sonnet 5.5
  $2/$10; Opus 5.5 $4/$20; Fable 5.2 $8/$40. The page says "A request's prompt length counts all of
  its input tokens, including cache reads and cache writes." `autoCompactWindow: 100000` for
  claude-haiku-5-5 in `home/claude/settings.shared.json` keeps a Haiku request in the lower tier, so
  Haiku gets jobs that fit in one pass.
- SWE-Bench Pro at max effort (each system card, Table 8.1.A): Haiku 5.5 64.8, Sonnet 5.5 81.3,
  Opus 5.5 89.9, Fable 5.2 93.0.
- Terminal-Bench 4.0: Haiku 5.5 39.2, Sonnet 5.5 70.6, Opus 5.5 66.4. Sonnet and Opus are within
  the stated standard errors of ±2.5 and ±2.6.
- Haiku 5.5 system card, section 6.2.3: "Claude Opus 5.5, Claude Sonnet 5.5, and Claude Mythos 5.1
  were all strictly better on input hallucination, important omissions, and false completion
  claims." So a Haiku thread needs a check that the starter runs again.
- Opus 5.5 system card, section 8.4: "Opus 5.5's highest FrontierCode scores—54.6% on Main and 65.3%
  on Extended—are at medium effort." So Opus threads stay at `medium`.
- claude.dev/blog/which-claude-model-should-you-build-with: Sonnet 5.5 for "well-scoped everyday
  work, like a bug fix or a feature built against a spec"; "Keep small models on work where a
  mistake is cheap to spot".

Cards: [Haiku 5.5](https://www.anthropic.com/document/claude-haiku-5-5-system-card),
[Sonnet 5.5](https://www.anthropic.com/document/claude-sonnet-5-5-system-card),
[Fable 5.2 and Mythos 5.2](https://www.anthropic.com/document/claude-fable-5-2-mythos-5-2-system-card),
[Opus 5.5](https://www-cdn.anthropic.com/fc1b44717c85dc068bc6ba5024219938094694bd/Claude%20Opus%205.5%20System%20Card.pdf).

### Fable 5.2 as advisor (Nov 13 2026)

`advisorModel: fable` in `home/claude/settings.shared.json` lets every session, subagents too,
consult Fable 5.2 ([advisor docs](https://code.claude.com/docs/en/advisor.md)). Fable runs a
session only to coordinate a planned orchestration. Evidence:

- The Request-only checkout planning session ran on Fable 5.2 (marketplace repo, Nov 13). It was
  a planning request, which these picks give to Opus. Fable did the hands-on work itself (276 Bash
  calls, 66 Edits, 62 Linear issue reads, 57 subagents) until told "no, orchestrate. a haiku".
  My corrections there were judgment slips, which coordinating doesn't help with.
- Each consult reads the whole session at Fable's full input price: "The advisor model's own read
  of the conversation is not cached." Measured: 41,693 input tokens, 0 cache reads, $0.376 for
  one consult. A 200K-token session pays about $1.60 a consult.

## Cache-friendly subagents

Each call reads the whole context again. Cached input is cheap, but it is not free.

- In a subagent brief, put the stable part first and the variable part last. Then parallel agents of
  the same type share a cached prefix up to the first difference.
- To start new work, start a fresh thread with a short spec. Do not revive a long thread, because each
  of its calls reads all of its history again.
- A thread that waits on a background run ends its turn once. A turn that only reports progress
  reads the whole context again and does no work.
- Use one subagent per independent concern, not many small ones. Each subagent loads its own system
  prompt and tools again.
- Switch models at a natural break. Run `/compact` first, or start fresh with a short plan. The
  cache belongs to the model that wrote it, so the first turn on the new model pays the cache-write
  price on the whole conversation. Opus 5.5 → Fable 5.2 keeps the earlier thinking; Fable 5.2 → any
  other model drops it.
- Where outcomes check themselves (tests, builds), run at `low` and re-run only the failures at
  `high`. Opus 5.5 did that at ~97% for $0.17 a task, against 95.3% for $0.29 with every task at `high`.
