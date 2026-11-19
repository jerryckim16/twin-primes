# Route card: bilinear structure in the MIDDLE of a twin pair (19 Nov 2026, Session 35)

Bounded attempt (about 1.5 hours). Nothing here bears on the twin prime conjecture, which stays OPEN. The parity paper is
frozen at v1.0; this card is NOT in the paper.

## Why this mechanism (new for the project)
Every parity-breaking result we have read (FI98 a^2+b^4, HB01 x^3+2y^3, Green-Sawhney x^2+ny^2) gets its Type II input
from multiplicative structure of the SIFTED quantity (a norm form). For a twin pair p, p+2 the sifted numbers have no such
structure, but the middle m = p+1 = 6k is composite, and if m is y-smooth it factors as m = ab with a, b in any prescribed
ranges: a Type II structure in the INDEX variable. Earlier cards did not test structure in the index set (the Session 34
card dealt with conics and lines in two variables, not with factorisations of the middle). Question: does restricting to
smooth middles give a bilinear input that separates true twins from the parity-fake weight?

## Success / no-go criteria (fixed before work)
- Success: a bilinear-in-the-middle statistic (sums over m = ab with arbitrary bounded coefficients alpha_a, beta_b,
  in residue classes) on which the true twin weight and the parity-fake weight provably differ by a main-term amount.
- No-go: the fake weight matches every such statistic up to an error that is itself a Chowla-type correlation expected
  (and in special cases known) to be small.

## Setup
M a set of middles m <= X (e.g. y-smooth m, 6 | m). f(m) = lambda(m-1) lambda(m+1), lambda the Liouville function.
Fake weight w(m) = 1 - f(m) in {0, 2}: w(m) = 0 whenever Omega(m-1) and Omega(m+1) have the same parity, in particular
whenever m-1, m+1 are both prime. Data a sieve-plus-Type-II argument for W(M) = #{m in M : m-1, m+1 prime} may use:
- Type I in the sifted variables: A_g(d1, d2) = sum_{m in M, d1 | m-1, d2 | m+1} g(m), d1 d2 <= D;
- bilinear in the middle: B_g(alpha, beta; q, r) = sum_{ab in M, ab <= X, ab = r mod q} alpha_a beta_b g(ab),
  |alpha_a|, |beta_b| <= 1, a, b in dyadic ranges.

## Result
1. (Proved here; trivial) A_w = A_1 - A_f and B_w = B_1 - B_f. So any argument that is linear in the sequence (as
   sieve lower bounds are) and uses these data only up to an error eta |M| gives the same lower bound for the sequence
   1_M w (normalised by its mass, which is |M| - A_f(1,1)) as for 1_M, whenever all |A_f|, |B_f| <= eta |M|. Since
   1_M w gives zero weight to every twin middle, such an argument cannot prove W(M) > 0. Hence middle-bilinear data
   break parity for "twins with middle in M" ONLY IF some B_f (or A_f) is large: a failure of a bilinear two-point
   Chowla statement, the opposite of what is expected.
2. (Proved here; trivial; the contrast) For a twist in a SIFTED multiplicative variable the analogous statistic is
   maximal: with g(n) = lambda(n) and alpha = beta = lambda on the ranges, sum alpha_a beta_b lambda(ab) = #(a, b)
   exactly, because lambda(ab) = lambda(a) lambda(b). This is the mechanism of FI98 / HB01 / GS (via a norm form) and of
   Tao's bilinear step (lambda(pn) = -lambda(n), see below). The middle variable has no such identity:
   lambda(ab-1) lambda(ab+1) does not factor through a and b.
