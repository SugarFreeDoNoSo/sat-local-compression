"""Independent finite checks of the incidence encoding and residual method."""

import unittest
from itertools import product

from experiments.obdd_residuals import disjointness, residual_widths


def exhaustive_unit_sat(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    """Evaluate the actual unit clauses over every candidate witness."""
    for witness in product((0, 1), repeat=len(a)):
        positive = all(not present or witness[i] for i, present in enumerate(a))
        negative = all(not present or not witness[i] for i, present in enumerate(b))
        if positive and negative:
            return 1
    return 0


class ResidualTests(unittest.TestCase):
    def test_incidence_predicate_against_exhaustive_sat(self):
        for m in range(1, 5):
            for values in product((0, 1), repeat=2 * m):
                with self.subTest(m=m, values=values):
                    self.assertEqual(
                        disjointness(values),
                        exhaustive_unit_sat(values[:m], values[m:]),
                    )

    def test_grouped_and_interleaved_theorem_instances(self):
        for m in range(1, 7):
            with self.subTest(m=m):
                grouped = residual_widths(disjointness, tuple(range(2 * m)))
                order = tuple(j for i in range(m) for j in (i, m + i))
                interleaved = residual_widths(disjointness, order)
                self.assertEqual(grouped[m], 2**m)
                self.assertLessEqual(max(interleaved), 3)
                self.assertEqual(grouped[0], 1)
                self.assertEqual(grouped[-1], 2)

    def test_parity_and_constant_residuals(self):
        for order in [(0, 1, 2, 3), (3, 1, 0, 2)]:
            self.assertEqual(
                residual_widths(lambda bits: sum(bits) % 2, order),
                (1, 2, 2, 2, 2),
            )
            self.assertEqual(
                residual_widths(lambda bits: 0, order), (1, 1, 1, 1, 1)
            )

    def test_invalid_input_order_is_rejected(self):
        with self.assertRaises(ValueError):
            residual_widths(lambda bits: 0, (0, 0))
        with self.assertRaises(ValueError):
            residual_widths(lambda bits: 0, (1, 2))


if __name__ == "__main__":
    unittest.main()
