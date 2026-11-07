# dotfiles

This repo holds CJ's home folder config and CJ's skills and mods for coding agents.

- The home folder config is a [home-manager](https://nix-community.github.io/home-manager/)
  config. [`flake.nix`](flake.nix) and [`home/`](home/README.md) put the Claude Code, Codex,
  zsh, nvim and tmux config in `~`.
- The skills and mods are a Claude Code plugin marketplace. The skills are in `plugins/`, and
  the mods are in `mods/`.

A skill is a method that an agent loads when a task needs it. A skill must work in each harness
where CJ runs agents. [Success in SCOPE.md](SCOPE.md#success) lists these harnesses. A mod is a
set of hooks that changes how a Claude Code session behaves. A mod works in Claude Code only.

- [Home](home/README.md): set up a new machine, change a home file, and sync `settings.json`.
- [Install](#install): add the marketplace and its plugins.
- [Skills](#skills): each skill, its plugin, and what it does.
- [Mods](#mods): each mod and what it does.
- [Models](models/README.md): which model does what, and why cross-vendor review stays.
- [Scope](SCOPE.md): what dotfiles is, its success criteria, and the ideas it rejects, each with
  its reason.
- [painting-craft: before and after](#painting-craft-before-and-after): two pictures from the
  original skill and from the current skill.

## Install

To install the plugins, run these commands in a Claude Code session:

```text
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install planning@dotfiles
/plugin install engineering@dotfiles
/plugin install design@dotfiles
/plugin install knowledge@dotfiles
/plugin install writing@dotfiles
/plugin install visual@dotfiles
/plugin install principles@dotfiles
/plugin install linear-gate@dotfiles
```

Install only the plugins that you need. To add a mod, run `/plugin install <name>@dotfiles`.

| Plugin | What it is for | Skills |
|---|---|---|
| `design` | Sign off UI work and motion. Check it against the design, add missing microinteractions, and make launch videos. | ui-polish, microinteraction, launch-video |
| `engineering` | Prove the work in the real app with playbooks, design-first builds, unattended loops, bug hunts, code history, review and PRs. | playbooks, break-it, feature-files, interrogate, commit, create-pr, architect, implement, drive, bug-hunt, blast-radius, self-verify, formal-verify, no-comments, cleanup, how, why, teach |
| `planning` | Turn an idea into tickets. Find and test ideas, write the spec, cut thin slices, and triage them in any tracker. | vision, shape, tickets, grill, scout, triage |
| `knowledge` | Keep what the team learns: a decision log, research pages, lessons from past sessions, and a recap of recent work. | project-knowledge, hone, recall |
| `writing` | Write docs in plain ASD-STE100, and cut the tells of AI-written prose. | technical-writing, unslop |
| `visual` | Paint scenes in code to a gallery standard, and re-pitch or catch up a chat in plain words with a picture. | painting-craft, bro, ketchup |
| `principles` | Apply engineering principles by name, such as "prove it works", "subtract before you add" and "attack the premise". | principles, and the 20 `principle-*` skills that it indexes |

If you installed the `dotfiles@dotfiles` or `cj-lab@dotfiles` plugin before, that plugin no
longer exists. To remove it and install the plugins above, follow
[Migrate from the dotfiles and cj-lab plugins](MIGRATING.md).

- To edit a mod, add the local clone as the marketplace with
  `/plugin marketplace add ~/Projects/dotfiles`. A directory marketplace hot-reloads.
- To give the skills to Codex and other agents that read `~/.agents/skills`, run
  `scripts/link-skills.sh`.

## Skills

Claude starts a model-invoked skill when your request matches the skill's description. A typed
skill starts only when you type its slash command. All 20 `principle-*` skills are typed.

| Skill | Plugin | What it does |
|---|---|---|
| [ui-polish](plugins/design/skills/ui-polish/README.md) | design | Reviews a UI and its motion against the design and a list of common mistakes. It gives a Before/After/Why table. |
| [microinteraction](plugins/design/skills/microinteraction/README.md) | design | Typed `/microinteraction` with a UI area. Finds the places that should animate, and plays each proposal before you pick one. |
| [launch-video](plugins/design/skills/launch-video/README.md) | design | Makes a trailer, promo, short, voiceover, thumbnails or captions for a launch. |
| [playbooks](plugins/engineering/skills/playbooks/README.md) | engineering | Gives the playbook for a bug, refactor, performance problem, feature, prototype or design. Each playbook has its own proof, such as a reproduced bug. |
| [break-it](plugins/engineering/skills/break-it/README.md) | engineering | Drives the app as a careless, impatient or confused user with worst-case data. Reports ranked bugs with video and repro steps. |
| [feature-files](plugins/engineering/skills/feature-files/README.md) | engineering | Keeps one short file for each feature that says how to reach, drive and check it. An E2E check reads only the file that it needs. |
| [interrogate](plugins/engineering/skills/interrogate/README.md) | engineering | Reviews a diff with fresh Claude reviewers, each on a different slice. Sorts the findings into act on, consider, noted and dismissed. |
| [commit](plugins/engineering/skills/commit/README.md) | engineering | Typed `/commit`. Makes small commits in the repo's style, then pushes. It matches the desktop **Commit and push** button. |
| [create-pr](plugins/engineering/skills/create-pr/README.md) | engineering | `/create-pr [draft]` or "open the PR". Commits, checks, pushes and opens a PR that links the issue and the evidence. It matches the desktop **Create PR** button. |
| [architect](plugins/engineering/skills/architect/README.md) | engineering | Typed `/architect`. Sketches the types, signatures and module structure before the code, then stays in the loop while the build fills them in. |
| [implement](plugins/engineering/skills/implement/README.md) | engineering | Typed `/implement` with a ticket. Builds one ready ticket without supervision, with the feature playbook and a review. |
| [drive](plugins/engineering/skills/drive/README.md) | engineering | "Loop until it passes" or "run it overnight". Sets the stop condition, then drives the work until the condition holds. |
| [bug-hunt](plugins/engineering/skills/bug-hunt/README.md) | engineering | Hunts bugs across a codebase in rounds, and fixes each bug test-first. It stops when a round finds no bug. |
| [blast-radius](plugins/engineering/skills/blast-radius/README.md) | engineering | Typed `/blast-radius`. Finds what a change can break outside its diff, and proves the fact that makes the change safe. |
| [self-verify](plugins/engineering/skills/self-verify/README.md) | engineering | Sets up and audits the repo's verify skill, so that agents prove "done" with a verdict for each PR. |
| [formal-verify](plugins/engineering/skills/formal-verify/README.md) | engineering | Model-checks a race, retry, lease or state machine that tests miss. Then keeps a project check in sync with the code. |
| [no-comments](plugins/engineering/skills/no-comments/README.md) | engineering | Typed `/no-comments` with a folder. Removes stale comments and suppressions in separate commits, with the same test results. |
| [cleanup](plugins/engineering/skills/cleanup/README.md) | engineering | Removes what a session left, such as dev servers, stale branches and the session itself, when it is safe. It does not tidy code. |
| [how](plugins/engineering/skills/how/README.md) | engineering | Typed `/how`. Explains how a part of the code works, and where a new piece should go. |
| [why](plugins/engineering/skills/why/README.md) | engineering | Explains why code is like it is, where a number came from, or if a guard can go. Labels the evidence from git, PRs and docs. |
| [teach](plugins/engineering/skills/teach/README.md) | engineering | Typed `/teach`. Gives one plain explanation of a body of work, from `how` and `why`. |
| [vision](plugins/planning/skills/vision/README.md) | planning | Asks you about a vague product idea, first whether it is worth building. Then writes the top of the plan, in risk-first order. |
| [shape](plugins/planning/skills/shape/README.md) | planning | Writes one project in any tracker: a spec with numbered requirements, milestones, descriptions and updates. Owns the tracker adapters and the plan-tree check. |
| [tickets](plugins/planning/skills/tickets/README.md) | planning | Cuts a confirmed spec into thin, demoable work items. Each item cites the requirements that it meets. |
| [grill](plugins/planning/skills/grill/README.md) | planning | Sizes an idea or a change, then asks you short rounds of questions with recommended answers, until no decision is open. |
| [scout](plugins/planning/skills/scout/README.md) | planning | Finds an idea worth building, or checks a niche, when apps are cheap to copy. |
| [triage](plugins/planning/skills/triage/README.md) | planning | Sets one state on an issue, for "what needs my attention" or "can an agent take this". Writes an agent brief. |
| [project-knowledge](plugins/knowledge/skills/project-knowledge/README.md) | knowledge | Keeps a decision log and research pages in the team's wiki, Notion, Linear, Obsidian or Confluence. |
| [hone](plugins/knowledge/skills/hone/README.md) | knowledge | Finds your repeated corrections in past transcripts, or one skill's with `/hone <skill>`. Proposes where each lesson goes, or what to prune. |
| [recall](plugins/knowledge/skills/recall/README.md) | knowledge | "Where was I". Gives a brief of recent work from transcripts, git and PRs. |
| [technical-writing](plugins/writing/skills/technical-writing/README.md) | writing | Typed `/technical-writing`. Writes or reviews a doc, README, spec, PR body or commit message by the repo's rules, then by ASD-STE100. |
| [unslop](plugins/writing/skills/unslop/README.md) | writing | Typed `/unslop` with text. Gives the same text back without the common tells of AI-written prose. |
| [painting-craft](plugins/visual/skills/painting-craft/README.md) | visual | Draws and paints in code to a gallery standard, with a screenshot review loop. |
| [bro](plugins/visual/skills/bro/README.md) | visual | Typed `/bro`. Re-pitches the last message in plain words, with the missing context first and one picture. |
| [ketchup](plugins/visual/skills/ketchup/README.md) | visual | Typed `/ketchup`. Tells you what changed in this chat since your last message, and which calls you must make. |
| [principles](plugins/principles/skills/principles/README.md) | principles | Picks the rule that applies from the 20 `principle-*` skills when you name a principle or make a design, test or debug decision. |

A skill holds no tool details and no project facts. The tool details go in the skill's
`references/<tool>.md` adapters. A project's own facts stay in that project.

## Mods

| Mod | What it does | Install |
|---|---|---|
| [linear-gate](mods/linear-gate/README.md) | Blocks Linear writes off shift. On shift, it asks you only before a delete or a cancel. | in the install list |
| [hone-nudge](mods/hone-nudge/README.md) | Suggests `/hone <skill>` after you correct Claude during a dotfiles skill run. | optional |
| [memory-lint](mods/memory-lint/README.md) | Denies an auto-memory write that holds task state, short-lived detail, PR or commit references, file:line pointers, code, or too much text. A prune always passes. | optional |
| [work-folder](mods/work-folder/README.md) | Denies a new agent working file, such as a plan or evidence, outside `.claude/work/`. Removes entries not changed for a day. | optional |
| [test-guard](mods/test-guard/README.md) | Denies an Edit or Write that changes or removes a test line at `HEAD`. Additions pass. `/test-guard allow <path>` lets one file change. | optional |

## painting-craft: before and after

Each prompt ran once in a fresh session. The left picture is from the original skill. The right
picture is from the current painting-craft. Nobody touched up a picture by hand.

**"Paint a 1600x1000 SVG of a knight asleep against an oak tree at dusk, in a Romantic oil-painting look."**

![Knight at dusk, full picture: before and after](docs/images/knight-full.jpg)

At 2× zoom on the knight, the current skill paints a 3D figure that the low sun lights. The
figure has separate plates, rows of mail and a visor. The original skill painted a mannequin of
tubes.

![Knight at dusk, 2x crop: before and after](docs/images/knight-zoom.jpg)

**"Draw a night city street as a 1600x1000 SVG: a car passes behind a row of trees on the near verge.
Flat vector style, but it must not look cheap."**

![Night street, full picture: before and after](docs/images/street-full.jpg)

At 2× zoom on a tree, the current skill builds each crown from clumps on a branch skeleton, in
three values with broken edges. The original skill piled up round blobs.

![Night street, 2x crop of a tree: before and after](docs/images/street-zoom.jpg)

These changes to painting-craft made the difference:

- Build recipes for the parts that fail up close, in
  [`references/recipes.md`](plugins/visual/skills/painting-craft/references/recipes.md).
- A study of each hero element against fetched public-domain references before the composition,
  with `scripts/refs.py` and `scripts/compare.py`.
- The bundled 3D figure renderer.
- A paint pass that unifies the painted styles, with `scripts/paintpass.py`.
- Delivery at twice the display size.