3. (Literature; Tao16 Thm 1.2 as stated in papers/parity-barrier, subsec:typeI, read 17 Nov) For each FIXED a the slice
   sum_{x/w0 < b <= x} lambda(ab-1) lambda(ab+1)/b = o(log w0) (take a1 = a2 = a, b1 = -1, b2 = 1, a1 b2 - a2 b1 = 2a != 0).
   So the fixed-a, log-averaged slices of B_f are KNOWN to be small: they confirm the obstruction. The full statement
   (uniform in alpha, beta over a ~ A, b ~ B with A, B -> infinity, natural averages) is open; it is at least as hard as
   two-point Chowla in arithmetic progressions (alpha = point mass) -- open.
4. (Computed; heuristic evidence, not a certificate) code/parity/middle_bilinear.py at X = 1e8, a, b in (3000, 6000]:
   lower bounds for the infinity->1 norm sup_{alpha, beta = +-1} sum alpha_a beta_b M[a,b] by alternating maximisation
   (20 starts): M_mid = lambda(ab-1)lambda(ab+1): 233972 = 0.026 AB = 1.007 sqrt(AB(A+B)); random +-1 matrix: 233890
   (1.007); M_sift = lambda(ab): 9000000 = AB exactly (witness alpha = beta = lambda). Restricting to ab = r mod 3 changes
   nothing (cut lower bounds 164072, 88448, 88452 on 5e6, 2e6, 2e6 cells). Same pattern at X = 1e6, A = 300 (1.007,
   0.997, 12.25 in units of sqrt(AB(A+B))). The middle twist looks like a random sign matrix; the alternating maximisation
   finds only a lower bound, so this is consistent with, not a proof of, bilinear Chowla in this range.
5. (Computed; context) Twin middles are smoother than typical multiples of 6 (for p >= 5, p | k has density 1/(p-2) among
   twin centres k, 1/p among all k): at X = 1e8 the y-smooth proportion is 0.490 / 0.146 / 0.035 / 0.0090 for
   y = X^{1/2}, X^{1/3}, X^{1/4}, X^{1/5}, against 0.438 / 0.111 / 0.021 / 0.0045 for all multiples of 6
   (ratios 1.12, 1.32, 1.64, 2.02). The fake weight is fair on smooth middles numerically: mean of f over smooth middles
   +0.0004 (y = X^{1/3}, 1841921 middles), -0.0012 (y = X^{1/4}, 357187 middles).

## Related literature (read this run)
A. V. Kontorovich, *A pseudo-twin primes theorem* (title spelled "Pseduo" on arXiv), arXiv:math/0507569v3 (4 Aug 2010),
11 pp., SHA-256 df63e6eba015f953e0dc258e02d4d6f3d4c0f09442c40f76946cfa45f744dd03 (PDF not kept). Read pp. 1-6
(Sections 1-3 start). Thm 1.1: #{p <= x : p = floor(iL(n)) for some n} ~ x/log^2 x (constant 1, "no arithmetic
interference"); the companion condition is detected by floor(Li(p+1)) - floor(Li(p)) and expanded through psi(Li(p)),
so the proof needs exponential sums sum Lambda(n) e(h Li(n)) (Vaughan's identity in n, van der Corput). The bilinear
structure is again in the SIFTED variable n; the companion set is Fourier-controlled, which the condition "p + 2 prime"
is not. Consistent with item 2.

## Classification
**Located (no-go modulo an expected Chowla-type statement; elementary; folklore in substance).** Bilinear structure in
the index (middle) variable cannot separate twins from the fake weight unless bilinear two-point Chowla FAILS; the
known special case (Tao16, fixed a, log-averaged) and the numerics point the other way. Parity-breaking Type II input
must live in a variable whose Liouville value factors (a sifted variable with multiplicative structure), which the twin
pair does not have. The principle "Type II must be in the sifted variable" is folklore (FI98, HB01 introductions); the
statement for the middle of a twin pair and the checks above are this card's content.
First unresolved implication: none toward twins (a no-go). The open statement it names (bilinear Chowla in the middle)
would CONFIRM the obstruction. Not in the paper. No parity-breaking content.

## Audit
See the section "Audit" appended below after the fresh-context review.
