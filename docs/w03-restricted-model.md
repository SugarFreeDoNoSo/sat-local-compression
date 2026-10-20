# W03: an explicit all-order grid family

Date: 2026-10-20. Work package: [W03 / issue #5](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/5).
Baseline: `d6417b7`. Technical extension: working draft v0.1.1.
Independent human mathematical review and proof-assistant verification remain
pending. The statements are expository; no originality is claimed.

## Model selection and scope

The unit-clause matching example in P03 becomes easy under interleaving. W03
therefore selects a fixed graph with selector inputs, retaining the manuscript's
deterministic layered ordered model. Every path reads every input bit once;
equivalent computations may merge freely within a layer. Width includes initial
and terminal layers. The robustness is over all orders of these selector bits,
not over arbitrary encodings, repeated reads, or general circuits.

For each fixed G=(V,E), a selector y chooses positive unit clauses z_v. All
negative binary clauses `(not z_u or not z_v)` for graph edges are fixed. The
resulting formula is satisfiable exactly when the selected vertices are an
independent set: any selected edge prevents satisfaction, and otherwise z=y is
a witness. This is a family of SAT inputs encoded by clause incidence; it is
not merely claimed to be the conventional SAT truth table at the same length.

The chosen explicit family is the r-by-r grid for even r>=2, with m=r^2
selector bits. Its formula encoding length n is a separate quantity, and the
full SAT table remains N=2^n. No width-preserving bitwise translation to T_n is
asserted.

## Proved statements and mechanism

- **L03:** q crossing edges that form an induced matching in the whole graph
  give 2^q distinct residual functions. Two prefix subsets are distinguished
  by choosing a single corresponding unread endpoint.
- A greedy packing step deletes at most 2 Delta^2 crossing edges in a graph
  of maximum degree at most Delta>=1. Consequently q>=c/(2 Delta^2), for c
  crossing edges. Requiring the matching to be induced in the whole graph
  excludes unwanted edges on both sides of the cut.
- **P05:** every half-size cut of an even r-by-r grid has at least r/2 crossing
  edges. Either at least r/2 rows are mixed, or a wholly selected row and a
  wholly unselected row force crossings in all columns. Since Delta<=4,
  every order requires width at least 2^(r/64)=2^Omega(sqrt(m)).

The manuscript provides complete proofs and stable labels. Claim dependencies
are `L02 -> L03 -> P05`; no dependency into T01/C01/Q01 is introduced.
The same graph predicate has general circuit size O(m+|E|), counting inputs,
and hence O(m) for grids. Order robustness alone does not exclude small circuits.

## Literature and candidate decision

[Bova and Slivovsky, On Compiling Structured CNFs to OBDDs](https://link.springer.com/article/10.1007/s00224-016-9715-z),
Theory of Computing Systems 61 (2017), 637–655, DOI 10.1007/s00224-016-9715-z,
Section 4, is primary background. Theorem 19 gives stronger exponential-size
examples using bounded-degree expander graphs. Its monotone graph CNF and our
negative-edge predicate are related by complementing the inputs, preserving
orders and diagram resources; the incidence-SAT interpretation is stated here
separately. This citation is context; the grid proof is self-contained.

Three candidates were considered:

| Candidate | Decision | Reason |
| --- | --- | --- |
| Original matching/unit clauses | Retain as an order-sensitivity example | Interleaving gives constant width, so it fails the all-order target. |
| Bounded-degree expanders | Record as a literature extension | Stronger bounds exist, but a chosen explicit construction and its hypotheses require a separate checked treatment. |
| Even square grids | Select for this deliverable | Explicit construction, elementary balanced-cut argument, and a complete self-contained superpolynomial bound. |

The selected result is established at this restricted-model scope; its role is
to improve the project's expository examples. A novel contribution and any
transfer to general local descriptions require further work.

## Exact finite experiment E02

For a read subset S, let w(S) count distinct residual functions on its
complement. Permuting the read variables changes only the enumeration of
prefixes; permuting the unread variables is a common bijection of all residual
truth tables. Neither operation changes w(S).

An ordering is a path through subsets. With b(empty)=w(empty), the recurrence is

```text
b(S) = max(w(S), min over v in S of b(S without v)).
```

Every path to S ends at some predecessor S without v, and its last layer costs
w(S). Minimizing over predecessors proves the recurrence. L02 realizes these
residual widths simultaneously with a residual-state diagram. The resulting
minimum maximum width is therefore the optimum over all orders in the named
layered model. The implementation reconstructs an attaining order deterministically.

The five finite cases are matching-3, cycle-6, grid-2x3, cube-3, and grid-3x3,
with at most nine bits. E02 depends on L02 and records finite calculations;
it is not evidence establishing P05's asymptotic assertion. In particular,
grid-3x3 has odd side length, outside P05's stated family.

Commands: `make experiments` regenerates both artifact families; `make verify`
checks tests, claim/reference integrity, generated data, PDF, and the LaTeX log.
The new independent tests compare with an all-permutations oracle on selected
functions up to five bits, and with exhaustive SAT witnesses for every simple
graph up to four vertices. Test outcomes and final rendering inspection are
recorded in the pull request after they actually run.

## W03 acceptance and remaining gates

| Original criterion | Deliverable | Technical status |
| --- | --- | --- |
| Define allowed orders, encodings, and sharing | Fixed graph-incidence inputs; arbitrary selector order; layered read-once diagrams; arbitrary merging | Specified |
| Give a complete proof or precise counterexample | L03 and P05, with full matching/packing/grid-cut proofs | Agent-prepared expository proof; human review pending |
| Separate from general SAT circuit bounds | Explicit incidence/formula length distinction and linear general-circuit upper bound | Retained |
| Add informative finite experiments | E02 and exact subset-DP optimizer with independent finite oracles | Prepared; outcomes recorded by actual validation |

The implementation gate is reproducibility and review of this bounded extension.
The human-review, originality, general-circuit-transfer, and publication gates
are not satisfied by preparing a proof or by passing finite/CI checks.
