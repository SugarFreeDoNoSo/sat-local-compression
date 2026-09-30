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
