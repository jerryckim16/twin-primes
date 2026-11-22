# Route card: levels of distribution beyond 1/2 on the sifting-dimension ladder (22 Nov 2026, Session 44)

**Classification: located for the pure beta-sieve at z = x^{1/2} with the known level theorems as black boxes (computed thresholds; exact exponent checks; literature read in the sources; possibly folklore). The switching route at smaller z is open (see the conclusion).**
Not in the parity paper (v1.0.1 frozen). No progress on twin primes and no way around parity.
Follows the Session 43 card [2026-11-22-dimension-ladder.md](2026-11-22-dimension-ladder.md), which left open
"whether a well-factorable level beyond 1/2 (Bombieri-Friedlander-Iwaniec type) gives any rung unconditionally".

## Question
Session 43: requiring every prime factor of p + 2 to lie in a set of primes of relative density 1 - kappa gives a sieve
problem of dimension kappa, and a congruence removes the one large prime left after sifting to z = x^{1/2}. With
level y = x^theta the beta-sieve parameter is s = log y / log z = 2 theta. The beta-sieve lower bound (Gaudet Prop. 5.1)
is available for s >= beta_kappa and positive exactly for s > beta_kappa; whether some other sieve has a smaller
sifting limit for 1/2 < kappa < 1 is not known (Ford, quoted in the Session 43 card). Bombieri-Vinogradov gives
theta < 1/2, so s < 1 = beta_{1/2}: the pure beta-sieve reaches no rung m >= 2, and kappa = 1/2 needs Iwaniec's
device. Which rungs do the known levels beyond 1/2 reach?

- Success criterion: some rung kappa > 1/2 with 2 theta > beta_kappa for a level theta that is PROVED for weights of the
  kind the beta_kappa-sieve needs; this would be an unconditional theorem (p + 2 composed of primes from a set of
  density <= 1/3) beyond the half-dimensional case.
- No-go criterion: every rung needs either a level above all known levels, or a level known only for a weight class
  (well-factorable / triply well-factorable) that the beta_kappa-sieve weights do not belong to.

## Setting (Proved here; elementary; the Session 43 reduction with a subgroup)
Abelian rungs only: q prime, H < (Z/q)^* of index m, Q_H = {primes l : l mod q in H}, kappa_m = 1 - 1/m, and
T_H(x) = #{p <= x : p + 2 mod q in H, every prime factor of p + 2 in Q_H}. Sift {p + 2 : p + 2 mod q in H} by the
odd primes l <= z = (x + 2)^{1/2} with l != q, l mod q not in H (l <= z, not l < z: otherwise p + 2 = r^2 = z^2
could survive, and for even index r^2 can lie in H). A survivor m has at most one prime factor r outside Q_H
(two would exceed z^2), and if m = r m' with m, m' in H then r is in H: contradiction. So T_H(x) = S(A_H, z), a sieve of
dimension kappa_m (prime number theorem mod q). Rung 2 is q = 3 (or H = squares), rung 3 is for example q = 7,
H = {1, 6} (primes = +-1 mod 7, i.e. split completely in Q(cos 2 pi/7)).
Only kappa = 1 - 1/m arises this way; the reduction needs the group structure (a Chebotarev set with no
group law gives no contradiction for the leftover prime).

## Sources read (PDFs fetched with WebFetch, read with pdftotext in /tmp/claude-0/lit44/, not committed)
- Lichtman, arXiv:2309.08522v1 (SHA-256 665693af...98c55b5): abstract; Defs 1.3, 1.4 (well-factorable, triply
  well-factorable); Cor. 1.5 (level 66/107 for triply well-factorable weights, fixed a != 0); Thm 1.7 (level
  (5 - 4 theta)/(8 - 6 theta), theta the Selberg-eigenvalue exponent; 5/8 under Selberg's conjecture; uniform range
  |a| < x^{1+eps} at level (5 - theta)/8); p. 6 and footnote 7 (linear sieve weights are not triply well-factorable;
  Iwaniec's modified weights are well-factorable; the level for linear sieve weights varies with the anatomy of the
  modulus, between 7/12 and 66/107); Sect. 6.1 (supports D^+-, D^well); Prop. 3.1 (sup over a outside the sum over q).
