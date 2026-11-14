# Referee audit: Proposition prop:psi-weight (paper/main.tex l. 800-897)

Verdict: **minor issues**. The mathematics is correct and both certificates pass. I found one numerical
typo, one statement about the change of variables that is false as written but easy to fix, and some
wording slips.

## Checked and correct
- Remark "another weight": an active m has a-S_A+n t_m >= a-(S-t_m) >= a-tau > 0. The sum over the
  active indices is beta*a. The fiber integrand is (1/beta) n/(a-S_A+nu), with n and S_A taken at (t',u)
  and m included (m is active on every fiber with |t'| <= tau). So M_k <= a sup I. n and S_A are Borel.
- Splitting: j is active iff x_j >= u-s. On [0,s] the denominator is c0+s+(k-1)u, which gives the log
  term. Layer cake: sum_{x_j>=w} x_j = N w + |t'| - M, so the denominator is c0+(1+N)s+M. Fiber length s+W.
- Change of variables, identity for J, f', f'' (re-derived), C-s=c0+mu*theta>0, concavity bound,
  g >= 1/C-1/(A+B) >= 0, dg/dC <= 0 (re-derived), Chebyshev with g and h oppositely monotone, equality
  case, admissible region (nu-1)W = M(W) <= tau-s.
- Cell bound: F increases in s, the integrand decreases in s, and d/dnu has the sign of c0-w. Corner choice correct.
- Scaling bound 1.04*(50/49)*log 50 = 4.1515346. Gap 4.15153-4.1463 = 0.0052. Correct.

## Issues
1. **l. 872, typo.** "c_0 = 0.0373" is wrong: c_0 = a - tau = 1.0373 - 0.96 = **0.0773**. 0 < c_0 < W = 0.08
   still holds, and the scripts compute c_0 correctly. Fix: write 0.0773.
2. **l. 847-862, case w_e > W.** If max x_j > W, then theta = M/mu maps [0,W] (not [0,w_e]) onto [0,W].
   The formula "int h = (w_e - W)/mu <= 0" would then be positive. The fix is to replace w_e by
   min(w_e, W), i.e. take sup{w in (0,W]: N(w) > 0}. Then int h = (min(w_e,W) - W)/mu <= 0. The equality
   case lies exactly in this regime, so the fix matters.
3. **l. 801-805, wording.** psi_m is undefined where n = 0, and it can be <= 0 where m is inactive
   (S_A can exceed a, since L > a). Lemma lem:dual asks for positivity on all of L R_k, but its proof
   only uses psi_m where m is active. Fix: "set psi_m = 1 where m is inactive". Also "exactly beta*a
   everywhere" should read "at every point with an active index (0 elsewhere)".
4. **Nit.** The docstring of code/psi_weight_cert.py cites "Prop. prop:psi-reduction". The label is
   prop:psi-weight.
5. **Nit, Remark "how sharp".** I get a*I = 4.146898 for (0.0811278^10, 0^39) and 4.146859 for the best
   (0.08^r) at a = 1.036, a gap of 3.95e-5 rather than 3.8e-5 (floating point). Other values reproduced:
   4.1463296 at a = 1.037, relaxed sup 4.1463525 at (s, nu) = (0.171, 10.86).

## Re-run certificates
- `python3 code/psi_weight_cert.py 10373 10000 41463 10000`: CERTIFIED, 3,518,636 cells, 3 min.
  tau = 24/25 is exact (fmpq). The box [0,tau]x[1,13] is exactly the start cell, bisection covers it,
  and the discard test (n1-1)W > tau-s1 is exact and correct. nu = 1 is handled exactly.
- `cd code/explore && python3 psi_scratch_certify.py 10373 10000 4.14631`: 0 failing cells, max 4.146309.
  Adjacent float cells share bit-identical endpoints. The last s-cell uses an enclosure of 24/25. Discards
  use the interval test. Depth-capped leaves are still checked in intervals. float(4.14631) < 4.14631,
  so the strict claim holds.
- Both cell bounds really dominate G on the cell, since they follow the monotonicity above.

## Independent check (my own evaluator, scratchpad)
Direct definition of "active" at (t',u), scipy quad split at the breakpoints u = s + x_j, cross-checked
by midpoint quadrature. 3000 random fibers with a in {0.97, 1, 1.0373, 1.1, 1.5}: max I - G = 9e-16, no
violation. Equality fibers: |I - G| < 5e-16. 1000 adversarial fibers with x_j near W: I - G < 0.
Float max of a*G at a = 1.0373 is 4.1462991, so the certificate has about 1e-6 of margin. The best fiber
found is 4.146173, so the true value lies in [4.14617, 4.1463).

## Not checked
python-flint and mpmath.iv were not audited. The literature claim "possibly folklore" was not checked.
Lemma lem:dual was only reread, not re-proved beyond the argument above.
