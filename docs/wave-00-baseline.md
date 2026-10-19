# Wave 00: reproducibility and repository baseline

Observed on October 19, 2026, at approximately 22:55 UTC. This is a dated
snapshot; later work should append new evidence rather than reinterpret this
record as a current status dashboard.

## Source and scope

- Repository: [SugarFreeDoNoSo/sat-local-compression](https://github.com/SugarFreeDoNoSo/sat-local-compression).
- Remote `main` and local `HEAD` both resolved to
  [`d6417b7fb5281b9230e1e68fa2e2ae9cdbfbe873`](https://github.com/SugarFreeDoNoSo/sat-local-compression/commit/d6417b7fb5281b9230e1e68fa2e2ae9cdbfbe873),
  dated October 1, 2026: “Publish validated manuscript PDFs as GitHub Releases.”
- This audit read GitHub metadata, diffs, workflow results, and upstream action
  definitions. It made no remote changes and did not merge the dependency PRs.
- Local verification used the baseline manuscript, scripts, tests, research
  metadata, data, and workflow files. Concurrent documentation work was present
  in the working tree. No tracked changes in those verification inputs were
  present when the baseline check was recorded.

## Local verification

`make verify` exited successfully on October 19, 2026. Its observed gates were:

| Gate | Observed result |
| --- | --- |
| Unit tests | Four tests passed, including comparison with an independent exhaustive unit-clause verifier for `1 <= m <= 4`. |
| Research consistency | 13 registered claims and six bibliography entries; metadata and reference checks passed. |
| Generated finite data | Checked-in outputs matched the experiment for `1 <= m <= 7`. |
| Manuscript artifact | `build/paper/main.pdf` passed the build script's PDF completeness check. Poppler reported seven A4 pages. |
| LaTeX log | No unresolved references, overfull boxes, or missing characters were reported by the log gate. |

The commands used were `make verify`, `python3 --version`, `latexmk -v`,
`pdflatex --version`, `bibtex --version`, `pdfinfo -v`, `git --version`,
`make --version`, `pdfinfo build/paper/main.pdf`, and
`sha256sum build/paper/main.pdf`.

| Local tool | Observed version |
| --- | --- |
| Python | 3.12.14 |
| latexmk | 4.86 |
| pdfTeX | 1.40.26, TeX Live 2025/dev/Debian |
| BibTeX | 0.99d, TeX Live 2025/dev/Debian |
| Poppler `pdfinfo` | 26.05.0 |
| Git | 2.52.0 |
| GNU Make | 4.4.1 |

The validated local PDF had 312,632 bytes and SHA256
`c57a41a650a9d8f5e2ca8d46599bb674f1ef5825aeea1da5bc7e1b56a3260d5d`.
This identifies the observed local artifact, not a reproducible-byte guarantee
or a match with the remote release asset. The run did not include a new visual
inspection of rendered pages. The historical visual inspection remains recorded
separately in [validation.md](validation.md).

## Existing remote CI and release evidence

The repository and remote CI now exist. The pending repository-creation and
first-remote-run items in the September 30 validation record are historical.

| Ref and event | Recorded run | Observed result |
| --- | --- | --- |
| `main`, push at `d6417b7` | [36796203830](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/36796203830), October 1, 2026 | `Research and finite experiments`, `Build manuscript`, and `Publish manuscript PDF` all completed successfully. |
| PR #1, `pull_request` at `5d6d9ee2e431adabd650b1dc4174696695815294` | [36747046262](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/36747046262), September 30, 2026 | Both research checks and manuscript jobs completed successfully. |
| PR #2, `pull_request` at `5f562e82d192ca259ed37517c446e91915382c12` | [36747058669](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/36747058669), September 30, 2026 | Both research checks and manuscript jobs completed successfully. |

These are existing remote runs inspected during this audit, not newly triggered
runs for the wave documents. The PR runs predate the October 1 release job.

The public [Manuscript d6417b7 release](https://github.com/SugarFreeDoNoSo/sat-local-compression/releases/tag/manuscript-d6417b7fb5281b9230e1e68fa2e2ae9cdbfbe873)
was published on October 1, 2026, at 00:28:07 UTC and lists a 312,625-byte
`main.pdf` asset. Its note explicitly states: “Working draft; independent
mathematical review is pending.” The release listing and successful publication
job were inspected; the remote PDF bytes were not downloaded or compared in
this wave.

## Dependency PR review

Both PRs were open, unmerged, and reported `mergeable: true` with
`mergeable_state: clean` by GitHub at the snapshot time. Each changes only
`.github/workflows/research.yml`. Their reported base SHA was
`ad16befd32d68e77cc7d8b20badf83719a032d8a`.

- [PR #1](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/1)
  changes the upload action pin from
  `b7c566a772e6b6bfb58ed0dc250532a479d7789f` (v6) to
  `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` (v7.0.1), one added and one
  removed line. The pinned upstream
  [action definition](https://github.com/actions/upload-artifact/blob/043fb46d1a93c77aae656e7c1c64a875d1fc6a0a/action.yml)
  uses Node 24 and retains the workflow's `name`, `path`, `if-no-files-found`,
  and `retention-days` inputs. Its new `archive` input defaults to `true`,
  preserving the workflow's named, multi-file archive behavior. The PR's
  historical artifact-upload step succeeded.
- [PR #2](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/2)
  changes both checkout pins from
  `d23441a48e516b6c34aea4fa41551a30e30af803` (v6) to
  `3d3c42e5aac5ba805825da76410c181273ba90b1` (v7.0.1), two added and two
  removed lines. The pinned upstream
  [action definition](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml)
  uses Node 24 and retains `persist-credentials`; the workflow sets it to
  `false`. The documented v7 change concerning fork checkouts under
  `pull_request_target` or `workflow_run` does not apply to the current
  `push`, `pull_request`, and `workflow_dispatch` triggers. Both checkout
  steps succeeded in the recorded PR run on `ubuntu-24.04`.

This static review and historical execution support compatibility with the
observed workflow usage. Integration with the current `main`, the combined
dependency updates, and the later release job has not been freshly exercised.
Keep the dependency PRs pending for a separate maintenance decision and current
CI evidence; no automatic merge was performed by this audit.

## Research backlog at the snapshot

All six research issues were open, with zero comments and unchecked acceptance
criteria in their bodies. Their existence records planned work, not completion.

| Issue | Remaining deliverable |
| --- | --- |
| [#3 / W01](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/3) | Audit evaluator universality, charged access, length-only advice, headers, constants, and finite exceptions; obtain an actual independent human review. |
| [#4 / W02](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/4) | Compare local description length with precise KT conventions, machine models, circuit accounting, and primary statements. |
| [#5 / W03](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/5) | Select a restricted model and explicit family; prove a bound robust under the allowed representation choices or record a counterexample. |
| [#6 / W04](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/6) | Establish or explicitly identify the missing reduction to the precise Gap-MCSP theorem, with both thresholds, all quantifiers, and resource overheads. |
| [#7 / W05](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/7) | Formalize L02 in a chosen proof assistant with a pinned verification command. |
| [#8 / W06](https://github.com/SugarFreeDoNoSo/sat-local-compression/issues/8) | Define contribution and novelty, complete independent review, and record author decisions on authorship, disclosure, licensing, and submission. |

Wave 00 establishes a working technical baseline and corrects stale repository
status through dated evidence. Automated consistency checks, finite examples,
successful CI, and a published PDF do not certify the mathematical proofs,
establish novelty, or resolve the open lower-bound target. Independent review,
proof-assistant verification, and any original research result remain separate
deliverables.
