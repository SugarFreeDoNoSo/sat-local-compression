# W01: evaluator model and advice-equivalence audit

Audit date: 2026-10-19. Manuscript baseline: `main` at `d6417b7`.
Work package: [W01 / issue #3](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/3).

**Outcome:** the technical audit below finds no blocking gap in T01 or C01
under the manuscript's stated efficient-universality and explicit-SAT-encoding
conventions. It supplies explicit simulation bounds and identifies conventions
that must be fixed before making encoding-sensitive or exact-exponent claims.
The independent human-review criterion remains pending. This agent-prepared
dossier does not close W01, change claim statuses, or constitute formal verification.

## 1. Sources, scope, and evidence

The audit reads the following repository sources at the baseline:

| Source | Audited material |
| --- | --- |
| [02-model.tex](../paper/sections/02-model.tex) | Lines 3–19: SAT encoding and evaluator; lines 21–37: definition and nonuniformity; lines 46–72: P01 |
| [03-equivalence.tex](../paper/sections/03-equivalence.tex) | Lines 8–37: T01 and both simulations; lines 39–65: C01, quantifiers, and scope |
| [claims.json](../research/claims.json) | P01, T01, C01, and Q01; existing dependencies and pending independent review |
| [backlog.json](../research/backlog.json) | W01's four original acceptance criteria |
| [review-checklist.md](review-checklist.md) | Model, costs, uniformity, finite exceptions, quantifiers, and evidence requirements |

The evidence produced here is a written technical audit by a Codex agent.
The calculations in Sections 4–6 are supplied in full. No human reviewer is
identified because no independent human review was performed as part of this
audit. No proof assistant, implemented universal evaluator, or parser for the
illustrative syntax below is supplied. No new local or remote test result is
claimed by this dossier. Artifact checks and finite experiments cannot establish
T01 or C01; their existing records remain separate evidence.

This audit introduces no new research claim ID: it expands the proofs and
conventions of existing T01/C01 without changing their statements. The manuscript
and `research/claims.json` are unchanged.

## 2. Model contract and a compatible implementation convention

The definition uses a fixed deterministic multitape evaluator U. For a binary
description d and query x of length n, a successful computation halts with the
single bit SAT(x). One description d_n must work for every x of that length.
The entire table has N = 2^n bits; query-time bounds are functions of n.

The following operational convention realizes the intended standard model:

- U has two read-only input tapes containing d and x, with endmarkers, a fixed
  finite number of ordinary work tapes, and a one-bit output. Each transition
  reads/writes finitely many symbols and moves each head at most one cell.
- Input-head movements, locating a symbol, parsing headers, copying auxiliary
  data, simulating transitions, and writing the output are charged. Binary
  arithmetic is performed by tape operations; there is no unit-cost operation
  on an unbounded integer or arbitrary random-access address.
- Each query starts with fresh work tapes. The model supplies no persistent
  cache, previously evaluated table, advice-construction procedure, SAT oracle,
  or other uncharged primitive.
- The finite control of U is fixed independently of n. Descriptions can depend
  on n, but are fixed before the particular query of length n is chosen.
  Choosing or constructing d_n is outside the query-time charge, as stated in
  the manuscript; accessing its contents during a query is charged.

For a concrete description layout, define the self-delimiting natural-number
header

```text
I(k) = 1^ell 0 bin(k+1),  ell = floor(log2(k+1)) + 1,  k >= 0.
|I(k)| = 2 floor(log2(k+1)) + 3.
```

The binary payload must have exactly ell bits and begin with 1. A program code
can be any fixed effective binary serialization of a deterministic multitape
machine's finite states, tape count, symbols, transition tuples, and halting
output. Integer fields can use I, with list lengths preceding lists. There are
no oracle instructions. Fix this serialization once; it does not vary with n.

If h_M is the length of a fixed machine M's code, use

```text
H(M) = I(h_M) code(M),
enc_M(a) = H(M) a,
kappa_M = |H(M)| = h_M + 2 floor(log2(h_M+1)) + 3.
```

The remainder of the description tape, ending at its endmarker, is auxiliary
data a. Therefore `|enc_M(a)| = |a| + kappa_M`: the program overhead is genuinely
constant for fixed M. Finding the endmarker or copying a still costs time.
No advice-length header and no separate encoding of n are needed. M may obtain
n by scanning x, with that scan charged.

This layout is a compatible representative for review, not a claim that the
manuscript already fixed this exact bit serialization or that U was implemented.
For any designated U satisfying the manuscript's contract, use its own encoding
and simulation constants in Sections 4–5. Replacing U by a compatible universal
machine preserves the polynomial-resource characterization; it need not preserve
the numerical value of local L for a fixed time budget.

### Why an ordinary universal simulator suffices

A scan-based interpreter can copy the encoded program and input tapes to work
tapes, encode virtual tapes with head markers, and look up each transition by
scanning the finite transition table. For fixed M and a simulation lasting tau
steps, only O_M(tau + n + D + 1) virtual tape cells are needed, where D is the
description length. Each virtual step can be implemented by polynomially many
ordinary scans and shifts of that finite configuration. Initialization, header
processing, input copies, and all virtual input accesses are included. This
gives a polynomial in tau, n, and D, without a free computational primitive.
The particular degree or leading constant is not used as a numerical claim.

The precise contract needed below is: for each fixed M there are finite
constants C_M >= 1 and integer k_M >= 1 such that, whenever M(a,x) halts in tau
steps with a bit, U(enc_M(a),x) returns that bit within

```text
C_M (tau + n + D + 1)^k_M steps,  D = |enc_M(a)|.
```

The encoding overhead is constant for fixed M; the simulation polynomial may
depend on M, exactly as allowed in `02-model.tex`. An arbitrary merely
computationally universal evaluator need not satisfy this contract, so efficient
universality is a necessary retained hypothesis in the reverse simulation.

### Optional extra headers

If a format additionally stores `I(m)` before advice of length m, that field has
`2 floor(log2(m+1)) + 3` bits. It is not constant overhead in m. Such a format
can be handled by a fixed wrapper that parses the header and simulates M, paying
all parsing/copying costs. Its length is at most `kappa + 3m + 3`, and its
simulation remains polynomial after adjusting the constants and degree. Thus it
does not invalidate T01, but it must not be mistaken for the stronger exact
constant-overhead layout above. The manuscript's short proof does not prescribe
a layout that forces this additional field.

## 3. SAT encoding and lengths

The current manuscript fixes a conventional explicit binary formula encoding
but does not serialize its grammar. T01 applies to every language, so its advice
equivalence does not depend on a particular SAT parser. P01 needs the fixed
language to be decidable. The final implication in C01 uses SAT in NP: if P = NP,
then SAT is in P and hence P/poly. NP-completeness is standard for conventional
SAT encodings, but NP membership alone suffices for that implication.

For specificity, the following is one compatible encoding proposal for a future
explicit choice. It is not silently substituted for the manuscript's T_n:

| Prefix token | Remaining payload |
| --- | --- |
| `000` | Constant false |
| `001` | Constant true |
| `010` | Variable index I(j), j >= 1 |
| `011` | One encoded subformula, negated |
| `100` | Two encoded subformulas, conjoined |
| `101` | Two encoded subformulas, disjoined |
| `110`, `111` | Invalid token |

An input is valid only if parsing consumes exactly one whole expression and all
bits. Truncated headers/subformulas, invalid indices/tokens, and trailing bits
are rejected and have SAT value 0. This is a prefix-tree syntax, not a succinct
circuit or oracle encoding. Distinct variable names appearing in an n-bit input
are at most O(n); a very large numerical variable index does not create that many
distinct variables. Parsing, collecting the actual names, guessing their Boolean
values, and evaluating the tree take polynomial time. Standard explicit 3-CNF
instances translate to this syntax with polynomial length increase by naming
variables and writing the corresponding conjunction/disjunction tree; thus the
usual NP-completeness interpretation is available for this proposed syntax.

Encoding-sensitive future work must first choose the actual serialization. Two
polynomially intertranslatable encodings need not have identical tables at each
length or identical local-description bounds at a fixed exponent. No such
pointwise transfer is used here. In particular, the separate incidence encoding
in P03/P04 is not the formula encoding of these tables.

The manuscript starts at n >= 1. Define the answer on the empty input separately
(0 for the proposed syntax). This is one finite case and does not affect T01 or
C01. Malformed inputs at every positive length remain part of the language's
truth table and must be answered correctly, not removed from the quantifiers.

## 4. T01: local descriptions give polynomial advice

Assume there exist positive integers a,b and an integer n_0 such that, for every
n >= n_0, `L^U_(n^b)(T_n) <= n^a`. Since an empty witness set has minimum infinity,
this finite upper bound supplies a description d_n satisfying both

```text
|d_n| <= n^a,
for every x of length n: U(d_n,x) = SAT(x) within n^b steps.
```

Give d_n as advice to a fixed deterministic machine. On input x it determines
whether its length is below n_0; otherwise it runs the fixed U with that advice.
Determining the length costs O(n) and is polynomial. Because b >= 1, the total
time on the large lengths is O(n^b + n), and advice length is at most n^a.
There is no advice depending on x beyond its length and no procedure to construct
the advice is invoked during a query.

For the finitely many lengths below n_0, including 0 if necessary, place the
correct answers in the decider's finite control or a fixed finite lookup routine.
This may have a very large but constant description and running-time bound.
Give empty advice at those lengths. A single polynomial with a sufficiently
large constant bounds the running time at all those finite inputs as well as the
large-length computation. The resulting machine and advice family satisfy the
standard definition of P/poly for every input length.

This direction uses determinism, charged computation, and a single witness per
length. It does not require efficient universality: U is already the fixed
advice-decoding algorithm being run. No algorithm for finding short descriptions
and no agreement among descriptions at different lengths is needed.

## 5. T01: polynomial advice gives local descriptions

Let a fixed deterministic machine M decide SAT using advice alpha_n of length
m_n and halting within tau_n steps for every query of length n. Choose finite
constants A,B >= 1 and positive integers r,s such that, for all n >= 1,

```text
m_n <= A(n+1)^r,
tau_n <= B(n+1)^s.
```

Any polynomial advice/time bounds can be dominated in this form. Define
`d_n = enc_M(alpha_n)` using Section 2, and let D_n = |d_n|. Then

```text
D_n = kappa_M + m_n <= D0 n^r,
D0 = kappa_M + A 2^r,
```

because n+1 <= 2n and n^r >= 1 for n >= 1. The simulator returns the correct bit
on every n-bit query within `C_M(tau_n+n+D_n+1)^k_M` steps. Set

```text
R = max(r,s,1),
S0 = B 2^s + D0 + 2,
T0 = C_M S0^k_M.
```

For n >= 1, each term is bounded by its coefficient times n^R, so

```text
tau_n + n + D_n + 1 <= S0 n^R,
time_U(d_n,x) <= T0 n^(k_M R).
```

Now choose the fixed positive integer exponents and finite threshold

```text
a = r + 1,
b = k_M R + 1,
n_0 = max(2, ceil(D0), ceil(T0)).
```

For every n >= n_0, `D0 <= n` and `T0 <= n`, giving

```text
D_n <= n^a,
for every x of length n: time_U(d_n,x) <= n^b.
```

Hence `L^U_(n^b)(T_n) <= n^a` eventually, as required. The same d_n contains M
and alpha_n for all queries at that length. All constants and exponents depend
only on the fixed machine, evaluator, and resource polynomials, not on n or x.
No optimal simulator or tight leading constant is required. The theorem allows
discarding finitely many lengths, which is exactly what absorbs these constants.

This derivation uses the constant-overhead format to keep the calculation
transparent. An additional logarithmic advice header also gives polynomial
length and, with a charged fixed wrapper, polynomial simulation time; one must
recompute the corresponding constants rather than call that field constant.

The advice/circuit characterization of P/poly is the standard background cited
in the manuscript. Neither this argument nor that characterization equates
description length with gate count, workspace, KT, Kt, or full-output K^t.
Explicit circuit/KT parameter comparisons remain W02 work.

## 6. C01: exact quantifier negation and its consequences

Write the resource assertion proved equivalent to SAT in P/poly as

```text
exists positive integers a,b; exists n_0;
for every n >= n_0: L^U_(n^b)(T_n) <= n^a.
```

Negate each quantifier and the final inequality, using the convention that
infinity is greater than every finite integer. Its exact negation is

```text
for every positive integer pair a,b; for every n_0;
there exists n >= n_0: L^U_(n^b)(T_n) > n^a.
```

For each fixed pair a,b this means that the failing lengths form an infinite
set. It does not require eventual failure at every length, or one common set of
lengths for all exponent pairs. It is equivalent to SAT not in P/poly by T01.
Since P is contained in P/poly and SAT is in NP under the standard explicit
encoding convention, P = NP would contradict this assertion. Thus it implies
P != NP. The converse from P != NP is not supplied.

The unbounded choice of a and b is essential. Excluding only constant- or
logarithmic-length descriptions, one selected polynomial exponent, or one
selected query-time exponent does not prove C01's full assertion. For fixed
positive constants alpha,c, a bound `|d| time^alpha >= n^c` alone still allows
both quantities to be polynomial. No such finite-exponent polynomial lower
bound is upgraded here to Q01.

## 7. Findings and dependency effects

| Finding | Technical disposition | Effect and follow-up |
| --- | --- | --- |
| F01: the formula encoding is described conventionally, without a bit grammar | Nonblocking for the language-general T01 proof and C01 under the intended SAT-in-NP convention | Choose an explicit syntax before per-length encoding-sensitive results; Section 3 is a candidate, not a change to T_n |
| F02: efficient universality is assumed, without numerical simulation constants | Sufficient at the existential polynomial-resource level; Section 2 states the needed contract and Section 5 absorbs its constants | A merely universal U is insufficient. Fix more detail before exact-exponent, circuit-size, or KT comparisons |
| F03: program and advice-length headers have different costs | A self-delimiting fixed program header gives constant overhead; an optional advice-length header is logarithmic and remains polynomial | No contradictory layout is imposed by the current prose. Future formats must record the actual overhead |
| F04: the definition omits length zero | A finite case handled explicitly in Section 4 | No asymptotic change or padding argument is needed |
| F05: C01 uses infinitely many lengths for each exponent pair | The manuscript's quantifiers match the exact negation; Section 6 expands it | Preserve these quantifiers in Q01 and subsequent reductions |
| F06: independent review and formal verification are not evidenced | They remain pending; no proof/review status is upgraded | W01's independent-human-review acceptance criterion remains open |

The existing dependency path `T01 -> C01 -> Q01` remains valid and unchanged.
P01 separately needs decidability and does not imply efficient local evaluation.
No new edge between the ordered-diagram claims and T01/C01/Q01 is justified.
This audit does not establish a new lower bound, a KT identity, or a reduction
to a magnification theorem. W02 can use the audited polynomial simulation
contract while identifying any stronger convention it needs. W03/W04 must still
state their own representation and transfer assumptions.

## 8. Questions and package for independent human review

The review package consists of this dossier, manuscript Definition 2.1 and
T01/C01, the current claim register, and the existing review checklist. Ask the
reviewer to resolve the following explicitly:

1. Is the evaluator's efficient-universality contract stated strongly enough for
   both the program/advice layout and the charged multitape simulation, without
   importing a free access primitive?
2. Is the distinction between the compatible conventions proposed here and the
   manuscript's designated U and SAT encoding clear? Which exact conventions
   should be adopted before future parameter-sensitive claims?
3. Do the constants D0,S0,T0, integer exponents, and finite threshold in Section 5
   correctly establish the eventual n^a/n^b inequalities for every query?
4. Does the reverse construction supply a single fixed decider and advice by
   length only, including small lengths and malformed SAT inputs?
5. Are C01's exponent/length quantifiers, the SAT-in-NP premise, and the missing
   converse from P != NP represented faithfully?
6. Is any additional correction needed before relying on this exposition in
   W02 or later research? Record a precise counterexample or missing hypothesis
   for any disputed step.

Record reviewer identity, date, independence, reviewed scope, findings, and their
resolution only after an actual review. No reviewer contact or endorsement is
claimed by preparing this package.

## 9. W01 acceptance evidence

| Original criterion | Evidence in this dossier | Status |
| --- | --- | --- |
| Check efficient universality and charged access costs | Section 2: operational model, compatible ordinary simulator, and explicit simulation contract; F02 | Technical agent audit completed under the stated contract; human review pending |
| Check advice depends only on input length | Sections 2, 4, and 5: one d_n/alpha_n per n and all queries at that n | Technical agent audit completed; human review pending |
| Verify headers, constants, and finite exceptions | Sections 2–5: exact header lengths, D0/S0/T0 bounds, exponents and threshold, finite lookup | Technical agent audit completed; human review pending |
| Record an actual independent human review | No such review is supplied | Pending; do not close W01 |

The technical dossier is complete at the scope of the current expository
statements. Exact machine implementation, an author-adopted bit serialization,
external mathematical review, formal proofs, and W02 comparisons are distinct
future outputs. No claim that these were completed is implied by this document.
