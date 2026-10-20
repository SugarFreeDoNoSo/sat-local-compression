"""Independent finite oracles for graph SAT semantics and all-order optimality."""

import unittest
from itertools import combinations, permutations, product

from experiments.graph_order_widths import (
    graph_predicate,
    grid_edges,
    optimal_order,
    residual_widths_by_subset,
)
from experiments.obdd_residuals import residual_widths


def exhaustive_selector_sat(bits, edges):
    """Evaluate the negative edge clauses and selected positive units on witnesses."""
    for witness in product((0, 1), repeat=len(bits)):
        units = all(not selected or witness[v] for v, selected in enumerate(bits))
        clauses = all(not witness[u] or not witness[v] for u, v in edges)
        if units and clauses:
            return 1
    return 0


class GraphOrderTests(unittest.TestCase):
    def test_graph_predicate_against_exhaustive_sat_on_all_small_graphs(self):
        for num_inputs in range(5):
            possible_edges = tuple(combinations(range(num_inputs), 2))
            for present in product((0, 1), repeat=len(possible_edges)):
                edges = tuple(edge for edge, bit in zip(possible_edges, present) if bit)
                function = graph_predicate(num_inputs, edges)
                for bits in product((0, 1), repeat=num_inputs):
                    with self.subTest(num_inputs=num_inputs, edges=edges, bits=bits):
                        self.assertEqual(function(bits), exhaustive_selector_sat(bits, edges))

    def test_minimax_matches_independent_exhaustive_order_oracle(self):
        functions = [
            (0, lambda bits: 0),
            (1, lambda bits: bits[0]),
            (4, lambda bits: 1),
            (4, lambda bits: sum(bits) % 2),
            (4, graph_predicate(4, ((0, 2), (1, 3)))),
            (5, graph_predicate(5, tuple((v, v + 1) for v in range(4)))),
            (5, graph_predicate(5, tuple((v, (v + 1) % 5) for v in range(5)))),
        ]
        for num_inputs, function in functions:
            with self.subTest(num_inputs=num_inputs, function=function):
                oracle = min(
                    max(residual_widths(function, order))
                    for order in permutations(range(num_inputs))
                )
                result = optimal_order(function, num_inputs)
                self.assertEqual(result.width, oracle)
                self.assertEqual(sorted(result.order), list(range(num_inputs)))
                self.assertEqual(max(residual_widths(function, result.order)), oracle)

    def test_subset_counts_match_each_cut_of_every_four_bit_order(self):
        function = graph_predicate(4, ((0, 1), (1, 2), (2, 3)))
        widths = residual_widths_by_subset(function, 4)
        for order in permutations(range(4)):
            subset = 0
            observed = [widths[subset]]
            for variable in order:
                subset |= 1 << variable
                observed.append(widths[subset])
            self.assertEqual(tuple(observed), residual_widths(function, order))

    def test_boundary_layers_for_constant_and_parity(self):
        for num_inputs in (0, 1, 4):
            constant = optimal_order(lambda bits: 0, num_inputs)
            self.assertEqual(constant.width, 1)
            self.assertTrue(all(width == 1 for width in constant.subset_widths))
        parity = optimal_order(lambda bits: sum(bits) % 2, 4)
        self.assertEqual(parity.width, 2)
        self.assertEqual(parity.subset_widths[0], 1)
        self.assertEqual(parity.subset_widths[-1], 2)

    def test_invalid_dimension_graph_or_output_is_rejected(self):
        for num_inputs in (-1, 11, 1.5):
            with self.assertRaises(ValueError):
                optimal_order(lambda bits: 0, num_inputs)
        for edges in (((0, 0),), ((0, 2),), ((0, 1), (1, 0)), ((0.5, 1),)):
            with self.assertRaises(ValueError):
                graph_predicate(2, edges)
        with self.assertRaises(ValueError):
            optimal_order(lambda bits: 2, 1)
        with self.assertRaises(ValueError):
            graph_predicate(2, ((0, 1),))((0,))
        with self.assertRaises(ValueError):
            grid_edges(0, 2)


if __name__ == "__main__":
    unittest.main()
