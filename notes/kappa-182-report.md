# Rung 182: the sharp five-prime mass deficit kappa_true (report)

Status: **finished**. kappa_true was computed by two independent methods; both agree with each other and confirm
the printed bracket. This checks one numerical ingredient ((4.2)-(4.3) and Sec. 13.3) of a **Claimed** preprint
(GPT-6 Astra / R. Sharifi, bundle [M]). It does not verify the 182 claim. In particular it does not check the
derivation of the minorant, the coefficient 24 (beyond a labeling count), or the distribution of the addback.

- Program: `code/sharifi182_kappa.py`. Run it with `/usr/bin/python3 -I`, because python-flint is only installed
  for /usr/bin/python3. `--selftest` passes.
- Result: `code/data182/kappa_result.json`.
- Log: `runs/kappa182.log`.
- Transcription: `notes/sources-182-kappa.md`.
- Runtime: 55 s wall in total (A 5 s, B with D = 60 is 50 s), with memory well under 1 GB.

## What was computed (all **Computed**)

The definition is (4.2): kappa_true = 24 int_{P_a} d alpha / (alpha_1 ... alpha_5) on
P_a = {alpha_1 > ... > alpha_5 > 0, sum = 1, alpha_1 + alpha_2 < a}, with a = 41361/100000.

**Method A (mine, no simplices).**
- The alpha_4-integral is done in closed form:
      int_{s/2}^{alpha_3} = (1/s) log(alpha_3/(s - alpha_3)),   s = 1 - alpha_1 - alpha_2 - alpha_3.
  Here alpha_4 > alpha_5 means alpha_4 > s/2. alpha_5 > 0 is automatic, since alpha_5 > 1 - 2a.
- The remaining 3-dim region is
      alpha_2 < alpha_1,  alpha_1 + alpha_2 < a,  alpha_1 + 4 alpha_2 > 1,  (1 - alpha_1 - alpha_2)/3 < alpha_3 < alpha_2.
  Its alpha_2-range is [(1-a)/3, a/2], with a kink at alpha_2 = 1/5.
- On each of the two pieces the integrand is analytic on the closed piece. Tensor Gauss-Legendre with 24 and 48
  nodes per dimension (mpmath, 60 digits) gives values that differ by 6e-65. Convergence is exponential.
- Two sanity checks:
  - A raw 4-dim float64 Gauss-Legendre of the original integrand, with no closed-form step, gives
    9.330708832406049e-05 (relative difference 8e-15).
  - The same region code with integrand 1 reproduces vol(P_a) = u^4 * (125/864)/4 to 6e-39.

**Method B (the paper's route), all exact rationals.**
- I enumerated the vertices of P_E from the inequalities (4.5) myself: 330 4-subsets of the 11 constraints, solved
  exactly. This gives exactly the 7 printed vertices.
- (4.5) agrees with my own translation of "first labeled E1 region", that is alpha_4 smallest, alpha_1 > alpha_2 >
  alpha_3 > alpha_4, every pair < a, on 20000 random rational points.
- vol(P_E) = 125/864, from an independent exact triangulation (qhull combinatorics with exact determinants).
- The three printed simplices:
  - their vertices lie in P_E;
  - each lies in its printed cut region (z3 + 2z4 >= -1 / between / z2 + 2z4 <= -1), so their interiors are
    disjoint;
  - their volumes are exactly 125/5184, 625/20736 and 625/6912, which sum to vol(P_E).
  - So the triangulation covers P_E.
- r_Sigma = 1361/15000, 1361/15000, 1361/10000, as printed.
- The moment series (4.8)-(4.9) was evaluated with python-flint integer polynomials for h_n(B) and exact Dirichlet
  moments:
  - **D = 22 rigorous interval (4.11):** [9.33070883240611846e-5, 9.33070883240612137e-5], width 2.91e-20 (< 3e-20 as
    claimed). It lies strictly inside the printed bracket (.000093307088324061, .000093307088324062).
  - **D = 60:** kappa_B = 9.330708832406119916592098704527262353773e-5, with rigorous tail bound 6.7e-52.
  - The per-simplex contributions are 1.55297e-5, 1.94262e-5 and 5.83511e-5.

## Agreement

    kappa_A = 0.00009330708832406119916592098704527262353773...
    kappa_B = 0.00009330708832406119916592098704527262353773...

- The two values differ by |A - B| = 2.1e-63, i.e. 58 significant digits.
- The guaranteed agreement is about 47 digits, limited by B's crude rigorous tail bound 6.7e-52. A's error is
  estimated from successive meshes, not proved.
- **The printed bracket .000093307088324061 < kappa_true < .000093307088324062 is confirmed.** Both the value and the
  rigorous D = 22 interval lie in it.
- kappa-bar = 46653544162031/5e17 is exactly the printed upper end, and kappa-bar - kappa_true = 8.0e-19 > 0.

## kappa_cvx (Sec. 13.3)

- The paper's convexity bound sums, over the 3 simplices, V_j * (mean of the density 6u^4/prod(1/5 + u z_i) at the
  5 vertices).
  - Recomputed exactly: per simplex 1.556266e-5, 1.947041e-5 and 5.853482e-5; total 9.35678858088923e-5.
  - This is at most kappa_cvx = 11696/125000000 = 9.3568e-5, with margin 1.14e-10.
  - The bound is valid because 1/prod(positive affine forms) is log-convex, hence convex.
- The order is confirmed: kappa_true (9.3307088e-5) < kappa-bar (9.3307088324062e-5) < vertex average
  (9.35678858e-5) <= kappa_cvx (9.3568e-5).

## Differences in formulation, and gaps

- None in substance. My A-domain was derived from the words "products of five distinct primes, every pair product
  < x^a, ordered decreasingly", which is literally P_a. The closure in (4.5) and the redundant z_i >= -2 do not
  affect the integral.
- The relation kappa_true = 6 kappa_{5,1} (4 labeled copies), with Jacobian u^4, is confirmed numerically, since
  A uses P_a directly and B uses P_E.
- The density 1/(alpha_1 ... alpha_5) d alpha_1..d alpha_4 and the multiplicity 24 are taken from the paper. The
  labeling counts 4 + 20 = 24 were brute-forced. The asymptotic (PNT and partial summation) was not rechecked.
- The paper does not print the three individual vertex averages of Sec. 13.3, only their rounded total. Nothing
  else needed for the computation was missing from the PDF.
