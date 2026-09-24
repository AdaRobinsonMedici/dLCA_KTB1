"""Unit tests for the offline checks; no scientific dependencies are required."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "repository_checks", Path(__file__).resolve().parents[1] / "scripts" / "check_repository.py"
)
checks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checks)


class RepositoryChecksTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def notebook(self, **cell_changes):
        cell = {"cell_type": "code", "metadata": {}, "source": ["print('demo')\n"], "outputs": [], "execution_count": None}
        cell.update(cell_changes)
        return json.dumps({"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": [cell]})

    def test_valid_repository(self):
        self.write("README.md", "[Guide](docs/guide.md)\n![Banner](assets/banner.svg)\n")
        self.write("docs/guide.md", "[Home](../README.md#top)\n")
        self.write("assets/banner.svg", '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.write("notebooks/demo.ipynb", self.notebook())
        self.assertEqual([], checks.check_repository(self.root))

    def test_invalid_json_and_structure(self):
        for text in ["{", "null", "[]", '{"nbformat": 3}', '{"nbformat": 4, "cells": []}']:
            with self.subTest(text=text):
                self.write("bad.ipynb", text)
                self.assertTrue(checks.check_repository(self.root))

    def test_invalid_cell(self):
        for changes in [{"cell_type": "unknown"}, {"source": [1]}, {"metadata": []}, {"source": None}]:
            with self.subTest(changes=changes):
                self.write("bad.ipynb", self.notebook(**changes))
                self.assertTrue(checks.check_repository(self.root))

    def test_notebook_outputs_and_counts(self):
        self.write("bad.ipynb", self.notebook(outputs=[{"output_type": "stream", "text": "old results"}], execution_count=1))
        errors = checks.check_repository(self.root)
        self.assertEqual(2, len(errors))
        self.assertIn("outputs", errors[0])
        self.assertIn("execution_count", errors[1])

    def test_markdown_cells_need_no_execution_fields(self):
        self.write("demo.ipynb", json.dumps({"nbformat": 4, "metadata": {}, "cells": [{"cell_type": "markdown", "metadata": {}, "source": "# Demo"}]}))
        self.assertEqual([], checks.check_repository(self.root))

    def test_external_anchor_code_and_html_links_ignored(self):
        self.write("README.md", '\n'.join([
            "[Web](https://example.org/x)", "[Mail](mailto:research@example.org)",
            "[Anchor](#section)", "[Protocol relative](//example.org/x)",
            '`[Not a link](missing.md)`', '<a href="missing.md">HTML</a>',
            '<!-- [hidden](missing.md) -->', "~~~markdown", "[Sample](missing.md)", "~~~",
            "```md", "[Sample](missing.md)", "```",
        ]))
        self.assertEqual([], checks.check_repository(self.root))

    def test_inline_and_reference_links(self):
        self.write("README.md", '[Read](missing.md "Title")\n[reference]: elsewhere.md\n')
        errors = checks.check_repository(self.root)
        self.assertEqual(2, len(errors))
        self.assertIn("line 1", errors[0])
        self.assertIn("line 2", errors[1])

    def test_encoded_spaces_parentheses_and_queries(self):
        self.write("data/figure (1).md", "# Figure")
        self.write("README.md", '[One](data/figure%20(1).md)\n[Two](<data/figure (1).md>)\n[Three](data/figure%20%281%29.md?raw=true#top)')
        self.assertEqual([], checks.check_repository(self.root))

    def test_nested_badge_link(self):
        self.write("README.md", '[![badge](https://example.org/badge.svg)](missing.md)')
        self.assertEqual(1, len(checks.check_repository(self.root)))

    def test_traversal_outside_root_rejected(self):
        self.write("README.md", '[Outside](../outside.md)\n[Encoded](%2e%2e/outside.md)\n')
        errors = checks.check_repository(self.root)
        self.assertEqual(2, len(errors))
        self.assertTrue(all("escapes" in error for error in errors))

    def test_git_internals_ignored_and_cannot_be_linked(self):
        self.write(".git/invalid.ipynb", "not JSON")
        self.assertEqual([], checks.check_repository(self.root))
        self.write("README.md", "[Internal](.git/invalid.ipynb)")
        self.assertIn("Git internals", checks.check_repository(self.root)[0])

    def test_symlink_cannot_escape(self):
        try:
            (self.root / "escape.md").symlink_to(self.root.parent / "external.md")
        except (NotImplementedError, OSError):
            self.skipTest("Symlink creation unavailable")
        self.assertIn("symlink escapes", checks.check_repository(self.root)[0])

    def test_credentials_detected_without_disclosing_values(self):
        value = "synthetic-value-for-test-only"
        for key in ["API_KEY", "ENTSOE_API_KEY", "ecoinvent_password", "access_token", "client_secret"]:
            with self.subTest(key=key):
                text = key + ' = "' + value + '"\n'
                errors = checks.credential_issues(text, "config.py")
                self.assertEqual(1, len(errors))
                self.assertNotIn(value, errors[0])

    def test_env_unquoted_credentials(self):
        self.write(".env", "ENTSOE_API_KEY" + "=synthetic-value-for-test-only\n")
        self.assertEqual(1, len(checks.check_repository(self.root)))

    def test_empty_env_values_never_consume_following_lines(self):
        for following in ["OTHER_VARIABLE=value", "# a comment", "ECOINVENT_USERNAME=", "\n", "  # comment", "ECOINVENT_PASSWORD="]:
            with self.subTest(following=following):
                text = "ENTSOE_API_KEY" + "=\n" + following + "\n"
                self.assertEqual([], checks.credential_issues(text, ".env.example", env_file=True))

    def test_empty_env_followed_by_actual_literal_is_precise(self):
        value = "synthetic-value-for-test-only"
        text = "ENTSOE_API_KEY" + "=\n# comment\nECOINVENT_PASSWORD=" + value + "\n"
        errors = checks.credential_issues(text, ".env.example", env_file=True)
        self.assertEqual(1, len(errors))
        self.assertIn("line 3", errors[0])
        self.assertNotIn(value, errors[0])

    def test_blank_lines_do_not_change_credential_line_number(self):
        text = "\n\nAPI_KEY" + ' = "synthetic-value-for-test-only"\n'
        self.assertIn("line 3", checks.credential_issues(text, "config.py")[0])

    def test_source_archive_skips_known_local_directories(self):
        for directory in [".venv", "__pycache__", "data/local", "model/local", "results"]:
            self.write(directory + "/invalid.ipynb", "not JSON")
        self.write("data/README.md", "# Data")
        self.assertEqual([], checks.check_repository(self.root))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_git_ignored_files_skipped_but_tracked_files_checked(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        self.write(".gitignore", ".venv/\n__pycache__/\ndata/local/\nmodel/local/\nresults/\n.env\n")
        for directory in [".venv", "__pycache__", "data/local", "model/local", "results"]:
            self.write(directory + "/invalid.ipynb", "not JSON")
        self.write(".env", "API_KEY" + "=synthetic-value-for-test-only\n")
        self.assertEqual([], checks.check_repository(self.root))
        subprocess.run(["git", "-C", str(self.root), "add", "-f", "results/invalid.ipynb"], check=True, capture_output=True)
        errors = checks.check_repository(self.root)
        self.assertEqual(1, len(errors))
        self.assertIn("results/invalid.ipynb", errors[0])

    def test_credentials_inside_notebook_source(self):
        self.write("demo.ipynb", self.notebook(source=["API_KEY" + ' = "synthetic-value-for-test-only"']))
        self.assertIn("cell 1", checks.check_repository(self.root)[0])

    def test_placeholder_values_do_not_fail(self):
        for value in ["", "<your-key>", "YOUR_ENTSOE_TOKEN", "replace-me", "changeme", "${ENTSOE_TOKEN}", "redacted"]:
            with self.subTest(value=value):
                self.assertEqual([], checks.credential_issues("API_KEY" + ' = "' + value + '"', "config.py"))

    def test_environment_calls_and_nonsensitive_names_do_not_fail(self):
        text = '\n'.join([
            "API_KEY" + ' = os.environ["ENTSOE_API_KEY"]',
            "password" + ' = getpass.getpass("Password: ")',
            'tokenizer = "word"', 'api_key_label = "API key"',
            '# ' + "API_KEY" + ' = "commented example"',
        ])
        self.assertEqual([], checks.credential_issues(text, "config.py"))

    def test_svg_invalid_root_and_entities_rejected(self):
        for svg in ["<svg>", "<html/>", '<!DOCTYPE svg [<!ENTITY x "x">]><svg/>']:
            with self.subTest(svg=svg):
                self.write("bad.svg", svg)
                self.assertEqual(1, len(checks.check_repository(self.root)))


if __name__ == "__main__":
    unittest.main()