- Maynard, arXiv:2006.07088v1 (SHA-256 04516b14...bb4) pp. 2-3: Thm 1.1 (triply well-factorable, level 3/5);
  Thm 1.2 (well-factorable UPPER-bound linear sieve weights lambda^+, level 7/12; for the lower-bound weights Lichtman p. 7
  quotes "at least 7/12 by [28]" for the modified weights in both directions); and: "Iwaniec [14] showed that a slight variant of the upper
  bound beta-sieve weights of level D ... is a linear combination of sequences which are well-factorable of level D
  provided beta >= 1 ... The factorable variant of the beta-sieve weights of level D are a linear combination of triply
  well factorable sequences of level D provided beta >= 2 ... the linear (beta = 1) sieve weights ... are not triply well
  factorable". CONVENTION: Maynard calls the linear sieve beta = 1, while his own support D^+(D) (line "p_1...p_{2j}
  p_{2j+1}^3 <= D") and Lichtman's Sect. 6.1 have exponent 3 = beta + 1 in the sifting-limit convention of
  OdC / Gaudet / Blight, where the linear sieve has beta = 2. So in the sifting-limit convention Iwaniec's
  well-factorability is asserted for beta >= 2 (the linear sieve and above). We did not open Iwaniec 1980 or OdC
  Ch. 12 to confirm this reading; see the gaps.
- Gaudet, arXiv:2408.01610v1 (SHA-256 d5bfce37...0d04e1) pp. 9-11: the beta-sieve theorem in dimension kappa (Prop. 5.1,
  quoting OdC Thm 11.13): lower bound for s >= beta; B(kappa) = 0 for kappa >= 1/2; Blight's table confirmed by Irving.
  The support of the beta-sieve weights is not written out there.
- Literature search (two WebSearch queries, 22 Nov): no source treats beta-sieve weights for 1/2 < kappa < 1 at a level
  beyond 1/2, and none treats shifted primes all of whose prime factors split in a cubic field. Not exhaustive.

## Findings

### 1. The threshold levels (Computed, numerical; code/parity/level_ladder.py part (i))
beta_kappa by the Session 43 method of steps at three step sizes (1e-3, 5e-4, 2.5e-4), cross-checked against
Blight's table at kappa = 0.6 (1.10412 here, 1.1042161 hers) and 0.75 (1.39812, 1.3981115):

| m | kappa_m | beta_kappa | threshold theta_m = beta/2 |
|---|---|---|---|
| 3 | 2/3 | 1.2241 | 0.6121 |
| 4 | 3/4 | 1.3981 | 0.6991 |
| 5 | 4/5 | 1.5106 | 0.7553 |
| 6 | 5/6 | 1.5884 | 0.7942 |
| 8 | 7/8 | 1.6881 | 0.8441 |

