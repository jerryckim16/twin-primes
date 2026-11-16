# Audit of parity paper v0.11, subsection subsec:pintz (Session 26, 16 Nov 2026)

Fresh-context adversarial auditor (general-purpose helper; mathbox:proof-audit not available), told to read Pintz
arXiv:1004.1065v1 and Maynard arXiv:1311.4600v3 in the source and attack Thm. thm:pintz-maynard, Cor. cor:pintz12 and
Rem. rem:pintz-parity line by line. Independent recomputation of M_2 from the JSON vector (exact match), and an
optimisation of Pintz's (3.22) in u (0.72302 / 0.61257 / 0.5516 / 0.51262 for k = 2..5), re-done by the coordinator
(same values, floating point).

Verdict: no ERROR. Findings and what was done:
1. Criterion theta M_k > 1 with Maynard's normalisation: OK.
2. lambda-twisted estimate for Maynard weights: OK. Fixed: (2.2) applied with 3N; cite Maynard (5.9) and (5.18)-(5.20);
   the gcd step now says h_k - h_1 < D_0, contradicting (prod d_i e_i, W) = 1.
3. Hypotheses on r: nothing missing (H u {r} need not be admissible; (2.2) covers all classes).
4. "Since r not in H" mis-placed in the final step: fixed (the step uses chi in {0,1}); a sentence after the theorem says r not in H
   only makes the statement non-trivial; M_1 = 1 noted.
5. BV for lambda rests on Pintz Lemma 3 (stated by analogy with Vaughan): now said explicitly, with the reduction of
   non-coprime classes. No further reference added (none read).
6. Corollary arithmetic: OK. Added: 0 < d <= 13 (Pintz 17); part (1) = Pintz Thms 5/7 at theta > 0.515, now unconditional.
7. Comparison of thresholds overstated: fixed (Pintz's optimised (3.22) gives 0.7230 / 0.6126 / 0.5516; the gain is small for
   k <= 4 and matters at k = 5, where it crosses 1/2).
8. Dangling tuples in proof of (4): now tied to Pintz's Theorem 7 with C_3 = 2, 6, 8; basis described as b + 2c <= 6.
9. "now holds unconditionally" moved to part (1) with the exact statement; "predicts" -> "predicts, heuristically".
10. Parity remark: last paragraph rewritten (star = position r never asked to be prime vs complete graph); fairness sentence
    now a heuristic about the twisted input; the Lean check is the k = 2 integer case, larger k by averaging (Rem. rem:marg);
    "consistent with Pintz's remark" (his remark is about his method).
11. Pintz's Thm 3 assumes r != 0: added to the literature paragraph.
12. Novelty: two more searches found nothing; keep "possibly folklore"; Pintz's post-2013 surveys not checked.
