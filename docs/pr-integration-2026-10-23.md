# Gated technical integration and review-packet refresh — 2026-10-23

## Accepted technical source

The technical review snapshot is existing main commit [`82a3af3844fdc11690f7ccf47d2d7fc259246ee0`](https://github.com/SugarFreeDoNoSo/sat-local-compression/tree/82a3af3844fdc11690f7ccf47d2d7fc259246ee0).
The author's later authorization covered gated integration of PRs #20, #21,
#22 and the refreshed review request #16. It superseded their earlier draft-only
integration instructions, not the independent-human-review or publication gates.
Original PR heads and history were preserved through merge commits; no branch
was force-pushed and no unrelated research extension was added.

| PR | Final reviewed head | Verified merge commit | Exact-head successful CI |
| --- | --- | --- | --- |
| [#20](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/20) | `34d1c2d369fb378e45ede45603755dd12ef78f4d` | `4211c587b1faf2d486da77d2e13e92514c2d637f` | [40013696403](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/40013696403) |
| [#21](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/21) | `52babeb15687e3f536861adf7b3497b25852615f` | `0c66c047b49f9336fc870b2166470e2220dd5084` | [40014207718](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/40014207718) |
| [#22](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/22) | `719737bd30231afb973bab94b67759132cb39d28` | `82a3af3844fdc11690f7ccf47d2d7fc259246ee0` | [40014762774](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/40014762774) |

Each final technical tree received a separate read-only Astra Ultra agent review.
The review checked the relevant proofs, code, scope and integration delta, rather
than treating CI as a mathematical correctness certificate. The final PR22 tree
also passed an independent isolated full verification. Agent review is not
independent human mathematical review.

## Integrated inventory and limits

- **17 registered claims:** L04 is now included; Q01 remains open and R02 conditional.
- **L04:** exact residual signatures for finite simple loopless graph-selector
  predicates, including empty/full cuts and zero vertices. No novelty claimed.
- **L03 certificates:** six committed finite whole-graph induced-matching
  certificates, independent validation and distinguishing assignments. Each
  certificate concerns its given graph and cut, not an asymptotic proof.
- **Formal scope:** L02 and P03 only; 27 theorem axiom closures audited with pinned
  Lean 4.35.0. P03 covers exact grouped midpoint width for every natural m,
  including zero. P04, L03/P05, L04, T01 and Q01 are not thereby formalized.
- **Technical verification:** 33 tests, metadata, deterministic tables and
  certificates, pinned Lean proof/audit, nine-page PDF and clean TeX log.
  Changed proof/scope pages were visually inspected. The signature tests cover
  all 33,867 graph/cut pairs through five vertices; finite tests are not proofs
  of the arbitrary-size theorem.
- **No transfer:** the selector-width results do not supply a width-preserving
  encoding map, general-circuit lower bound or missing Gap-MCSP reduction.

## Post-merge baseline evidence

Main CI [40015064494](https://github.com/SugarFreeDoNoSo/sat-local-compression/actions/runs/40015064494)
completed successfully at the exact accepted source SHA above, including the
existing working-draft Release job. The actual
[commit-pinned PDF asset](https://github.com/SugarFreeDoNoSo/sat-local-compression/releases/download/manuscript-82a3af3844fdc11690f7ccf47d2d7fc259246ee0/main.pdf)
was downloaded on 2026-10-23: 357,617 bytes, nine A4 pages, SHA256
`5de4635c8942dd4b88049914bed01da85055a7be017887fb330f32c2a981dafb`.
Its bytes matched GitHub asset 670228851's reported SHA256. This identifies
that working-draft artifact; it is not a scholarly submission or endorsement.
Release assets can be replaced by reruns, so verify the recorded digest rather
than trusting only a stable-looking URL. The packet itself does not manufacture
an existing-PDF assertion from its source SHA.

## Refreshed review request

[PR16](https://github.com/SugarFreeDoNoSo/sat-local-compression/pull/16) preserves its original history and corrected L01 counting
direction: each time-valid description determines at most one total answer table;
multiple descriptions may determine the same table.

The [manifest](../research/review-packet.json) pins **48 technical source files**
to the accepted source commit above and covers all **17 claims in seven units**.
Before regeneration, every working-tree fingerprint was compared byte-for-byte
with `git show <source_revision>:<path>`. The packet checker, its tests, this
integration record, and the publication-refresh prose are deliberately excluded
from the technical snapshot: they were added after that source baseline.
`make check` validates local consistency; it still does not authenticate Git
history, verify a reviewer identity, or infer an existing Release/PDF from a SHA.
The [generated packet](independent-review-packet.md) supplies reproduction commands
rather than an unverified release link.

The packet branch adds regression checks for technical scope, nonrecursive
fingerprints, L04 coverage, correct P03 formal-evidence labels, preserved L01
wording, and absence of inferred release identities. Its final head and CI
belong to PR16 and are distinct from the pinned technical source revision.

Human review, novelty assessment, contribution selection, authorship, licensing,
venue and submission decisions remain open under [PUBLICATION.md](../PUBLICATION.md).
No reviewer outreach or scholarly submission was performed by this integration.
