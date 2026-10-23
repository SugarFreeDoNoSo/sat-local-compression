# L02 and P03: residual widths and grouped disjointness

This project formalizes both directions of manuscript Lemma L02
(`lem:residual`) and the exact midpoint-width statement of Proposition P03
(`prop:grouped`) in Lean **4.35.0**, using its bundled `Std` library.
There are no external Lake packages or Mathlib dependency.

## Reproduce

On Linux x86_64, install Python 3.11+, Make, and `zstd`, then run
from the repository root:

```sh
python3 scripts/setup_lean.py
make formal LAKE="$PWD/build/lean/lean-4.35.0-linux/bin/lake"
```

The installer downloads the official Lean release, checks the pinned byte count
and SHA256 in [toolchain.json](toolchain.json), and installs under `build/lean/`.
The archive is about 595 MB; the extracted toolchain needs about 3 GB.
`--archive /path/to/lean-4.35.0-linux.tar.zst` permits an offline installation
from an archive with the same digest. It does not install system software.

An existing matching toolchain can be used with `make formal LAKE=/path/to/lake`.
Both `lean-toolchain` files pin `leanprover/lean4:v4.35.0`; the verifier checks
the actual compiler version and source commit before building. `make verify`
also runs the research, manuscript, and LaTeX-log gates, and accepts the same
`LAKE` variable. `make check` continues to need only Python.
`make clean` removes `build/`, including a toolchain installed there; rerun
setup afterwards, or keep an external toolchain and pass its `LAKE` path.

The formal job in GitHub Actions performs the verified installation and uploads
`build/formal/` as a commit-specific artifact. Releases of the manuscript depend
on that job as well as the research and manuscript jobs. Local verification
does not establish that a remote run has succeeded.

## Statement and manuscript correspondence

All names below are in namespace `ResidualWidths`.

| Manuscript concept | Formal definition or theorem |
| --- | --- |
| Fixed input order | `Word = List Bool`; positions are the ordered variables |
| Every assignment to the first `k` variables | `allWords k`, with `mem_allWords_iff` and `length_allWords` |
| Deterministic diagram and state after a prefix | `Diagram`, `runFrom`, `run` |
| Correctness on all `n`-bit inputs | `CorrectAt D f n` |
| Suffix residual | `residual f p` |
| Number of different residuals | `residualCount f k` |
| Width of reachable states at cut `k` | `reachableWidth D k` |
| Equal states force equal residuals | `equal_state_equal_residual` |
| Every correct diagram has width at least the residual count | `residualCount_le_reachableWidth` |
| One diagram attains every cut simultaneously | `canonical_attains_all_cuts` |
| Both directions of L02 | `residual_width_characterization` |
| Initial and final cuts | `initial_width`, `initial_residual_count`, `terminal_residual_count` |

For each `n`, the function is arbitrary; no uniformity or efficient construction
across lengths is assumed. Every transition reads exactly the next input bit.
The transition receives the layer index, so the formalism permits different
transition maps at different layers and arbitrary merging. Any fixed variable
order is represented by listing the variables in that order. The theorem is
not an assertion that different orders give the same widths.

`f` is a total function on lists supported at length `n`: it returns false at
other lengths (`SupportedAt`). This is bookkeeping for a truth table whose
natural domain is exactly the `n`-bit words. Any such table has this extension
by `atLength_supported`, and `atLength_agrees` preserves every valid input.
For prefixes of length `k`, `residual_eq_iff_on_valid_suffix` proves that equality
of total residuals is exactly agreement on all valid unread suffixes;
`valid_suffix_length_iff` identifies their length as `n-k` when `k <= n`.
Thus invalid suffixes do not create extra residuals.

The common state carrier `Q` may be infinite. Width counts the **finite image of
all reachable prefixes**, rather than all of `Q`. `distinctList` has exact
membership and no duplicates; its length defines `distinctCount`.
`reachableWidth_le_prefixes` bounds each layer by `2^k`, and `reachable_step`
proves that every outgoing bit edge lands in the next reachable layer. Taking
disjoint copies of these finite images for layers `0,...,n`, retaining their
transitions and final outputs, gives the manuscript's finite layered diagram.
Conversely, layer-specific finite state types embed in a common carrier using
disjoint copies. No executable equality test on all functions is assumed.

The canonical diagram has residual functions as states. Its initial state is
`f`, a bit transition maps `r` to `s ↦ r(bit :: s)`, and its output is `r []`.
`run_canonical` identifies the reached state with the prefix residual. It is
one global diagram, correct on every full input and optimal at all cuts, rather
than a separately chosen diagram for each cut. The terminal count is the number
of Boolean outputs actually attained, so constant functions have final width
one; a two-state final layer is not assumed.

