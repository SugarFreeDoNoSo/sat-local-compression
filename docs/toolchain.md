# Toolchain

- Python 3.11 or later; standard library only.
- Make, latexmk, pdfLaTeX, BibTeX.
- LaTeX: fontenc, inputenc, lmodern, geometry, amsmath, amssymb, amsthm,
  microtype, booktabs, enumitem, xurl, hyperref.
- Optional PDF inspection: Poppler pdfinfo and pdftoppm.
- Formal L02 proof: Lean 4.35.0, commit
  `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`, bundled `Std` only.
  Linux x86_64 setup uses Python and `zstd`; archive SHA256 is pinned.
  See [formal setup and correspondence](../formal/README.md).

CI uses Ubuntu 24.04. Actions are pinned to verified commit hashes.
TeX packages come from the runner's distribution repositories; mirrors are
not frozen, so byte-identical PDFs across future toolchains are not promised.
The mathematical CSV and LaTeX table are exact and deterministic.

Run make verify for every required local gate. Record exact Python and TeX
versions for a publication release. Retain its build logs as artifacts.
The formal job kernel-checks the named L02 theorems and audits their axiom
dependencies. Passing the research or manuscript jobs does not verify proofs.
Neither CI nor the L02 proof substitutes for independent human review.
