# Contributing

Contributions may strengthen a model, repair a proof, test an example,
document a failed approach, or add a precisely scoped result.

## Mathematical changes

1. Open an issue stating the problem and proposed claim.
2. Identify input size, model, uniformity, parameters, and hypotheses.
3. Add or update the stable entry in research/claims.json.
4. Supply a proof, precise source reference, or explicit open status.
5. Check small cases and counterexamples where useful.
6. Run make verify and inspect the PDF.
7. Submit a focused pull request using the review checklist.

Review the hardest implication and its dependencies, not just the conclusion.
A citation must support the exact statement under the same assumptions.
Definition changes require rechecking dependent claims.

## Evidence categories

- **Expository-proved:** a self-contained proof of a standard or elementary
  consequence; not an originality claim or a formal verification certificate.
- **Conditional-literature:** an external result retaining its assumptions.
- **Open:** an unproved conjecture or research target.
- **Finite-experiment:** deterministic checks over a stated finite domain.

A stronger status needs an explicit reason and review. CI checks metadata,
code, finite examples, and typesetting, not arbitrary proof correctness.

## Reproducibility

Record representation, range, algorithm, resource scale, and exact commands.
Commit small derived tables and validate them with the experiment's --check mode.
Do not commit temporary build output or copies of third-party papers.

## Review and releases

An author is not their own independent reviewer. Use human review before a
scholarly submission. Maintain CHANGELOG.md and PUBLICATION.md.
Archive sources, bibliography, data, toolchain notes, and PDF from one commit.
Publication licensing is an author decision described in RIGHTS.md.
