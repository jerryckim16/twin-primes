# Route card: one-step Chen switching on rung 3 of the sifting-dimension ladder (22 Nov 2026, Session 45)

**Classification: refuted at level 1/2 (one-step switching, linear-sieve upper bound, level 1/2 for both A_H and the
switched set; main terms by a heuristic identification checked against data; numerical, floating point); located
for a common level: the method works for rung 3 iff both sets have a common level theta > theta* = 0.5692 for the
weights involved (below the direct route's 0.6121, and below BFI's 4/7, which is NOT known to apply to these
weights). Audited (2 errors, 1 slip, 4 gaps; fixed below).**
Not in the parity paper (v1.0.1 frozen). No progress on twin primes and no way around parity.
Follows the Session 44 card [2026-11-22-level-ladder.md](2026-11-22-level-ladder.md), whose "first unresolved
implication" this is: sift only to z = x^{1/u}, u > 2, where Bombieri-Vinogradov gives s = u/2 > beta_{2/3}, and
remove the survivors with two bad primes by switching.

## Question and criteria
Setting of the Session 43/44 cards: q prime, H < (Z/q)^* of index m, good primes l (l mod q in H), bad primes the
others, A_H = {p + 2 : p <= x, p + 2 mod q in H}, kappa = 1 - 1/m. Rung 3 is q = 7, H = {1, 6}, kappa = 2/3. For
z = x^{1/u}, 2 < u <= 3, a survivor of sifting A_H by the bad primes below z has 0 or 2 bad prime factors (one is
excluded by the congruence; b^2 g needs b^2 in H, impossible for m = 3, and is O(x/z) in general), so
S(A_H, z) = T_H(x) + W(x), W = #{p : p + 2 = g b1 b2, z <= b1 < b2 bad, b1 b2 in H, g all good}. For 3 < u <= 4 also
three bad primes (W3).
- Success criterion: with the beta-sieve lower bound at level x^{1/2} (s = u/2) and an upper bound W <= C * (main term
  of W) from switching (sieve the primes p = n - 2, n in the switched set B = {g b1 b2}, at level x^{1/2}, C = 2/theta = 4
  for the linear sieve), margin(u) = f_kappa(u/2) - C Z(u) (R2 + R3)(u) > 0 for some u. This would give
  T_H(x) >> x/(log x)^{1 + kappa} unconditionally for rung 3.
