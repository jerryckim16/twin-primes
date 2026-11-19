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

## Success / no-go criteria (fixed before work; M5 of the audit made precise)
- Success: a bilinear-in-the-middle statistic (sums over m = ab with arbitrary bounded coefficients alpha_a, beta_b,
  in residue classes) on which the true twin weight and the parity-fake weight, both normalised to mass |M|, provably
  differ by >> |M|/log^2 X (the size of the twin count).
- No-go: the fake weight matches every such statistic up to an error that is itself a Chowla-type correlation expected
  to be small.

## Setup
M a set of middles m <= X (e.g. y-smooth m, 6 | m). f(m) = lambda(m-1) lambda(m+1), lambda the Liouville function.
Fake weight w(m) = 1 - f(m) in {0, 2}: w(m) = 0 whenever Omega(m-1) and Omega(m+1) have the same parity, in particular
whenever m-1, m+1 are both prime. Data a sieve-plus-Type-II argument for W(M) = #{m in M : m-1, m+1 prime} may use:
- Type I in the sifted variables: A_g(d1, d2) = sum_{m in M, d1 | m-1, d2 | m+1} g(m), d1 d2 <= D;
- bilinear in the middle: B_g(alpha, beta; q, r) = sum_{ab in M, ab <= X, ab = r mod q} alpha_a beta_b g(ab),
  |alpha_a|, |beta_b| <= 1, a, b in dyadic ranges.

## Result
1. (Proved here; trivial; the standard parity principle with the twisted data swapped in) A_w = A_1 - A_f and
   B_w = B_1 - B_f. Give 1_M w the main-term mass |M| - A_f(1,1) in place of |M|, so its sieve remainders are
   r_d(1_M w) = r_d(1_M) - (A_f(d) - g(d) A_f(1,1)), and similarly for the bilinear data. Any argument that is linear in
   the sequence and uses only non-negativity and these data with total error budget E gives a lower bound for
   sum 1_M w 1_twin = 0 within E of its lower bound for W(M) (1_M w gives zero weight to every twin middle). It therefore
   cannot prove W(M) >> |M|/log^2 X unless
   sum_{d1 d2 <= D} |A_f(d) - g(d) A_f(1,1)| + sum over the bilinear data used of |B_f| (each B_f measured against its
   own number of pairs #{(a,b): a ~ A, b ~ B, ab in M})
   FAILS to be o(|M|/log^2 X). The A_f part is the usual two-point Chowla-in-progressions input of the parity principle;
   the B_f part is a bilinear two-point Chowla statement. Middle-bilinear data break parity for "twins with middle in M"
   only if one of these fails, the opposite of what is expected.
2. (Proved here; trivial) For a twist in a multiplicative SIFTED variable the analogous statistic is maximal: with
   g(n) = lambda(n) and alpha = beta = lambda on the ranges, sum alpha_a beta_b lambda(ab) = #(a, b) exactly, because
   lambda(ab) = lambda(a) lambda(b). (Literature, our reading) This is the mechanism of FI98 / HB01 / Green-Sawhney
   p^2 + nq^2 (via a norm form) and of Tao's bilinear step (lambda(pn) = -lambda(n)). The middle variable has no such
   identity: lambda(ab-1) lambda(ab+1) does not factor through a and b.
3. (Literature; Tao16 Thm 1.2 as stated in papers/parity-barrier, subsec:typeI, read 17 Nov) For each fixed a and the
   specific coefficients beta_b = 1/b, sum_{x/w0 < b <= x} lambda(ab-1) lambda(ab+1)/b = o(log w0) (a1 = a2 = a,
   b1 = -1, b2 = 1, a1 b2 - a2 b1 = 2a != 0). This is ONE coefficient choice: it is not an instance of the bilinear
   statement with arbitrary beta (for which a single slice can be as large as its length, beta_b = f(ab)), and it is
   consistent with the obstruction but does not confirm it. The full bilinear statement (A, B -> infinity, natural
   averages, arbitrary bounded alpha, beta) is open. Taking alpha = beta = 1 (optionally on ab = r mod q) it implies a
   divisor-weighted two-point Chowla estimate sum_{m = r (q)} tau_{A,B}(m) lambda(m-1) lambda(m+1) = o(AB),
   tau_{A,B}(m) = #{(a,b): a ~ A, b ~ B, ab = m}, which is open; by Cauchy-Schwarz it follows from the four-point
   correlations sum_b lambda(ab-1)lambda(ab+1)lambda(a'b-1)lambda(a'b+1) = o(B) for most a != a', also open. (A point
   mass in alpha gives only a trivial instance, since then |B_f| <= B = o(AB).)
