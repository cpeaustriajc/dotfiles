# Migrate from the cj-stack and cj-lab plugins

## The cj-stack marketplace is now dotfiles

On 2026-10-31 the marketplace `cj-stack` got the name `dotfiles`, and the repo moved to
`cpeaustriajc/dotfiles`. A plugin that you installed as `design@cj-stack` is now
`design@dotfiles`. To move your installs:

1. Remove the old marketplace: `claude plugin marketplace remove cj-stack`.
2. Add the new one: `claude plugin marketplace add cpeaustriajc/dotfiles`.
3. Install each plugin again with the new name, for example `claude plugin install design@dotfiles`.
4. In your settings files, change each `<plugin>@cj-stack` key in `enabledPlugins` and the
   `cj-stack` key in `extraKnownMarketplaces` to `dotfiles`.

The rest of this guide is for older installs. It uses the old name `cj-stack`.

## The split into skill plugins

On 2026-10-31 the cj-stack marketplace split its skills into four plugins: `design`,
`engineering`, `planning` and `knowledge`. The old plugin names no longer exist. A settings file
that still enables an old name shows this error in the `/plugin` **Errors** tab:

```
Plugin "cj-lab" not found in marketplace "cj-stack"
```

This guide removes the old names and installs the new plugins. It also fixes the
`source doesn't match its extraKnownMarketplaces entry` error.

## Replace each old plugin

| Old plugin | Install now |
|---|---|
| `cj-stack@cj-stack` | The skill plugins that you use: `design`, `engineering`, `planning`, `knowledge`. The [README](README.md#install) lists the skills in each plugin. |
| `cj-lab@cj-stack` | The plugins that now hold the lab skills: `engineering`, `planning`, `knowledge` and `design`. The principles became paste-in prompts in [PROMPTS.md](PROMPTS.md). The [README](README.md#install) lists the skills in each plugin. |
| `usage-pace@cj-stack` | Nothing. The Claude desktop app shows its own weekly pace banner. |
| `loop-brake@cj-stack` | Nothing. Claude Code ends a turn after 8 Stop-hook continuations in a row. |
| `git-guard@cj-stack`, `kill-guard@cj-stack` | Nothing. The auto-mode classifier blocks destructive git commands and kills of processes that the session did not start. |
| `bash-trim@cj-stack` | Nothing. The `bashOutputMaxChars` setting caps Bash output. |
| `secret-guard@cj-stack` | Nothing. The marketplace has no replacement. |
| `linear-gate@cj-stack` | Nothing. A connector in the Claude desktop app sets its own tool permissions. |
| `work-folder@cj-stack` | Nothing. The marketplace has no replacement. |

The mods `hone-nudge` and `memory-lint` were removed later; see the next section.

## The mods are gone

The repo no longer has mods. Uninstall each one you installed, and delete its line from
`enabledPlugins`.

### implement-gate and test-guard are now project hooks

On 2026-11-15 the mods `implement-gate` and `test-guard` left the marketplace. A cloud session runs the
hooks in a repo's committed `.claude/settings.json`; its docs do not say it runs a mod. The `implement` skill now sets up a stop gate hook, and `review-loop`
sets up a test guard hook, in the project's committed `.claude/settings.json`, with a config
fitted to that project. To move:

1. Uninstall the mods: `claude plugin uninstall implement-gate@dotfiles` and
   `claude plugin uninstall test-guard@dotfiles`.
2. Delete their lines from `enabledPlugins` in your settings files.
3. Run `/implement` or `review-loop` once in each project; its setup adds the hook.

### hone-nudge and memory-lint are removed

On 2026-11-15 the mods `hone-nudge` and `memory-lint` were removed with no replacement. To move,
run `claude plugin uninstall hone-nudge@dotfiles` and `claude plugin uninstall memory-lint@dotfiles`.
Then delete their lines from `enabledPlugins`. The `/hone` skill still works; you start it
yourself.

## Remove the old names

Do these steps for your user settings first. Then do them in each project that names cj-stack.

1. Find each settings file that enables an old name:

   ```bash
   grep -l -E '"(cj-stack|cj-lab|usage-pace|loop-brake|git-guard|kill-guard|bash-trim|secret-guard)@cj-stack"' ~/.claude/settings*.json ~/Projects/*/.claude/settings*.json
   ```

2. In each file from step 1, delete the lines of the old names from `enabledPlugins`. Keep the
   lines of the dotfiles plugins.
3. Uninstall each old plugin that is still installed. For your user settings, run the command in
   any folder:

   ```bash
   claude plugin uninstall cj-lab@cj-stack
   ```

   For a project, run the command in the project folder and add the scope:

   ```bash
   claude plugin uninstall cj-lab@cj-stack --scope project
   ```

   If the command says `not found in installed plugins`, that plugin is already gone. Go to the
   next name.
4. If a project file changed in step 2, commit it. Your teammates read the same file.

## Install the new plugins

1. Get the current plugin list from the marketplace:

   ```bash
   claude plugin marketplace update cj-stack
   ```

2. Install each skill plugin that you use. This example installs `planning`:

   ```bash
   claude plugin install planning@cj-stack
   ```

   To install a plugin for all the people on a project, run the command in the project folder
   and add `--scope project`. Then commit `.claude/settings.json`.

## Fix "source doesn't match its extraKnownMarketplaces entry"

This error comes when your user settings and a project's settings give cj-stack two different
sources. Example: `~/.claude/settings.json` names your local clone, and the project names the
GitHub repo. Your user settings win, so Claude Code does not add the project's entry.

> **Warning:** The **Errors** tab asks "Remove "cj-stack" from extraKnownMarketplaces in user and
> project settings?" If you press **y**, Claude Code also removes every cj-stack plugin from
> `enabledPlugins` in both files. Press **n** to keep them.

To fix the error, give cj-stack the same source in both files. Use the GitHub source in
`~/.claude/settings.json`:

```json
"extraKnownMarketplaces": {
  "cj-stack": {
    "source": { "source": "github", "repo": "cpeaustriajc/dotfiles" }
  }
}
```

With the GitHub source, a project runs your change to a plugin only after you push it and run
`claude plugin marketplace update cj-stack`. To try a change before you push it, start a session
with the plugin folder: `claude --plugin-dir ~/Projects/dotfiles/plugins/<plugin>`.

## Check the result

1. Run `claude plugin list` in each project from the first step. No plugin shows
   `failed to load`.
2. Open `/plugin` in Claude Code. The **Errors** tab shows no cj-stack error.
