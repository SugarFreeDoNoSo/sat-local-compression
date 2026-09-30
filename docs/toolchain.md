# Toolchain

- Python 3.11 or later; standard library only.
- Make, latexmk, pdfLaTeX, BibTeX.
- LaTeX: fontenc, inputenc, lmodern, geometry, amsmath, amssymb, amsthm,
  microtype, booktabs, enumitem, xurl, hyperref.
- Optional PDF inspection: Poppler pdfinfo and pdftoppm.

CI uses Ubuntu 24.04. Actions are pinned to verified commit hashes.
TeX packages come from the runner's distribution repositories; mirrors are
not frozen, so byte-identical PDFs across future toolchains are not promised.
The mathematical CSV and LaTeX table are exact and deterministic.

Run make verify for every required local gate. Record exact Python and TeX
versions for a publication release. Retain its build logs as artifacts.
A passing CI run is not a proof certificate.
