# Local Descriptions of SAT Truth Tables

An English-language mathematical research workspace for studying the trade-off
between description length and exact local evaluation time for SAT truth tables.

**Status: working draft v0.1.1.** The manuscript is expository.
It does not prove P != NP or a new general circuit lower bound.
Independent mathematical review is pending.

## Start here

- [Manuscript source](paper/main.tex) and [paper guide](paper/README.md).
- [Claim register](research/claims.json): status, dependencies, and scope.
- [Research plan](docs/research-plan.md) and [backlog](research/backlog.json).
- [Execution waves](docs/execution-waves.md), [detailed roadmap](docs/roadmap.md),
  and [live tracking issue](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/9).
- [Literature notes](docs/literature.md).
- [Gap-MCSP applicability audit](docs/w04-transfer-audit.md): exact promises,
  reduction direction, resource accounting, and the missing transfer.
- [Lean formalization of L02](formal/README.md): minimum layered width equals
  the number of distinct residuals, with one diagram attaining all cuts.
- [Contribution rules](CONTRIBUTING.md) and [review checklist](docs/review-checklist.md).
- [Publication plan](PUBLICATION.md) and [citation metadata](CITATION.cff).
- [Publication preparation](docs/w06-publication-preparation.md): contribution
  scope, source/version checks and remaining review and author decisions.
- [Initial validation record](docs/validation.md).
- [Codex research handoff](docs/codex-handoff.md).

The main definition is

$$
L^U_t(T_n)=\min\{|d|:\ \forall x\in\{0,1\}^n,\
U(d,x)=T_n[x]\text{ within }t(n)\text{ steps}\}.
$$

Here n is the query length; the full table has N = 2^n bits.
A description may depend on n but must answer every query of that length.
Its construction cost is excluded. Interpretation and access costs are included.

The initial paper gives self-contained expository proofs of the standard
equivalence between polynomial descriptions with polynomial query time and
polynomial advice. It also contains counting and self-reduction observations
and ordered decision-diagram examples. An explicit grid-incidence SAT family has
layered width at least 2^(r/64) for every order of its r^2 selector bits, for
even r >= 2, while its general circuit size remains linear. This is an
expository result in a specified representation, with no claimed transfer to
general SAT circuits or novelty.

The graph experiment finds an optimal order exactly using a subset dynamic
program. Its finite data cover five named graphs with at most nine selector
bits. See [the graph data guide](data/README.md) and
[the W03 scope and verification note](docs/w03-restricted-model.md).

## Reproduce

Requirements: Python 3.11 or later, Make, latexmk, pdfLaTeX, BibTeX, and the
LaTeX packages listed in [toolchain notes](docs/toolchain.md).
No third-party Python packages are required.
The full verification also requires pinned Lean 4.35.0 (bundled `Std`, no
Mathlib); [formal setup and theorem correspondence](formal/README.md).

On Ubuntu/Debian:

```sh
sudo apt-get install latexmk texlive-latex-extra texlive-fonts-recommended lmodern
sudo apt-get install zstd
python3 scripts/setup_lean.py
```

From the repository root:

```sh
make check       # experiments, tests, claim/reference integrity
make pdf         # build/paper/main.pdf
make formal LAKE="$PWD/build/lean/lean-4.35.0-linux/bin/lake"
make verify LAKE="$PWD/build/lean/lean-4.35.0-linux/bin/lake" # all gates
make experiments # regenerate the committed finite tables
```

GitHub Actions runs research checks, verifies L02 in Lean, and builds a
downloadable PDF artifact on pushes and pull requests. After all three jobs
succeed on `main`, it also publishes
`main.pdf` in a [GitHub Release](https://github.com/SugarFreeDoNoSo/sat-local-compression/releases)
with a `manuscript-<commit SHA>` tag. Manual runs on `main` publish a Release
as well; rerunning the same commit replaces its PDF asset. Release assets are
not subject to the 30-day Actions artifact retention period.
A successful local build is not evidence that remote CI has run.

## Layout

| Directory | Purpose |
| --- | --- |
| paper/ | LaTeX manuscript and BibTeX sources |
| research/ | Claim register and initial issue backlog |
| docs/ | Research, review, literature, and toolchain notes |
| experiments/ | Exact finite residual-function experiments |
| formal/ | Pinned Lean proof and manuscript correspondence for L02 |
| tests/ | Independent finite consistency checks |
| data/ | Reproducible CSV and LaTeX table |
| scripts/ | Metadata and build-log validation |
| .github/ | CI and review/issue templates |

## Working method

Use an issue for each proposed statement, proof gap, or experiment.
Change one coherent claim per branch. Pull requests identify the model,
assumptions, dependencies, and evidence. Keep conjectures labeled as conjectures
until a complete proof is reviewed. Finite tests do not establish asymptotic
lower bounds. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Authorship and publication

Project author: Matías Donoso Quiroga. Initial drafting and code were assisted
by OpenAI ChatGPT/Codex. L02 has a Lean formalization; independent human review
is pending. No venue, affiliation, or DOI is claimed. Public hosting and
scholarly submission are separate steps.

No additional reuse license has been selected yet. See [RIGHTS.md](RIGHTS.md).
The author can choose manuscript and software licenses before a tagged release.
