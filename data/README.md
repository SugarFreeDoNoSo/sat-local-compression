# Residual-function data

Regenerate with: python3 experiments/obdd_residuals.py --max-m 7

- Domain: incidence-encoded unit-clause SAT, 1 <= m <= 7.
- Predicate: no index has a_i = b_i = 1.
- Model: deterministic layered ordered decision diagrams.
- Method: exhaustive residual truth tables at each cut.
- Orders: all a then all b; alternating a_i and b_i.
- Arithmetic: exact, with no randomness.
- Scope: finite consistency evidence for P03 and P04, not their proof.

The CSV and TeX table are generated together and checked for drift.
