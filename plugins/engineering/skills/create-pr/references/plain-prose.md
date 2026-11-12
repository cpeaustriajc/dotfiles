# Plain prose

Read this before you open the PR. Step 7 of `SKILL.md` says when.

Rewrite the title and body through `../../blast-radius/references/ai-tells.md` (rules 26, 32 and 33 catch
most PR slop). These are the extra rules for a PR:

- **Real names.** Use the name in the code. "the config loader" becomes `loadConfig`.
- **Arrows and symbol-speak.** Write the sentence. "login → token → retry" becomes "After
  login, the client gets a token and retries once."
- **Dropped articles.** Keep "the" and "a" in sentences. "Fixes bug in parser" becomes "This
  fixes a bug in the parser."
- **Feelings, not facts.** Give the measure. "This greatly improves search" becomes "Search
  takes 80 ms, not 900 ms." Test: could the sentence sit unchanged in another project's docs?
