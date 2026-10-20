"""Exact finite minimax widths over all variable orders of fixed graph predicates.

The input bits select vertices of a fixed simple graph; acceptance means that
the selected vertices are independent. This is the incidence SAT family from
the manuscript, not the unrestricted SAT truth table T_n.

For each subset S of already-read variables, enumerate its residual truth tables
and count distinct ones. Their count depends on S, not its internal order.
A subset dynamic program then minimizes the maximum count along an ordering.
It explores all orders implicitly, rather than sampling or enumerating m! orders.
The exhaustive residual stage uses O(m 4^m) elementary projection operations,
plus integer-bitset costs; m is the graph-selector input length and is capped
at ten. No asymptotic proof follows from
these finite observations. Initial and terminal layers are included.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import io
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
MAX_INPUTS = 10


def _check_num_inputs(num_inputs: int) -> None:
    if not isinstance(num_inputs, int) or not 0 <= num_inputs <= MAX_INPUTS:
        raise ValueError(f"num_inputs must be an integer from 0 to {MAX_INPUTS}.")


def graph_predicate(
    num_inputs: int, edges: Iterable[tuple[int, int]]
) -> Callable[[tuple[int, ...]], int]:
    """Return the independent-set predicate for a fixed labeled simple graph."""
    _check_num_inputs(num_inputs)
    normalized = []
    for u, v in edges:
        if (
            not isinstance(u, int)
            or not isinstance(v, int)
            or not (0 <= u < num_inputs and 0 <= v < num_inputs)
            or u == v
        ):
            raise ValueError("Graph edges require distinct valid vertex indices.")
        normalized.append((min(u, v), max(u, v)))
    if len(set(normalized)) != len(normalized):
        raise ValueError("Graph edges must be distinct.")
    fixed_edges = tuple(sorted(normalized))

    def evaluate(bits: tuple[int, ...]) -> int:
        if len(bits) != num_inputs or any(bit not in (0, 1) for bit in bits):
            raise ValueError("A Boolean assignment of the graph's size is required.")
        return int(all(not (bits[u] and bits[v]) for u, v in fixed_edges))

    return evaluate


def residual_widths_by_subset(
    function: Callable[[tuple[int, ...]], int], num_inputs: int
) -> tuple[int, ...]:
    """Count residuals for each bitmask S; bit v means that variable v is read.

    Vertex 0 is the least significant bit of an enumerated assignment. Within
    each S, increasing vertex indices fix canonical prefix/suffix coordinates.
    A residual is an integer bitset of its complete, equally sized truth table;
    leading zero outputs do not distinguish otherwise identical functions.
    """
    _check_num_inputs(num_inputs)
    truth = []
    for assignment in range(1 << num_inputs):
        bits = tuple((assignment >> v) & 1 for v in range(num_inputs))
        output = function(bits)
        if output not in (0, 1):
            raise ValueError("The function must return a Boolean value.")
        truth.append(int(output))

    nonzero = [assignment for assignment, output in enumerate(truth) if output]
    widths = []
    for subset in range(1 << num_inputs):
        prefix = tuple(v for v in range(num_inputs) if subset & (1 << v))
        suffix = tuple(v for v in range(num_inputs) if not subset & (1 << v))
        residuals = [0] * (1 << len(prefix))
        for assignment in nonzero:
            prefix_index = sum(
                ((assignment >> v) & 1) << i for i, v in enumerate(prefix)
            )
            suffix_index = sum(
                ((assignment >> v) & 1) << i for i, v in enumerate(suffix)
            )
            residuals[prefix_index] |= 1 << suffix_index
        widths.append(len(set(residuals)))
    return tuple(widths)


@dataclass(frozen=True)
class OptimalOrder:
    width: int
    order: tuple[int, ...]
    subset_widths: tuple[int, ...]


def optimal_order(
    function: Callable[[tuple[int, ...]], int], num_inputs: int
) -> OptimalOrder:
    """Find the minimum possible maximum layered width, including terminals.

    If variable v is last among S, all earlier cuts lie on an optimal path to
    S without v. Thus best[S] = max(w[S], min_v best[S without v]). Numeric
    subset order visits every predecessor first. Ties choose the smallest last
    variable index; reconstruction and generated files are deterministic.
    """
    widths = residual_widths_by_subset(function, num_inputs)
    best = [0] * len(widths)
    previous = [0] * len(widths)
    best[0] = widths[0]
    for subset in range(1, len(widths)):
        variable = min(
            (v for v in range(num_inputs) if subset & (1 << v)),
            key=lambda v: (best[subset ^ (1 << v)], v),
        )
        best[subset] = max(widths[subset], best[subset ^ (1 << variable)])
        previous[subset] = variable

    order = []
    subset = len(widths) - 1
    while subset:
        variable = previous[subset]
        order.append(variable)
        subset ^= 1 << variable
    return OptimalOrder(best[-1], tuple(reversed(order)), widths)


def grid_edges(rows: int, columns: int) -> tuple[tuple[int, int], ...]:
    """Use row-major vertex indices for a rectangular nearest-neighbor grid."""
    if not isinstance(rows, int) or not isinstance(columns, int) or rows < 1 or columns < 1:
        raise ValueError("Grid dimensions must be positive.")
    edges = []
    for row in range(rows):
        for column in range(columns):
            vertex = row * columns + column
            if column + 1 < columns:
                edges.append((vertex, vertex + 1))
            if row + 1 < rows:
                edges.append((vertex, vertex + columns))
    return tuple(edges)


def cases() -> tuple[tuple[str, int, tuple[tuple[int, int], ...]], ...]:
    return (
        ("matching-3", 6, tuple((v, v + 3) for v in range(3))),
        ("cycle-6", 6, tuple((v, (v + 1) % 6) for v in range(6))),
        ("grid-2x3", 6, grid_edges(2, 3)),
        (
            "cube-3",
            8,
            tuple(
                (v, v ^ (1 << bit))
                for v in range(8)
                for bit in range(3)
                if v < (v ^ (1 << bit))
            ),
        ),
        ("grid-3x3", 9, grid_edges(3, 3)),
    )


def artifact_contents() -> dict[Path, str]:
    observations = []
    for family, num_inputs, edges in cases():
        result = optimal_order(graph_predicate(num_inputs, edges), num_inputs)
        observations.append(
            {
                "family": family,
                "input_bits": num_inputs,
                "min_order_width": result.width,
                "chosen_order": " ".join(str(v) for v in result.order),
            }
        )
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=list(observations[0]), lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(observations)
    latex = [
        "% Generated by experiments/graph_order_widths.py; do not edit.",
        r"\begin{tabular}{lrr}",
        r"\toprule",
        r"Family & Input bits & Minimum maximum width \\",
        r"\midrule",
    ]
    for row in observations:
        latex.append(
            f"{row['family']} & {row['input_bits']} & {row['min_order_width']} "
            + r"\\"
        )
    latex.extend([r"\bottomrule", r"\end{tabular}", ""])
    return {
        ROOT / "data/graph_order_widths.csv": stream.getvalue(),
        ROOT / "data/graph_order_widths.tex": "\n".join(latex),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, content in artifact_contents().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        print("Generated graph data is stale: " + ", ".join(stale))
        print("Run python3 experiments/graph_order_widths.py.")
        return 1
    print(
        f"Finite graph data {'verified' if args.check else 'generated'}: "
        "five fixed graph families, at most nine input bits."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
