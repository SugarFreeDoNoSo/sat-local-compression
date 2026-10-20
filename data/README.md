# Residual-function data

Regenerate with: python3 experiments/obdd_residuals.py --max-m 7

- Domain: incidence-encoded unit-clause SAT, 1 <= m <= 7.
- Predicate: no index has a_i = b_i = 1.
- Model: deterministic layered ordered decision diagrams.
- Method: exhaustive residual truth tables at each cut.
- Orders: all a then all b; alternating a_i and b_i.
- Arithmetic: exact, with no randomness.
- Scope: finite consistency evidence for P03 and P04, not their proof.

The CSV and TeX table are generated together and checked for drift.

## Optimal graph-selector orders

Regenerate with: `python3 experiments/graph_order_widths.py`.
Check without rewriting: `python3 experiments/graph_order_widths.py --check`.
`make experiments` and `make check` include both experiment families.

- Predicate: selected vertices form an independent set in a fixed simple graph.
  Equivalently, the fixed negative edge clauses and selected positive units
  have a satisfying witness. These are incidence inputs, not general SAT bitstrings.
- Cases: matching-3 (6 bits), cycle-6 (6), grid-2x3 (6), cube-3 (8), and
  grid-3x3 (9). Grid labels are row-major; cube vertices are 3-bit numbers.
- `min_order_width` is the minimum, over every variable order, of the maximum
  reachable-state count across all layers, including the terminal layer.
- Method: enumerate exact residual truth tables at every subset of read bits,
  then optimize paths through subsets by minimax dynamic programming. This
  covers all orders implicitly, without enumerating factorially many permutations.
- The CSV records a deterministic attaining order using zero-based vertex labels.
  The TeX table contains family name, input-bit count, and optimum width.
- The tool supports at most ten bits. Its exhaustive stage is exponential;
  no scalable solver or asymptotic proof is claimed.
- The finite grid examples are rectangular/odd, while P05 proves an all-order
  lower bound for every even square side length. They must not be conflated.

Tests compare the minimax optimizer against an independent all-permutations
oracle on selected functions of at most five bits, and compare graph semantics
with exhaustive SAT witnesses for all simple graphs of at most four vertices.
