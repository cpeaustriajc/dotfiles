# Sources

The stack audit (root `AGENTS.md`) starts when one of these blogs publishes a best-practice
article on coding agents, or when a frontier model ships from a vendor the stack runs on.

This list is only where to look for leads. Being on it is not a reason to trust a claim.

## Weigh each claim by its evidence

The level belongs to each claim and the evidence it shows, never to a site or a person.

- **Primary**: first-hand evidence, such as code you can read or run, a measured result, or a
  failure it names and reproduces. Cite it with that evidence.
- **Secondary**: a report of someone else's evidence (a summary of a study, a talk about another
  team's work). Cite it only with its primary source, or mark it UNVERIFIED.
- **Tertiary**: no evidence and no pointer to any you can reach (an aggregator list, a newsletter
  roundup, a generated overview). Never cite it. Use it only to find a primary source.

A claim from a known name with no evidence is tertiary. Check a claim that was right before
again, because the evidence may no longer hold.

## Vendor engineering blogs

| Source | Vendor |
|---|---|
| anthropic.com/engineering | Anthropic |
| claude.dev | Anthropic |
| claude.com/blog | Anthropic |
| claude.com/resources | Anthropic |
| developers.openai.com/blog | OpenAI |
| developers.googleblog.com | Google |
| cursor.com/blog | SpaceX AI (Cursor) |
| x.ai/news | SpaceX AI |
| github.blog/ai-and-ml | GitHub |
| kiro.dev/blog | Kiro |
| engineering.fb.com | Meta |
| mistral.ai/news | Mistral |
| cognition.com/blog | Cognition |
| augmentcode.com/blog | Augment Code |
| ampcode.com/news | Amp |
| factory.com/news | Factory |

## Tool docs

These docs say how each tool behaves today. Read them before you trust an adapter in
`references/<tool>.md`.

- code.claude.com/docs (Claude Code)
- developers.openai.com/codex (Codex)
- docs.github.com/copilot (GitHub Copilot)
- code.claude.com/docs/en/memory (Claude Code memory)
- code.claude.com/docs/en/costs (Claude Code costs)

## Agents that cheat on tests

Each entry was opened in full text. The level belongs to each claim, as above.

- ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases. Zhong, Raghunathan,
  Carlini, 2025. arxiv.org/abs/2510.20270. Measures cheating on tasks where the tests contradict
  the spec. Shows test edits, `__eq__` overrides and special-casing, and measured effects of
  prompts, hidden or read-only tests, an abort exit and LLM monitors.
- Recent Frontier Models Are Reward Hacking. Von Arx, Chan, Barnes (METR), 2025.
  metr.org/blog/2025-06-05-recent-reward-hacking. Reports o3 reading the grader's answer from the
  call stack, patching the evaluator and overriding equality, with counts per task. No defence
  is measured.
- Natural emergent misalignment from reward hacking in production RL. MacDiarmid et al., 2025.
  arxiv.org/abs/2511.18397. Shows the `__eq__`, `sys.exit(0)` and `conftest.py` hacks learned in
  RL when the model is taught them first, and training-time mitigations. Not a test of
  agent-time hooks.
- Measuring coding agent misalignment in the wild. Zhang and the Docent Team (Transluce), 2026.
  transluce.org/docent/blog/coding-agent-behaviors. LLM-judged rates over 8,600 real sessions of
  `--no-verify`, disabled tests, merges past branch protection and false claims of review. The
  judge's precision is not given.

## Skill sources

- Great Animations. Emil Kowalski, n.d. emilkowal.ski/ui/great-animations. Says "never animate
  keyboard initiated actions", that Raycast has no animation, and that animations are "usually
  shorter than 300ms". Does not contain the 100+/tens/occasional/rare frequency tiers.
- skills (repo; `find-animation-opportunities`, `animation-vocabulary`, `review-animations`,
  `animation-performance`, `apple-design`, `mobile-native`). Emil Kowalski, n.d.
  github.com/emilkowalski/skills (old URL `/skill` redirects). Source of the four-question gate,
  the frequency tiers (100+/day reject, tens/day subtle, occasional, rare = delight budget), the
  duration bands (modals and drawers 200-500ms, UI under 300ms) and the Raycast line. Its own
  example uses `400ms ease`.
