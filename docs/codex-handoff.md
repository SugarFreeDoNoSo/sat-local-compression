# Codex research handoff

## Project and scope

Author: Matias Donoso Quiroga. Repository: `SugarFreeDoNoSo/sat-local-compression`.
Write all repository content, code, issues, and manuscript prose in English.
The initial working draft v0.1.0 is expository. It does not establish
`P != NP`, `SAT not in P/poly`, or a new general circuit lower bound.
Independent mathematical review is pending.

The project studies exact local descriptions of SAT truth tables. The query
length is `n`; the full table length is `N = 2^n`. A description may depend on
`n`, but it must answer every query of that length. Construction time is
excluded; interpretation and description-access costs are included.

Polynomial description length with polynomial local query time characterizes
`P/poly`, under the evaluator assumptions stated in the manuscript. This is
a standard equivalence explained here without claiming novelty. The general
SAT lower bound remains an open target. The grouped-order unit-clause
decision-diagram example is a restricted-model result: interleaving makes
that example easy. Finite experiments check implementation consistency;
they are not proofs of asymptotic bounds.

## Read first

1. `AGENTS.md` and `README.md`.
2. `research/claims.json` and `research/backlog.json`.
3. `docs/research-plan.md` and `docs/literature.md`.
4. The manuscript sections associated with the chosen claim.

## First useful task

Start with backlog item W01, auditing the evaluator model and advice
equivalence. Check efficient universality, charged access costs, input-length
advice, headers, constants, and finite exceptions. Record any gap explicitly
and propose a focused correction with its proof dependencies. An agent audit
does not satisfy the requirement for independent human mathematical review.

Then consider W02, comparing this local description measure with established
KT conventions while tracking both query and table lengths. Retain every
hypothesis in cited results and distinguish KT, Kt, and time-bounded K.

Use one coherent mathematical claim per branch and pull request. Run
`make verify` after changes affecting the manuscript or experiments, and
inspect the rendered PDF after substantial layout changes.

## Human decisions

Independent review, authorship changes, publication licensing, venue
selection, and scholarly submission remain human decisions. Public GitHub
hosting does not imply journal submission or independent verification.

## Session continuity

This file transfers project context to a new Codex chat or CLI session. It
does not import the complete parent conversation or authenticate the CLI.
Start a session in a clone of this repository and ask it to read this file
before continuing the selected backlog item.
