# Route card: levels of distribution beyond 1/2 on the sifting-dimension ladder (22 Nov 2026, Session 44)

**Classification: located (computed thresholds + literature read in the sources; one gap of standard type; possibly folklore).**
Not in the parity paper (v1.0.1 frozen). No progress on twin primes and no way around parity.
Follows the Session 43 card [2026-11-22-dimension-ladder.md](2026-11-22-dimension-ladder.md), which left open
"whether a well-factorable level beyond 1/2 (Bombieri-Friedlander-Iwaniec type) gives any rung unconditionally".

## Question
Session 43: requiring every prime factor of p + 2 to lie in a set of primes of relative density 1 - kappa gives a sieve
problem of dimension kappa, and a congruence removes the one large prime left after sifting to z = x^{1/2}. With
level y = x^theta the beta-sieve parameter is s = log y / log z = 2 theta, and the lower bound is non-trivial iff
2 theta > beta_kappa. Bombieri-Vinogradov (theta = 1/2) reaches only kappa <= 1/2 (Iwaniec's case, with his extra
device at the boundary). Which rungs do the known levels beyond 1/2 reach?

- Success criterion: some rung kappa > 1/2 with 2 theta > beta_kappa for a level theta that is PROVED for weights of the
  kind the beta_kappa-sieve needs; this would be an unconditional theorem (p + 2 composed of primes from a set of
  density <= 1/3) beyond the half-dimensional case.
- No-go criterion: every rung needs either a level above all known levels, or a level known only for a weight class
  (well-factorable / triply well-factorable) that the beta_kappa-sieve weights do not belong to.

