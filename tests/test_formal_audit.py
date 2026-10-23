"""Fail-closed controls for the real Lean axiom-closure report parser."""

import json
from pathlib import Path
import re
import unittest

from scripts.check_formal import ALLOWED_AXIOMS, THEOREMS, parse_audit


def report(name, axioms=()):
    data = (f"'{name}' depends on axioms: [{', '.join(axioms)}]" if axioms
            else f"'{name}' does not depend on any axioms")
    return json.dumps({"severity": "information", "data": data})


class FormalAuditTests(unittest.TestCase):
    def test_complete_audit_accepts_only_declared_standard_axioms(self):
        text = "\n".join(report(name, sorted(ALLOWED_AXIOMS)) for name in sorted(THEOREMS))
        result = parse_audit(text)
        self.assertEqual(set(result), THEOREMS)
        self.assertTrue(all(set(axioms) == ALLOWED_AXIOMS for axioms in result.values()))

    def test_audit_source_and_expected_declarations_match(self):
        source = (Path(__file__).resolve().parents[1] / "formal/AxiomAudit.lean").read_text()
        declarations = re.findall(r"^#print axioms (\S+)$", source, re.M)
        self.assertEqual(len(declarations), len(set(declarations)))
        self.assertEqual(set(declarations), THEOREMS)
        self.assertIn("ResidualWidths.grouped_width_characterization", THEOREMS)

    def test_missing_or_duplicate_declaration_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing declarations"):
            parse_audit("")
        name = next(iter(THEOREMS))
        with self.assertRaisesRegex(ValueError, "repeated declaration"):
            parse_audit(report(name) + "\n" + report(name))

    def test_forbidden_axioms_and_namespaced_lookalikes_are_rejected(self):
        name = next(iter(THEOREMS))
        for axiom in ("sorryAx", "fakeProof", "Untrusted.propext", "Untrusted.Quot.sound"):
            with self.subTest(axiom=axiom), self.assertRaisesRegex(ValueError, "forbidden axioms"):
                parse_audit(report(name, (axiom,)))

    def test_warnings_and_errors_are_not_success(self):
        for severity in ("warning", "error"):
            with self.subTest(severity=severity), self.assertRaisesRegex(ValueError, "Lean diagnostic"):
                parse_audit(json.dumps({"severity": severity, "data": "proof placeholder"}))

    def test_unknown_declaration_and_unexpected_message_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unexpected or repeated declaration"):
            parse_audit(report("ResidualWidths.unlisted"))
        with self.assertRaisesRegex(ValueError, "Unexpected axiom-audit output"):
            parse_audit(json.dumps({"severity": "information", "data": "success"}))


if __name__ == "__main__":
    unittest.main()
