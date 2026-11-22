# Route card: one-step Chen switching on rung 3 of the sifting-dimension ladder (22 Nov 2026, Session 45)

**Classification: refuted for the stated method (one-step switching, linear-sieve upper bound, level 1/2 on both sides;
main terms by a heuristic identification checked against data; numerical, floating point). The failure is a level
problem, not a parity problem, for rung 3; for rungs m >= 4 (with u <= 4) it falls below the parity limit 2 of
upper-bound sieves.**
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
In units of |A_H| V(z), V(z) = prod_{bad l < z, l != q} (1 - 1/(l - 1)):
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
   checked). The direct route of Session 44 needs level 0.612 for A_H; switching needs more, not less.
2. **Consistency test passes.** At m = 2 (kappa = 1/2) the margin with C = 4 is positive for u in (2, 3.75]
   (+0.263 at u = 3, C_need = 81 at u = 2.05, where W is tiny), so one-step switching reproduces a half-dimensional
   Iwaniec-type statement (p + 2 composed of quadratic residues mod q) at level 1/2. Folklore in substance; Iwaniec's
   own device is different (not re-read here).
3. **Level versus parity.** Selberg's example shows that a sieve upper bound for primes cannot beat twice the expected
   count from level-of-distribution information alone, so C >= 2 for any sieve-only switching. For rung 3,
   C_need = 2.455 > 2: the obstruction is the level of distribution of the switched set, not parity. For m = 4 and
   m = 5 the maximum over u <= 4 is 1.788 and 1.452 (at the edge u = 4; u > 4 needs four bad primes and was not
   examined), below 2: there one-step switching is blocked by the parity limit of the upper-bound sieve, whatever the
   level (for u <= 4).

## Conclusion and first unresolved implication
One-step Chen switching does not reach rung 3 at level 1/2: it would need the switched set to have level > 0.815,
while the pure beta-sieve at z = x^{1/2} needs only 0.612 for A_H (Session 44). With the Session 44 card this
locates rung 3 (kappa = 2/3) between two specific level requirements, neither known. For rungs m >= 4 the switching
step is parity-blocked (u <= 4). First unresolved implication: a switching step that does not discard the structure of
B (a lower-bound sieve inside W, Chen's double sieve or a vector sieve on (p, n) jointly), or a level > 0.612 for the
lower-bound beta_{2/3}-sieve weights on A_H. Neither touches kappa = 1 (twins): there f_1(u/2) = 0 for u <= 4 and parity
rules.

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
