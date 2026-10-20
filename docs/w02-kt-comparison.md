# W02: local descriptions, KT, and circuit representations

Audit date: 2026-10-20. Manuscript baseline: `d6417b7`.
Work package: [W02 / issue #4](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/4).
Dependency: [W01 evaluator audit](w01-evaluator-audit.md), whose independent
human-review criterion remains pending.

This preparatory technical dossier gives simulations in both directions under
explicit machine conventions. It claims no numerical identity, novelty,
independent human review, or formal verification. It changes neither the
manuscript nor the claim register. The derivations are evidence for review, not
newly registered research results or a lower-bound advance.

## 1. Primary sources and conventions

The checked primary text is the author version of Allender, Buhrman, Koucky,
van Melkebeek, and Ronneburger, *Power from Random Strings*, dated 17 October
2005, available at [the author's KT.pdf](https://people.cs.rutgers.edu/~allender/papers/KT.pdf).
Its printed page numbers below are **author-version pages**, not journal pages.
The journal article is the 2006 SIAM paper cited in the manuscript; the final
journal PDF and its page-specific correspondence were not checked for this audit.

| Primary locator | Exact material used |
| --- | --- |
| Section 2.2, p. 7 | Random-access input model and finite oracles; an out-of-range finite-oracle access returns `*` |
| Proposition 5, pp. 7–8; Definition 6, p. 8 | Efficient universal machine; fixed-program description overhead and `c_M T log T` simulation, linear for a two-work-tape simulated machine |
| Definition 7 and its explanation, p. 8 | End-of-string symbol at position `|w|+1`; distinguishing rather than full-output convention |
| Definitions 8–10, pp. 8–9 | Indexed Kt, indexed fixed-time K^t, and KT; their different resource charges |
| Definition 2, p. 7; Theorem 11, p. 10 | Truth-table circuit convention and the two parameterized circuit comparisons |
| [Allender–van Melkebeek clarification](https://people.cs.rutgers.edu/~allender/papers/clarification.pdf), p. 1 | Theorem 11 requires size to count **input gates plus connections**; counting connections alone loses the arity cost; end-of-string cases also require attention |

The source uses its own symbol U for a KT machine. Here **U** always denotes
the manuscript's sequential-input evaluator and **V** the efficiently universal
KT machine. All logarithms are base 2. In our own bounds `log(z+2)` regularizes
small arguments; it is not a literal replacement of a printed source formula.
Constants and polynomial degrees below can depend on these fixed machines and
fixed encodings, but never on the particular truth table or query.

## 2. Parameters and the precise KT interface

Fix n >= 1, N = 2^n, and a binary table B of length N. The entry B[x] is indexed
by the n-bit string x in lexicographic order, starting with the all-zero string.
The discussion applies to arbitrary such B; setting B = T_n gives SAT's table.

| Symbol | Meaning |
| --- | --- |
| n | Query length and circuit arity |
| N = 2^n | Length of the complete truth-table string |
| s,t | Local-description length and worst-case U query time |
| z,m | KT finite-oracle description and its length m = |z| |
| tau | KT acceptance-time witness, shared by all required index/symbol queries |
| k = m+tau | Cost of this KT witness; the minimum over witnesses is KT_V(B) |
| g | Ordinary internal Boolean gates in the circuit convention of Section 6 |

Write `L_U(B; t)` for the scalar-budget instance of the manuscript's local
measure: the minimum |d| such that U(d,x) returns B[x] within t transitions for
every n-bit x. This is shorthand for the original definition evaluated at this
length, not a new compression measure.

Definition 10, with the external oracle fixed to the empty set and conditional
string empty, says that (z,tau) is a KT witness precisely when

```text
for every positive i <= N+1 and every b in {0,1,*}:
V^z(i,b) accepts within tau steps  iff  B_i = b,
where B_(N+1) = *.
KT_V(B) = min (|z| + tau).
```

The entries B_i for 1 <= i <= N are binary. The symbol `*` at N+1 is part of
the required contract. Definition 10 does not require the same time bound at
every i > N+1. Nor does its literal acceptance predicate guarantee that an
incorrect-symbol computation halts or rejects within tau: it merely does not
accept within tau. Both facts matter in the simulations below.

V has sequential work tapes but random access to its input and finite oracles,
using address/query tapes. Producing and changing an address costs ordinary
tape steps; an arbitrarily large integer operation is not free. The finite
oracle z answers z_j at in-range positions and `*` out of range. Random access
to the input must also be simulated when moving back to U. No SAT oracle,
nonempty external oracle, or length-dependent conditional string is available.

For a concrete query serialization use `enc(i,b) = tag(b) bin(i)`, with
`tag(0)=00`, `tag(1)=01`, and `tag(*)=10`; `11` is invalid. The index is positive
canonical binary, without leading zeroes, and extends to the input endmarker.
Every required query has at most n+3 bits. Copying and decoding this format can
be done in O((n+1)^2) charged steps, including binary address generation in the
random-access model. The source says that i is binary but does not impose our
literal pair serialization. All conversions below pay for this fixed
representation; changing it is not asserted to preserve numerical KT values.

For efficient universality, use the fixed-program compiler implementation of
Proposition 5: compiling a fixed oracle machine M with finite data y gives one
oracle z of length at most |y|+c_M, with runtime at most
`c_M T log(T+2)`. The same compiled z is used for **all** queries; there is no
per-query description choice. The `+2` and a larger constant cover small T.
The linear improvement for two-work-tape M is not needed below.

## 3. Local U to KT: a charged wrapper and its bound

Assume `L_U(B; t) <= s`, witnessed by d, where |d| <= s and t >= 1. Use W01's
self-delimiting integer header

```text
I(j) = 1^ell 0 bin(j+1),  ell = floor(log2(j+1))+1,
h(j) = |I(j)| = 2 floor(log2(j+1))+3.
```

Give the fixed wrapper M_U finite-oracle data `y = I(n)d`. It operates as follows:

1. Decode n. For a required input (i,b), recognize i = N+1 by binary arithmetic
   on n+1 bits, accepting exactly b = `*` in that case. N is never expanded into
   a unary table or enumerated merely to recognize this position.
2. For 1 <= i <= N, construct `x = bin_n(i-1)`, padded with leading zeroes to
   exactly n bits. This is the conversion between the source's 1-based index
   and the manuscript's lexicographic n-bit query.
3. Recover d from the finite oracle after I(n), scanning until its out-of-range
   `*`, and install its ordinary read-only-tape representation. Copy the query
   into its virtual input tape. This charges all address creation, copying,
   and endmarker handling.
4. Simulate the fixed U on (d,x). When it returns q in {0,1}, accept exactly
   when b = q; in particular reject b = `*` at a data position.

The n header is necessary for this general wrapper: the binary index of a
small i does not specify the number of leading zeroes or the table endpoint.
No s header is needed because this particular source's finite oracles reveal
their end with `*`. A bit-oracle model returning 0 beyond its end would require
an additional length convention, for example I(|d|), costing O(log(s+2)) bits.

The wrapper is fixed independently of B,n,s,t. It need not know t: on every
valid query, the given local witness already halts within t. Its finite-oracle
copy uses O(s+h(n)+1) queries with explicitly written binary addresses. Index
conversion and copying are polynomial in n+s; U has a fixed finite transition
table and can then be simulated on copied input tapes with constant per-step
overhead by a fixed multitape machine. A conservative charged wrapper bound is

```text
F(n,s,t) = C_F (n+s+t+2)^3.
```

Compile M_U into V using Proposition 5. Its one compiled oracle z has

```text
m <= s + h(n) + c_F,
tau <= c_F F(n,s,t) log(F(n,s,t)+2).
```

Consequently, after increasing a fixed constant, one may use the explicit
polynomial envelope

```text
KT_V(B) <= s + h(n) + c_F + P_F(n,s,t),
P_F(n,s,t) = C'_F (n+s+t+2)^4.
```

This proves a polynomial simulation, not `KT = s+t`, not additive-constant
invariance, and not an optimized exponent. Interpretation and oracle-access
costs have not been discarded. Constructing z is irrelevant to this nonuniform
existence bound, but accessing it during a query is charged.

## 4. KT to local U: synchronized acceptance search

Let (z,tau) be any KT witness for B, with |z| = m. A fixed ordinary multitape
wrapper R_V receives z as auxiliary data and an n-bit query x. It obtains
n = |x| by a charged scan and constructs the positive index `i = value(x)+1`.
Even the largest data index N and the sentinel N+1 have binary length n+1;
no N-bit representation of the table is required.

The wrapper simulates V^z(i,0) and V^z(i,1) in synchronized rounds: complete
one **logical V transition** of each nonhalted computation, including the work
needed to emulate a random-access query, before advancing to the next round.
It returns the symbol of the first accepting branch. A rejecting halted branch
can be frozen while the other continues.

Exactly one of 0 and 1 is B[x]. Its branch accepts in at most tau logical
transitions. The other branch cannot accept within tau transitions, although
it could accept later. Until the correct branch accepts, neither simulated
branch has advanced beyond its corresponding round. Thus a later false
acceptance cannot win this synchronized search. There are at most tau rounds
and 2tau simulated transitions. Alternating according to physical simulator
runtime rather than logical V transitions would not justify this argument.

Neither tau nor n needs a description header: tau is used only to prove the
running-time bound, and n is available from x. One must not instead run a
false candidate until rejection; it might not halt. A clocked alternative
would be valid if tau were explicitly encoded and charged, but is unnecessary.

To implement each random-access query sequentially, copy z and the two finite
query-input encodings to work tapes. Compare the requested binary address with
the relevant finite length, return `*` if out of range, and otherwise locate
the cell by a charged scan. The conditional empty finite oracle returns `*`;
the empty set oracle returns 0. Work tapes remain ordinary sequential tapes.
An address written during tau transitions has O(n+tau+1) bits in a conservative
bound. Never allocate space proportional to its potentially exponential
**numerical value**. Comparison with m or the O(n)-bit input length comes first.

Copies, binary counters, comparisons, and at most 2tau queries can all be
bounded conservatively by

```text
G(n,m,tau) = C_G (n+m+tau+2)^3
```

ordinary multitape steps. Apply W01's U compiler to this fixed wrapper. For
fixed constants c_R,C_R and integer k_R >= 1, the resulting local description
and time satisfy

```text
|d| <= m+c_R,
time_U(d,x) <= C_R (G(n,m,tau)+n+m+c_R+1)^k_R
            <= C'_R (n+m+tau+2)^(3k_R).
```

The same d works for every query at this length. Set
`P_R(n,k) = C'_R(n+k+2)^(3k_R)`. Taking an optimal KT witness, whose cost is
k = m+tau, gives the useful consequence

```text
L_U(B; P_R(n,KT_V(B))) <= KT_V(B)+c_R.
```

The proof requires deterministic V, the source's finite-oracle convention,
its bounded-time acceptance predicate, and U's efficient simulation contract.
It supplies no corresponding numerical bound for an arbitrary uncharged
random-access machine, external oracle, or different KT variant.

## 5. Circuit literature: retain the corrected size convention

For comparison, Theorem 11 in the checked author version prints, with k standing
for KT^A(B|y), a constant c and the following two bounds:

```text
Size^(A,y)(B) <= c k^2 (k^2 + log |B| + log |y|),
KT^A(B|y) <= c [Size^(A,y)(B)]^2
                (log Size^(A,y)(B) + log log |B|).
```

These displays reproduce its parameters rather than specialize the empty-y
case; literal log(0) is not evaluated here. The source treats strings as padded
truth tables under Definition 2. Our tables already have power-of-two length,
so no zero-padding change is needed. Its oracle circuitry and conditional y
are additional structure, not automatically available to the local evaluator.

The author clarification is essential: the corrected size counts **input gates
plus connections**, not just internal gates or connections alone. The original
connection-only convention permits constant-size constant functions irrespective
of their declared input arity and does not justify both parts as intended. The
clarification also explicitly calls attention to end-of-string index cases.
It is unsafe to transfer the printed statements while dropping either condition.

Here `log |B| = n`, whereas `log log |B| = log n` where those expressions are
defined. The additive n term in the first display is retained. These statements
do not supply a bound depending only on k with n silently removed. For our
unconditional comparisons, the direct constructions in Section 6 avoid the
empty-condition and small-log corners; their regularized logarithms and constants
are our explicit conventions, not a claimed verbatim version of Theorem 11.

## 6. Direct circuit encodings and charged evaluations

Fix the finite basis AND, OR, NOT of fan-in at most two. Keep n labelled variable
input nodes even when some are unused, and allow two fixed constant nodes 0 and
1. Let g count the other, ordinary internal gates. The output designates a
node. A difference of two constant nodes is accounted for as a fixed overhead,
not conflated with the source's Size measure.

Number constants, input nodes, and gates topologically, and set

```text
w = ceil(log2(n+g+2)).
```

A description consists of I(n), I(g), for each gate a 2-bit type and two w-bit
predecessor slots (one ignored for NOT), and a w-bit output reference. Valid
predecessors precede their gate. Adding a fixed evaluator program header gives
the explicit upper bound

```text
D_C <= c_C + h(n) + h(g) + g(2+2w) + w
     = O((g+1) log(n+g+2) + log(n+2)).
```

This is a bound on a **binary description**, not an equality with g. The log n
term and references to n variable inputs remain even if g is small. The fixed
evaluator scans the n-bit assignment, checks the encoded arity, and evaluates
gates in order, looking up predecessor values by ordinary scans. A conservative
bound is `C_C(n+g+2)^3` before the U compiler and therefore, for some fixed
integer k_C >= 1,

```text
L_U(B; C'_C(n+g+2)^(3k_C)) <= D_C
```

whenever such a circuit computes B. This construction builds no full truth table.
It charges the sequential cost of locating a circuit record or predecessor.

For the other direction, fix a U witness of length at most s and worst-case
time t. Hardwire d and simulate at most t transitions by a Boolean computation
circuit, making a halted configuration persist. There are n variable inputs;
the readonly d bits are constants. A configuration uses O(n+s+t+1) cells and
head/state indicators in a direct finite encoding. One transition can be
computed by O((n+s+t+2)^2) bounded-fan-in gates, a conservative bound permitting
multiplexers and head updates. Concatenate t transitions and select the output.
For a constant C_U depending only on U this gives

```text
g <= C_U(n+s+t+2)^3.
```

The description can be hardwired because this is a nonuniform construction.
It does not assert an efficient algorithm to discover d. For a pruned circuit
let e be its number of gate-input connections and define the conservative
corrected size `S = n+e+2`, retaining both constant nodes. With bounded fan-in,
e <= 2g, and every nonoutput useful internal gate has an outgoing connection.
Thus g <= e+1, and

```text
n+g <= S <= n+2g+2.
```

This accounts for the input-node term and agrees with the corrected source
convention up to a fixed additive constant. Internal gate count, connection
count, declared arity, and encoding length are separate quantities. An n-input
constant function can have g = 0 in this representation while S = n+2.

## 7. Polynomial-family consequence, with quantifiers

For any family B_n of strings of length 2^n, the preceding simulations show
equivalence of the following eventual polynomial-resource statements:

```text
(a) exists positive integers a,b and n_0 such that for every n >= n_0:
    L_U(B_n; n^b) <= n^a;
(b) exists a positive integer c and n_0 such that for every n >= n_0:
    KT_V(B_n) <= n^c;
(c) exists a positive integer d and n_0 such that for every n >= n_0:
    B_n has an n-input circuit with at most n^d ordinary internal gates.
```

Indeed, substitute the polynomial bounds into P_F, P_R, and the circuit
constructions; their degrees are fixed. Increase integer exponents and exclude
finitely many lengths to absorb constants and headers, just as in W01. Including
all n input nodes preserves this family-level equivalence since n itself is
polynomial. No sequence of descriptions, circuits, or KT witnesses is required
to be efficiently constructible or even uniformly specified.

For B_n = T_n this is the standard polynomial-advice/circuit characterization
already underlying T01. It is not a new lower bound. Negating (b) gives
`for every c and every n_0, some n >= n_0 has KT_V(T_n) > n^c`. This retains
infinitely many lengths **for each exponent**, not an eventual lower bound or
one selected exponent. With the stated models it reformulates the same open
SAT-not-in-P/poly target; it does not resolve Q01.

## 8. KT, Kt, and the two fixed-time K conventions

| Notation used here | Operation and charged resource | Relevant distinction |
| --- | --- | --- |
| KT_V(B), source Definition 10 | Indexed distinguishing with sentinel; minimize m+tau | Linear time weight; random-access finite oracles and input |
| Kt_idx,V(B), source Definition 8 | Same indexed distinguishing predicate; minimize m+log tau | Logarithmic time weight, not KT; the source discusses comparison with Levin's original convention after Definition 8 |
| K^T_idx,V(B), source Definition 9 | Same predicate with time fixed at T(|B|), minimize m | The source's Definition 9 is **indexed**, despite the notation K^t often being used for full output elsewhere |
| K^T_out,W(B), a separately specified conventional full-output measure | Minimize program length subject to W writing all B and halting within T(|B|) | Requires at least N output steps in a bit-output model; not Definition 9 |

The source recalls Levin's original full-output Kt in Section 2.1 and explains
that its indexed version changes the comparison by logarithmic terms for
suitable machines. No exact identity with that original convention is imported
here. Similarly, the manuscript's phrase “full-output K^t” must not be attributed
to the source's **indexed Definition 9**; these are different conventions bearing
similar notation.

The time function in source Definition 9 is evaluated on |B| = N. The local
query budget is evaluated on n. A poly(n) bound corresponds to poly(log N), not
to an arbitrary polynomial in N. A full-output computation cannot write an
N-bit table in poly(log N) transitions for all sufficiently large N. Enumeration
of all local queries would itself require N output bits and would be a separate
simulation with that cost. No fast full-output claim or fixed-time equality is
proved in this dossier.

## 9. Evidence against W02 acceptance criteria and remaining limits

| Original W02 criterion | Concrete evidence | Technical status |
| --- | --- | --- |
| Specify machine and access models | Sections 1–4 distinguish U sequential inputs from V random-access input/oracles; compilation, endmarkers, and addresses are charged | Addressed under the fixed contracts; independent human review not supplied |
| Track input length versus table length | Sections 2–4 define N=2^n, 1-based indices, leading-zero padding, and the N+1 sentinel; Sections 5, 7, and 8 retain both time scales | Addressed |
| Account for input nodes and description headers in circuit size | Section 3 charges h(n); Section 6 gives D_C, g, e, S, input arity, and both circuit simulations; Section 5 records the source correction | Addressed without a gate-count/description-length identity |
| Cite precise primary statements and label unresolved directions | Author-version locators and clarification in Section 1; literal scope in Sections 5 and 8; limitations below | Addressed for the checked primary version; journal-version page reconciliation remains unverified |

The two local/KT directions are justified above for the fixed unrelativized
setting. Remaining limits must stay explicit:

- Tight constants, optimal exponents, numerical invariance, and an exact local-L/KT
  identity are not established. The broad polynomial envelopes are deliberate.
- Conditional or relativized KT comparisons need explicit resources for their
  extra oracle/string. A free SAT oracle cannot be introduced through notation.
- A different finite-oracle end convention, query pairing, universal compiler,
  circuit basis, or succinct description format requires its own simulation.
- Source Definition 9 and full-output fixed-time K remain distinct. No fixed-time
  equality or tight transfer between them is asserted.
- The checked author version and its clarification are primary evidence; the
  final journal pagination/version was not independently reconciled here.
- Human mathematical review and proof-assistant verification are absent. W01's
  pending independent-review criterion is not completed by this dependent audit.

No finite experiment can certify these asymptotic simulations. This dossier is
the proposed evidence for reviewing W02's technical criteria; it does not itself
change an issue checkbox, close an issue, or add a manuscript/claim-register entry.
