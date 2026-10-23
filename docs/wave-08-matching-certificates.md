# Wave 08: checkable whole-graph induced-matching certificates

Issue: [#18](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/18).
This implements finite certificates for existing **L03**, not a new theorem,
formal proof, novelty claim, or general SAT/circuit lower bound.

## Certificate contract

The certificate contains a finite simple loopless graph, a read vertex set S,
and pairs `(a_i,b_i)` oriented from S to its complement. The checker verifies
that every pair is an edge, endpoints are distinct, and the subgraph induced
by **all** endpoints contains precisely those matching edges. It inspects
same-side edges as well as crossing edges. Loops, duplicate edges, invalid
vertices, duplicate read vertices, reversed pairs, and unknown JSON claim
fields are rejected. No claimed degree or width is trusted from the input.

For a matching of q edges, every subset A of its read endpoints is independent.
Different subsets differ on some a_j. The common unread assignment selecting
only b_j distinguishes the resulting residuals: the output is false exactly
when a_j was selected. All other selectors are zero. Thus L03 and L02 imply
width at least `2^q` **at this specified cut**, irrespective of the internal
order on either side. `separating_assignments` constructs a witness on demand;
the checker never enumerates all `2^q` assignments. The empty certificate gives
the valid but possibly uninformative bound one.

## Separate packing evidence

The producer chooses the lexicographically first remaining crossing edge uv,
then removes every remaining crossing edge incident to `N(u) union N(v)` in
the whole graph. The independent checker does not trust this construction.
It recomputes the maximum degree Delta and original crossing-edge count c,
and checks whether the chosen endpoints' open neighborhoods cover all crossing
edges. A non-greedy certificate satisfying the same condition is also accepted.

Each chosen edge's neighborhood union has at most `2 Delta` vertices, and
at most `2 Delta^2` original crossing edges are incident to it. Union coverage
therefore gives `c <= 2 Delta^2 q`. For Delta >= 1 this is the packing estimate
used by L03. For Delta = 0, c=q=0; only the integer inequality and width one
are reported, with no division by zero. A smaller valid matching still certifies
`2^q` even when coverage fails. An accidentally true numerical inequality is
not labeled a coverage/packing certificate.

## Counterexamples that the checker must reject

- Read `{0,1}`, edges `{02,13,03}`, proposed matching `{02,13}`: the unmatched
  crossing edge invalidates the certificate, and the true cut width is 3, not 4.
- Read `{0,1,2}`, edges `{03,14,25,01}`, proposed matching `{03,14,25}`:
  the crossing graph alone is a matching, but the same-side edge 01 makes some
  prefixes dead. The true width is 7, not 8.
- Unread-side endpoint edges also violate the stated whole-graph contract,
  even when a numerical lower bound happens to survive.

These prevent an apparently harmless relaxation of the proof hypothesis.

## Reproduce and scope

```sh
make check
python3 experiments/matching_certificates.py --check
python3 experiments/matching_certificates.py --verify /path/to/certificate.json
```

The single-file verifier accepts the object under an example's `certificate`
key in [the generated data](../data/matching_certificates.json), not its wrapper
or a user-supplied claimed result. Running the script without flags regenerates
the six deterministic examples. The input cap is 256 vertices.

Tests independently compare all 33,867 graph/cut pairs on every simple labeled
graph with at most five vertices against full residual truth tables; they
check every pair of certified prefix masks in that finite range. Adversarial
tests cover both counterexamples, nonmaximal certificates, misleading numeric
packing bounds, malformed/tampered JSON, and 128 matching edges whose certified
width is `2^128` without exponential enumeration.

The committed examples include empty and matching graphs, the read-side
obstruction, and one row-half cut of each 4x4, 8x8, and 16x16 grid. These certify
width lower bounds 4, 16, and 256 for those three cuts, not their exact widths or
all orders. The manuscript's P05 is the separate all-order asymptotic proof.
Selector input size, conventional SAT formula length, and full-table length
remain different quantities. No Gap-MCSP reduction is supplied. Independent
human mathematical review remains pending.
