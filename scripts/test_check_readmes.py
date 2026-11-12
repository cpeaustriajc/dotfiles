#!/usr/bin/env python3
"""Tests the banned-word check in check_readmes.py."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_readmes import banned  # noqa: E402
import contextlib  # noqa: E402
import io  # noqa: E402
import tempfile  # noqa: E402

import check_readmes  # noqa: E402
from check_readmes import MOD_HEADINGS, SKILL_HEADINGS, check, folders, main  # noqa: E402
import subprocess  # noqa: E402

# The limits from .claude/rules/wiki.md, pinned here so a changed limit fails a test.
MAX_LINES, MAX_WORDS, MAX_STEP_WORDS = 100, 25, 20


def hits(text):
    return banned(text.splitlines())


class Banned(unittest.TestCase):
    def test_filler_word_in_prose(self):
        self.assertEqual(hits("You just run it."), [(1, "just")])

    def test_each_listed_word(self):
        text = "It is simply fast.\nA powerful tool.\nA seamless install."
        self.assertEqual(hits(text), [(1, "simply"), (2, "powerful"), (3, "seamless")])

    def test_capital_at_sentence_start(self):
        self.assertEqual(hits("Just run it."), [(1, "Just")])

    def test_word_inside_another_word(self):
        self.assertEqual(hits("Adjust the cap. It is justified. Simplify it. Seamlessness."), [])

    def test_abbreviations(self):
        self.assertEqual(hits("A tool, e.g. a hook.\nThe mod, i.e. the hook."), [(1, "e.g."), (2, "i.e.")])

    def test_abbreviation_in_capitals_and_before_comma(self):
        self.assertEqual(hits("E.g., a hook."), [(1, "E.g.")])

    def test_letters_without_dots_are_not_abbreviations(self):
        self.assertEqual(hits("The eg flag and the ie folder."), [])

    def test_code_span(self):
        self.assertEqual(hits("The mod blocks `just fixed` and `e.g.`."), [])

    def test_unclosed_backtick_is_prose(self):
        self.assertEqual(hits("A ` sign, just one."), [(1, "just")])

    def test_fenced_block(self):
        self.assertEqual(hits("```\njust e.g.\n```\nText."), [])

    def test_indented_fence_in_a_list(self):
        self.assertEqual(hits("1. Run:\n   ```\n   just run\n   ```\n2. Done."), [])

    def test_line_after_fence_is_checked(self):
        self.assertEqual(hits("```\nx\n```\nJust that."), [(4, "Just")])

    def test_link_target(self):
        self.assertEqual(hits("See [the guide](https://example.com/just-simply)."), [])

    def test_link_text(self):
        self.assertEqual(hits("See [a powerful guide](guide.md)."), [(1, "powerful")])

    def test_table_cell_and_table_rule(self):
        self.assertEqual(hits("| A | B |\n|---|:--:|\n| x | just y |"), [(3, "just")])

    def test_heading(self):
        self.assertEqual(hits("## Just the start"), [(1, "Just")])

    def test_every_hit_on_one_line(self):
        self.assertEqual(hits("Just add it, e.g. simply."), [(1, "Just"), (1, "e.g."), (1, "simply")])

    def test_emoji(self):
        self.assertEqual(hits("Done \U0001F680 now."), [(1, "\U0001F680")])

    def test_symbols_that_are_not_emoji(self):
        self.assertEqual(hits("Mark it ✓ or ✗, then go → next."), [])

    def test_emoji_presentation_selector(self):
        self.assertEqual(hits("Warn ⚠️ here."), [(1, "⚠️")])


class Check(unittest.TestCase):
    """check(), prose(), folders() and main() on a temp root, each limit at its edge."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.old_root, check_readmes.ROOT = check_readmes.ROOT, self.root
        self.skill = self.root / "plugins" / "p" / "skills" / "s"
        self.skill.mkdir(parents=True)

    def tearDown(self):
        check_readmes.ROOT = self.old_root
        self.tmp.cleanup()

    HEAD_LINES = 1 + 3 * len(SKILL_HEADINGS)  # "# s", then "## h", "", "Text." per heading

    def readme(self, body="", heads=SKILL_HEADINGS, first="# s"):
        lines = [first] + [x for h in heads for x in (f"## {h}", "", "Text.")] + body.splitlines()
        (self.skill / "README.md").write_text("\n".join(lines) + "\n")
        return check(self.skill, SKILL_HEADINGS)

    def test_good_readme(self):
        self.assertEqual(self.readme(), [])

    def test_no_readme(self):
        self.assertEqual(check(self.skill, SKILL_HEADINGS), ["plugins/p/skills/s: no README.md (see .claude/rules/wiki.md)"])

    def test_first_line(self):
        for first in ("# other", "# z"):
            self.assertEqual(self.readme(first=first), ["plugins/p/skills/s/README.md:1: first line must be '# s'"])

    def test_headings_in_order(self):
        for heads in (list(reversed(SKILL_HEADINGS)), SKILL_HEADINGS + ["Extra"], SKILL_HEADINGS[:-1]):
            errors = self.readme(heads=heads)
            self.assertEqual(len(errors), 1, heads)
            self.assertIn("## headings are", errors[0])

    def test_line_limit_edge(self):
        room = MAX_LINES - self.HEAD_LINES
        self.assertEqual(self.readme("x\n" * room), [])
        self.assertEqual(self.readme("x\n" * (room + 1)),
                         [f"plugins/p/skills/s/README.md: {MAX_LINES + 1} lines, at most {MAX_LINES}"])

    def test_sentence_word_limit_edge(self):
        self.assertEqual(self.readme(" ".join(["w"] * MAX_WORDS) + ".\n"), [])
        sentence = " ".join(["word"] * (MAX_WORDS + 1)) + "."
        self.assertEqual(self.readme(sentence + "\n"), [f"plugins/p/skills/s/README.md:{self.HEAD_LINES + 1}: "
                                                         f"{MAX_WORDS + 1} words, at most {MAX_WORDS}: {sentence[:60]}..."])

    def test_step_word_limit_edge(self):
        self.assertEqual(self.readme("1. " + " ".join(["w"] * MAX_STEP_WORDS) + ".\n"), [])
        errors = self.readme("1. " + " ".join(["w"] * (MAX_STEP_WORDS + 1)) + ".\n")
        self.assertEqual(len(errors), 1)
        self.assertIn(f"{MAX_STEP_WORDS + 1} words, at most {MAX_STEP_WORDS}", errors[0])

    def test_code_span_is_one_word_and_link_counts_its_text(self):
        words = " ".join(["w"] * (MAX_WORDS - 4))
        self.assertEqual(self.readme(f"{words} `a b c` [x y z](u v).\n"), [])
        self.assertEqual(len(self.readme(f"w {words} `a b c` [x y z](u v).\n")), 1)

    def test_table_cell_limit_and_rule_row(self):
        cell = " ".join(["w"] * (MAX_WORDS + 1))
        self.assertEqual(self.readme("| a | b |\n|---|---|\n| x | y |\n"), [])
        self.assertEqual(len(self.readme(f"| a | {cell} |\n")), 1)

    def test_fenced_lines_and_headings_are_not_prose(self):
        long = " ".join(["w"] * (MAX_WORDS + 5))
        self.assertEqual(self.readme(f"```\n{long}\n```\n### {long}\n"), [])

    def test_prose_after_a_fence_and_a_table_is_checked(self):
        long = " ".join(["w"] * (MAX_WORDS + 1)) + "."
        self.assertEqual(len(self.readme(f"```\nx\n```\n{long}\n")), 1)
        self.assertEqual(len(self.readme(f"| a | b |\n|---|---|\n| c | {long} |\n")), 1)
        self.assertEqual(len(self.readme(f"| a | b |\n{long}\n")), 1)

    def test_run_as_a_script(self):
        r = subprocess.run([sys.executable, "-I", "-B", str(pathlib.Path(check_readmes.__file__))],
                           capture_output=True, text=True)
        self.assertIn(r.returncode, (0, 1))
        self.assertTrue(r.stdout.strip(), "the script printed nothing")

    def test_banned_word_names_path_and_line(self):
        errors = self.readme("You just run it.\n")
        self.assertEqual(errors, [f'plugins/p/skills/s/README.md:{self.HEAD_LINES + 1}: banned "just" (see .claude/rules/wiki.md)'])

    def test_folders_lists_skills_then_mods(self):
        (self.root / "mods" / "m").mkdir(parents=True)
        self.assertEqual([(d.name, h) for d, h in folders()], [("s", SKILL_HEADINGS), ("m", MOD_HEADINGS)])

    def test_main_exit_and_output(self):
        (self.root / "mods" / "m").mkdir(parents=True)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(), 1)
        self.assertEqual(out.getvalue().splitlines(), ["plugins/p/skills/s: no README.md (see .claude/rules/wiki.md)",
                                                       "mods/m: no README.md (see .claude/rules/wiki.md)"])
        self.readme()
        (self.root / "mods" / "m").rmdir()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(), 0)
        self.assertEqual(out.getvalue(), "readmes ok\n")


if __name__ == "__main__":
    unittest.main()
