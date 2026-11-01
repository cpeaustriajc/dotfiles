#!/usr/bin/env bash
# Sourced by the implement-* fixtures: a small Python repo with a bare origin.
set -euo pipefail
git init -q --bare -b main ../origin.git
git init -q -b main
git config user.email f@x && git config user.name f
git remote add origin ../origin.git
cat > stats.py <<'PY'
def total(xs):
    return sum(xs)
PY
cat > test_stats.py <<'PY'
import unittest
from stats import total

class T(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([1, 2]), 3)

if __name__ == "__main__":
    unittest.main()
PY
printf '.claude/work/
__pycache__/
' > .gitignore
mkdir tickets
cat > CLAUDE.md <<'MD'
# shop

## Tracker

Tickets are Markdown files in `tickets/`, named by key: SHOP-42 is `tickets/SHOP-42.md`. The
`state:` line is the ticket state. `blocked-by:` lists the blockers. `stack-base:` names the
branch to build on. A PR closes a ticket with `Closes SHOP-N` in its body. Tests:
`python3 -m unittest`.
MD
cat > tickets/SHOP-44.md <<'MD'
# SHOP-44 Add count()
state: in-review
MD
cat > tickets/SHOP-45.md <<'MD'
# SHOP-45 Add mean()
state: ready-for-agent
blocked-by: SHOP-44
stack-base: shop-44

## Criteria
- `mean([2, 4])` returns 3.
- `mean([])` returns 0.

## Out of scope
- `total()` stays as it is.
MD
git add -A && git commit -qm init && git push -q -u origin main
git switch -q -c shop-44
cat >> stats.py <<'PY'


def count(xs):
    return len(xs)
PY
git commit -qam "SHOP-44: add count()" && git push -q -u origin shop-44
git switch -q main
