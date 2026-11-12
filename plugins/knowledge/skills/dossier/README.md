# dossier

A skill that keeps a decision log and research pages for your team. The pages live in the place your team already writes, such as a wiki or Notion, and Claude writes them for people.

## When to use it

Use it when a decision or a finding must outlive the chat.

- You say "note that down as a decision" or "supersede that decision".
- You ask "what did we decide about X".
- You ask Claude to record research or a finding.
- A decision made in conversation will matter to others.

Do not use it for instructions to an agent. Those belong in `CLAUDE.md`. It starts no log in your code repository, but follows an existing `docs/adr/`.

## Example

You say: "Note that down as a decision: we move from REST to tRPC for the internal API."

1. Claude finds your decision log, or asks you once where it lives.
2. Claude writes a `Decision NNN: <Topic>` page with Context, Decision and Consequences.
3. Claude adds the page to the top of the decisions index.

You get one new page and one new index row. In a shared space, Claude shows you the first write before it publishes.

## Install

The `knowledge` plugin ships this skill. Add the marketplace, then install the plugin:

```
/plugin marketplace add cpeaustriajc/dotfiles
/plugin install knowledge@dotfiles
```

To turn the plugin off, run `claude plugin disable knowledge@dotfiles`. This also turns off every other skill in `knowledge`.

A GitHub wiki needs the `gh` CLI signed in. Notion and Linear need their MCP server connected.

## What it does

- It finds the log in this order: a pointer line in your project `CLAUDE.md`, `~/.claude/dossier.json`, GitHub wiki detection, then a question to you.
- It saves your answer to `~/.claude/dossier.json`, so it asks once.
- It supports these backends: GitHub wiki, Notion, Linear documents, Obsidian vault, and Confluence or Google Docs through MCP.
- Before its first write, Claude reads your log's newest pages and copies their template, numbering and status words.
- Claude offers a decision page unasked only for a choice that is hard to undo, surprising, and a real trade-off.
- A decision page is never rewritten. To supersede it, Claude changes only the Status line and adds a new page.
- When it answers "what did we decide", it follows each "Superseded by" link to the current decision.
- Research pages carry a date, and Claude marks unconfirmed facts UNVERIFIED. Replaced findings move under a `## History` heading.
- A decision date comes from a commit, an issue or your word. If none exists, Claude writes the month only.
- Claude does not invent a reason. If the record does not say why, the page says so and Claude asks you.
- For a log held as files, `scripts/check_pages.py` checks names, Status, sections, links and index order.
- Before it publishes, Claude reads each page for AI-sounding prose, such as arrows and metaphor nouns, and rewrites it.
- For a GitHub wiki, `scripts/ghwiki.sh` keeps one managed clone under `~/.cache/dossier/github/<owner>/<repo>`.

## Limits

- It does not write agent instructions.
- It does not fake a write. If a backend has no create tool, Claude gives you the page text to paste.
- It never force-pushes a wiki.
- A GitHub wiki that was never initialised needs a first page, which you create in the web UI.
- It has no settings.

## More

- [SKILL.md](SKILL.md): the method Claude follows.
- [references/github-wiki.md](references/github-wiki.md), [notion.md](references/notion.md), [linear.md](references/linear.md), [obsidian.md](references/obsidian.md) and [other-backends.md](references/other-backends.md): one adapter for each backend.
- [references/locate.md](references/locate.md): the order in which Claude looks for your decision log.
- [references/publish.md](references/publish.md): the review and the checks before a page is published.
- [references/shape.md](references/shape.md): the page layout, the decision template and where dates come from.
- [references/operations.md](references/operations.md): record or supersede a decision, file research, move rationale out of a repo.
- [references/plain-prose.md](references/plain-prose.md): the prose patterns to rewrite before a page is published.
- [scripts/ghwiki.sh](scripts/ghwiki.sh) and [scripts/test_ghwiki.sh](scripts/test_ghwiki.sh): the GitHub wiki helper and its test.
- [scripts/check_pages.py](scripts/check_pages.py) and [scripts/test_check_pages.py](scripts/test_check_pages.py): the page-shape check and its test.
- Source: Matt Pocock's `domain-modeling` and `chief-of-staff` skills, from `mattpocock/skills` on `main`. Their rules: offer an ADR only when it passes three tests, and follow an existing wiki's conventions. They give no measured result.
