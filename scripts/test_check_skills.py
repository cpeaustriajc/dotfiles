#!/usr/bin/env python3
"""Tests check_skills.py on a temp root, each limit at its edge."""
import contextlib
import io
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_skills  # noqa: E402
from check_skills import check, costs, description, files, main, sentences, tokens, units  # noqa: E402

# The limits from .claude/rules/skills.md, pinned here so a changed limit fails a test.
MAX_ALWAYS_ON, MAX_SKILL_TOKENS, MAX_SENTENCE = 2000, 5000, 50
REL = "plugins/p/skills/s/SKILL.md"


def ws(n, word="w"):
    return " ".join([word] * n)


class Units(unittest.TestCase):
    def test_wrapped_lines_join_into_one_paragraph(self):
        self.assertEqual(list(units(["One two", "three four.", "", "Next."])), [(1, "One two three four."), (4, "Next.")])

    def test_each_list_item_is_its_own_unit_with_its_wrapped_lines(self):
        lines = ["- First item", "  goes on.", "- Second.", "1. Step one", "   wraps."]
        self.assertEqual(list(units(lines)), [(1, "First item goes on."), (3, "Second."), (4, "Step one wraps.")])

    def test_table_cells_headings_and_fences(self):
        lines = ["| a | b c |", "|---|:-:|", "# Head", "```", "code here", "```", "After."]
        self.assertEqual(list(units(lines)), [(1, " a "), (1, " b c "), (7, "After.")])

    def test_semicolon_ends_a_sentence(self):
        self.assertEqual(sentences("A b; c d. E f"), ["A b;", "c d.", "E f"])


