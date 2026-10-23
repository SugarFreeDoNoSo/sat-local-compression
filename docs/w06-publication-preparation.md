# W06: contribution and publication preparation

Prepared on 2026-10-23 for the project author, Matías Donoso Quiroga.
Work package: [W06 / issue #8](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/8).
Coordination: [execution tracking / issue #9](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/9).

The project has an expository research framework, parameterized model comparisons,
restricted-representation examples, reproducible finite experiments, and formal
verification of specified elementary statements. These artifacts support an
author decision about the article's scope. They do not establish a new complexity
separation, independent human review, or a completed novelty audit. W06 remains
open, and no scholarly submission or reuse license is selected by this draft.

## Current integrated snapshot — 2026-10-23

The subsequent authorized integration of PRs #20, #21 and #22 is now recorded in
[the integration and review-packet refresh record](pr-integration-2026-10-23.md).
Its accepted technical source is `82a3af3844fdc11690f7ccf47d2d7fc259246ee0`:
17 claims, L04 graph signatures, whole-graph matching certificates, and named
Lean evidence for L02/P03 only. PR16 is refreshed against that existing source,
with 48 fingerprints and seven review units; it remains a review request, not a
completed independent human review.

The historical inventory, branch snapshots and local-combination evidence below
are retained as dated records. Their earlier “awaiting integration” and “keep
PR16 draft” directions describe the pre-authorization state and are superseded
only for the authorized technical integration. All human-review, novelty,
authorship, licensing and submission gates remain unchanged. Use the linked
current record rather than these older counts when evaluating the integrated tree.

## Historical contribution inventory before PR20/21/22

The following is a candidate contribution statement for the author's review:

> An expository framework for exact local descriptions of SAT truth tables,
> accompanied by explicit comparisons of resource conventions, examples that
> separate representation constraints from general circuit complexity, exact
> finite validation, and reproducible formal verification of named lemmas.

The article may emphasize exposition, model comparison, or reproducible methods.
The author should select that emphasis after considering the completed results,
their relationship to prior work, and independent review. No assertion of a new
general circuit lower bound follows from any of these options.

| Area | Project artifact | Scope and contribution category |
| --- | --- | --- |
| Foundations | Local-description model; T01 advice equivalence; C01 quantifier negation; W01 audit | Self-contained exposition of standard polynomial-resource consequences. Efficient universality, charged access, length-only advice, and finite exceptions remain explicit. |
| Model comparison | W02 dossier relating local descriptions, KT conventions, and circuit representations | Parameterized simulations and resource accounting under specified machines. No numerical identity among local L, KT, Kt, or whole-output time-bounded K is asserted. |
| Representation examples | Matching/unit-clause example P03/P04 and graph/grid statements L03/P05 | The grid family supplies an explicit all-order bound in the named layered selector model. It also has linear general-circuit size, so the result does not transfer to arbitrary SAT encodings or circuits. No originality is claimed for the lower-bound technique. |
| Finite methods | E01/E02 data, exact subset optimizer, and independent small-case oracles | Reproducible code and finite observations. The subset recurrence is an exact bottleneck dynamic program; a novel algorithmic result is not claimed. Finite checks do not prove the asymptotic grid bound. |
| Formal methods already recorded | L02 proof and correspondence guide in pinned Lean | A project proof artifact for the residual-width characterization, including lower bound and simultaneous canonical attainability. It does not formalize T01, L03/P05, or Q01. |
| Transfer analysis | W04 applicability dossier, merged in PR #23 at `67f36b1` | A requirements and obstruction analysis. There is no established resource-preserving reduction activating the cited Gap-MCSP magnification theorem. |

The distinction between query length `n`, full table length `N = 2^n`, and graph
selector length `m` must remain visible. Robustness over selector orders is a
property of the chosen incidence representation; no width-preserving translation
to the conventional SAT truth table is asserted.

## Historical prepared additions before author-authorized integration

PRs [#20](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/20),
[#21](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/21), and
[#22](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/22) were still
draft, unmerged proposals when this preparation was requested. Their artifacts
must not be described as integrated merely because a branch audit or CI passed.
Each PR explicitly says “Draft for author review; do not merge automatically.”
They remain outside this document's integrated contribution inventory. If the
author authorizes integration, the inventory can add:

| Proposal | Addition to describe after integration | Remaining limit |
| --- | --- | --- |
| PR #20 | L04 exact residual signatures for the fixed graph-selector setting, with the statement and hypotheses read from the integrated manuscript | Treat as an expository structural result unless a separate novelty audit supports a stronger description. |
| PR #21 | Whole-graph induced-matching certificates for L03, greedy coverage checks, and distinguishing prefix/suffix witnesses | A certificate verifies its specified graph and cut. These finite artifacts do not establish P05 for all lengths or a general complexity separation. |
| PR #22 | Lean formalization of P03's exact grouped midpoint width `2^m`, including `m = 0`, using L02 | Scope becomes L02 and P03 only. P04, L03/P05, L04, T01, and Q01 do not thereby become formally verified. |

PR #22's source audit at `eb4f41ff8f456de853e22f021de85a8b8c90a749`
confirmed the real predicate, exact residual count, lower bound for every correct
diagram, and canonical attainability. Its
[branch CI](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/39879435427)
passed at that head. This is branch-specific evidence, not evidence for an
unseen merged snapshot or independent human review.

A fresh local-only combination on top of PR #23's source was also checked on
2026-10-23, using heads `d43804a83869df9179470fc72afc7ea2f4e912d6` (#20),
`3b37c3aaa99a7805821d707bbf0ae29e5c1d54f0` (#21), and
`eb4f41ff8f456de853e22f021de85a8b8c90a749` (#22). Verification after each step
passed; the final combination passed 33 tests, 17 claim entries, 27 theorem
axiom closures, deterministic data/certificate checks, and the nine-page PDF/log
gates. Changed pages were visually inspected. The candidate source tree is
`2c27be90a4c5f6cd87ab4b3f27f2e662f59fbc56`. A README conflict was resolved
locally by retaining the W04 audit link and the expanded L02/P03 formalization
link. This local result does not authorize or perform any remote merge.

The integrated technical baseline for this preparation is pinned separately
from the draft branches:

| Snapshot field | Evidence |
| --- | --- |
| Integrated technical source | `67f36b1e0788b82291885a914c261dd7b73c33f2` (PR #23), before this preparation PR |
| Successful main CI | [39919613432](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/39919613432), completed / success for research, Lean, manuscript and Release |
| Local verification of PR #23's source tree | `make verify LAKE=/workspace/toolchains/lean-4.35.0-linux/bin/lake` passed |
| Formal scope | L02 only; 18 theorem axiom closures audited in the pinned Lean 4.35.0 toolchain |
| Claim register | 16 entries; R02 conditional and Q01 open; human review pending |
| Finite artifacts | Nine tests; matching data for `1 <= m <= 7`, five graph families with at most nine bits |
| Manuscript | Nine A4 pages with clean reference/overflow/character log checks; [commit-pinned published PDF](https://github.com/SugarFreeDoNoSo/sat-local-compression/releases/download/manuscript-67f36b1e0788b82291885a914c261dd7b73c33f2/main.pdf) |

This is evidence for that technical baseline, not approval of a submission-ready
version. Validation of this preparation PR is recorded in its own PR and CI.
If draft technical branches are later integrated, refresh the source, claim
count, formal scope, data/certificate inventory, PDF and verification anchors
together; a locally tested combination is not a remote merge.

## Bibliographic metadata checked against primary records

The seven current `paper/references.bib` entries received a metadata check on
2026-10-23 using primary author/editorial pages, publisher-deposited DOI records,
and the pinned report revision where applicable. This verifies the listed
identity and publication details; it is not an exhaustive literature or novelty
audit, nor a review of every cited proof.

| Entry | Metadata and primary record | Chronology and locator discipline |
| --- | --- | --- |
| AroraBarak2009 | Sanjeev Arora and Boaz Barak, *Computational Complexity: A Modern Approach*, Cambridge University Press, 2009; DOI `10.1017/CBO9780511804090`; [author materials](https://theory.cs.princeton.edu/complexity/) | The print record is 2009; the DOI also records a digital publication date in 2012. Retain the cited print year. The author page confirms the subtitle, which the DOI's shorter title omits. A precise advice/circuit section locator should be checked before adding one to the article. |
| AllenderEtAl2006 | Eric Allender, Harry Buhrman, Michal Koucký, Dieter van Melkebeek, and Detlef Ronneburger, *Power from Random Strings*, SIAM Journal on Computing 35(6), 1467–1493 (2006); DOI `10.1137/050628994`; [author manuscript](https://people.cs.rutgers.edu/~allender/papers/KT.pdf) | The author manuscript is dated 17 October 2005. W02's Proposition 5, Definitions 8–10, and Theorem 11 locators refer to that author version. Do not relabel those locators as journal pages without checking the correspondence. |
| Bryant1986 | Randal E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE Transactions on Computers C-35(8), 677–691, August 1986; DOI `10.1109/TC.1986.1676819`; [author bibliography](https://www.cs.cmu.edu/~bryant/pubs.html) | The author bibliography and DOI agree on the journal metadata. The manuscript supplies its own residual argument; this check does not certify that every modern layered-model convention occurs verbatim in Bryant's paper. |
| BovaSlivovsky2017 | Simone Bova and Friedrich Slivovsky, *On Compiling Structured CNFs to OBDDs*, Theory of Computing Systems 61(2), 637–655 (2017); DOI `10.1007/s00224-016-9715-z`; [editorial article](https://link.springer.com/article/10.1007/s00224-016-9715-z) | Online publication was 26 October 2016; print volume/issue is 2017. Retain 2017 in the citation. The Bib entry records issue 2. Section 4/Theorem 19 is background for stronger expander-based examples, not a novelty claim for this project's grid example. |
| ChapmanWilliams2015 | Brynmor Chapman and Ryan Williams, *The Circuit-Input Game, Natural Proofs, and Testing Circuits With Data*, ITCS 2015, 263–270, ACM; DOI `10.1145/2688073.2688115`; [author PDF](https://people.csail.mit.edu/rrw/itcs-single-column.pdf) | The author PDF is dated 10 December 2014; the cited conference publication is 2015. Theorem 1.1 concerns properties useful against the specified SAT solvers; its solver/checking restriction must remain attached to the cited characterization. |
| OliveiraPichSanthanam2021 | Igor C. Oliveira, Ján Pich, and Rahul Santhanam, *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17, Article 11, 1–38 (2021); DOI `10.4086/toc.2021.v017a011`; [editorial article](https://theoryofcomputing.org/articles/v017a011/) | Published 30 November 2021. Theorem 1.4 is on printed page 6 of the editorial PDF. The publisher identifies Article 11; a DOI registry response with an empty title and `issue = 1` must not override this primary record. Both promise thresholds and all parameter quantifiers remain essential. |
| KabanetsKolokolova2026 | Valentine Kabanets and Antonina Kolokolova, *Kolmogorov's Approach to P vs. NP: Chain Rules for Time-Bounded Kolmogorov Complexity*, ECCC TR25-089, Revision 1, 13 March 2026; [report record](https://eccc.weizmann.ac.il/report/2025/089/) and [revision PDF](https://eccc.weizmann.ac.il/report/2025/089/revision/1/download) | The original report was posted 10 July 2025. Some report-page meta-tags retain the original title/date; the revision body and PDF identify the extended title and 2026 revision. Retain the additional stated NP-hardness hypothesis in the simplified equivalence with `P = NP`. |

The auxiliary [Allender–van Melkebeek clarification](https://people.cs.rutgers.edu/~allender/papers/clarification.pdf)
is an undated one-page primary note, not an eighth already registered Bib entry.
It requires counting input gates plus connections and addresses missing handling
of out-of-range positions. If the article directly relies on the clarification's
corrected statement, give it a suitable explicit citation rather than silently
attributing the correction to an unchanged original theorem. Do not invent a
publication year for the note.

The historical initial literature table lists six entries. The W06 dated
addendum supplies Bova–Slivovsky separately and retains the W02/W04 source audits;
the original check date is not used to imply that later claims were examined then.

## Novelty and mathematical review that remain open

The current evidence supports distinguishing project artifacts from new
mathematical results:

- T01/C01 and the elementary residual machinery are standard exposition.
- The grid argument is self-contained and new to this workspace, but it is not
  presented as a new lower-bound technique; the cited literature includes
  stronger all-order examples under specified CNF restrictions.
- W02 supplies useful explicit simulations under selected conventions. Their
  relationship to existing local-access and Kolmogorov conventions still needs
  independent mathematical scrutiny before any originality claim.
- L04, once integrated, needs its own comparison with established subfunction,
  neighborhood, and residual-count results before being described as original.
- Code, certificates, data, and Lean developments are reproducible project
  artifacts. Their existence does not by itself establish a novel theorem or
  a publishable contribution for a particular venue.

A full novelty assessment should compare exact statements, hypotheses, models,
parameters, and reductions with the relevant literature. An unsuccessful search
or a metadata check is not evidence of priority.

## W06 issue criteria

The original issue criteria remain authoritative. Preserve the unchecked states
below until the corresponding evidence or author decision exists.

- [ ] Identify the article contribution beyond the expository foundation.
- [ ] Complete a novelty and bibliography audit.
- [ ] Obtain independent mathematical review.
- [ ] Confirm authorship and AI-assistance disclosure.
- [ ] Select manuscript and code licenses.
- [ ] Select a venue before applying venue-specific formatting.

| Criterion | Preparation available | Why final closure is still pending |
| --- | --- | --- |
| Article contribution | Scope and artifact inventory; candidate expository/model-comparison positioning | The author must select the article's final contribution and intended audience. No new separation or theorem novelty is established. |
| Novelty and bibliography | Metadata check of the seven current references and version-sensitive source notes | The combined criterion also requires a substantive novelty/literature assessment and final exact-statement source verification. |
| Independent review | Agent audits and named formal verification evidence; a legacy draft review packet | No actual independent human reviewer report is recorded. |
| Authorship and disclosure | Existing author attribution and factual ChatGPT/Codex assistance statement | Submission-specific authorship, contributions, acknowledgments, and disclosure need author confirmation. |
| Licenses | `RIGHTS.md` records that no additional reuse license has been selected | Manuscript and software licensing are author decisions; public repository visibility does not select either license. |
| Venue | A possible scope can be evaluated | No journal, conference, preprint destination, or submission decision has been selected by this preparation. |

Technical integration, a green workflow, and release creation do not satisfy the
human-review, novelty, licensing, or venue decisions in this table.

## Historical independent review packet and PR 16

The legacy [draft PR #16](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/16)
was prepared against the older `19a33be` baseline with 16 registered entries.
Its existence is not an independent review, and no reviewer contact is claimed.
Keep that PR draft and preserve its history. A refreshed review packet should
target the actual final integrated commit after the new structural and formal
work, rather than imply that the older packet already covers it.

The refreshed package should include the exact manuscript/PDF, claim register,
W01/W02 conventions, graph/grid and any L04 statements, finite-verifier scope,
Lean correspondence and trusted-toolchain description, open findings, and a short
set of questions for the requested scope. Record reviewer identity, date,
independence, reviewed material, findings, and resolution only after a real
review. Drafting a package does not authorize contacting anyone.

## Decisions reserved to the author

| Decision | Current evidence | Required author action |
| --- | --- | --- |
| Article scope and claim strength | Expository framework and bounded extensions; Q01 remains open | Choose the intended contribution and approve its wording. |
| Authorship and contributions | Matías Donoso Quiroga is the recorded project author | Confirm final names, contributions, affiliations if any, and acknowledgments. Do not invent affiliations or endorsements. |
| AI assistance | Existing prose records ChatGPT/Codex drafting and code assistance | Confirm that the final disclosure accurately reflects the work and the selected venue's actual policy. AI systems are not listed as authors. |
| Text and code licensing | No additional reuse license is currently granted | Select any manuscript and software licenses separately, or explicitly retain the present status. This draft makes no selection. |
| Venue and submission | No submission authorization or venue decision is recorded | Decide whether to submit, where, and under which actual formatting and disclosure requirements. |
| Archival version and identifiers | Living citation metadata and automated working-draft releases exist | Approve a submission/archive snapshot if appropriate; record DOI/preprint identifiers only after assignment. |

## Final technical and editorial gates

Before presenting a submission-ready snapshot, retain evidence from one exact
source commit:

1. Confirm that intended changes are integrated and that all source links,
   statement labels, dependencies, and evidence fields match that commit.
2. Run `make verify` with the pinned Lean toolchain from a clean checkout;
   retain the actual commands, versions, logs, and complete formal axiom report.
3. Verify deterministic data and any integrated certificate artifacts. State the
   finite domain and verifier's mathematical scope explicitly.
4. Inspect the final rendered PDF, especially pages changed by new statements or
   verification prose, and record its digest and page count.
5. Resolve blocking proof/review findings, while preserving explicit open targets
   and unresolved comparison or transfer directions.
6. Complete actual independent human review and author decisions before recording
   those checklist items as complete.
7. Archive sources, bibliography, data, formal sources, toolchain notes, logs,
   and the matching PDF. Automatic manuscript releases continue to be working
   drafts unless the author approves a different scholarly snapshot.

This preparation delivers an inventory, bounded bibliographic checks, pinned
technical evidence and the remaining decision list. Issue #8 stays open.
A submission or license change is a separate author-controlled action.
