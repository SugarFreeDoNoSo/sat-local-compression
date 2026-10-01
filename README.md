# Local Descriptions of SAT Truth Tables

An English-language mathematical research workspace for studying the trade-off
between description length and exact local evaluation time for SAT truth tables.

**Status: working draft v0.1.0.** The initial manuscript is expository.
It does not prove P != NP or a new general circuit lower bound.
Independent mathematical review is pending.

## Start here

- [Manuscript source](paper/main.tex) and [paper guide](paper/README.md).
- [Claim register](research/claims.json): status, dependencies, and scope.
- [Research plan](docs/research-plan.md) and [backlog](research/backlog.json).
- [Literature notes](docs/literature.md).
- [Contribution rules](CONTRIBUTING.md) and [review checklist](docs/review-checklist.md).
- [Publication plan](PUBLICATION.md) and [citation metadata](CITATION.cff).
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
and an ordered decision-diagram example. No novelty is claimed for these results.

## Reproduce

Requirements: Python 3.11 or later, Make, latexmk, pdfLaTeX, BibTeX, and the
LaTeX packages listed in [toolchain notes](docs/toolchain.md).
No third-party Python packages are required.

On Ubuntu/Debian:

```sh
sudo apt-get install latexmk texlive-latex-extra texlive-fonts-recommended lmodern
```

From the repository root:

```sh
make check       # experiments, tests, claim/reference integrity
make pdf         # build/paper/main.pdf
make verify      # checks + paper build + LaTeX warning gate
make experiments # regenerate the committed finite tables
```

GitHub Actions runs the checks and builds a downloadable PDF artifact on
pushes and pull requests. After both jobs succeed on `main`, it also publishes
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
by OpenAI ChatGPT/Codex. No venue, affiliation, DOI, or independent verification
is claimed. Public hosting and scholarly submission are separate steps.

No additional reuse license has been selected yet. See [RIGHTS.md](RIGHTS.md).
The author can choose manuscript and software licenses before a tagged release.
