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
printf '# shop\n\nTests: `python3 -m unittest`.\n' > CLAUDE.md
cat > tickets/SHOP-40.md <<'MD'
# SHOP-40 Add total()
state: done
MD
cat > tickets/SHOP-43.md <<'MD'
# SHOP-43 Add median()
state: needs-info

## Criteria
- `median([3, 1, 2])` returns 2.
MD
git add -A && git commit -qm "SHOP-40: add total()" && git push -q -u origin main