## P03: grouped-order disjointness correspondence

The additional source is [Disjointness.lean](ResidualWidths/Disjointness.lean).
For each natural `m`, `groupedDisjointness m` is a Boolean function supported
at length `m + m`. Its first `m` bits encode the positive unit clauses and its
last `m` bits encode the negative unit clauses. The recursive `disjointBits`
predicate checks `not (a_i and b_i)` at every corresponding pair. Unequal
lengths are rejected; the theorem `groupedDisjointness_append` proves that the
supported extension agrees exactly with this predicate on every valid pair of
`m`-bit words. Thus no extra answer is introduced by the total-list convention.
This is the manuscript's incidence encoding, not a general SAT bit encoding.

| Manuscript P03 step | Formal theorem |
| --- | --- |
| All-zero suffix is compatible with any prefix | `disjointBits_zero_right` |
| Different prefixes have different disjointness-answer functions | `disjointBits_left_injective` |
| Fixed-length support and valid grouped-input semantics | `groupedDisjointness_supported`, `groupedDisjointness_append` |
| Different midpoint prefixes induce different residuals | `grouped_residual_injective` |
| Every `m`-bit prefix occurs exactly once | `nodup_allWords`, with existing `length_allWords` |
| Exactly `2^m` midpoint residuals | `grouped_residual_count` |
| Every correct grouped-order diagram needs that width | `grouped_width_lower_bound` |
| Lower bound and one correct diagram attaining it | `grouped_width_characterization` |

The injectivity proof uses the same distinguishing-suffix mechanism as the
manuscript. A suffix with its first bit true and all remaining bits false
recovers the first prefix bit. False-leading suffixes reduce equality of answer
functions to equality for the remaining coordinates, and induction recovers the
whole prefix. This proves injectivity on all `m`-bit prefixes, not just finite
tested examples. The count uses their duplicate-free enumeration and the
existing cardinality `2^m`, rather than assuming the desired number of residuals.
L02 then supplies the lower bound and canonical attainability simultaneously.

Every natural `m` is covered, including `m = 0`: the empty pair is accepted,
there is one residual, and `2^0 = 1` is the width of the initial/terminal layer.
The fixed order is all positive selectors followed by all negative selectors.
Nothing here formalizes P04's different interleaved order, the graph/grid
arguments, arbitrary SAT encodings, general circuits, or the open Q01 target.

## Verification evidence and trust

`scripts/check_formal.py` builds with warnings treated as errors, then invokes
Lean on [AxiomAudit.lean](AxiomAudit.lean). It requires an axiom-closure report for
every listed theorem, prints fully qualified names, and permits only the
standard logical axioms `propext`, `Classical.choice`, and `Quot.sound`.
It rejects `sorryAx`, custom axioms, warnings, errors, missing reports, and a
mismatched compiler. Fully qualified printing prevents a namespaced custom
axiom from masquerading as an allowed short name.

The evidence is regenerated under `build/formal/`: `toolchain.log`, `build.log`,
`axioms.jsonl`, and `verification.json`. It relies on the pinned Lean compiler,
kernel, bundled library artifacts, and the usual platform/toolchain trust.
The release archive is checked against its pinned digest; this is not a claim
of a reproducible source bootstrap or an axiom-free foundation.

Local validation on October 20, 2026: `make verify` passed with the pinned
compiler, 18 audited theorem closures, nine Python tests, 16 registered claims,
seven references, deterministic data, and a clean nine-page PDF. The changed
scope and reproducibility pages were visually inspected. Temporary Lean control
fixtures confirmed rejection of custom axioms, a namespaced `propext`, direct
`sorry`, and both custom axioms and `sorry` hidden behind opaque helpers.
The warning gate also rejected `sorry` with a nonzero compiler exit code.
These control fixtures test the verification guard; they are not the L02 proof.

Wave 09 local validation on October 23, 2026: the pinned compiler verified
P03 and its L02 dependency with **27 audited theorem closures**. The nine new
closures cover the P03 predicates, correspondence, injectivity, exact count, and
width characterization. The earlier 18-closure report above is historical.
`build/formal/verification.json` now lists `claims: ["L02", "P03"]` explicitly.

This is formal verification of **L02 and P03 only**. It does not formalize T01,
P04, the graph/grid lower bounds, or any open SAT lower-bound target, and does
not fulfill W01's independent human-review criterion. Claim statuses retain
their existing research categories; separate evidence fields record these
formalizations. The correspondence prose still requires mathematical review.
