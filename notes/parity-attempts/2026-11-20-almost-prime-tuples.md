# Almost-prime k-tuples and the parity class: the limit DHL_Omega[k; floor(3k/2)]

Session 37 (7:34 PM CT slot of 19 Nov 2026, run 01:34 UTC 20 Nov). Bounded attempt (about one hour). Nothing here
bears on the twin prime conjecture, which stays OPEN. The parity paper is frozen at v1.0; this card is NOT in the paper.

## Question
A different target family from all earlier cards: almost-prime tuples. For an admissible k-tuple of linear forms
L_1, ..., L_k and P(n) = L_1(n) ... L_k(n), DHL_Omega[k; r] is the statement "Omega(P(n)) <= r for infinitely many n"
(notation of Lewulis, arXiv:2203.09432v1, Problem 2). Twin primes are DHL_Omega[2; 2] for (n, n+2); Chen's theorem gives
DHL_Omega[2; 3]. What does the Liouville-pattern (PM8b-type) class of parity obstructions forbid for general k, and is
it the bottleneck of the known results?

## Success / no-go criteria (fixed before work)
- Success: an exact characterisation of the blocked pairs (k, r) in the class, with proof, consistent with Chen at k = 2
  and with Polymath8b's DHL[3,2] under GEH; and an honest comparison with the best published values.
- No-go: the class gives nothing beyond a previous card (then record that and stop).

## Class (as in the bipartite card, 2026-11-15)
Weights w(n) = W(lambda(L_1(n)), ..., lambda(L_k(n))), W >= 0 on {+-1}^k, not identically 0, fair (singleton Fourier
coefficients 0, i.e. the sign -1 has density exactly 1/2 at each position under w) or weakly fair (density >= 1/2).
The class itself is the heuristic part (Moebius randomness of the twisted inputs, PM8b p. 70). A weight blocks a target
iff W vanishes on every sign pattern compatible with the target.

## Result (Proved here, for the class; an immediate corollary of the bipartite criterion; possibly folklore)
1. Sign-space identity. For n large each L_i(n) > 1, so Omega_i := Omega(L_i(n)) >= 1, and lambda(L_i(n)) = -1 iff
   Omega_i is odd. A pattern with t plus signs needs sum Omega_i >= k + t (each plus sign means Omega_i even, >= 2), and
   k + t is attained (1 at minus, 2 at plus). So the patterns compatible with Omega(P) <= r are exactly those with at
   least 2k - r minus signs: in this class DHL_Omega[k; r] is indistinguishable from DHL[k, 2k - r]
   (at least 2k - r of the L_i(n) prime).
2. Hence (bipartite criterion: DHL[k, m+1] is blocked iff k <= 2m) DHL_Omega[k; r] is blocked iff
   r <= floor(3k/2) - 1. Direct proof: with s0 = r - k + 1 the weight lives on patterns with t >= s0; fairness gives
   E[t] = sum_i P(+ at i) = k/2 (weakly fair: <= k/2), so s0 > k/2 is impossible; for s0 <= floor(k/2) the uniform
   weight on the layer t = k/2 (k even), or the half/half mixture of the layers t = (k-1)/2 and (k+1)/2 (k odd), is fair
   and vanishes on every compatible pattern. Example k = 3, r = 3: W = 3 - (ab + bc + ca) (zero iff a = b = c).
3. The smallest unblocked value is r = floor(3k/2), which forces at least ceil(k/2) primes among the L_i(n).

## Comparison with the literature (Literature, read in the sources)
| k | class limit floor(3k/2) | best known under GEH | best known unconditionally |
|---|---|---|---|
| 2 | 3 | 3 (Chen) | 3 (Chen) |
| 3 | 4 | 6 (Sono 2016, as tabulated by Lewulis) | 7 (Maynard, arXiv:1205.5021) |
| 4 | 6 | 8 (Lewulis 2022) | 11 (Maynard) |
| 5 | 7 | 11 | 14 (Lewulis 2018) |
| 6 | 9 | 14 | 18 |
| 7 | 10 | 17 | 21 (Lewulis 2022) |
| 8 | 12 | 21 | 25 |
| 9 | 13 | 24 | 29 |
| 10 | 15 | 27 | 33 |
Large k: known r_k ~ (1/2) k log k (Franze, arXiv:1111.2003v1, abstract and Thm 1.1); the class limit is ~ 3k/2.
Sources opened (pdftotext; SHA-256 prefixes): Lewulis arXiv:2203.09432v1 (7662e4a3e25589dd; Table A, Theorem 4 / Table B,
and p. 12: "In the k = 2 case ... passing through the constant 3 seems impossible, most probably because of the parity
obstruction as mentioned in [Pol14]"); Lewulis arXiv:1806.09034v3 (292dc2881748fa63; Tables A, B, Thm 1.11);
Maynard arXiv:1205.4610 (8a2bfe83a6d31843; Tables 1-2) and arXiv:1205.5021 (a59bd98f635d2d76; r_3 = 7, r_2 = 3 by the
same method); Franze arXiv:1111.2003 (57c06a1e6b8338f9). Sono 2016 and Porter 1972 not opened (values quoted from
Lewulis's Table A).

## Classification: located (consistency test; no parity-breaking content)
- k = 2: the class is sharp; Chen's DHL_Omega[2; 3] sits exactly at the class limit, as Lewulis remarks.
- k >= 3: every published value, even under GEH, is well above the class limit (gap 2 at k = 3, 4; 12 at k = 10;
  ~ (1/2) k log k against 3k/2 asymptotically). So for k >= 3 the bottleneck of the almost-prime k-tuple results is
  NOT the parity obstruction of this class but the Omega-weighting technology.
- First unresolved implication (concrete, not parity-blocked in the class): under GEH, DHL_Omega[3; 4], i.e. for
  (n, n+2, n+6): two primes and the third a P_2, the Chen-type strengthening of Polymath8b's DHL[3,2]. Best known: 6.
- Iwaniec's n^2 + 1 = P_2 against n^2 - 1 = (n-1)(n+1): the reducible case is the k = 2 tuple, where "Omega <= 2" is
  the twin target (blocked) and "Omega <= 3" is Chen (not blocked). For the irreducible n^2 + 1 there is no
  prime-detecting input at that position, so no fairness constraint applies there; "Omega <= 2" is compatible with both
  signs, so only W = 0 kills it (not blocked), while "n^2 + 1 prime" is killed by 1 + lambda(n^2 + 1) (Selberg's example).
  Consistent with what is known; recorded only as a consistency check (folklore).

## What this is not
No statement about any new sieve result; nothing about twin primes beyond the k = 2 consistency; the class is heuristic;
"not blocked in the class" never means "provable". Literature-check: the sources above and two web searches (20 Nov) found
no statement of the limit floor(3k/2) for k >= 3 ("possibly folklore"); mathbox not available.

## Checks
- code/parity/almost_prime_tuples.py (/usr/bin/python3 -I; 2 s; output .out): (1) the sign-space identity by enumeration of
  Omega-vectors (entries <= 4, k <= 7, r in [k, 2k]); (2) LP feasibility (scipy HiGHS) for k <= 10, r in [k, 2k], fair and
  weakly fair; (3) an independent exact check in rationals (explicit layer weights; averaging obstruction); all agree with
  r <= floor(3k/2) - 1.
- Lean: the k = 3, r = 4 case is the existing theorem triangle_no_fair_weight (TwinPrimes/Parity.lean): its four killed
  patterns (at least two minus signs) are exactly the patterns compatible with Omega(P) <= 4.