class Check(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.old_root, check_skills.ROOT = check_skills.ROOT, self.root
        self.skill = self.root / "plugins" / "p" / "skills" / "s"
        (self.skill / "references").mkdir(parents=True)

    def tearDown(self):
        check_skills.ROOT = self.old_root
        self.tmp.cleanup()

    def skill_md(self, text, name="SKILL.md"):
        p = self.skill / name
        p.write_text(text)
        return check(p)

    def test_good_skill(self):
        self.assertEqual(self.skill_md("---\nname: s\n---\n\n# S\n\nRun the tests.\n"), [])

    def test_skill_token_budget_edge(self):
        self.assertEqual((tokens("x" * 4), tokens("x" * 5)), (1, 2))
        text = "x" * (MAX_SKILL_TOKENS * 4)
        self.assertEqual(self.skill_md(text), [])
        self.assertEqual(self.skill_md(text + "w"),
                         [f"{REL}: {MAX_SKILL_TOKENS + 1} tokens, at most {MAX_SKILL_TOKENS}; "
                          "move detail to a file the step that needs it reads"])

    def test_other_files_have_no_token_limit(self):
        self.assertEqual(self.skill_md(ws(MAX_SKILL_TOKENS * 2, "w."), "references/r.md"), [])

    def test_frontmatter_skips_the_text_checks(self):
        front = "---\ndescription: Ask Claude. " + ws(MAX_SENTENCE + 1) + " simply\n---\n"
        self.assertEqual(self.skill_md(front + "Run it.\n"), [])

    def test_sentence_limit_edge_across_wrapped_lines(self):
        self.assertEqual(self.skill_md(ws(MAX_SENTENCE - 10) + "\n" + ws(10) + ".\n"), [])
        sentence = ws(MAX_SENTENCE - 10) + " " + ws(11) + "."
        self.assertEqual(self.skill_md(ws(MAX_SENTENCE - 10) + "\n" + ws(11) + ".\n"),
                         [f"{REL}:1: {MAX_SENTENCE + 1} words in one sentence, at most {MAX_SENTENCE}: {sentence[:60]}..."])

    def test_bold_lead_in_is_its_own_sentence(self):
        self.assertEqual(self.skill_md(f"- **Label.** {ws(MAX_SENTENCE)}.\n"), [])

    def test_wordy_seeded_skill_fails_on_each_count(self):
        text = f"# S\n\nYou can simply run it.\n\n{ws(MAX_SENTENCE + 5)}.\n"
        errors = self.skill_md(text)
        self.assertEqual([e.split(": ", 1)[1].split(" ")[0] for e in errors], [str(MAX_SENTENCE + 5), 'filler'])

    def test_harness_names(self):
        errors = self.skill_md("Ask Claude, then Codex or Cursor.\nGPT-5 and Opus too.\n")
        self.assertEqual([e.split('"')[1] for e in errors], ["Claude", "Codex", "Cursor", "GPT-5", "Opus"])
        self.assertTrue(errors[0].startswith(f"{REL}:1: names"))

    def test_harness_name_in_code_or_another_word_passes(self):
        self.assertEqual(self.skill_md("Read `CLAUDE.md` and `claude -p`.\n```\nClaude\n```\nA haiku, a cursor.\n"), [])

    def test_named_exception_holds_only_for_its_file_and_word(self):
        check_skills.EXCEPTIONS[(REL, "Codex")] = "test"
        try:
            self.assertEqual([e.split('"')[1] for e in self.skill_md("Codex and Claude.\n")], ["Claude"])
        finally:
            del check_skills.EXCEPTIONS[(REL, "Codex")]

    def test_files_skip_readmes_and_include_nested_folders(self):
        for rel in ("SKILL.md", "README.md", "references/r.md", "library/x/index.md"):
            (self.skill / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.skill / rel).write_text("Text.\n")
        self.assertEqual([str(p.relative_to(self.skill)) for p in files()],
                         ["SKILL.md", "library/x/index.md", "references/r.md"])

    def test_main_exit_and_output(self):
        self.skill_md("---\nname: s\ndescription: Runs it.\n---\nRun it.\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(), 0)
        self.assertEqual(out.getvalue(), f"skills ok: every turn 3 tokens, limit {MAX_ALWAYS_ON}, target 1000\n")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            main(["--report"])
        self.assertEqual(out.getvalue().splitlines()[:3],
                         ["skill\tevery turn\tSKILL.md\tother files", "plugins/p/skills/s\t3\t12\t0", "total\t3\t12\t0"])
        self.skill_md("Ask Claude.\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(main(), 1)
        self.assertIn('names "Claude"', out.getvalue())

    def test_description_forms(self):
        for front, want in (("name: s\ndescription: Plain text.", "s: Plain text."),
                            ("name: s\ndescription: \"Quoted text.\"", "s: Quoted text."),
                            ("name: s\ndescription: >\n  Folded\n  text.\nuser-invocable: false", "s: Folded text.")):
            self.assertEqual(description(f"---\n{front}\n---\nBody.\n"), want)
        self.assertEqual(description("No frontmatter."), "")

    def test_every_turn_cost_is_all_skills_together(self):
        desc = "x" * 3995  # "s: " plus 3,995 characters is 3,998 characters: 1,000 tokens
        self.skill_md(f"---\nname: s\ndescription: {desc}\n---\n")
        other = self.root / "plugins" / "q" / "skills" / "t"
        other.mkdir(parents=True)
        (other / "SKILL.md").write_text(f"---\nname: s\ndescription: {desc}\n---\n")
        self.assertEqual(sum(c[1] for c in costs()), MAX_ALWAYS_ON)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(), 0)
        (other / "SKILL.md").write_text(f"---\nname: s\ndescription: {desc}xxxx\n---\n")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(main(), 1)
        self.assertIn(f"every-turn cost: {MAX_ALWAYS_ON + 1} tokens of names and descriptions, at most {MAX_ALWAYS_ON}",
                      out.getvalue())

    def test_typed_only_skill_costs_nothing_every_turn(self):
        self.skill_md("---\nname: s\ndescription: A long description.\ndisable-model-invocation: true\n---\n")
        self.assertEqual([c[1] for c in costs()], [0])
        self.skill_md("---\nname: s\ndescription: A long description.\ndisable-model-invocation: false\n---\n")
        self.assertEqual([c[1] for c in costs()], [6])

    def test_costs_count_nested_files_but_not_the_readme(self):
        self.skill_md("---\nname: s\ndescription: d\n---\n")
        (self.skill / "references" / "r.md").write_text("x" * 40)
        (self.skill / "README.md").write_text("x" * 400)
        self.assertEqual([c[3] for c in costs()], [10])

    def test_run_as_a_script(self):
        r = subprocess.run([sys.executable, "-I", "-B", str(pathlib.Path(check_skills.__file__))],
                           capture_output=True, text=True)
        self.assertIn(r.returncode, (0, 1))
        self.assertTrue(r.stdout.strip(), "the script printed nothing")


if __name__ == "__main__":
    unittest.main()
