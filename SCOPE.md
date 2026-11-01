# Scope

dotfiles is a skill stack for one developer. Its skills hold methods that work on any tool. A
fan-out runs each agent on the cheapest model that can do its job: see
[models/README.md](models/README.md).

## Success

Assume that all harnesses converge into a single chat interface. The stack succeeds when each
shipped skill does its job through that chat only. Until then, each skill must do its job in every
harness where the user runs agents:

- agent multiplexers, such as T3 Code and Herdr
- native harnesses, such as Claude Code, the ChatGPT desktop app, Antigravity and Muse Code

## Rejected

An idea goes on this list only with a reason. If you change your mind later, edit its line. Do
not add a new dated line.

- **Skill-fire log mod**: `/skill-doctor` already reports the uses, the last-used date and the
  7-day tokens of each skill.
- **Careful mode** (hooks that run only while a skill runs): a hook in skill frontmatter stays on
  for the rest of the session after the skill starts. See "Hooks in skills and agents" in the
  [hooks docs](https://code.claude.com/docs/en/hooks). Also, a deny would override the
  permission mode, and a mod never does that.
- **Multi-model panels** (arena, a model mix in interrogate, cross-family judges): they need
  models from another vendor.
- **Autopilot**: it needs a fleet of agents.
- **Orchestrate at fleet scale** (pstack: hundreds of cloud subagents, verifiers from another
  model family): it needs a fleet and other vendors. `implement` hands a spec to Claude Code
  Projects, a few threads at a time.
- **Babysit's watcher**: it needs a fleet of agents that watch pull requests.
- **Cursor automations**, **Bugbot** and **Grok Bot UI**: they work only in Cursor.
- **Cloud agents** from pstack: they need Cursor's cloud agents.
- **setup-pstack's model map**: it maps models from other vendors.
