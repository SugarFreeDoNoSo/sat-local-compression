"""Exact graph-selector residual widths from forbidden-neighborhood signatures.

For a fixed finite simple graph G and read set S, an independent selected prefix
A has signature N_G(A) outside S. A nonindependent prefix has the separate dead
signature None. Lemma L04 proves that these signatures classify residuals exactly.

All-subset counting performs O(3^m) submask visits after O(2^m) precomputation,
counting integer mask operations separately from their bit complexity. It never
constructs the residual truth tables. The finite implementation retains the
existing ten-selector safety cap; this is not an algorithm for unrestricted SAT.
"""

from __future__ import annotations

from typing import Iterable

from experiments.graph_order_widths import MAX_INPUTS, OptimalOrder, optimal_order_from_subset_widths


def _adjacency_masks(num_inputs: int, edges: Iterable[tuple[int, int]]) -> tuple[int, ...]:
    if type(num_inputs) is not int or not 0 <= num_inputs <= MAX_INPUTS:
        raise ValueError(f"num_inputs must be an integer from 0 to {MAX_INPUTS}.")
    adjacency = [0] * num_inputs
    seen = set()
    for edge in edges:
        try:
            u, v = edge
        except (TypeError, ValueError) as error:
            raise ValueError("Each graph edge must contain two vertices.") from error
        if (type(u) is not int or type(v) is not int
                or not 0 <= u < num_inputs or not 0 <= v < num_inputs or u == v):
            raise ValueError("Graph edges require distinct valid vertex indices.")
        normalized = (min(u, v), max(u, v))
        if normalized in seen:
            raise ValueError("Graph edges must be distinct.")
        seen.add(normalized)
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    return tuple(adjacency)


def _subset_information(adjacency: tuple[int, ...]) -> tuple[list[bool], list[int]]:
    """Independence and open-neighborhood union of every selected vertex set."""
    independent = [True] * (1 << len(adjacency))
    neighbors = [0] * len(independent)
    for selected in range(1, len(independent)):
        least = selected & -selected
        vertex = least.bit_length() - 1
        rest = selected ^ least
        independent[selected] = independent[rest] and not (adjacency[vertex] & rest)
        neighbors[selected] = neighbors[rest] | adjacency[vertex]
    return independent, neighbors


def residual_signature(
    num_inputs: int, edges: Iterable[tuple[int, int]], read_subset: int, selected_prefix: int
) -> int | None:
    """Return the forbidden unread mask, or None for the distinct dead residual.

    Masks use vertex 0 as the least significant bit. The selected prefix must
    be contained in the read set. Mask zero is a live signature, never a dead
    marker: its residual accepts the empty suffix even at the terminal cut.
    """
    adjacency = _adjacency_masks(num_inputs, edges)
    full = (1 << num_inputs) - 1
    if (type(read_subset) is not int or not 0 <= read_subset <= full
            or type(selected_prefix) is not int or not 0 <= selected_prefix <= full
            or selected_prefix & ~read_subset):
        raise ValueError("Read and selected-prefix masks must be valid, with the prefix contained in the read set.")
    forbidden = 0
    for vertex, neighbors in enumerate(adjacency):
        if selected_prefix & (1 << vertex):
            if neighbors & selected_prefix:
                return None
            forbidden |= neighbors
    return forbidden & (full ^ read_subset)


def signature_widths_by_subset(
    num_inputs: int, edges: Iterable[tuple[int, int]]
) -> tuple[int, ...]:
    """Count all live signatures plus one dead residual iff G[S] has an edge."""
    adjacency = _adjacency_masks(num_inputs, edges)
    independent, neighbors = _subset_information(adjacency)
    full = (1 << num_inputs) - 1
    widths = []
    for read in range(full + 1):
        unread = full ^ read
        signatures = set()
        selected = read
        while True:
            if independent[selected]:
                signatures.add(neighbors[selected] & unread)
            if selected == 0:
                break
            selected = (selected - 1) & read
        widths.append(len(signatures) + int(not independent[read]))
    return tuple(widths)


def optimal_graph_order(
    num_inputs: int, edges: Iterable[tuple[int, int]]
) -> OptimalOrder:
    """Use exact signature widths in the existing all-order minimax recurrence."""
    widths = signature_widths_by_subset(num_inputs, edges)
    return optimal_order_from_subset_widths(widths, num_inputs)
