"""Regression checks for review-request integrity, not mathematical truth."""

import copy
from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from scripts import check_review_packet as checker
from scripts.check_review_packet import ROOT, MANIFEST, DOCUMENT, render, validate


class ReviewPacketTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.packet = json.loads((ROOT / MANIFEST).read_text(encoding="utf-8"))
        self.register = json.loads((ROOT / "research/claims.json").read_text(encoding="utf-8"))
        for name in self.packet["source_sha256"]:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def check(self):
        validate(self.root, self.packet, self.register)

    def test_current_snapshot_and_generated_document(self):
        self.check()
        self.assertEqual(render(self.packet, self.register),
                         (ROOT / DOCUMENT).read_text(encoding="utf-8"))

    def test_missing_claim_coverage(self):
        self.packet["review_units"][0]["claim_ids"].remove("T01")
        with self.assertRaisesRegex(ValueError, "cover every claim"):
            self.check()

    def test_duplicate_claim_coverage(self):
        self.packet["review_units"][1]["claim_ids"].append("T01")
        with self.assertRaisesRegex(ValueError, "Duplicate review claim"):
            self.check()

    def test_unknown_claim(self):
        self.packet["review_units"][0]["claim_ids"][0] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "cover every claim"):
            self.check()

    def test_changed_source(self):
        (self.root / "paper/sections/02-model.tex").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Source changed"):
            self.check()

    def test_missing_source(self):
        (self.root / "formal/AxiomAudit.lean").unlink()
        with self.assertRaisesRegex(ValueError, "Snapshot file set changed"):
            self.check()

    def test_added_source(self):
        (self.root / "paper/sections/new.tex").write_text("new claim", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Snapshot file set changed"):
            self.check()

    def test_unpinned_reading_source(self):
        self.packet["review_units"][0]["sources"].append("missing.md")
        with self.assertRaisesRegex(ValueError, "Unpinned reading source"):
            self.check()

    def test_empty_question(self):
        self.packet["review_units"][0]["questions"].append(" ")
        with self.assertRaisesRegex(ValueError, "Empty review question"):
            self.check()

    def test_duplicate_unit(self):
        self.packet["review_units"].append(copy.deepcopy(self.packet["review_units"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate review-unit"):
            self.check()

    def test_short_revision_and_false_certification(self):
        self.packet["source_revision"] = "19a33be"
        with self.assertRaisesRegex(ValueError, "full commit SHA"):
            self.check()
        self.packet["source_revision"] = "19a33beaf62e6b8ec096955ea7a766001a16c723"
        self.packet["kind"] = "review-complete"
        with self.assertRaisesRegex(ValueError, "remain a review request"):
            self.check()

    def test_symlink_cannot_escape_checkout(self):
        path = self.root / "paper/sections/02-model.tex"
        path.unlink()
        path.symlink_to(ROOT / "paper/sections/02-model.tex")
        with self.assertRaisesRegex(ValueError, "escapes the checkout"):
            self.check()

    def run_cli(self, arguments):
        (self.root / MANIFEST).write_text(json.dumps(self.packet), encoding="utf-8")
        document = self.root / DOCUMENT
        document.parent.mkdir(parents=True, exist_ok=True)
        output = io.StringIO()
        with patch.object(checker, "ROOT", self.root), redirect_stdout(output), redirect_stderr(output):
            result = checker.main(arguments)
        return result, output.getvalue()

    def test_cli_rejects_stale_document(self):
        (self.root / DOCUMENT).write_text("stale", encoding="utf-8")
        result, output = self.run_cli([])
        self.assertEqual(result, 1)
        self.assertIn("Review document is stale", output)

    def test_cli_write_regenerates_document_without_changing_pins(self):
        before = copy.deepcopy(self.packet)
        result, _ = self.run_cli(["--write"])
        self.assertEqual(result, 0)
        self.assertEqual((self.root / DOCUMENT).read_text(encoding="utf-8"),
                         render(self.packet, self.register))
        self.assertEqual(json.loads((self.root / MANIFEST).read_text(encoding="utf-8")), before)

    def test_cli_write_refuses_source_drift(self):
        (self.root / "paper/main.tex").write_text("changed", encoding="utf-8")
        result, output = self.run_cli(["--write"])
        self.assertEqual(result, 1)
        self.assertIn("Source changed", output)
        self.assertFalse((self.root / DOCUMENT).exists())


if __name__ == "__main__":
    unittest.main()
