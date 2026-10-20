# Initial validation record

Date: September 30, 2026. Scope: working draft v0.1.0.

## Completed locally

- `make verify` passed: four unit tests, 13 registered claims, six bibliography
  entries, acyclic claim dependencies, matching references, and generated-data
  consistency.
- The exhaustive data table was reproduced for 1 <= m <= 7. The tests also
  compare the incidence predicate with an independent exhaustive unit-clause
  verifier for 1 <= m <= 4.
- pdfLaTeX and BibTeX produced a seven-page A4 PDF. Poppler parsed the PDF and
  rendered all pages; the pages were visually inspected for clipping and
  legibility. The final log has no undefined references, missing characters,
  or overfull boxes.
- An incomplete initial PDF was discarded and rebuilt. The build now checks
  for a complete PDF end marker, and the log gate requires an output record.
- The citation and GitHub configuration files were parsed as YAML.

Toolchain: Python 3.12.14; latexmk 4.83; pdfTeX 1.40.25
(TeX Live 2023/Debian). YAML parsing used PyYAML for this local inspection;
it is not a project runtime dependency.

## Pending

- Public GitHub repository creation and the first remote Actions run.
- Independent human review of the mathematical statements and proofs.
- Proof-assistant verification, a novelty audit for any future original
  result, and author decisions on submission and reuse licenses.

Automated checks establish artifact consistency and finite observations.
They do not certify the proofs or resolve the open lower-bound target.

## October 19, 2026 addendum: wave 00 baseline

The September 30 record above is preserved as history. Its pending repository
creation and first remote Actions run have since been completed. This addendum
records evidence inspected on October 19, 2026, rather than changing the meaning
of the earlier record.

- Remote `main` and local `HEAD` resolved to
  [`d6417b7fb5281b9230e1e68fa2e2ae9cdbfbe873`](https://github.com/SugarFreeDoNoSo/sat-local-compression/commit/d6417b7fb5281b9230e1e68fa2e2ae9cdbfbe873).
- `make verify` passed locally: four tests, 13 claims, six bibliography entries,
  finite data for `1 <= m <= 7`, PDF completeness, and the LaTeX log gate.
  Poppler reported seven A4 pages. No new rendered-page visual inspection was
  performed as part of this baseline check.
- Observed local toolchain: Python 3.12.14; latexmk 4.86; pdfTeX 1.40.26 and
  BibTeX 0.99d (TeX Live 2025/dev/Debian); Poppler 26.05.0; Git 2.52.0;
  GNU Make 4.4.1. These are the current local versions, distinct from the
  historical toolchain above.
- Existing [main run 36796203830](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/36796203830)
  completed research checks, the manuscript build, and PDF publication
  successfully on October 1, 2026. This was inspected, not newly triggered.
- The [Manuscript d6417b7 release](https://github.com/SugarFreeDoNoSo/sat-local-compression/releases/tag/manuscript-d6417b7fb5281b9230e1e68fa2e2ae9cdbfbe873)
  lists `main.pdf` and explicitly identifies it as a working draft pending
  independent mathematical review.
- Dependency PRs [#1](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/1)
  and [#2](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/2) remain
  open and unmerged. Their September 30 CI runs passed, but predate the release
  job. No new integration run or automatic merge was performed by this audit.
- Research issues #3 through #8 remain open at the recorded snapshot. No
  independent human review, proof-assistant verification, or original
  lower-bound result is certified by these technical checks.

See [wave-00-baseline.md](wave-00-baseline.md) for the exact source and PR SHAs,
CI links, dependency compatibility review, local artifact digest, and scope.
