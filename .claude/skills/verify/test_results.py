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
case("canary ok line", parse("canary ok: 23 test files went red\n"), (1, 0, 1))
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

# Mutation-run additions: sums across lines, each regex's capture, verdict edges, the CLI.
case("two bun summaries add up", parse(" 3 pass\n 1 fail\n 4 pass\n 2 fail\n"), (7, 3, 4))
case("two summary lines add up", parse("3 passed, 1 failed\n4 passed, 2 failed\n"), (7, 3, 2))
case("two unittest runs add up", parse("Ran 5 tests in 0.1s\n\nOK\nRan 7 tests in 0.1s\n\nOK (skipped=1)\n"), (12, 0, 2))
case("a unittest failure adds to earlier counts", parse(" 5 pass\nRan 10 tests in 0.1s\n\nFAILED (failures=2)\n"), (13, 2, 2))
case("unittest errors alone count", parse("Ran 10 tests in 0.1s\n\nFAILED (errors=3)\n"), (7, 3, 1))
case("unittest failures and errors count together", parse("Ran 10 tests in 0.1s\n\nFAILED (failures=2, errors=3, skipped=1)\n"), (5, 5, 1))
case("a stray OK without Ran is no result line", parse("OK\n"), (0, 0, 0))
case("a line after OK is still read", parse("Ran 2 tests in 0.1s\n\nOK\n 3 pass\n"), (5, 0, 2))
case("a line after a bun count is still read", parse(" 3 pass\n 1 fail\nreadmes ok\n"), (4, 1, 3))
case("pytest passed only", parse("===== 5 passed in 0.10s =====\n"), (5, 0, 1))
case("pytest errors only", parse("===== 2 errors in 0.10s =====\n"), (0, 2, 1))
case("pytest one error", parse("===== 1 error in 0.10s =====\n"), (0, 1, 1))
case("pytest failed only, twice", parse("== 2 failed in 1.0s ==\n== 3 failed in 1.0s ==\n"), (0, 5, 2))
case("two pytest lines add up", parse("== 2 passed in 1.0s ==\n== 3 passed, 1 failed in 1.0s ==\n"), (5, 1, 2))
case("steps add up", parse("[1/3] ✔ a\n[2/3] ✘ b\n[3/3] ✔ c\n"), (2, 1, 3))
case("self-test adds its count", parse("SELF-TEST PASSED: all 7 cases\nSELF-TEST PASSED: all 5 cases\n"), (12, 0, 2))
case("checks add up", parse("a ok\nb-c d ok\nPASSED: x\nc FAILED\nSELF-TEST FAILED: y\n✘ Validation failed: z\n"), (3, 3, 6))
case("an indented ok is not a result line", parse(" a ok\n"), (0, 0, 0))
case("trailing space on a result line is ignored", parse("23 passed, 0 failed  \n"), (23, 0, 1))
case("a bun line with other text is not a result line", parse("x 3 pass\n3 pass x\n"), (0, 0, 0))
case("a unittest failure adds to counts with shared bits",
     parse(" 3 pass\n 1 fail\nRan 3 tests in 0.1s\n\nFAILED (failures=1)\nreadmes ok\n"), (6, 2, 4))
case("two bun fail lines add up", parse(" 1 fail\n 1 fail\n"), (0, 2, 2))
case("two summary lines add up with shared bits", parse("3 passed, 1 failed\n3 passed, 1 failed\n"), (6, 2, 2))
case("two failed steps add up", parse("[1/2] ✘ a\n[2/2] ✘ b\n"), (0, 2, 2))
case("two passed steps add up", parse("[1/2] ✔ a\n[2/2] ✔ b\n[3/3] ✔ c\n"), (3, 0, 3))
case("two bun pass lines add up with shared bits", parse(" 3 pass\n 3 pass\n"), (6, 0, 2))


case("exit 3 is NOT VERIFIED", verdict(3, BUN)[0], "NOT VERIFIED")
case("a negative exit is NOT VERIFIED", verdict(-1, BUN)[0], "NOT VERIFIED")
case("BLOCKED reason is the last BLOCKED line", verdict(2, "BLOCKED: a\nx\nBLOCKED: b\nz\n"), ("BLOCKED", "BLOCKED: b"))
case("BLOCKED without a reason line says exit 2", verdict(2, "nothing\n"), ("BLOCKED", "exit 2"))
case("a failed exit reports the failures", verdict(1, " 3 pass\n 2 fail\n"), ("NOT VERIFIED", "exit 1, 2 failed"))
case("one fewer than the base counting its failures", verdict(0, " 27 pass\n 0 fail\n", " 27 pass\n 1 fail\n"),
     ("NOT VERIFIED", "27 passed, but the same command ran 28 at the base"))
case("as many as the base ran counting its failures", verdict(0, " 28 pass\n 0 fail\n", " 27 pass\n 1 fail\n"),
     ("VERIFIED", "28 passed, 0 failed (base ran 28)"))
case("one more than the base", verdict(0, " 29 pass\n 0 fail\n", " 27 pass\n 1 fail\n"),
     ("VERIFIED", "29 passed, 0 failed (base ran 28)"))


def cli(*args, logs=()):
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for i, text in enumerate(logs):
            paths.append(os.path.join(d, f"log{i}"))
            with open(paths[-1], "w", encoding="utf-8") as f:
                f.write(text)
        r = subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.py"),
                            *[a.format(*paths) for a in args]], capture_output=True, text=True)
        return r.returncode, r.stdout.strip(), r.stderr.strip()


USAGE = "usage: results.py <exit status> <log> [<base log>]"
case("the CLI prints VERIFIED and exits 0", cli("0", "{0}", logs=(BUN,)), (0, "VERIFIED: 28 passed, 0 failed", ""))
case("the CLI prints NOT VERIFIED and exits 1", cli("0", "{0}", logs=(BUN_RED,)),
     (1, "NOT VERIFIED: exit 0 but 1 failed in the result lines", ""))
case("the CLI prints BLOCKED and exits 2", cli("2", "{0}", logs=("BLOCKED: no token\n",)), (2, "BLOCKED: BLOCKED: no token", ""))
case("the CLI reads the base log", cli("0", "{0}", "{1}", logs=(BUN, BUN + UNITTEST)),
     (1, "NOT VERIFIED: 28 passed, but the same command ran 48 at the base", ""))
case("the CLI takes a negative status", cli("-1", "{0}", logs=(BUN,))[0], 1)
case("the CLI with no arguments prints its usage", cli(), (64, "", USAGE))
case("the CLI with one argument prints its usage", cli("0"), (64, "", USAGE))
case("the CLI with four arguments prints its usage", cli("0", "a", "b", "c"), (64, "", USAGE))
case("the CLI with a word for a status prints its usage", cli("x", "{0}", logs=(BUN,)), (64, "", USAGE))

print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
