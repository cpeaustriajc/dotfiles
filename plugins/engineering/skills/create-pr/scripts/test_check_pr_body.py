#!/usr/bin/env python3
"""Re-runnable check of check_pr_body.py: each case bends a good body one way and asserts on the findings."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_pr_body import check  # noqa: E402

GOOD = """The digest now batches notifications per user, so a user gets one email an hour. SHOP-42

Evidence: ![before](./before.png) ![after](./after.png), `npm run e2e -- digest`
Merge danger: two-way door; blast radius: the digest job.
Test changes: tests kept: 41 tests, 120 assertions (base: 40, 117)

```diff
- # old -> new
+ ## Summary
```
"""

passed = failed = 0


def case(name, body, want, template=False):
    global passed, failed
    text = "\n".join(f"{n}: {c}" for n, c in check(body, template))
    ok = (not text) if want is None else want in text
    if ok:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: {text or 'no findings'}")


case("a good body passes, code blocks and inline code ignored", GOOD, None)
case("Closes #12 is a closing keyword", GOOD + "Closes #12\n", "closing keyword 'Closes #12'")
case("fixes: SHOP-42 is a closing keyword", GOOD + "This fixes: SHOP-42.\n", "closing keyword")
case("resolved owner/repo#3 is a closing keyword", GOOD + "resolved a/b#3\n", "closing keyword")
case("a closing keyword counts with --template too", GOOD + "Fixes #1\n", "closing keyword", True)
case("fix in plain prose passes", GOOD + "This is a fix for the digest.\n", None)
case("a heading is rejected", "## Summary\n" + GOOD, "1: heading")
case("a heading passes with --template", "## Summary\n" + GOOD, None, True)
case("a checklist item is rejected", GOOD + "- [ ] run tests\n", "checklist item")
case("a missing Test changes line is named", GOOD.replace("Test changes:", "Tests:"), "missing 'Test changes:'")
case("a missing Merge danger line is named", GOOD.replace("Merge danger:", "Danger:"), "missing 'Merge danger:'")
case("a 4-line summary is rejected", "a\nb\nc\nd\n" + GOOD, "4: summary over 3 lines")
case("a 3-line summary passes", "a\nb\n" + GOOD, None)
case("a long summary passes with --template", "a\nb\nc\nd\n" + GOOD, None, True)
case("an em dash is rejected", GOOD + "It is faster — much faster.\n", "em dash")
case("an arrow is rejected", GOOD + "login → token → retry\n", "arrow")
case("an arrow in inline code passes", GOOD + "Run `a -> b` once.\n", None)

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
