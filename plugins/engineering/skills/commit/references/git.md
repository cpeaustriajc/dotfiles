# Git

Commands for the steps of `SKILL.md`.

1. Read: `git status`, `git diff HEAD` and `git log --oneline -10`.
2. Stage by path: `git add -- <paths>`, never a blind `git add -A`.
3. Branch: `git switch -c <name>`.
4. Push: `git push -u origin <branch>`. If it is rejected because the remote moved:
   `git pull --rebase`, only when it applies cleanly. On a conflict, stop and tell me; do not
   resolve it.
