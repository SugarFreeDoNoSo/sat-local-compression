# Wave 07: exact graph residual signatures

Work issue: [#17](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/17).
Technical baseline: `0da3eedd3100499460b42eeba911ab440a02066c`.
This extends the expository restricted-model work; it does not activate the
conditional Gap-MCSP transfer or complete independent human review.

## Mathematical deliverable

[L04](../paper/sections/05b-graph-signatures.tex) gives the exact cut width for
the existing independent-set selector predicate of a finite simple graph.
For read vertices S and unread vertices T, each independent selected prefix A
has the live signature `N(A) intersect T`. Different signatures are separated
by a singleton unread assignment. Every live residual accepts the empty suffix;
the single dead residual therefore remains distinct and occurs exactly when
the read graph contains an edge.

The proof explicitly covers empty/full cuts and the empty graph. Looplessness
is indispensable to the singleton argument; the implementation rejects loops.
No novelty is claimed. The input length here is the selector count m, not a
conventional SAT formula length n or its full-table length N = 2^n.
No arbitrary-encoding or general-circuit lower bound follows.

## Executable deliverable

[`experiments/graph_signatures.py`](../experiments/graph_signatures.py) provides:

- `residual_signature(m, edges, S, A)`: a forbidden unread bitmask for a live
  prefix, or the distinct `None` marker for a dead prefix. Zero is a live mask.
- `signature_widths_by_subset(m, edges)`: all exact read-set widths without
  materializing residual truth tables.
- `optimal_graph_order(m, edges)`: the same deterministic minimax ordering as
  the existing exhaustive backend, using the new widths.

The existing truth-table backend remains available and the committed data
generation deliberately continues using it. Its minimax recurrence is extracted
into `optimal_order_from_subset_widths`; this helper validates table shape and
positive integer entries, not the correctness of arbitrary caller-provided data.

Precomputation stores independence and neighborhood unions for all 2^m subsets.
Enumeration visits each pair A subset S once, at most 3^m visits across all read
sets, and keeps a set of live forbidden masks for the current S. This is an
integer-mask operation count, not unit-cost access to arbitrary-size integers.
The ten-selector cap remains; no polynomial-time claim is made.

## Validation and scope

`make check` runs the added regression tests, including every cut of every
labeled simple graph on zero through five vertices, comparing the new oracle
against the separate full-truth-table implementation. It also compares all
five existing named graph families and exact deterministic order outputs.

Targeted cases cover dead/live separation, duplicate neighborhood unions,
read-side and unread-side edges, one-shot iterators, and rejected invalid input.
These finite checks validate the implementation; the manuscript proof supplies
the arbitrary-finite-graph statement. L04 is not Lean-formalized by this wave.
Run `make verify` with the pinned Lean toolchain for the combined artifact gates.