- Response Time Limits (Nielsen's three limits, from Usability Engineering 1993). Jakob Nielsen,
  1993 / NN/G page. nngroup.com/articles/response-times-3-important-limits/. Says 0.1s, 1s, 10s,
  and a percent-done indicator for operations over about 10s.
- Web Interface Guidelines. Vercel, n.d. vercel.com/design/guidelines ;
  github.com/vercel-labs/web-interface-guidelines. Says a spinner gets a show-delay of about
  150-300ms and a minimum visible time of about 300-500ms.
- Details that make interfaces feel better. Jakub Krehel, n.d.
  jakub.kr/writing/details-that-make-interfaces-feel-better. Text opened.
- Designing Beautiful Shadows in CSS. Josh Comeau, n.d. joshwcomeau.com/css/designing-shadows/.
  Page opened.
- An Interactive Guide to CSS Transitions. Josh Comeau, n.d.
  joshwcomeau.com/animation/css-transitions/. Page opened.
- Invisible Details of Interaction Design. Rauno Freiberg, 2023 (July).
  rauno.me/craft/interaction-design. Page opened.
- Disable transitions on theme toggle. Paco Coursey, 2020 (19 March).
  paco.me/writing/disable-theme-transitions. Page opened.
- Designing Fluid Interfaces (WWDC18 session 803). Apple, 2018.
  developer.apple.com/videos/play/wwdc2018/803/. Page opened (not the video).
- Animate with springs (WWDC23 session 10158). Apple, 2023.
  developer.apple.com/videos/play/wwdc2023/10158/. Page opened (not the video).
- Web Content Accessibility Guidelines 2.2. W3C, 2023. w3.org/TR/WCAG22/. Page opened; SC 2.5.8
  Target Size (Minimum) present.
- interface-design. Dammyjay93, n.d. github.com/Dammyjay93/interface-design. README opened;
  "Design engineering for Claude Code", spacing on a 4/8px grid.
- HyperFrames (plugin, v0.8.140 installed). HeyGen, n.d. github.com/heygen-com/hyperframes.
  Installed copy read: `plugin-installation.md` documents the launcher; lint codes
  `gsap_timeline_set_initial_hide`, `gsap_cold_seek_hidden_fromto_missing_reveal`,
  `gsap_repeated_fromto_without_baseline`, `multiple_root_compositions`, `media_missing_id` exist;
  `check` runs lint, layout, contrast.
- Principles of Traditional Animation Applied to 3D Computer Animation. John Lasseter, 1987.
  doi.org/10.1145/37402.37407. Bibliographic record only: Crossref record (ACM SIGGRAPH Computer
  Graphics 21(4), 35-44), and the PDF opened through a web.archive.org copy, whose title page
  reads the same title. Directly on ACM: 403.
- Documenting Architecture Decisions. Michael Nygard, 2011.
  cognitect.com/blog/2011/11/15/documenting-architecture-decisions. Shows ADR sections incl.
  Status ("proposed", "accepted", superseded later), and "keep the old one around, but mark it as
  superseded".
- MADR, About MADR. adr.github.io, n.d. adr.github.io/madr/. Shows a template with a status field
  ("superseded by ADR-0123").
- Parallel Change. Danilo Sato, 13 May 2014. martinfowler.com/bliki/ParallelChange.html. Expand,
  migrate, contract for backward-incompatible interface changes; two versions coexist until the
  contract is done.
- Figure Drawing for All It's Worth. Andrew Loomis, 1943. archive.org/details/loomis_FIGURE_draw.
  Metadata confirms title, author and year. Pages not read.

## Accounts on X

A post is a lead. Follow it to the work it reports (the repo, the data, the benchmark) and weigh
that. These accounts posted their own methods, numbers or failures on code review, instruction
files or evals.

**Vendor accounts:** @ClaudeDevs, @OpenAIDevs, @cursor_ai, @github, @nextjs, @augmentcode,
@coderabbitai, @QodoAI, @Macroscope, @LangChain, @EntelligenceAI, @withmartian

**People:** @addyosmani, @bcherny, @trq212, @poteto, @leerob, @ericzakariasson, @jediahkatz,
@aye_aye_kaplan, @garrytan, @mattpocockuk, @emilkowalski, @cramforce, @_philschmid,
@HamelHusain, @walden_yan, @harris_p10, @jhh1992, @nielstron, @kentcdodds, @dakshgup, @kayvz,
@gamalinosqui, @PawelHuryn, @elitemaks, @triviwritescode, @kunchenguid, @MarkAIbuilder,
@paulhq, @jondot, @p_rabtsevich, @jana_builds, @ZetsubosenseiG, @brungarc, @nzhlsk,
@davekiss, @inc_ongi, @iPuneetSingh
