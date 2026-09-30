# Primary-source reading notes

Checked on 2026-09-29. Original statements and proofs remain authoritative.

| BibTeX key | Primary source | Scope |
| --- | --- | --- |
| AroraBarak2009 | [Author-hosted materials](https://theory.cs.princeton.edu/complexity/) | Advice and circuit conventions |
| AllenderEtAl2006 | [Power from Random Strings](https://doi.org/10.1137/050628994) | Resource-bounded descriptions and circuit connections |
| Bryant1986 | [Author publication list](https://www.cs.cmu.edu/~bryant/pubs.html) | Ordered decision-diagram background |
| ChapmanWilliams2015 | [Author manuscript](https://people.csail.mit.edu/rrw/itcs-single-column.pdf) | Theorem 1.1: specialized properties for SAT solvers |
| OliveiraPichSanthanam2021 | [Published article](https://theoryofcomputing.org/articles/v017a011/) | Theorem 1.4: Gap-MCSP magnification |
| KabanetsKolokolova2026 | [ECCC revision 1](https://eccc.weizmann.ac.il/report/2025/089/) | Conditional chain-rule characterizations |

Parameter checkpoints:

- Chapman-Williams requires specialized solver/checking behavior.
- Oliveira-Pich-Santhanam uses full-table length N, general circuits, and every
  sufficiently small constant beta. Retain both promise thresholds.
- Kabanets-Kolokolova's direct equivalence with P = NP additionally assumes the
  stated NP-hardness hypothesis; retain time slack and sublinear error.

[Allender and van Melkebeek's clarification](https://people.cs.rutgers.edu/~allender/papers/clarification.pdf)
is relevant to the circuit-size conventions in W02. No exact local-L/KT
identity is asserted in the present draft.
