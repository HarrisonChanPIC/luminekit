"""Independent malformed-input and bundle-boundary expectations for repository checks."""

import tempfile
import unittest
from pathlib import Path

from scripts.check_links import check as check_links
from scripts.check_links import check_reserved, heading_ids, links
from scripts.check_skills import check as check_skills
from scripts.vendor.okf_validate import validate

ROOT = Path(__file__).resolve().parents[1]
HEADER = "---\nname: luminekit-example\ndescription: A useful example.\nlicense: Proprietary. All rights reserved.\n---\n"


class Workspace(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target


class MarkdownChecks(Workspace):
    def test_real_links_references_images_spaces_and_fragments(self):
        page = self.write(
            "entry.md",
            "[Owner][ref]\n\n[ref]: <a b.md#repeated-1>\n\n![asset](pic.png)\n[local](#entry)\n# Entry\n",
        )
        self.write("a b.md", "# Repeated\n\n# Repeated\n")
        self.write("pic.png", "not parsed as Markdown")
        self.assertEqual(check_links([page], self.root), [])

    def test_missing_file_and_heading_are_distinct_failures(self):
        page = self.write("entry.md", "[missing](gone.md)\n[bad heading](other.md#gone)\n")
        self.write("other.md", "# Present\n")
        errors = check_links([page], self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("missing target" in e for e in errors))
        self.assertTrue(any("missing heading" in e for e in errors))

    def test_code_examples_and_external_links_are_not_local_targets(self):
        text = "```md\n[wrong](missing.md)\n```\n`[wrong](also.md)`\n[remote](https://invalid.example/#x)\n[mail](mailto:fake@example.invalid)\n"
        self.assertEqual(links(text), ["https://invalid.example/#x", "mailto:fake@example.invalid"])
        self.assertEqual(check_links([self.write("a.md", text)], self.root), [])

    def test_unicode_punctuation_inline_code_setext_and_collision(self):
        self.assertEqual(
            heading_ids(
                "# Héllo, 世界! `value`\n# Héllo, 世界! `value`\nTitle\n=====\n# title\n# title-1\n"
            ),
            {"héllo-世界-value", "héllo-世界-value-1", "title", "title-1", "title-1-1"},
        )

    def test_leading_slash_uses_bundle_root_and_directory_entry(self):
        page = self.write("nested/a.md", "[bundle](/b.md#owner)\n[index](../group/#contents)\n")
        self.write("b.md", "# Owner\n")
        self.write("group/index.md", "# Contents\n")
        self.assertEqual(check_links([page], self.root), [])


class SkillChecks(Workspace):
    def entry(self, body="Useful procedure.\n", header=HEADER):
        return self.write("luminekit-example/SKILL.md", header + body)

    def errors(self, selected=None):
        return check_skills(self.root, selected)[1]

    def test_valid_resources_and_selected_sibling_closure(self):
        self.entry("[Read when needed](references/a.md)\n")
        self.write("luminekit-example/references/a.md", "# Procedure\nUseful guidance.\n")
        self.assertEqual(self.errors(["luminekit-example"]), [])
        self.entry("Use `luminekit-missing`.\n")
        self.assertTrue(any("unknown or unselected" in e for e in self.errors()))

    def test_orphan_and_escape(self):
        self.entry("[escape](../outside.md)\n")
        self.write("outside.md", "An unrelated file.")
        self.write("luminekit-example/orphan.txt", "not distributed by a reachable route")
        errors = self.errors()
        self.assertTrue(any("Link leaves" in e for e in errors))
        self.assertTrue(any("Not reachable" in e for e in errors))

    def test_file_and_directory_symlink_escape(self):
        self.entry("[escape](link.md)\n")
        outside = self.write("outside.md", "# External\n")
        (self.root / "luminekit-example/link.md").symlink_to(outside)
        (self.root / "luminekit-example/ext").symlink_to(self.root, target_is_directory=True)
        self.assertTrue(any("symlink leaves" in e for e in self.errors()))

    def test_internal_file_symlink_keeps_resource_reachable(self):
        self.entry("[procedure](alias.md)\n")
        original = self.write("luminekit-example/procedure.md", "# Procedure\nUseful guidance.\n")
        (self.root / "luminekit-example/alias.md").symlink_to(original)
        self.assertEqual(self.errors(), [])

    def test_frontmatter_license_name_and_types(self):
        for header, expected in [
            ("---\nname: [\n---\n", "YAML"),
            (HEADER.replace("name: luminekit-example", "name: Wrong"), "name must match"),
            (HEADER.replace("description: A useful example.", "description: []"), "description"),
            (
                HEADER.replace("license: Proprietary. All rights reserved.", "license: MIT"),
                "rights-reserved",
            ),
            (HEADER.replace("---\nname:", "---\nextra: value\nname:"), "Unknown frontmatter"),
            (HEADER.replace("---\nname:", "---\nmetadata: {n: 4}\nname:"), "metadata must map"),
        ]:
            with self.subTest(expected=expected):
                self.entry(header=header)
                errors = self.errors()
                self.assertTrue(errors)
                if expected != "YAML":
                    self.assertTrue(any(expected in e for e in errors), errors)

    def test_missing_resource_is_caught_by_link_gate(self):
        self.entry("[read](missing.md)\n")
        self.assertTrue(check_links([self.root], self.root))


class OkfChecks(Workspace):
    def test_tracked_valid_fixture_and_reserved_structure(self):
        bundle = ROOT / "tests/fixtures/okf/valid"
        self.assertEqual(validate(bundle).errors, [])
        self.assertEqual(check_reserved(bundle), [])
        self.assertEqual(check_links([bundle], bundle), [])

    def test_invalid_fixtures_fail_for_expected_reason(self):
        for folder, reason in [
            ("missing-type", "type"),
            ("bad-yaml", "YAML"),
            ("empty-type", "type"),
        ]:
            with self.subTest(folder=folder):
                errors = validate(ROOT / "tests/fixtures/okf" / folder).errors
                self.assertTrue(any(reason in error for error in errors), errors)

    def test_unknown_type_extension_optional_absence_and_broken_links_are_consumable(self):
        self.write(
            "unknown.md",
            "---\ntype: RenewalWindow\nopaque: {keep: true}\n---\n[future](not-written.md)\n",
        )
        self.assertEqual(validate(self.root).errors, [])
        self.assertTrue(check_links([self.root], self.root))  # maintained-route policy is stricter

    def test_root_only_version_exception_and_log_order_are_gated(self):
        self.write(
            "index.md", '---\nokf_version: "0.2"\n---\n# Knowledge\n* [Item](item.md) - Item.\n'
        )
        self.assertEqual(check_reserved(self.root), [])
        self.write(
            "nested/index.md",
            '---\nokf_version: "0.2"\n---\n# Wrong\n* [Item](../item.md) - Item.\n',
        )
        self.write("log.md", "# Updates\n## 2026-01-01\n* Old.\n## 2026-02-01\n* New.\n")
        errors = check_reserved(self.root)
        self.assertTrue(any("reserved frontmatter" in e for e in errors))
        self.assertTrue(any("newest first" in e for e in errors))
        self.write(
            "index.md",
            '---\nokf_version: "0.2"\nupkeep: true\n---\n# Items\n* [Item](item.md) - Item.\n',
        )
        self.assertTrue(any("root okf_version" in e for e in check_reserved(self.root)))

    def test_reserved_malformed_dates_and_concept_frontmatter_are_rejected(self):
        self.write(
            "log.md", "---\ntype: Reference\n---\n# Updates\n## 2026-02-31\n* Impossible date.\n"
        )
        self.assertTrue(any("YYYY-MM-DD" in e for e in check_reserved(self.root)))
        self.assertTrue(any("reserved frontmatter" in e for e in check_reserved(self.root)))


if __name__ == "__main__":
    unittest.main()
