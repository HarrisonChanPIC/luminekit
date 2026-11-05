"""Behavior of scripts bundled inside skills: fingerprints and quotation filling."""

import contextlib
import copy
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    # Keep bytecode caches out of the shipped skill folders.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fp = load("fingerprints", "skills/luminekit-docs/scripts/fingerprints.py")
fq = load("fill_quotation", "skills/luminekit-corporate-quotation/scripts/fill_quotation.py")


class Fingerprints(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "folder"
        self.root.mkdir()
        self.out = self.root / fp.DEFAULT_NAME

    def put(self, rel, data):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def run_scan(self, *extra):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(io.StringIO()):
            code = fp.main(["scan", str(self.root), *extra])
        return code, json.loads(buffer.getvalue())

    def test_duplicates_moves_changes_and_additions(self):
        self.put("a/quote.docx", b"same bytes")
        self.put("b/quote copy.docx", b"same bytes")
        self.put("c/notes.txt", b"one")
        self.put("c/old.pdf", b"pdf bytes")
        code, first = self.run_scan()
        self.assertEqual(code, 0)
        self.assertEqual(first["duplicates"], [["a/quote.docx", "b/quote copy.docx"]])
        self.assertEqual(sorted(first["added"]), sorted(fp.read(self.out)))

        (self.root / "c/old.pdf").rename(self.root / "c/renamed.pdf")
        self.put("c/notes.txt", b"two, longer")
        self.put("d/new.xlsx", b"new")
        _, second = self.run_scan()
        self.assertEqual(second["moved"], [{"from": "c/old.pdf", "to": "c/renamed.pdf"}])
        self.assertEqual(second["changed"], ["c/notes.txt"])
        self.assertEqual(second["added"], ["d/new.xlsx"])
        self.assertEqual(second["deleted"], [])

        (self.root / "d/new.xlsx").unlink()
        _, third = self.run_scan()
        self.assertEqual(third["deleted"], ["d/new.xlsx"])

    def test_file_is_sorted_csv_and_skips_hidden_lock_symlink_and_excluded(self):
        self.put("b.txt", b"b")
        self.put("a.txt", b"a")
        self.put(".hidden/x.txt", b"x")
        self.put("~$lock.docx", b"lock")
        self.put("knowledge/index.md", b"# Index")
        (self.root / "link.txt").symlink_to(self.root / "a.txt")
        self.run_scan("--exclude", str(self.root / "knowledge"))
        lines = self.out.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "path,size,mtime_ns,sha256")
        self.assertEqual([line.split(",")[0] for line in lines[1:]], ["a.txt", "b.txt"])

    def test_unchanged_files_are_not_rehashed_and_full_rehashes(self):
        path = self.put("doc.txt", b"aaaa")
        self.run_scan()
        stat = path.stat()
        path.write_bytes(b"bbbb")  # same size
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        _, quick = self.run_scan()
        self.assertEqual(quick["changed"], [])
        _, full = self.run_scan("--full")
        self.assertEqual(full["changed"], ["doc.txt"])

    def test_partial_scan_reports_no_deletions_and_keeps_entries(self):
        self.put("keep.txt", b"k")
        locked = self.put("locked/inner.txt", b"i")
        self.run_scan()
        os.chmod(locked.parent, 0)
        self.addCleanup(os.chmod, locked.parent, 0o755)
        if os.access(locked.parent, os.R_OK):
            self.skipTest("permissions are not enforced for this user")
        code, report = self.run_scan()
        self.assertEqual(code, 1)
        self.assertEqual(report["deleted"], [])
        self.assertEqual(report["not_seen"], ["locked/inner.txt"])
        self.assertIn("locked/inner.txt", fp.read(self.out))

    def test_compare_two_files(self):
        old = {"x": {"path": "x", "size": 1, "mtime_ns": 1, "sha256": "h1"}}
        new = {"y": {"path": "y", "size": 1, "mtime_ns": 2, "sha256": "h1"}}
        self.assertEqual(fp.compare(old, new)["moved"], [{"from": "x", "to": "y"}])
        new["x"] = old["x"]
        report = fp.compare(old, new)
        self.assertEqual(report["copied"], [{"from": "x", "to": "y"}])
        self.assertEqual(report["duplicates"], [["x", "y"]])


