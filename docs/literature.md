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

## W02 source audit — October 20, 2026

The W02 comparison checks the following primary author files. Page numbers in
this paragraph refer to the author manuscript, not to verified journal layout.

- [Power from Random Strings, author PDF](https://people.cs.rutgers.edu/~allender/papers/KT.pdf),
  dated October 17, 2005: Proposition 5 and Definition 6 (pp. 7–8),
  Definitions 8–10 (pp. 8–9), and Theorem 11 (p. 10).
  SHA256: `71343970c18cc01db2eaa6f603d4c47de669e19935650dd798a13777252ffba8`.
- [A Comment Regarding KT and Circuit Size](https://people.cs.rutgers.edu/~allender/papers/clarification.pdf),
  p. 1; no publication date is printed on this note.
  SHA256: `5af94af02de9c7a1ec119cfba0a7fb57a50385228101c49d8381db010a937186`.

The source definitions use indexed symbol-distinguishing acceptance, including
the end position, and random access to finite description/condition oracles.
Its Definition 9 is an indexed fixed-budget K^t convention; a whole-output
K^t convention must be distinguished explicitly. Proposition 5 specifies
efficient simulation overhead, rather than computability alone.

The clarification requires circuit size to count input gates plus connections
and acknowledges missing treatment of out-of-range positions in the earlier
proof discussion. A gate-only comparison or an exact local-L/KT identity is
not justified by those sources. The publisher PDF returned HTTP 403 during
this audit; no journal-specific page locators are inferred from the author PDF.

## W04 source audit — October 23, 2026

The published Oliveira–Pich–Santhanam PDF was checked for Section 1.2 (p. 4),
Theorem 1.4 (p. 6), Definition 2.4 (p. 11), and the proof in Section 4.1
(pp. 17–18). SHA256:
`81b1ff4ede5180dc88f99c8a4856cfde623f6fefb5b99ef9f5526899bf43ab4a`.

The exact NO promise is circuit complexity **strictly greater** than the upper
threshold. The introduction's informal wording does not replace the definition.
The theorem uses fixed-basis fan-in-two general circuits, counting gates, and
the full table length `N = 2^n`. A common epsilon must work for every sufficiently
small fixed beta. See the [applicability audit](w04-transfer-audit.md) for the
promise, resource contract, and explicit missing reduction. No transfer is
established.

## W06 metadata check — October 23, 2026

The [publication preparation dossier](w06-publication-preparation.md) records
primary/editorial metadata checks for all seven bibliography entries. These
checks do not complete a novelty assessment or human mathematical review.

The original six-entry table above predates the graph extension. Its additional
source is Bova and Slivovsky, [On Compiling Structured CNFs to OBDDs](https://link.springer.com/article/10.1007/s00224-016-9715-z),
Theory of Computing Systems 61(2), 637–655 (2017), DOI
`10.1007/s00224-016-9715-z`. The editorial page distinguishes online publication
on October 26, 2016 from the 2017 print issue. Section 4/Theorem 19 supplies
stronger expander-based background; the grid example claims no novelty.

The dossier also distinguishes author-PDF dates from conference/journal dates,
the print and digital book dates, and ECCC's original report from Revision 1.
The source's actual article/revision record takes precedence over stale or
incomplete machine-readable metadata. No unverified theorem-page locator or
publication date is supplied for the undated Allender–van Melkebeek clarification.
