#!/usr/bin/env python3
"""Tests results.py on result lines as each runner in this repo prints them."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from results import parse, verdict  # noqa: E402

passed = failed = 0


def case(name, got, want):
    global passed, failed
    if got == want:
        passed += 1
        print(f"ok   {name}")
    else:
        failed += 1
        print(f"FAIL {name}: got {got}, want {want}")


BUN = "(pass) a [1ms]\n\n 28 pass\n 0 fail\nRan 28 tests across 1 file. [0.38s]\n"
BUN_RED = " 27 pass\n 1 fail\nRan 28 tests across 1 file.\n"
UNITTEST = "....\n----------------------------------------------------------------------\nRan 20 tests in 0.000s\n\nOK\n"
UNITTEST_RED = "Ran 20 tests in 0.001s\n\nFAILED (failures=1, errors=2)\n"
OWNED = "[1/2] ✔ a module tests\n[2/2] ✔ b module tests\nPASSED: no mod denies or approves a Claude Code-owned action\n"
SMOKE = BUN + "readmes ok\n" + UNITTEST + "descriptions ok\nok   a\n23 passed, 0 failed\n"

case("bun pass and fail lines", parse(BUN), (28, 0, 2))
case("bun with a failure", parse(BUN_RED), (27, 1, 2))
case("this repo's summary line", parse("ok   a\n23 passed, 0 failed\n"), (23, 0, 1))
case("unittest OK", parse(UNITTEST), (20, 0, 1))
case("unittest FAILED counts failures and errors", parse(UNITTEST_RED), (17, 3, 1))
case("pytest summary", parse("===== 3 failed, 40 passed, 1 error in 2.10s =====\n"), (40, 4, 1))
case("claude-owned steps and PASSED", parse(OWNED), (3, 0, 3))
case("named checks", parse("readmes ok\ntrunk ok\ndescriptions FAILED\nFAILED: uv run x\n"), (2, 2, 4))
case("claude plugin validate", parse("✔ Validation passed with warnings\n"), (1, 0, 1))
case("tests kept line", parse("tests kept: 3 tests, 3 assertions (base: 3, 3)\n"), (1, 0, 1))
case("a FAIL line alone is not a result line", parse("FAIL a: no findings\n"), (0, 0, 0))
case("prose is not a result line", parse("all good, everything ok here\n"), (0, 0, 0))

case("a whole smoke log is VERIFIED", verdict(0, SMOKE)[0], "VERIFIED")
case("a non-zero exit is NOT VERIFIED", verdict(1, BUN_RED), ("NOT VERIFIED", "exit 1, 1 failed"))
case("exit 2 is BLOCKED with its reason", verdict(2, "BLOCKED: no token\n"), ("BLOCKED", "BLOCKED: no token"))
case("exit 0 printed early is NOT VERIFIED", verdict(0, "starting\n"),
     ("NOT VERIFIED", "exit 0 but no runner result line in the log"))
case("a runner that prints nothing is NOT VERIFIED", verdict(0, "")[0], "NOT VERIFIED")
case("|| true over a failing runner is NOT VERIFIED", verdict(0, BUN_RED),
     ("NOT VERIFIED", "exit 0 but 1 failed in the result lines"))
case("zero tests is NOT VERIFIED", verdict(0, " 0 pass\n 0 fail\n"), ("NOT VERIFIED", "0 passed: zero tests ran"))
case("fewer than at the base is NOT VERIFIED", verdict(0, BUN, BUN + UNITTEST),
     ("NOT VERIFIED", "28 passed, but the same command ran 48 at the base"))
case("a base failure still counts as a test the base ran", verdict(0, " 27 pass\n 0 fail\n", BUN_RED)[0], "NOT VERIFIED")
case("as many as at the base is VERIFIED", verdict(0, BUN, BUN), ("VERIFIED", "28 passed, 0 failed (base ran 28)"))
case("a base with no result line sets no floor", verdict(0, BUN, "usage: x\n")[0], "VERIFIED")

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