- No-go criterion: margin(u) < 0 for every u in (2, 4] with C = 4, and also with the best known levels for the switched set.
- Consistency test (must pass): the same method at m = 2 (kappa = 1/2, where Iwaniec's theorem holds) must give a
  positive margin.

## Main terms (Heuristic identification; checked against data; NOT proved here)
In units of |A_H| V(z), V(z) = prod_{bad l < z, l != 2, q} (1 - 1/(l - 1)) (2 never divides p + 2):
- Z(u) = m e^{gamma kappa} / Gamma(1 - kappa) * u^{-kappa}: expected T_H (Selberg-Delange for all-good integers, which
  lie only in the classes of H, hence the factor m; Mertens for V(z)/V(x) = u^kappa).
- Z(u) R_j(u), R_j(u) = c_j(m) kappa^j / j! * int_{t_i >= 1/u, sum t_i <= 1} (1 - sum t_i)^{-kappa} prod dt_i / t_i:
  expected W (j = 2) and W3 (j = 3). Here c_j(m) = ((m-1)^j + (-1)^j (m-1)) / (m (m-1)^j) is the probability that a
  product of j bad primes, independent and uniform over the m - 1 bad cosets of the cyclic quotient of order m, lies
  in H. c_2 = 1/(m-1), c_3(3) = 1/4. **The counting identity behind c_j is Lean-checked** for all m >= 2 and all j
  (lean/TwinPrimes/Cosets.lean: coset_count_zero, coset_count_nonzero, coset_prob_two, coset_count_three).
- The identification of the switched main term with Z R (the local factors of "n - 2 prime" agree on all-good n and on
  g b1 b2, since both avoid the bad primes below z and are equidistributed in (Z/l)^* for every other small l) is the
  Kubilius-model step; it is not proved here. It is checked against data (Computed, finite X):

| X | u | T_H (units) | pred. Z | W (units) | pred. Z R2 | W/T | pred. R2 |
|---|---|---|---|---|---|---|---|
| 1e7 | 3 | 0.8064 | 0.7910 | 0.2004 | 0.2111 | 0.2485 | 0.2669 |
| 1e8 | 3 | 0.7992 | 0.7910 | 0.2039 | 0.2111 | 0.2551 | 0.2669 |
| 1e8 | 2.5 | 0.9015 | 0.8933 | 0.1048 | 0.1125 | 0.1162 | 0.1259 |
| 1e8 | 3.5 | 0.7281 | 0.7138 | 0.2709 | 0.2838 | 0.3721 | 0.3977 |

  W3/T at 1e8, u = 3.5: 0.0022 against R3 = 0.0036. The finite-X values move toward the predictions from 1e7 to 1e8;
  S(A_H, z)/(|A_H| V(z)) is 1.001-1.006, against Z(1 + R2 + R3) = 1.002 (u = 3), 1.006 (u = 2.5), 1.000 (u = 3.5).

## Findings (Computed, numerical; code/parity/switch_ladder.py, output code/parity/switch_ladder.out)
f_kappa by the Session 43/44 solver at three step sizes (beta_{2/3} = 1.2241, beta_{3/4} = 1.3981 as before; R2(3) by
two quadratures agreeing to 3e-5).

1. **Rung 3 fails with C = 4.** margin(u) is negative on the whole grid u in [2.05, 4]: for example -0.352 at u = 3
   (f_{2/3}(1.5) = 0.492 against 4 Z R2 = 0.845) and -0.443 at u = 3.5. The largest switching constant that would
   suffice is C_need(3) = max_u f/(Z (R2 + R3)) = 2.455 (at u = 3.40). With the linear-sieve upper bound at level theta
   for the switched set, C = 2/theta; C < 2.455 needs theta > 0.815, against 1/2 (BV for the convolution b1 * (b2 g)) and
   4/7, 7/12 for well-factorable weights (C = 3.5, 3.43; whether those theorems even apply to this convolution set was not
   checked). This raises the level of B ONLY, with A_H kept at 1/2; see Finding 4 for the fair comparison (an earlier
   draft compared 0.815 with the direct route's 0.612 and concluded "switching needs more"; the audit showed that is
   wrong).
2. **Consistency test passes.** At m = 2 (kappa = 1/2) the margin with C = 4 is positive for u in (2, 3.75]
   (+0.263 at u = 3, C_need = 81 at u = 2.05, where W is tiny), so one-step switching reproduces a half-dimensional
   Iwaniec-type statement (p + 2 composed of quadratic residues mod q) at level 1/2. Folklore in substance; Iwaniec's
   own device is different (not re-read here).
3. **Level versus parity, with A_H at level 1/2.** Selberg's example shows that a sieve upper bound for primes cannot
   beat twice the expected count from level-of-distribution information alone, so C >= 2 for any sieve-only switching.
   With A_H at level 1/2: for rung 3, C_need = 2.455 > 2, so raising the level of B alone would suffice in principle;
   for m = 4 and m = 5 the maximum over u <= 4 is 1.788 and 1.452 (at the edge u = 4; u > 4 needs four bad primes and
   was not examined), below 2, so raising the level of B alone cannot help. Raising the level of A_H changes this
   (Finding 4).
4. **A common level (added after the audit; part (vi) of the script).** With level theta for both A_H and B the
   margin is f_kappa(theta u) - (2/theta) Z(u) (R2 + R3)(u). Least theta with a positive margin for some u in [2.02, 4]:
   theta* = 0.5692 for m = 3 (three step sizes: 0.5691-0.5693; the audit found 0.5693 independently),
   0.6651 for m = 4, 0.7262 for m = 5, against the direct route's beta_kappa/2 = 0.6121, 0.6991, 0.7553 (Session 44).
   At theta = 4/7 the best margin for m = 3 is +0.0093 (u = 2.50), at 7/12 it is +0.0575 (u = 2.46). So, at a common
   level, switching needs LESS than the direct route, and 4/7 would just suffice for rung 3, IF a level 4/7 were known
   for both (i) the lower-bound beta_{2/3}-sieve weights on shifted primes and (ii) the linear upper-bound sieve on the
   convolution set B. Neither is known: (i) fails the well-factorability hypothesis of BFI / Maynard / Lichtman (Session 44,
   Finding 2: the beta_{2/3} weights are not well-factorable, beta_{2/3} < 2), and for (ii) the BFI-type theorems are
   stated for primes, not for such convolution sets (not checked). For general weights the only known level is 1/2.

## Conclusion and first unresolved implication
One-step Chen switching does not reach rung 3 at level 1/2 (margin -0.35 at u = 3). With a common level theta for
A_H and the switched set it works exactly when theta > 0.5692 (numerically), which is lower than the 0.6121 that
the pure beta-sieve at x^{1/2} needs, and lower than 4/7. First unresolved implication: a level 0.5692 for the
lower-bound beta_{2/3}-sieve weights on shifted primes (these weights are not well-factorable, so BFI's 4/7 does not
apply as stated) together with a level 0.5692 for the upper-bound linear sieve on the convolution set B. A
well-factorable lower-bound sieve of dimension 2/3 with sifting limit close to beta_{2/3} would be one way in (not
examined). Other ways in: switching that keeps the structure of W (Chen's double sieve, a vector sieve on (p, n)).
None of this touches kappa = 1 (twins), where f_1(s) = 0 for s <= 2 and parity rules.

## Sources and caveats
- Sources: no new source opened. Used as quoted in the Session 43/44 cards: the beta-sieve theorem (Gaudet
  arXiv:2408.01610v1 Prop. 5.1, quoting Opera de Cribro Thm 11.13); Bombieri-Vinogradov for convolutions with one
  Siegel-Walfisz factor and the linear-sieve upper bound F(s) = 2e^gamma/s (s <= 3) are standard black boxes, NOT re-read
  this run; Selberg's parity example is quoted from memory as the standard statement (Friedlander-Iwaniec, Opera de
  Cribro Ch. 16 has it; not opened this run).
- Literature: not searched this run (Session 44 ran two queries on this setting, none found). Possibly folklore.
- Floating point throughout (scipy quad, numpy solver); no interval certificate. The margins are large (-0.35 against
  rounding of order 1e-3), but the heuristic identification of the switched main term is an assumption.
- Better switching (Chen's double sieve, weighted Buchstab iterations, using the bad-freeness of g in W) was not tried.
- Audit (fresh-context helper, adversarial; mathbox not available). ERRORS: (1) the level analysis raised the level
  of B only, so the comparison "0.815 against 0.612" and "switching needs more" were wrong; fixed by Finding 4 (theta*
  recomputed here by part (vi), agreeing with the auditor's independent bisection); (2) "parity-blocked whatever the
  level" for m >= 4 holds only with A_H at level 1/2; reworded; (3) V(z) must exclude l = 2 (the code did); fixed.
  GAPS recorded: (4) the switched main term can be made rigorous (Selberg-Delange for g, PNT in progressions for
  b1, b2); it is still only identified heuristically here, and the verdict at level 1/2 would need a 42% error in it
  against about 5% seen in the data; (5) level 1/2 for B is a standard but unchecked black box; (6) the m = 2 test
  mainly checks bookkeeping: near u = 2, W is negligible, and f_{1/2} converges only like sqrt(h) (0.932 printed at
  s = 2 against the exact 0.9385, the safe direction); (7) other sieves of dimension 2/3 were not considered. HOLDS: the
  reduction, the constants Z, c_j, R_j and the code's limits (Z(3) = 0.791041, R2(3) = 0.266903 recomputed
  independently with mpmath), C = 2/theta, the solver, the parity-limit statement.