Against the known levels (fixed residue a = -2): BV 1/2, BFI 4/7 = 0.5714 (well-factorable), Maynard 7/12 = 0.5833
(well-factorable linear sieve weights; stated for lambda^+), Maynard 3/5 (triply well-factorable), Lichtman 66/107 = 0.6168 (triply
well-factorable), Lichtman 5/8 (triply well-factorable, under Selberg's eigenvalue conjecture):
- Rung 3 (kappa = 2/3) sits between 3/5 and 66/107: s = 2 * 66/107 = 1.2336 exceeds beta_{2/3} = 1.2241 by 0.0095
  (the step-size spread of beta is 4e-4), with f_{2/3}(1.2336) = 0.026; at 5/8, f_{2/3}(1.25) = 0.069. Every UNIFORM level
  known for well-factorable (not triply) weights is below the threshold (Lichtman's anatomy-dependent levels for
  the modified linear-sieve weights reach 66/107 for some moduli).
- Rungs m >= 4 need theta > 0.699, beyond every known level, even 5/8 under Selberg's conjecture.

### 2. The beta_{2/3}-sieve weights are not well-factorable at their level (Proved here; exact; elementary)
The lower-bound beta-sieve support is {d = p_1 ... p_r, p_1 > ... > p_r : p_1 ... p_{m-1} p_m^{beta+1} < D for every
even m <= r, and p_1^beta < D} (the linear case D^- is written in Lichtman Sect. 6.1, with exponent 3 = beta + 1 and the
extra condition p_1^2 < D; Maynard writes only the upper-bound support D^+; the general-beta form is the standard one of
OdC Ch. 11, NOT opened here). Take p_1, p_2, p_3 primes near D^{3/10}. The conditions are m = 2 and p_1^beta < D:
p_1 p_2^{beta+1} ~ D^{0.3 (beta + 2)} = D^{0.967} < D and p_1^beta ~ D^{0.367} < D, for beta <= 1.225 (a numerical bound
for beta_{2/3}, Finding 1); so d = p_1 p_2 p_3 ~ D^{0.9} is in the support. Its divisors have sizes D^0, D^{0.3}, D^{0.6}, D^{0.9}, so d has no factorisation
d = q_1 q_2 with q_1, q_2 <= D^{1/2}: any sequence supported on such d with lambda_d != 0 is not well-factorable of level
D (Def. 1.3). Each summand of a linear combination of well-factorable sequences of level D vanishes at d, so no such
linear combination equals the weights either. Since Def. 1.4 allows Q_3 = 1, triply well-factorable implies
well-factorable (Maynard p. 3: "not well-factorable (and so not triply well factorable)"); so the weights are not
triply well-factorable, and Cor. 1.5 / Thm 1.7 (66/107, 5/8), the only levels above 0.6121, do not apply to them.
With D = x^theta, theta in (0.61, 0.63), d ~ x^{0.55} lies above the Bombieri-Vinogradov range and
p_i ~ x^{0.18} < z, so this modulus genuinely needs the beyond-1/2 estimate. For the linear sieve the same d is
excluded (p_1 p_2^3 ~ D^{1.2}). The obstruction is exactly that beta_{2/3} < 2: the parity-indexed conditions no longer
imply the conditions p_1 ... p_{m-1} p_m^2 < D for all m (the set D^well), because p_m^2 <= p_{m-1}^beta fails.
(An earlier draft left triple well-factorability open and said it held for this d; both were wrong, see above.)
Convention check (Proved here, elementary): for m of the unconstrained parity, p_m <= p_{m-1} gives
p_1 ... p_{m-1} p_m^2 <= p_1 ... p_{m-2} p_{m-1}^3, so the parity-indexed conditions with exponent beta + 1 imply all of
D^well exactly when beta + 1 >= 3, i.e. beta >= 2 in the sifting-limit convention; exponent 4 gives the "triple"
analogue. This matches Maynard's "well-factorable provided beta >= 1, triply provided beta >= 2" with his beta equal to
ours minus 1 (his statements are about the upper-bound weights). Iwaniec's modified weights change the support only
slightly; the obstruction beta < 2 is structural.
Lichtman's anatomy-dependent route does not rescue this d either (Computed, exact exponent check): his sufficient
condition (6.3) of Prop. 6.1 (alpha = 0, theta = 7/32, delta -> 0) needs, for EVERY A in [x^delta, x^{1/3}], a
factorisation d = abc with a <= A, A^2 b c^2 <= x, A a b^5 c^2 <= x^2, (Ac/b)^{2 theta} A a b^5 c^2 <= x^2. For
p_i = x^{0.3 * 0.6121} none of the 27 assignments works for A in [x^{0.041}, x^{0.183}] or [x^{0.225}, x^{1/3}]
(found by the audit, re-checked here). (6.3) is only sufficient, so this is not a proof that no level works.

### 3. One gap of standard type: the auxiliary congruence mod q (not an obstruction)
The target needs p + 2 mod 7 in H in addition to p = -2 mod d. Lichtman's and Maynard's theorems are stated for pi(x; q, a) with one fixed
residue; Siegel-Walfisz coefficients appear in the internal propositions (Lichtman Prop. 3.1). In the Type II sums the
extra condition splits as 1_{nm = b (7)} = sum_{uv = b} 1_{n = u (7)} 1_{m = v (7)}, but the restricted coefficients no
longer satisfy (2.2) as stated (it fails for moduli divisible by 7), and the Type I / divisor piece (Prop. 3.2) needs
the extra congruence too. Lichtman remarks after Thm 1.8 that it "holds for general modulus q_0, following [11]",
which supports that a fixed auxiliary modulus is routine. A version
with a fixed auxiliary modulus is presumably routine; it is not stated in the sources. (An earlier draft of this card
argued that the residue mod 7d varies with d and invoked the uniform range |a| < x^alpha at level (5 - alpha theta)/8;
that is wrong, because in Prop. 3.1 the supremum over a is outside the sum over q.)

### 4. Finite-X data for rung 3 (Computed at finite X only; part (iii))
q = 7, H = {1, 6}, X = 1e8 (code/parity/level_ladder.out): |A_H| = 1920725, #T_H = 297565, + share of lambda(p + 2)
on T_H 0.345, sieve-normalised ratio 1.044. At X = 1e6: |A_H| = 26159, #T_H = 4902, + share of
lambda(p + 2) on T_H 0.306, sieve-normalised ratio 1.04. Proves nothing; it only shows the rung is populated.

## Conclusion and first unresolved implication
For the pure beta-sieve at z = x^{1/2}, with the known level theorems used as black boxes, no rung beyond Iwaniec's
kappa = 1/2 is reached unconditionally. Rung 3 (p + 2 composed of primes = +-1 mod 7, dimension 2/3) is the only
candidate: its threshold level 0.6121 lies in the window (3/5, 66/107), open only to triply well-factorable weights, and
the beta_{2/3}-sieve weights are not well-factorable, hence not triply well-factorable, at their level (Finding 2);
Lichtman's anatomy-dependent sufficient condition also fails for an explicit modulus of size x^{0.55}. So a level beyond
0.612 for these weights needs new input or different weights.

First unresolved implication (the more promising route, NOT examined here): sift only to z = x^{1/u}, u > 2. Then
Bombieri-Vinogradov alone gives s = u/2 > beta_{2/3} (f_{2/3}(1.5) = 0.492 at z = x^{1/3}, f_{2/3}(2) = 0.821 at
z = x^{1/4}; computed with the same solver), the congruence still removes survivors with exactly one bad prime, and one
must subtract the survivors with two bad primes r_1 r_2 whose product lies in H (for index 3, half of the pairs of bad
cosets). That is a Chen-Iwaniec switching problem at level 1/2, of the type of Iwaniec's own kappa = 1/2 device. By rough
heuristics it is borderline, not obviously hopeless; no evidence either way here. If any version held, it would give
T_H(x) >> x/(log x)^{5/3}, an unconditional dimension-2/3 analogue of Iwaniec's theorem. That is still a sieve result of
dimension < 1 and says nothing about kappa = 1 (twins), where f_1(2) = 0 and parity rules.

## Not done / caveats
- beta_kappa values are floating-point (three step sizes; no interval certificate). beta is quantised to the grid (the
  bisection lands on half-grid points), so the uncertainty is about h/2 plus discretisation, and the 1e-5 match with
  Blight at kappa = 0.75 is partly coincidental; the margin 0.0095 still exceeds it by more than 20 times.
- The general-beta support is quoted from the standard construction (OdC Ch. 11, not opened); the beta-convention reading
  of Maynard's remark is supported by the elementary check in Finding 2, not by Iwaniec 1980 (not opened).
- Other sieves of dimension 2/3 (vector sieves, Iwaniec's semi-linear device, Buchstab iterations with switching) were
  not examined (switching is the first unresolved implication above); a lower sieving limit or better-factorable
  weights would change Finding 1's comparison.
- Possibly folklore; the literature search was two queries.
- Possibly folklore: the auditor knows of no source proving rung 3 or any unconditional rung kappa > 1/2 for shifted
  primes (closest: Iwaniec 1972 at kappa = 1/2; smooth shifted primes, a different problem). No novelty is claimed.
- Audit (22 Nov, fresh-context adversarial referee, read l.txt, m.txt, g.txt; re-ran the script at 1e6): 5 errors
  (triple well-factorability wrongly left open; Lichtman's (6.3) already fails for the example modulus; Maynard cited for
  the lower-bound support; Maynard's Thm 1.2 is upper-bound only; an "only if" that holds only for the beta-sieve),
  4 gaps (the switching route at z = x^{1/3} was not examined and the conclusion overstated its scope; the convention
  check can be proved; linear combinations; the auxiliary congruence under-argued) and wording fixes (l <= z, "split
  completely", uniform levels, BV gives theta < 1/2, grid quantisation, the "EXACT" label of script part (ii), a wrong
  printed note). All applied above; its two computations (the (6.3) intervals, f_{2/3}(1.5) and f_{2/3}(2)) were re-run
  here and agree. No script bug changed a result.
