"""Independent finite checks of L04's exact graph-residual classification."""

from itertools import combinations
import unittest

from experiments.graph_order_widths import (
    cases, graph_predicate, optimal_order, optimal_order_from_subset_widths,
    residual_widths_by_subset,
)
from experiments.graph_signatures import (
    optimal_graph_order, residual_signature, signature_widths_by_subset,
)


class GraphSignatureTests(unittest.TestCase):
    def test_signatures_classify_actual_residual_truth_tables(self):
        for num_inputs in range(5):
            possible = tuple(combinations(range(num_inputs), 2))
            full = (1 << num_inputs) - 1
            for edge_mask in range(1 << len(possible)):
                edges = tuple(edge for i, edge in enumerate(possible) if edge_mask & (1 << i))
                predicate = graph_predicate(num_inputs, edges)
                for read in range(full + 1):
                    unread = full ^ read
                    by_signature = {}
                    by_table = {}
                    for selected in range(full + 1):
                        if selected & ~read:
                            continue
                        signature = residual_signature(num_inputs, edges, read, selected)
                        table = tuple(
                            predicate(tuple(((selected | suffix) >> v) & 1 for v in range(num_inputs)))
                            for suffix in range(full + 1) if not suffix & ~unread
                        )
                        self.assertEqual(by_signature.setdefault(signature, table), table)
                        self.assertEqual(by_table.setdefault(table, signature), signature)
                        self.assertEqual(table[0], int(signature is not None))

    def test_every_cut_of_every_simple_graph_on_at_most_five_vertices(self):
        checked_graphs = 0
        checked_cuts = 0
        for num_inputs in range(6):
            possible = tuple(combinations(range(num_inputs), 2))
            for edge_mask in range(1 << len(possible)):
                edges = tuple(edge for i, edge in enumerate(possible) if edge_mask & (1 << i))
                expected = residual_widths_by_subset(graph_predicate(num_inputs, edges), num_inputs)
                actual = signature_widths_by_subset(num_inputs, edges)
                self.assertEqual(actual, expected, (num_inputs, edges))
                checked_graphs += 1
                checked_cuts += len(actual)
        self.assertEqual(checked_graphs, 1100)
        self.assertEqual(checked_cuts, 33867)

    def test_named_graph_orders_match_full_table_backend(self):
        for name, num_inputs, edges in cases():
            with self.subTest(family=name):
                self.assertEqual(optimal_graph_order(num_inputs, edges),
                                 optimal_order(graph_predicate(num_inputs, edges), num_inputs))

    def test_empty_graph_and_empty_full_cuts(self):
        self.assertEqual(signature_widths_by_subset(0, ()), (1,))
        self.assertEqual(residual_signature(0, (), 0, 0), 0)
        for num_inputs in range(6):
            self.assertEqual(signature_widths_by_subset(num_inputs, ()), (1,) * (1 << num_inputs))
        widths = signature_widths_by_subset(2, ((0, 1),))
        self.assertEqual(widths, (1, 2, 2, 2))

    def test_dead_signature_never_collides_with_live_zero_mask(self):
        edges = ((0, 1),)
        self.assertIsNone(residual_signature(2, edges, 3, 3))
        self.assertEqual(residual_signature(2, edges, 3, 0), 0)
        self.assertEqual(residual_signature(2, edges, 3, 1), 0)
        self.assertEqual(signature_widths_by_subset(2, edges)[3], 2)

    def test_equal_neighborhoods_merge_and_independent_prefixes_only(self):
        edges = ((0, 2), (1, 2))
        self.assertEqual(residual_signature(3, edges, 3, 1), 4)
        self.assertEqual(residual_signature(3, edges, 3, 2), 4)
        self.assertEqual(residual_signature(3, edges, 3, 3), 4)
        self.assertEqual(signature_widths_by_subset(3, edges)[3], 2)
        # Six independent read subsets give six distinct masks, plus one dead residual.
        edges = ((0, 3), (1, 4), (2, 5), (0, 1))
        self.assertEqual(signature_widths_by_subset(6, edges)[7], 7)

    def test_unread_internal_edges_do_not_identify_different_live_signatures(self):
        edges = ((0, 2), (1, 3), (2, 3))
        self.assertEqual(signature_widths_by_subset(4, edges)[3], 4)
        self.assertEqual(residual_signature(4, edges, 3, 1), 4)
        self.assertEqual(residual_signature(4, edges, 3, 2), 8)

    def test_one_shot_edge_iterables(self):
        expected = signature_widths_by_subset(3, ((0, 1), (1, 2)))
        self.assertEqual(signature_widths_by_subset(3, iter(((0, 1), (1, 2)))), expected)
        self.assertEqual(residual_signature(3, iter(((0, 1), (1, 2))), 1, 1), 2)

    def test_invalid_graphs_dimensions_and_masks_are_rejected(self):
        for num_inputs in (-1, 11, 1.5, True):
            with self.assertRaises(ValueError):
                signature_widths_by_subset(num_inputs, ())
        for edges in (((0, 0),), ((0, 2),), ((0, 1), (1, 0)), ((False, 1),),
                      ((0.5, 1),), ((0,),), ((0, 1, 2),), (0,)):
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                signature_widths_by_subset(2, edges)
        for read, selected in ((-1, 0), (4, 0), (1, 2), (3, 4), (3, -1), (True, 0), (3, True)):
            with self.subTest(read=read, selected=selected), self.assertRaises(ValueError):
                residual_signature(2, (), read, selected)

    def test_precomputed_width_table_requires_shape_and_positive_integers(self):
        for widths in ((), (1,), (1, 0), (1, -1), (1, 1.0), (1, True), (1, 2, 3)):
            with self.subTest(widths=widths), self.assertRaises(ValueError):
                optimal_order_from_subset_widths(widths, 1)
        result = optimal_order_from_subset_widths(iter((1, 2, 2, 2)), 2)
        self.assertEqual(result.width, 2)
        self.assertEqual(result.order, (1, 0))


if __name__ == "__main__":
    unittest.main()
