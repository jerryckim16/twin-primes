# Audit of the Lean note v1.1 changes (Session 59, 27 Nov 2026)

Fresh-context helper agent, adversarial, no edits. Scope: new Section 4 (thm:s2), abstract, hyp:s2, the
"Reproducing the checks" counts, history item 1.1; checked against lean/TwinPrimes/MaynardS2.lean,
MaynardS2Hpw.lean and Maynard arXiv:1311.4600v3 (PDF fetched into /tmp, not committed).

Counts re-run by the auditor: lake build 26 jobs; 23 files, 6309 lines; Reduction + 7 Maynard* + 2 Mu* = 3132
lines; Audit.lean 239 declarations (129 / 61 / 21 / 28); no sorryAx, sorry, native_decide or axiom. All cited
theorem names exist.

Findings (all applied in v1.1):
1. Slip: item (3) cited count_zero_of_not_good_S2 (full moduli); the erased-moduli statement is
   count_zero_reduced_of_not_good. Fixed.
2. Gap: m < k omitted in items (2)-(3); item (3) needs item (2)'s hypotheses. Fixed.
3. Overstatement: the Lean sum uses 1[pr(n+h_m)] with pr only sound; equals S_2^(m) only for an exact test
   (completeness of primeB not proved). Sentence added.
4. Overstatement: no non-vacuity example for item (4) (maynard_S2_count_residue). Fixed.
5. Citation: Maynard's S2 change of variables is (5.21)-(5.24) (y^(m) in (5.23)); (5.8) is the S1 inversion used in
   Lemma 5.3. Fixed (line numbers of (5.21), (5.23), (5.24) confirmed in the PDF text here).
6. Gap: "not covered" list now includes coprimality of the class in (4) to q, and "over good pairs".
7. Minor: hyp:s2 wording separated the analytic prime counts from the algebraic analogue of thm:diag. Fixed.
Checked correct: item (1) hypothesis-free; item (4) hypotheses; bad-pair step uses neither residue nor primality;
abstract; history.
