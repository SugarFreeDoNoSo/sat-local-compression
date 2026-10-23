"""Independent finite checks of L03 certificate conditions and witnesses."""

from dataclasses import replace
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from experiments.graph_order_widths import graph_predicate, residual_widths_by_subset
from experiments.matching_certificates import (
    MatchingCertificate, artifact_contents, certificate_from_dict,
    greedy_certificate, separating_assignments, verify_certificate,
)


class MatchingCertificateTests(unittest.TestCase):
    def test_all_small_graphs_and_cuts_against_full_truth_tables(self):
        checked = 0
        for n in range(6):
            possible = tuple(combinations(range(n), 2))
            for mask in range(1 << len(possible)):
                edges = tuple(edge for i, edge in enumerate(possible) if mask & (1 << i))
                function = graph_predicate(n, edges)
                widths = residual_widths_by_subset(function, n)
                for cut in range(1 << n):
                    read = tuple(v for v in range(n) if cut & (1 << v))
                    certificate = greedy_certificate(n, edges, read)
                    result = verify_certificate(certificate)
                    self.assertTrue(result.covers_crossing_edges)
                    self.assertLessEqual(result.width_lower_bound, widths[cut])
                    self.assertLessEqual(result.crossing_edges,
                                         2 * result.maximum_degree**2 * result.matching_size)
                    for a, b in combinations(range(1 << result.matching_size), 2):
                        left, right = separating_assignments(certificate, a, b)
                        self.assertNotEqual(function(left), function(right))
                        self.assertTrue(all(left[v] == right[v] for v in range(n) if v not in read))
                    checked += 1
        self.assertEqual(checked, 33867)

    def test_rejects_cross_and_same_side_noninduced_matchings(self):
        # Crossing-only matching is insufficient: true widths are 3 and 7.
        cases = [
            (4, ((0, 2), (1, 3), (0, 3)), (0, 1), ((0, 2), (1, 3)), 3),
            (6, ((0, 3), (1, 4), (2, 5), (0, 1)), (0, 1, 2),
             ((0, 3), (1, 4), (2, 5)), 7),
        ]
        for n, edges, read, matching, width in cases:
            certificate = MatchingCertificate(n, edges, read, matching)
            with self.assertRaisesRegex(ValueError, "whole graph"):
                verify_certificate(certificate)
            actual = residual_widths_by_subset(graph_predicate(n, edges), n)
            self.assertEqual(actual[sum(1 << v for v in read)], width)
            self.assertLess(width, 1 << len(matching))
        # Even when the numeric width bound survives, unread-side interference
        # must be rejected by the stated whole-graph certificate contract.
        with self.assertRaisesRegex(ValueError, "whole graph"):
            verify_certificate(MatchingCertificate(4, ((0, 2), (1, 3), (2, 3)),
                                                   (0, 1), ((0, 2), (1, 3))))

    def test_width_certificate_does_not_require_maximal_cover(self):
        certificate = MatchingCertificate(4, ((0, 2), (1, 3)), (0, 1), ())
        result = verify_certificate(certificate)
        self.assertEqual(result.width_lower_bound, 1)
        self.assertFalse(result.packing_bound_verified)
        # Numerical c <= 2*Delta^2*q may hold accidentally without coverage.
        result = verify_certificate(replace(certificate, matching=((0, 2),)))
        self.assertEqual(result.width_lower_bound, 2)
        self.assertFalse(result.packing_bound_verified)
        self.assertLessEqual(result.crossing_edges, 2 * result.maximum_degree**2 * result.matching_size)

    def test_non_greedy_maximal_matching_is_a_valid_cover(self):
        certificate = MatchingCertificate(4, ((0, 2), (0, 3), (1, 3)), (0, 1), ((0, 3),))
        result = verify_certificate(certificate)
        self.assertTrue(result.packing_bound_verified)
        self.assertEqual(result.width_lower_bound, 2)

    def test_zero_degree_empty_and_full_cuts(self):
        for n, edges in ((0, ()), (4, ()), (2, ((0, 1),))):
            for read in ((), tuple(range(n))):
                result = verify_certificate(greedy_certificate(n, edges, read))
                self.assertEqual(result.width_lower_bound, 1)
                self.assertTrue(result.covers_crossing_edges)
                self.assertEqual(result.crossing_edges, 0)

    def test_input_validation_and_untrusted_claim_fields(self):
        good = greedy_certificate(4, ((0, 2), (1, 3)), (0, 1))
        self.assertEqual(certificate_from_dict(good.as_dict()), good)
        bad = [replace(good, num_vertices=True), replace(good, num_vertices=257),
               replace(good, edges=((0, 0),)), replace(good, edges=((0, 2), (2, 0))),
               replace(good, edges=((0, 4),)), replace(good, read_vertices=(0, 0)),
               replace(good, read_vertices=(False, 1)), replace(good, matching=((2, 0),)),
               replace(good, matching=((0, 3),)), replace(good, matching=((0, 2), (0, 2)))]
        for certificate in bad:
            with self.assertRaises(ValueError):
                verify_certificate(certificate)
        for value in (None, [], {}, {**good.as_dict(), "width_lower_bound": 1000},
                      {**good.as_dict(), "schema_version": True},
                      {**good.as_dict(), "matching": [[0]]}):
            with self.assertRaises(ValueError):
                certificate_from_dict(value)
        for a, b in ((0, 0), (-1, 0), (0, 4), (True, 0)):
            with self.assertRaises(ValueError):
                separating_assignments(good, a, b)

    def test_large_certificate_does_not_enumerate_prefixes(self):
        # 128 crossing edges certify width 2^128 without building that many words.
        certificate = greedy_certificate(256, ((i, i + 128) for i in range(128)), range(128))
        self.assertEqual(verify_certificate(certificate).width_lower_bound, 1 << 128)
        left, right = separating_assignments(certificate, 0, (1 << 128) - 1)
        self.assertNotEqual(all(not (left[u] and left[v]) for u, v in certificate.edges),
                            all(not (right[u] and right[v]) for u, v in certificate.edges))

    def test_examples_deterministic_and_cli_rejects_tampering(self):
        self.assertEqual(artifact_contents(), artifact_contents())
        payload = json.loads(artifact_contents())
        self.assertEqual(len(payload["examples"]), 6)
        for example in payload["examples"]:
            verified = verify_certificate(certificate_from_dict(example["certificate"]))
            self.assertEqual(verified.__dict__, example["verified"])
        script = Path(__file__).resolve().parents[1] / "experiments/matching_certificates.py"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            value = greedy_certificate(4, ((0, 2), (1, 3)), (0, 1)).as_dict()
            path.write_text(json.dumps(value))
            result = subprocess.run([sys.executable, str(script), "--verify", str(path)], capture_output=True)
            self.assertEqual(result.returncode, 0)
            value["edges"].append([0, 1])
            path.write_text(json.dumps(value))
            result = subprocess.run([sys.executable, str(script), "--verify", str(path)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b"whole graph", result.stdout)


if __name__ == "__main__":
    unittest.main()
