# GitHub wiki adapter

Page `Foo Bar` is the file `Foo-Bar.md`, linked `[[Foo Bar]]`. A private repo's wiki answers 404
to an unauthenticated fetch even when the page exists: check with `git ls-remote` or the clone,
never `curl`.

`scripts/ghwiki.sh` keeps one managed clone per wiki under
`${XDG_CACHE_HOME:-~/.cache}/dossier/github/<owner>/<repo>`, the single source of truth for every
session and agent. It uses `gh auth`. `owner/repo` defaults to the current directory's `origin`.

`S=<this skill's base directory>/scripts/ghwiki.sh`; `$S --help` lists the subcommands.

Edit files under `$($S path)` with the file tools, then `save` straight away. `push` only after
the user has seen the change (SKILL.md step 5).

## Quirks

- A never-initialised wiki has no repo: `detect` says `missing`, and the user creates any first
  page in the web UI.
- No dots, slashes or `#` in page names: a dotted name breaks `[[links]]`.
- The web editor commits too. On a rebase conflict, show the user both versions. Never
  force-push.
- Wiki pages bypass pull requests, hence the show-before-push rule.
- Link from the repo with `https://github.com/<owner>/<repo>/wiki/<Page-Name>`.
