# Development and research roadmap

Planning date: 2026-10-19. Baseline: `main` at `d6417b7`.
Status: staged execution initiated at the author's request on 2026-10-19.
See [execution-waves.md](execution-waves.md) and
[tracking issue #9](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/9).
Work-package acceptance criteria remain open unless supported by their own
evidence. Adopting this roadmap does not complete W01–W06 or change any
mathematical claim status.

## 1. Intended outcome

Turn the initial expository workspace into a reviewed, reproducible research
artifact with a clearly identified contribution. Possible contributions include
a parameterized model comparison, a theorem in a specified restricted model,
a documented obstruction, or a deliberately expository article.

Q01 remains the open target `SAT not in P/poly`. The roadmap does not assign a
discovery deadline to that target. A restricted diagram bound or finite experiment
does not establish it. A bound `|d| * t^alpha >= n^c`, for fixed positive constants
alpha and c, still permits both resources to be polynomial in n.

## 2. Evidence at the starting point

- Working draft v0.1.0; seven-page manuscript.
- Thirteen registered entries: eight expository proved statements, three
  conditional literature connections, one open target, and one finite experiment.
- T01 gives the standard polynomial-description/polynomial-advice equivalence
  under the stated evaluator convention. C01 records its exact negation.
- L02/P03/P04 give the residual-width characterization and the contrast between
  grouped width `2^m` and interleaved width at most three for the unit-clause
  incidence function. This function also has a linear-size general circuit.
- On 2026-10-19, `make verify` passed locally: four tests, metadata/reference
  checks, exact generated data for `1 <= m <= 7`, PDF build, and LaTeX log gate.
- The baseline GitHub workflow passed, including PDF publication. A manuscript
  release exists. These are artifact checks, not mathematical certification.
- Six research issues are open (#3–#8), together with two dependency PRs (#1–#2).
- Independent human mathematical review, proof-assistant verification, a new
  established contribution, and publication/license decisions remain pending.

The initial `docs/validation.md` predates remote setup. Wave 00 adds a dated
addendum while preserving that historical record; its original pending list
should not be read as current.

## 3. Dependency and decision order

1. Establish the reproducible baseline (M00), then prepare W01.
2. Fix W01's technical conventions before completing W02's simulations.
3. Start W03's literature/model selection once W01's relevant conventions are
   stable; use W02 whenever a candidate compares description or circuit resources.
4. W05 can proceed in parallel after L02's diagram convention is fixed. Its
   completion is not a prerequisite for exploratory W03 work.
5. W04's primary-source reading can begin early. Attempt an actual transfer only
   after identifying a concrete source result and proposed reduction.
6. Start W06's contribution inventory early; close publication preparation only
   after the chosen scope, reviews, and author decisions are complete.

Human review waiting time does not prevent clearly labeled exploratory work.
Any discovered foundational gap blocks dependent assertions until corrected.

## 4. Work packages

### M00 — Reproducible baseline and maintenance

**Budget:** 0.5–1 working day. **Owner:** implementation contributor; author
reviews any proposed merges. This is supporting work, not a new research claim.

Actions:

- Record baseline commit, exact commands, toolchain versions, and local outcomes.
- Add dated remote CI/release evidence to the validation record, separating local
  checks, remote checks, human review, and formal verification.
- Review dependency PRs individually for relevant migration requirements and CI.
- Link the detailed roadmap from the research-plan overview.

**Exit:** another checkout can reproduce the baseline; current evidence and
remaining limitations are recorded. A merge or publication is a separate action.

### W01 — Audit the evaluator and advice equivalence

Issue: [#3](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/3).
Claims: T01 and dependent C01/Q01; relevant definition and P01.
**Budget:** 2–3 working days of preparation/correction, excluding external review.

Proposed deliverable: `docs/w01-evaluator-audit.md`, with focused manuscript
corrections if needed.

Actions:

1. Specify a concrete implementation convention for U: input tapes, permitted
   operations, description format, output, and charged access/simulation costs.
2. Check SAT encoding, malformed inputs, `n` versus `N = 2^n`, and that one
   description answers every query of length n. Description construction remains
   excluded; descriptions are advice by length, not by individual query.
3. Audit both T01 simulations, self-delimiting headers, constants, polynomial
   overhead, and finitely many exceptional lengths.
4. Write out C01's quantifier negation: failure at infinitely many lengths for
   every fixed pair of polynomial exponents, without strengthening it to an
   eventual lower bound.
5. List findings, their effect on dependent claims, and precise review questions.
6. Prepare a human-review package; record reviewer identity, date, scope, findings,
   and resolution only after an actual independent review.

**Exit:** technical dossier complete; proof gaps resolved or explicitly blocking
dependent claims; actual independent human review recorded for the issue's final
review criterion. An agent audit alone leaves that criterion pending.

**Stop/rework:** if a simulation requires an uncharged primitive or a stronger
universality assumption, correct the definition and re-audit affected claims
before using them in a new theorem.

### W02 — Parameterized comparison with KT and circuit size

Issue: [#4](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/4).
**Dependency:** stable W01 conventions. **Budget:** 3–5 working days.

Proposed deliverable: `docs/w02-kt-comparison.md`, plus separately registered
statements for proved comparisons that are added to the manuscript.

Actions:

1. Fix primary-source definitions and versions for local L, KT, Kt, and `K^t`.
2. Build a resource table with query length n, table length N, description length,
   worst-case query time, access model, circuit gate count, and encoding length.
3. Derive both simulation directions wherever valid. Retain overheads for index
   encoding, headers, end-of-string tests, input nodes, and circuit descriptions.
4. Separate additive, multiplicative, logarithmic, and polynomial losses; identify
   assumptions such as random access rather than hiding them in notation.
5. Check exact cited statements against primary sources and identify comparisons
   that are standard, newly proved, partial, or unresolved.

**Exit:** each direction has a proof/reference with all hypotheses, or an explicit
unresolved status. A partial comparison is a useful checkpoint, but any unmet
issue acceptance criterion stays open. No exact identity is inferred by analogy.

**Stop/rework:** incompatible machine conventions require a stated simulation
or a narrower claim; do not silently change the model to make the comparison work.

### W03 — A result in a specified restricted model

Issue: [#5](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/5).
**Dependency:** stable relevant model; W02 informs resource comparisons.
**Budget:** 5–10 working days for the first investigation, followed by a decision.
This is an exploration budget, not a theorem-delivery promise.

Proposed deliverable: `docs/w03-restricted-model.md`, a candidate statement and
proof or counterexample; targeted experiments only where they answer a question.

Actions:

1. Compare two or three candidate families/models with established literature.
2. Choose one model and state allowed orders, encodings, sharing, skipped levels,
   and uniformity. State the measured resource and all quantifiers.
3. Check the representation changes the proposed bound is supposed to tolerate.
   The current unit-clause family already fails robustness to arbitrary orders.
4. Formulate one scoped lemma and identify its hardest step before coding.
5. Use small exact instances and an independent oracle where useful to seek
   counterexamples and validate implementations.
6. Produce a complete proof, a precise counterexample, or a documented obstruction.

**Decision after the first 1–2 days:** keep a candidate only if its scope,
literature position, and plausible proof mechanism are explicit.

**Exit:** a proved statement or explicit counterexample within the named model.
An obstruction report is a valid research output; unresolved proof criteria remain
open. Any originality claim requires a literature audit and independent review.

**Stop/rework:** after the exploration budget, record what failed and select a
different family/model or contribution type. Increasing m alone does not repair
a missing asymptotic argument.

### W05 — Formalize the residual-width lemma

Issue: [#7](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/7).
Claim: L02. **Dependency:** stable layered-diagram convention.
**Budget:** 3–6 working days; optional parallel track when capacity permits.

Proposed deliverables: pinned proof-assistant project, a manuscript correspondence
note, and one reproducible verification command. The assistant is selected after
a small feasibility check; no tool is assumed to be installed already.

Actions:

1. Choose Lean, Rocq, Isabelle, or another suitable assistant after a short spike.
2. Define finite inputs, fixed order, layers, deterministic transitions, terminal
   output, and residual functions under the manuscript's conventions.
3. Prove different residuals require different reachable states.
4. Construct the residual-state diagram and prove it attains the widths.
5. Verify boundary layers and match each formal hypothesis to L02.
6. Pin dependencies, add a clean verification command, and integrate CI when ready.

**Exit:** both directions are checked without unproved theorem placeholders or
unchecked assumptions replacing the target proof. Document any axioms and the
trusted toolchain. State precisely that L02, rather than all of T01 or the paper,
has been formalized.

**Stop/rework:** if library infrastructure dominates the budget, narrow to the
finite L02 theorem and document deferred extensions.

### W04 — Audit transfer to the exact Gap-MCSP theorem

Issue: [#6](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/6).
Literature entry: R02. **Dependency for transfer:** a concrete source result
and a proposed reduction. **Budget:** 2–4 working days, starting with a short
feasibility assessment.

Proposed deliverable: `docs/w04-transfer-audit.md`.

Actions:

1. Check Oliveira–Pich–Santhanam Theorem 1.4 against the primary source.
2. State source and target problems, reduction direction, promise sets, and
   behavior outside the promise if relevant.
3. Retain both thresholds, the constant c, epsilon, every sufficiently small
   beta, and the full-table input length N.
4. Tabulate all size/time/circuit-model transformations, explicitly using
   `N = 2^n` when appropriate.
5. Prove each reduction and resource-preservation step, or identify exactly
   which step is absent.

**Exit:** a fully justified transfer, or a checked applicability report with an
explicit missing reduction. A restricted OBDD lower bound alone is insufficient.

**Stop/rework:** without a proposed reduction meeting the target's requirements,
return to W02/W03 or keep the report as a documented limit of the approach.

### W06 — Contribution, independent review, and publication preparation

Issue: [#8](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/8).
**Dependency for final closure:** chosen contribution and resolved review findings.
**Budget:** 1–3 working days of preparation, excluding review and author decisions.

Actions and deliverables:

- Write a contribution statement distinguishing standard exposition, proved model
  comparisons, restricted results, finite data, and open targets.
- Check primary bibliography, novelty claims, and the scope of all borrowed results.
- Obtain actual independent human review; record findings and their resolution.
- Have the author decide authorship/disclosure, separate manuscript/software
  licenses, and whether/where to submit.
- Run final checks from a clean checkout; inspect the rendered PDF; archive source,
  data, bibliography, toolchain versions, logs, and PDF from the same commit.
- Prepare a submission snapshot only when appropriate. Add identifiers only when
  assigned. Existing automated manuscript releases remain working drafts.

**Exit:** the selected publication checklist is complete with real evidence and
author decisions. Preparation can continue while a decision is pending; sending
messages, choosing licenses on the author's behalf, or submitting is not implied
by adopting this roadmap.

## 5. Suggested first cycle

Planning assumption: one principal contributor working about 8–10 hours per week,
with implementation assistance. A working day in the budgets above is about six
focused hours. The complete program is approximately 17–32 such days, excluding
external waiting time and any renewed research cycle. Parallel work requires
additional capacity; it does not remove review dependencies.

Use a six-week first cycle (48–60 hours) to produce an audited foundation,
a first KT comparison, and a scoped research choice; defer excess scope rather
than compressing review to meet a date.

| Window | Main activity | Reviewable output |
| --- | --- | --- |
| Week 1 | M00 and W01 setup | Baseline record; model/cost checklist; T01 proof map |
| Week 2 | W01 technical dossier | Audit note; corrections if needed; human-review questions |
| Weeks 3–4 | W02 | Definition/resource table; first simulations; explicit unresolved directions |
| Weeks 5–6 | W03 selection and first investigation | Chosen model/family; candidate lemma; counterexample search or proof skeleton |
| If separate capacity exists | W05 feasibility and finite definitions | Assistant choice and a small compiling project |
| End of cycle | Scope decision | Continue W03, repair foundations, pursue a comparison/exposition, or change candidate |

For example, allocate 4 hours to M00, 14–18 to W01, 18–24 to W02, and the remaining
12–14 to W03 selection. W02 completion and external review may extend into the
next cycle. W03/W05/W04/W06 final closure is not promised by week six.

## 6. Working method and evidence

- Keep repository content in English. Use one coherent claim per branch/PR.
- Each mathematical change records model, quantifiers, hypotheses, claim ID,
  dependencies, precise sources, proof status, counterexamples, and review evidence.
- Preserve the existing claim-status schema; track review progress separately.
  The labels below do not add new `research/claims.json` statuses.
- Distinguish: finite checks; consistency checks; agent audit; independent human
  review; and proof-assistant verification of a named theorem.
- Run `make verify` for manuscript/experiment changes. Inspect the PDF after
  substantial layout changes. Test new experiments against independent small
  instances; do not add tests that simply restate the implementation.
- At each weekly checkpoint, record completed outputs, blockers, remaining budget,
  findings that change a claim, and the next specific question.
- Keep GitHub issue criteria unchecked until actually fulfilled. Do not close W01
  merely because an automated audit finished.

## 7. Risks and responses

| Risk | Observable warning | Response |
| --- | --- | --- |
| Wrong asymptotic scale | A bound polynomial in N is described as polynomial in n | Show both sizes in every simulation/reduction table |
| Representation dependence | An allowed order/encoding destroys the lower bound | Restrict the statement explicitly or change the family |
| Rediscovering known results | A claim matches an existing theorem after renaming | Cite it as exposition and reassess the contribution |
| Experiment expansion without a proof mechanism | Larger m is the only proposed next step | Return to a precise lemma or record an obstruction |
| Mistaking CI for mathematical review | A green check is used to upgrade proof/review status | Attach the correct kind of evidence to each assertion |
| W04 without a valid reduction | A restricted bound is used as a general-circuit bound | Record the absent step and stop the transfer claim |
| External review delay | No real reviewer report is available | Continue labeled exploratory work; retain pending review |
| Formalization scope growth | Most work builds unrelated infrastructure | Reduce to the exact finite L02 theorem |

## 8. Milestones and immediate queue

- **R0:** reproducible and accurately documented baseline.
- **R1:** W01 technical dossier; human-review status explicitly tracked.
- **R2:** parameterized W02 comparison with proved and unresolved directions separated.
- **R3:** W03 result, counterexample, or obstruction report and a continue/change decision.
- **R4 (parallel):** formal verification of L02 with matching conventions.
- **R5 (conditional):** checked W04 transfer or explicit applicability limit.
- **R6:** author-approved, reviewed publication scope and reproducible snapshot.

The next implementation task is a focused W01 audit PR. Suggested initial queue:
baseline validation addendum; evaluator convention table; both T01 simulations;
C01 quantifier audit; findings/dependency updates; review dossier. Treat dependency
maintenance in separate PRs. This document plans those changes; it does not assert
that they have been performed.

Version intent: v0.1.x for foundation corrections and reproducibility; v0.2.x for
the actual reviewed extension, which need not be a new lower bound; v1.0.0 only
for an author-approved submission snapshot if the project reaches that stage.

See [research-plan.md](research-plan.md), [review-checklist.md](review-checklist.md),
[../research/backlog.json](../research/backlog.json), and
[../PUBLICATION.md](../PUBLICATION.md) for the existing acceptance criteria.