4. (Computed; heuristic evidence, not a certificate) code/parity/middle_bilinear.py at X = 1e8, a, b in (3000, 6000]
   (Part 1 uses ALL products ab in these ranges, without restricting to M or to 6 | ab): lower bounds for the
   infinity->1 norm sup_{alpha, beta = +-1} sum alpha_a beta_b M[a,b] by alternating maximisation (20 starts):
   M_mid = lambda(ab-1)lambda(ab+1): 233972 = 0.026 AB = 1.007 sqrt(AB(A+B)); random +-1 matrix: 233890 (1.007);
   M_sift = lambda(ab): 9000000 = AB exactly (witness alpha = beta = lambda). Restricting to ab = r mod 3 (10 starts)
   gives cut lower bounds of the same size as a random +-1 matrix with the same mask (X = 1e8: 164072, 89168, 88876 on
   5e6, 2e6, 2e6 cells against 163498, 88636, 88496; X = 1e6, A = 300: 5168, 2776, 2808 against 5230, 2832, 2800). At X = 1e6, A = 300: middle 1.007, random 0.997, sifted 12.25 in
   units of sqrt(AB(A+B)). The middle twist looks like a random sign matrix. Caveats: the alternating maximisation
   gives only a lower bound, and at A = 3000 the random scale sqrt(AB(A+B)) is already 0.026 AB, so these numerics
   cannot tell o(AB) from a small constant times AB; they are consistent with, not a proof of, bilinear Chowla here.
5. (Computed; context) Twin middles are smoother than typical multiples of 6 (Heuristic, Hardy-Littlewood: for p >= 5,
   p | k has density 1/(p-2) among twin centres k, 1/p among all k): at X = 1e8 the y-smooth proportion is 0.490 /
   0.146 / 0.035 / 0.0090 for y = X^{1/2}, X^{1/3}, X^{1/4}, X^{1/5} (y computed in floating point), against 0.438 /
   0.1105 / 0.021 / 0.0045 for all multiples of 6 (ratios 1.12, 1.32, 1.64, 2.02). The fake weight is fair on smooth
   middles numerically: mean of f over smooth middles +0.0004 (y = X^{1/3}, 1841921 middles), -0.0012 (y = X^{1/4},
   357187 middles).

## Related literature (read this run)
A. V. Kontorovich, *A pseudo-twin primes theorem* (title spelled "Pseduo" in the PDF), arXiv:math/0507569v3 (4 Aug 2010),
11 pp., SHA-256 df63e6eba015f953e0dc258e02d4d6f3d4c0f09442c40f76946cfa45f744dd03 (PDF not kept). Read pp. 1-6
(Sections 1-3 start). Thm 1.1: #{p <= x : p = floor(iL(n)) for some n} ~ x/log^2 x (constant 1, "no arithmetic
interference"; a Piatetski-Shapiro-type result, which the author says also follows from Leitmann 1977); the companion condition is detected by floor(Li(p+1)) - floor(Li(p)) and expanded through psi(Li(p)),
so the proof needs exponential sums sum Lambda(n) e(h Li(n)) (Vaughan's identity in n and van der Corput, per the outline on p. 2; Section 4, pp. 9-11, not read). The bilinear
structure is again in the SIFTED variable n; the companion set is Fourier-controlled, which the condition "p + 2 prime"
is not. Consistent with item 2.

## Classification
**Located (no-go modulo expected Chowla-type statements; elementary; folklore in substance).** Bilinear structure in
the index (middle) variable cannot separate twins from the fake weight unless two-point Chowla in progressions or
bilinear two-point Chowla FAILS at the precision o(|M|/log^2 X); Tao16 (one fixed-a, log-averaged coefficient choice)
is consistent with this, and the numerics point the same way. (Heuristic, folklore) Parity-breaking Type II input
appears to need a variable whose lambda-value factors; this card checks only the middle variable of a twin pair, for
linear arguments, conditional on bilinear two-point Chowla. The principle that bilinear input must sit in the sifted
sequence is discussed by Friedlander-Iwaniec (Opera de Cribro; not opened here) and in the introductions of FI98 and
HB01; the statement for the middle of a twin pair and the checks above are this card's content.
First unresolved implication: none toward twins (a no-go). The open statements it names would CONFIRM the
obstruction. Not in the paper. No parity-breaking content.

## Audit
Fresh-context adversarial review (helper agent, mathbox not available), 19 Nov 2026. Found 3 errors in the first draft,
all fixed: (E1) "at least as hard as two-point Chowla in APs (alpha = point mass)" was false (a point mass gives a
trivial instance); replaced by the divisor-weighted / four-point formulation. (E2) Tao16's fixed-a log-averaged slices
were called "known small slices of B_f" that "confirm" the obstruction; they are one coefficient choice and only
consistent with it. (E3) The error tolerance eta|M| had the wrong scale (must be o(|M|/log^2 X), summed over the data
used) and the wrong normalisation for B_f (its own number of pairs). Gaps fixed: Part 1 is not restricted to M (stated);
a masked random control added to the script and the run repeated; the 1/(p-2) density labelled Heuristic; the general
principle relabelled Heuristic/folklore; Literature vs Proved-here labels separated in item 2. Minor items applied
(Green-Sawhney p^2 + nq^2; Kontorovich title spelling and Section 4 not read; ordering of the X = 1e6 triple; rounding;
success criterion made precise; random scale at A = 3000). The auditor judged "folklore in substance" fair and found no
overclaim about twin primes or parity.