## Setting (Proved here; elementary; the Session 43 reduction with a subgroup)
Abelian rungs only: q prime, H < (Z/q)^* of index m, Q_H = {primes l : l mod q in H}, kappa_m = 1 - 1/m, and
T_H(x) = #{p <= x : p + 2 mod q in H, every prime factor of p + 2 in Q_H}. Sift {p + 2 : p + 2 mod q in H} by the
odd primes l != q, l mod q not in H, up to z = (x + 2)^{1/2}. A survivor m has at most one prime factor r outside Q_H
(two would exceed z^2), and if m = r m' with m, m' in H then r is in H: contradiction. So T_H(x) = S(A_H, z), a sieve of
dimension kappa_m (prime number theorem mod q). Rung 2 is q = 3 (or H = squares), rung 3 is for example q = 7,
H = {1, 6} (primes = +-1 mod 7, i.e. split in the real cubic field Q(cos 2 pi/7)).
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
  Thm 1.2 (well-factorable linear sieve weights, level 7/12); and: "Iwaniec [14] showed that a slight variant of the upper
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
(well-factorable linear sieve weights), Maynard 3/5 (triply well-factorable), Lichtman 66/107 = 0.6168 (triply
well-factorable), Lichtman 5/8 (triply well-factorable, under Selberg's eigenvalue conjecture):
- Rung 3 (kappa = 2/3) sits between 3/5 and 66/107: s = 2 * 66/107 = 1.2336 exceeds beta_{2/3} = 1.2241 by 0.0095
  (the step-size spread of beta is 4e-4), with f_{2/3}(1.2336) = 0.026; at 5/8, f_{2/3}(1.25) = 0.069. Every level
  known for well-factorable (not triply) weights is below the threshold.
- Rungs m >= 4 need theta > 0.699, beyond every known level, even 5/8 under Selberg's conjecture.

### 2. The beta_{2/3}-sieve weights are not well-factorable at their level (Proved here; exact; elementary)
The lower-bound beta-sieve support is {d = p_1 ... p_r, p_1 > ... > p_r : p_1 ... p_{m-1} p_m^{beta+1} < D for every
even m <= r} (the linear case written in Lichtman Sect. 6.1 and Maynard p. 6 with exponent 3 = beta + 1; the general-beta
form is the standard one of OdC Ch. 11, NOT opened here). Take p_1, p_2, p_3 primes near D^{3/10}. The only
condition (m = 2) is p_1 p_2^{beta+1} ~ D^{0.3 (beta + 2)} = D^{0.967} < D for beta <= 1.225; so d = p_1 p_2 p_3 ~
D^{0.9} is in the support. Its divisors have sizes D^0, D^{0.3}, D^{0.6}, D^{0.9}, so d has no factorisation
d = q_1 q_2 with q_1, q_2 <= D^{1/2}: any sequence supported on such d with lambda_d != 0 is not well-factorable of level
D (Def. 1.3). With D = x^theta, theta in (0.61, 0.63), d ~ x^{0.55} lies above the Bombieri-Vinogradov range and
p_i ~ x^{0.18} < z, so this modulus genuinely needs the beyond-1/2 estimate. For the linear sieve the same d is
excluded (p_1 p_2^3 ~ D^{1.2}). The obstruction is exactly that beta_{2/3} < 2: the parity-indexed conditions no longer
imply the conditions p_1 ... p_{m-1} p_m^2 < D for all m (the set D^well), because p_m^2 <= p_{m-1}^beta fails.
(Triple well-factorability is not decided by this example; for d = p_1 p_2 p_3 with three equal factors it holds.
It is not claimed either way here.)

### 3. One gap of standard type: the auxiliary congruence mod q (not an obstruction)
The target needs p + 2 mod 7 in H in addition to p = -2 mod d. Lichtman's and Maynard's theorems are stated for one fixed
residue and Siegel-Walfisz coefficients. In the Type II sums the extra condition splits as 1_{nm = b (7)} =
sum_{uv = b} 1_{n = u (7)} 1_{m = v (7)}, but the restricted coefficients no longer satisfy (2.2) as stated. A version
with a fixed auxiliary modulus is presumably routine; it is not stated in the sources. (An earlier draft of this card
argued that the residue mod 7d varies with d and invoked the uniform range |a| < x^alpha at level (5 - alpha theta)/8;
that is wrong, because in Prop. 3.1 the supremum over a is outside the sum over q.)

### 4. Finite-X data for rung 3 (Computed at finite X only; part (iii))
q = 7, H = {1, 6}: see code/parity/level_ladder.out (X = 1e8). At X = 1e6: |A_H| = 26159, #T_H = 4902, + share of
lambda(p + 2) on T_H 0.306, sieve-normalised ratio 1.04. Proves nothing; it only shows the rung is populated.

## Conclusion and first unresolved implication
Unconditionally, no rung beyond Iwaniec's kappa = 1/2 is reached by this route. Rung 3 (p + 2 composed of primes
= +-1 mod 7, dimension 2/3) is the only candidate: its threshold level 0.6121 lies in the window (3/5, 66/107), open
only to triply well-factorable weights, and the beta_{2/3}-sieve weights are not even well-factorable at their level
(Finding 2). First unresolved implication: a level > 0.6121 for (a modification of) the lower-bound sieve weights of
dimension 2/3 with sifting limit < 1.234 (for example an anatomy-dependent level in Lichtman's style, Sect. 6, for the
beta_{2/3}-support), together with the auxiliary-congruence version (Finding 3). If it held, it would give
T_H(x) >> x/(log x)^{5/3}, an unconditional dimension-2/3 analogue of Iwaniec's theorem; the margin is thin
(f = 0.026 at 66/107). This would still be a sieve result of dimension < 1 and says nothing about kappa = 1 (twins),
where f_1(2) = 0 and parity rules.

## Not done / caveats
- beta_kappa values are floating-point (three step sizes; no interval certificate). The margin 0.0095 is about 20 times
  the step-size spread.
- The general-beta support is quoted from the standard construction (OdC Ch. 11, not opened); the beta-convention reading
  of Maynard's remark was not checked in Iwaniec 1980.
- Other sieves of dimension 2/3 (vector sieves, Iwaniec's semi-linear device, Buchstab iterations with switching) were
  not examined; a lower sieving limit or better-factorable weights would change Finding 1's comparison.
- Possibly folklore; the literature search was two queries.
- Audit: see the section below.
