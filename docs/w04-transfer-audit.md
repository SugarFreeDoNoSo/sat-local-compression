# W04: applicability of Gap-MCSP magnification

Date: 2026-10-23. [Issue #6](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/6), execution wave 05.
Baseline: `0da3eedd3100499460b42eeba911ab440a02066c`.

**Outcome:** no transfer from the project's current local-description or
layered-diagram results to the general-circuit antecedent is established.
This is an applicability report with an explicit missing reduction, an allowed
W04 exit. It does not prove that every possible reduction is impossible.
R02 remains conditional, Q01 remains open, and independent human review remains
pending and deferred by the author.

## 1. Published statement and exact promise

Authoritative source: Oliveira, Pich, and Santhanam, *Hardness Magnification
Near State-of-the-Art Lower Bounds*, Theory of Computing 17, Article 11 (2021),
pp. 1–38, DOI `10.4086/toc.2021.v017a011`.
The [published PDF](https://theoryofcomputing.org/articles/v017a011/v017a011.pdf)
was checked directly. SHA256:
`81b1ff4ede5180dc88f99c8a4856cfde623f6fefb5b99ef9f5526899bf43ab4a`.

| Printed locator | Material checked |
| --- | --- |
| Section 1.2, p. 4 | Fixed-basis, fan-in-two Boolean circuits, unrestricted depth, size counted in gates |
| Theorem 1.4, p. 6 | Universal constant, two thresholds, common epsilon and every sufficiently small beta |
| Definition 2.4, p. 11 | Full truth-table inputs and exact YES/NO promises |
| Section 4.1, pp. 17–18 | Contrapositive proof using the Anti-Checker Lemma and Succinct-MCSP |

Let `n` be the arity of the represented function and `N = 2^n` the length of
its entire table `B`. Write `C(B)` for its minimum general-circuit gate count
in the fixed basis. Definition 2.4 uses integer-valued `s1 <= s2` and

```text
YES: C(B) <= s1(n)
NO:  C(B) >  s2(n).
```

The interval `s1 < C(B) <= s2` is outside the promise; a solver can answer
arbitrarily there. The theorem's displayed thresholds are

```text
lower(N) = N^beta / (c log2 N),    upper(N) = N^beta.
```

The published display suppresses rounding. This audit interprets inequalities
against those real expressions literally on integer `C(B)`, equivalently using
`s1 = floor(lower)` and `s2 = floor(upper)`. In particular, NO means
`C(B) >= floor(upper)+1`, not `C(B) >= upper`. The introduction's informal
“at least” wording does not override Definition 2.4. The manuscript's endpoint
is corrected accordingly.

There is a universal `c >= 1` such that the following antecedent implies
`NP` is not contained in `P/poly`:

```text
exists epsilon > 0, exists beta0 > 0, such that for every fixed
0 < beta < beta0:
  Gap-MCSP[lower(N), upper(N)] is not in SIZE[N^(1+epsilon)].
```

Beta is constant with respect to length. One epsilon must work throughout a
sufficiently small beta interval; a lower bound for one beta, or with epsilon
tending to zero with beta, does not establish the antecedent. The constant c
is the theorem's constant. `SIZE` concerns nonuniform circuit families that
classify all promised tables, rather than the complexity of one represented
function. The circuit basis must remain fixed through any reduction. W02's
separate input-gates-plus-connections convention cannot be substituted as an
exact identity with this gate count.

The main parameters are unchanged in earlier ECCC/CCC versions; the published
numbering is used here. The source's p. 8 warning that a separate Anti-Checker
Hypothesis was refuted does not retract Theorem 1.4. This audit uses the theorem,
not that hypothesis.

## 2. Lengths and objects that must remain separate

| Parameter | Meaning |
| --- | --- |
| `ell` | Source decision-input length, e.g. a conventional SAT encoding |
| `2^ell` | Length of the complete SAT table at that source length |
| `n` | Arity of a target represented function |
| `N = 2^n` | Number of bits input to the Gap-MCSP classifier |
| `m = r^2` | Selector-input length for W03's even grid family |

The incidence encoding does not identify `m` with `ell`. Exporting the grid
predicate's full table sets `n = m` and `N = 2^m`. Polynomial target cost in N
is then exponential in m.

Minimum circuit size of a represented function, width of a layered diagram,
and circuit size of a classifier for arbitrary truth tables are three different
resources. W02 compares witnesses for the first, W03 bounds the second, and
the magnification antecedent concerns the third.

## 3. Reduction direction and quantitative contract

To transfer a source lower bound to `B_beta = Gap-MCSP[lower,upper]`, the useful
many-one direction is `A <= B_beta`: a small target solver must yield a small
source solver. The opposite direction alone does not transfer hardness from A
to B_beta.

For each relevant beta and source length ell, supply

```text
R_beta,ell : {0,1}^ell -> {0,1}^{N_beta(ell)},
N_beta(ell) = 2^{n_beta(ell)},
```

and prove, for every promised source input x,

```text
x in A_YES -> C(R_beta,ell(x)) <= lower(N_beta(ell))
x in A_NO  -> C(R_beta,ell(x)) >  upper(N_beta(ell)).
```

An output in the gap satisfies neither required promise. If a reduction swaps
the sides, complement the final Boolean decision of the composed classifier
and charge its cost. Complementing the represented truth table does not swap
the circuit-complexity promises. No correctness is needed on unpromised source
inputs. If output lengths depend on the input,
a common-length padding preserving the promises must be justified separately.

Let `r_beta(ell)` count reduction gates and necessary adapters in the same
bounded-fan-in basis. Target circuits of size at most `K N^(1+epsilon)` give,
by ordinary circuit composition,

```text
source circuit size <= r_beta(ell) + K N_beta(ell)^(1+epsilon).
```

To obtain a contradiction, an established general-circuit source lower bound
must dominate this sum on hard source lengths with target lengths tending to
infinity. For instance, if the three bounds are respectively `O(ell^rho)`,
`N_beta(ell) = Theta(ell^a)`, and `Omega(ell^alpha)` on infinitely many source
lengths, `alpha > max(rho, a(1+epsilon))` suffices. This is a conditional
accounting criterion, not a source lower bound established by the project.

| Output length | Target solver's contribution | Consequence for a proposed transfer |
| --- | --- | --- |
| `N = Theta(ell^a)` | `O(ell^{a(1+epsilon)})` | Retain this degree and the reduction cost |
| `N = 2^ell` | `O(2^{(1+epsilon)ell})` | A polynomial source lower bound does not contradict this exponential upper bound |
| Succinct description instead of the N-bit table | No literal input for this target | Prove and charge a separate expansion or access simulation |

Writing N output bits takes at least N sequential output steps. This does not
imply a universal `r_beta >= N` gate bound when output ports and repeated wires
are free. Calling a reduction “polynomial-time” also discards the degrees
needed for the near-linear target bound.

Using a restricted-model source lower bound would require a further proof:
every composed general target circuit must convert to a source device in that
restricted model within the forbidden resource bound. No such conversion is
supplied for the project's layered diagrams.

## 4. Concrete candidate checks

### A. Export the complete W03 grid truth table

For `m = r^2`, W03 supplies a general circuit for `g_G` of size at most `K m`,
since the grid has `2r(r-1)` edges. For its full table B, with `N = 2^m`,

```text
C(B) <= K m = K log2 N <= 2^(beta m)/(c m)
```

eventually for each fixed beta > 0: `2^(beta m)` eventually dominates `c K m^2`.
These tables are on the YES side, despite their large layered width. The
starting length may depend on beta; beta is not made length-dependent.

Moreover, `y -> tt(g_G)` is constant in the selector query y. The source
predicate accepts the all-zero selection and rejects selection of an edge.
A constant output cannot send those two sides into disjoint YES and NO sets.
This rules out that map, not every possible reduction using graph gadgets.

The width bound `2^(sqrt(m)/64)` becomes `N^{1/(64 sqrt(m))}`, subpolynomial
in N. This arithmetic does not change the more fundamental model mismatch:
width is not the gate count of a Gap-MCSP classifier.

### B. Convert the width bound through W02's local/KT simulations

W02 gives charged polynomial simulations between general representations; it
does not turn W03 width into a general-circuit lower bound. The explicit linear
grid circuit precludes that inference. A polynomial distortion also need not
preserve a gap of ratio `c log N` or a common near-linear target exponent.
Both promise implications and the quantitative composition must be proved.

### C. Assume the full SAT target Q01

T01/C01 characterize Q01 as `SAT` not in `P/poly`. Q01 is open. Assuming it
already implies `NP` not in `P/poly`, since SAT is in NP, so that assumption
does not supply an independent magnification advance. T01 is a characterization,
not the source lower bound required in Section 3.

## 5. Missing obligations and exit decision

| Obligation | Evidence | Status |
| --- | --- | --- |
| State direction, models, and source/target promises | Contract above and a concrete grid-table candidate | Specified for this audit |
| Preserve YES and NO and avoid the gap | The constant full-grid-table candidate fails | No replacement reduction established |
| Supply hardness in the required model | Grid has large layered width and linear general circuits | Missing model-preserving argument |
| Control length and size overhead | Composition inequality and explicit length regimes | Required accounting identified |
| Cover all sufficiently small beta with one epsilon | No target general-circuit lower bound supplied | Antecedent remains open |

The original issue criteria are answered through their permitted missing-
reduction outcome. Technical closure of this audit does not certify a successful
transfer, new SAT hardness, or independent review. Keep R02 conditional and Q01
open. Resume only with a candidate specifying both promise implications, model,
length map, reduction cost, and common-epsilon beta range. Enlarging finite
examples or strengthening order robustness alone does not fill these gaps.