SAMPLE = {
    "issuer": {
        "name": "Seller Inc.",
        "tin": "000-000-000-00000",
        "address": "1 Seller St",
        "website": "https://seller.example",
    },
    "customer": {
        "name": "Buyer Corp.",
        "address": "2 Buyer Rd",
        "contact_name": "Alex Buyer",
        "contact": "+00 0000",
    },
    "quotation": {
        "number": "Q-1",
        "date": "November 5, 2026",
        "project": "Widgets",
        "valid_until": "December 5, 2026",
    },
    "currency": "PHP",
    "vat": {"basis": "exclusive", "rate": "0.12"},
    "items": [
        {
            "title": "Widget",
            "detail": "Delivered.",
            "charge": "one-time",
            "unit_price": "1000.005",
            "quantity": 3,
        },
        {
            "title": "Support",
            "charge": "recurring",
            "period": "year",
            "unit_price": "500.00",
            "quantity": 1,
            "unit": "/ yr",
        },
        {
            "title": "Later support",
            "charge": "recurring",
            "period": "year",
            "price_note": "CPI + 2%",
            "quantity": 1,
        },
    ],
    "remarks": ["Prices exclude VAT."],
    "payment_terms": "Payment due within 30 days.",
    "signatories": {
        "issuer": [
            {"role": "General Manager", "name": "Sam Seller"},
            {"role": "Head of Finance", "name": "Pat Finance"},
        ],
        "customer": [{"role": "President", "name": "Alex Buyer"}],
    },
}
TEMPLATE = ROOT / "skills/luminekit-corporate-quotation/assets/quotation-template.docx"


def text_of(path):
    import docx

    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for table in d.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    for section in d.sections:
        parts.extend(p.text for p in section.header.paragraphs + section.footer.paragraphs)
    props = d.core_properties
    parts += [props.author or "", props.last_modified_by or "", props.title or ""]
    return "\n".join(parts)


class Quotation(unittest.TestCase):
    def totals(self, data):
        totals, variable = fq.compute(fq.validate(copy.deepcopy(data)))
        return {t["group"]: t for t in totals}, variable

    def test_template_has_no_source_quotation_data(self):
        text = text_of(TEMPLATE)
        for leaked in (
            "Yuanta",
            "Regina",
            "NCR",
            "1,130,025",
            "Schedule",
            "SCHEDULE",
            "October 20",
            "November 6",
            "Sheng-Hui",
            "Kao",
            "010-873",
            "pic.net",
        ):
            self.assertNotIn(leaked, text)
        self.assertIn("{{customer_name}}", text)

    def test_exclusive_totals_round_half_up_and_keep_groups_apart(self):
        groups, variable = self.totals(SAMPLE)
        self.assertEqual(groups["one-time"]["net"], Decimal("3000.02"))  # 3000.015
        self.assertEqual(groups["one-time"]["vat"], Decimal("360.00"))
        self.assertEqual(groups["one-time"]["gross"], Decimal("3360.02"))
        self.assertEqual(groups["recurring per year"]["net"], Decimal("500.00"))
        self.assertEqual(variable, [3])

    def test_inclusive_basis_extracts_vat(self):
        data = copy.deepcopy(SAMPLE)
        data["vat"]["basis"] = "inclusive"
        data["items"] = [
            {"title": "Box", "charge": "one-time", "unit_price": "1120", "quantity": 1}
        ]
        groups, _ = self.totals(data)
        self.assertEqual(groups["one-time"]["gross"], Decimal("1120"))
        self.assertEqual(groups["one-time"]["vat"], Decimal("120.00"))
        self.assertEqual(groups["one-time"]["net"], Decimal("1000.00"))

    def test_issuer_needs_exactly_two_signatories(self):
        for count in (1, 3):
            data = copy.deepcopy(SAMPLE)
            data["signatories"]["issuer"] = [
                {"role": "Role", "name": f"N{n}"} for n in range(count)
            ]
            with self.assertRaises(fq.InputError) as caught:
                fq.validate(data)
            self.assertIn("exactly 2", str(caught.exception))

    def test_missing_and_invalid_inputs_are_refused_together(self):
        data = copy.deepcopy(SAMPLE)
        del data["vat"]["rate"]
        del data["customer"]["name"]
        data["items"][0]["unit_price"] = 1000.5
        del data["items"][1]["period"]
        with self.assertRaises(fq.InputError) as caught:
            fq.validate(data)
        message = str(caught.exception)
        for expected in ("vat.rate", "customer.name", "not a float", "items[2].period"):
            self.assertIn(expected, message)

    def test_filled_document_matches_inputs_and_has_no_placeholders(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "in.json"
            source.write_text(json.dumps(SAMPLE), encoding="utf-8")
            output = Path(temp) / "out.docx"
            with contextlib.redirect_stdout(io.StringIO()) as printed:
                self.assertEqual(fq.main([str(source), str(output)]), 0)
            report = json.loads(printed.getvalue())
            self.assertEqual(report["totals"][0]["gross"], "3360.02")
            text = text_of(output)
            self.assertNotIn("{{", text)
            for value in (
                "Buyer Corp.",
                "1,000.005",
                "3,000.02",
                "PHP 3,360.02",
                "Variable",
                "Payment due within 30 days.",
                "Head of Finance: Pat Finance",
                "valid until December 5, 2026",
                "VAT (12%)",
            ):
                self.assertIn(value, text)
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(fq.main([str(source), str(output)]), 2)  # no overwrite


if __name__ == "__main__":
    unittest.main()
