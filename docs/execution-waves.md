# Execution waves and GitHub tracking

Execution started on 2026-10-19 at the author's request.
Coordination: [roadmap issue #9](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/9).
Detailed scope and budgets: [roadmap.md](roadmap.md).

## Live tracking

GitHub issues retain their original mathematical acceptance criteria. Milestones
and labels organize execution; they do not certify a proof or independent review.
The repository [milestone view](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestones)
and [roadmap issue](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/9)
are the current working tracking views.

| Wave | Work package | Issue | Milestone | Activation and exit gate |
| --- | --- | --- | --- | --- |
| 00 | M00 baseline and coordination | [#10](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/10) | [1](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/1) | Started: publish roadmap, verify baseline, and record remote evidence and maintenance limits. |
| 01 | W01 evaluator/advice audit | [#3](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/3) | [2](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/2) | Started: technical dossier in a separate focused PR. Final closure still requires actual independent human review. |
| 02 | W02 KT/circuit comparison | [#4](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/4) | [3](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/3) | Next after W01 technical conventions stabilize; every simulation keeps its hypotheses and overhead. |
| 03 | W03 restricted-model result | [#5](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/5) | [4](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/4) | Scoped model/family selection, then a proof, counterexample, or budgeted obstruction report. |
| 04 | W05 formal L02 | [#7](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/7) | [5](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/5) | Implementation: pinned Lean proof of both directions, boundary layers, correspondence, and axiom audit. See [formal guide](../formal/README.md); live issue records PR and CI evidence. |
| 05 | W04 Gap-MCSP applicability | [#6](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/6) | [6](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/6) | [Applicability report](w04-transfer-audit.md): exact promise, resource contract, and failed grid-table candidate. No successful transfer is established. |
| 06 | W06 contribution/publication | [#8](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/8) | [7](https://github.com/SugarFreeDoNoSo/sat-local-compression/milestone/7) | [Preparation dossier](w06-publication-preparation.md): contribution inventory and bounded bibliography check. Closure still requires independent review and author decisions. |

Milestone numbers identify repository objects; wave numbers identify execution
order. W04 and W05 keep their original work-package IDs even though formalization
can start before a transfer investigation.

## Started work

Wave 00 records the reproducible baseline and corrects the historical validation
record through a dated addendum. See [wave-00-baseline.md](wave-00-baseline.md) and
[validation.md](validation.md). The roadmap/baseline work and W01 audit are prepared
as separate branches and PRs. Current PR links and verification outcomes belong
in the live tracking issue, so this document does not depend on a fixed PR number.

Dependency PRs #1 and #2 remain separate maintenance proposals. Their historical
CI and static compatibility review do not establish a new integration run against
the current main branch. They are not merged as part of the roadmap publication.

## Native GitHub Projects board: permission limitation

The active GitHub connection successfully manages this repository's issues,
milestones, branches, and PRs. However, GitHub rejected native Projects operations:

- Listing account projects: `Resource not accessible by integration`.
- Creating the requested board: `Resource not accessible by integration (createProjectV2)`.

No native Projects board was created. The working tracking view above is a
repository-scoped substitute. Account-level Projects write access is distinct
from repository write/admin permissions. Completing the board requires a GitHub
connection authorized for the account's Projects. Credentials should remain in
the supported connection/CLI authentication flow; do not put tokens in issues,
files, or chat.

When that access is available, inspect existing projects first to avoid duplicates,
then create or reuse **SAT Local Compression — Research Roadmap**, link this
repository, and add issues #3–#10 and the wave PRs. Preserve the issues and their
history rather than creating duplicate work items.

Suggested fields:

| Field | Values or purpose |
| --- | --- |
| Status | Todo, In progress, In review, Done |
| Wave | 00, 01, 02, 03, 04, 05, 06 |
| Work package | M00, W01, W02, W03, W05, W04, W06, Coordination |
| Review gate | Planned, Technical review, Human review pending, Conditional, Accepted |
| Evidence | PR, audit, proof, counterexample, or verification URL |

Suggested views: board by Status; table grouped by Wave; a review view filtered
to Human review pending; and a conditional-work view. Populate status from the
actual issue/PR evidence, with W01 still awaiting independent human review after
its technical audit. Project status is execution metadata, not a claim-register
proof status. Board visibility should be an explicit author choice.

## Handoff between waves

1. Link the focused PR and its exact verification evidence to the work issue.
2. Record the delivered scope and any missing criterion; preserve human-review
   requirements and unresolved proof directions.
3. Resolve foundational gaps before promoting dependent assertions.
4. Start the next applicable wave with one concrete question and a bounded
   exploration budget. A failed approach is recorded, not hidden.
5. Keep review/merge decisions and external human availability separate from
   technical execution. No unattended future execution is implied by the queue.

The first six-week cycle remains a planning assumption at 8–10 hours per week,
not a guarantee of a new theorem or a review response date.
