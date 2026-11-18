# Route card: E2 numbers (parity-even target) as a consistency test of the bipartite criterion (18 Nov 2026)

Bounded attempt (about 45 minutes; helper agent). Nothing here bears on the twin prime conjecture, which stays OPEN.
No paper, STATE, status, README or log file was edited.

## Idea
Prop. prop:bipartite (parity paper, sec:bip) says when a fair Liouville-pattern weight kills a target. Remark rem:chen
tested it on a parity-odd target (primes, lambda = -1). Here we test it on a parity-EVEN target: E2 numbers
(n = p1 p2, p1 != p2, so lambda(n) = +1). Goldston, Graham, Pintz and Yildirim (GGPY) proved bounded gaps between E2
numbers unconditionally, and statements that they describe as overcoming the parity problem. If the class "blocked" one of
their theorems, the heuristic class would be refuted, or we would have made a mistake.

Convention (as in rem:chen): a weight sees only lambda; it kills a target if it vanishes on every sign pattern the target
can produce. An E2 value forces +1, a prime forces -1. "At least two of the n+h_i are E2" can therefore produce exactly
the patterns with at least two +1 entries. Flipping all signs maps this onto DHL-type targets, and fairness survives the flip
(marginals 1/2). So all of Prop. prop:bipartite carries over with the roles of +1 and -1 swapped.

## Success and no-go criteria (fixed before work)
- Success (consistent): every GGPY theorem is unblocked in the coordinates in which they prove it. Then record what the
  class predicts for the open neighbours (n, n+d both E2; E2 next to a prime).
- Refutation: a GGPY theorem whose target, in their own parametrisation, is killed by a non-negative fair weight. That would
  be a real finding, to investigate before anything else.
- No-go: GGPY's statements cannot be opened. (They could: all three papers were read from arXiv PDFs.)

## Sources read
Downloads are in /tmp/claude-0/e2src/{a,b,c}/paper.pdf (not committed). Text extracted with pdftotext. The page numbers
below are the PDF/printed page numbers of the arXiv versions.
- [GGPY-a] D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yildirim, "Small gaps between products of two primes",
  arXiv:math/0609615v1 (21 Sep 2006; the only version; journal version Proc. LMS 2009, not read).
  SHA-256 411a638e959e6fa41d9f489477b26a8abe6550f3a61e5f2058ccdc88a6461680.
  - p. 1, parity: "The phenomenon that we cannot specify which one of the two equations (1.3) and (1.4) has infinitely many
    solutions ... is the most significant particular case of the parity problem"; and E2 problems "seemed to be as
    difficult as problems involving primes ... due to the parity problem."
  - p. 4, Theorem 1: among any admissible k-tuple of linear forms, nu+1 forms take E2 values at once (both prime factors > D)
    if k >= C1(nu) = (4 e^{-gamma}/B)(1+o(1)) e^{B nu/4}, where B = 2/theta (B = 4 unconditionally) and o(1) is as nu -> oo
    (footnote 2).
  - p. 4, Theorem 2: in every admissible triple of linear forms, two forms are both E2 infinitely often, with all prime factors
    > n^{1/144}.
  - p. 4, Theorem 3: for every admissible pair, both values are in **P2** (not E2) infinitely often; so n, n-d are both in P2
    for every even d. This is a union target, like Chen's.
  - p. 5, Corollary 1: liminf(q_{n+nu} - q_n) <= e^{-gamma} nu e^{B nu/4}(1+o(1)). Corollary 2: liminf(q_{n+1} - q_n) <= 6,
    from Theorem 2 with {n, n+2, n+6}.
  - p. 7: they announce Erdos-type results "thereby overcoming the parity problem in these cases".
  - pp. 15, 33-36: Theorems 7-8 (the main terms J0, J1, J2, J3), criterion (8.1) and (8.15); the proof of Theorem 2 on p. 36
    (k = 3, B = 4, eta = 1/144, P = 1+6x, J = 0.00016493...).
- [GGPY-b] same authors, "Small gaps between almost primes, the parity problem, and some conjectures of Erdos on consecutive
  integers", arXiv:0803.2636v1 (18 Mar 2008; only version). SHA-256
  7dc2b2427fd1149845ac17b526849bc73d6fb6cd21a6888e4a05c06e76b1153d.
  - p. 2: "the seemingly much easier assertion that for infinitely many primes p, p + 2 (or 2p + 1) has an odd (or even)
    number of prime factors, is still open [Hildebrand, p. 310]"; p. 3: "the parity problem is not bypassed but overcome".
  - p. 3, Theorems 1-3: Omega(x) = Omega(x+1) = A for every A >= 4; omega(x) = omega(x+1) = A for every A >= 3; d(x) = d(x+1) = A
    for 24 | A. p. 4, Theorem 4 (exponent pattern {2,1,1,1}) and the "Basic Theorem" (= GGPY-a Theorem 2). pp. 4-5: the
    method, e.g. (1.11)-(1.12) L = 6m+1, 8m+1, 9m+1 with 4L1 = 3L2+1, 3L1 = 2L3+1, 9L2 = 8L3+1.
  - p. 5, Theorems 5-6: omega(x) = omega(x+2) = B for B >= 4, and Omega(x) = Omega(x+2) = B for B >= 5.
  - pp. 5-6: "(1.16) liminf(q_{n+1} - q_n) <= 6 ... Although (1.16) is clearly much stronger than (1.15), it is still
    unclear whether there is any theoretical obstacle which prevents us to find infinitely many pairs of E2-numbers with a
    fixed difference."
  - p. 6, Theorem 7: liminf(R_{n+1} - R_n) <= 2 for Omega(R) = 3. pp. 6-8: Theorems 8-12 (shift n; Hypothesis T).
- [GGPY-c] same authors, "Small gaps between primes or almost primes", arXiv:math/0506067v1 (3 Jun 2005; only version).
  SHA-256 e7b065dd7b3bb0802a699c42df400a7c32164eb6e69d33e80b570fe2ed480c3f.
  - p. 4: "While one expects that there are infinitely many primes p such that p + 2 is an E2, this appears to be as
    difficult as the twin prime conjecture"; Theorem 3: liminf(q_{n+1} - q_n) <= 26. (GGPY-a p. 2 says this came from an
    admissible 8-tuple containing two E2 numbers infinitely often.)
- A web-search summary claimed that GGPY prove "n and n+2 both E2". That is wrong: GGPY-a Theorem 3 is about P2. Disregarded.

## What was checked
Script: code/parity/e2_consistency.py, output code/parity/e2_consistency.out (/usr/bin/python3 with scipy, about 2 min).
Every blocked/unblocked verdict is certified exactly with fractions: an explicit rational fair measure on the allowed
patterns for blocked targets, and a rational Farkas hyperplane c.x <= c0 < c.(1/2,...) for unblocked ones. The LP only
proposes the certificate.
- A. "At least j of k positions E2": blocked iff k <= 2(j-1). This is the sign flip of (b), checked for k <= 8 and all j
  with 0 mismatches. "n, n+d both E2" (k = 2) is blocked by 1 - eps1 eps2, the same weight that blocks twin primes. "Two E2
  among 3" is unblocked, so GGPY-a Theorem 2 and the Basic Theorem are unblocked; so are "two among 8" (GGPY-c) and
  Theorem 1 asymptotically (C1(nu) grows exponentially, 2 nu linearly).
- B. Windows on admissible shift tuples (sign flip of (c)): "two E2 within distance g" is blocked iff every interval of
  length g holds at most 2 tuple elements. {0,2,6} is blocked at g = 2 and 4 and unblocked at g = 6; {0,2,8,12} is blocked
  at g = 6. So in shift coordinates the class blocks every proof of liminf(q_{n+1} - q_n) <= g exactly when g < H(3) = 6.
  **GGPY's bound 6 (GGPY-a Cor. 2) sits exactly at the class's limit.** This mirrors Cor. cor:six for primes under GEH.
- G. GGPY's own sieve functional (GGPY-a (8.1), Theorems 7-8). The method gives nu+1 E2 values among k forms iff
  rho = k(k-1)(J1+J2+J3)/(B J0) > nu. rho is a ratio of quadratic forms in the coefficients of P, maximised by a generalized
  eigenvalue computation (deg P <= 6, eta = 0, Gauss-Legendre; floating point). Our code reproduces the paper's numbers for
  Theorem 2: J0 = 38/15 and rho = 1.000065 > 1.
  - max rho for k = 2..8 at B = 4: 0.758, 1.004, 1.208, 1.382, 1.535, 1.671, 1.794.
  - at B = 3: 0.860, ..., 2.161.
  - at B -> 2 (EH-type level): 0.961, 1.363, 1.709, 2.012, 2.280, 2.521, 2.741.
  - Always rho < k/2 (largest ratio rho/(k/2) = 0.961, at k = 2 and B -> 2), so the method never reaches a case the class
    blocks.
  - Caution: the main-term formula C1(nu) of Theorem 1, read without its o(1), is below 2 nu for small nu (e.g. 3.05 < 4 at
    B = 2, nu = 2). That is not a contradiction, because o(1) -> 0 only as nu -> oo. The finite-k computation above is the
    real test, and it passes.
- C. Mixed targets: "some n+h_i E2 and some n+h_j prime" (i != j) is blocked for every k by 1/2 (all +) + 1/2 (all -),
  checked for k = 2..6. In particular "p prime, p+2 E2" is blocked (as in rem:chen), and the union "n prime, n+2 prime or
  E2" is unblocked (Chen). GGPY prove no mixed statement, so there is nothing to contradict.
- D. Erdos-type results (GGPY-b). In shift coordinates (x, x+1), the target Omega(x) = Omega(x+1) = A forces
  lambda(x) = lambda(x+1), so it IS killed by the fair weight 1 - lambda(x) lambda(x+1). Yet GGPY-b Theorem 1 proves it.
  - This is not a refutation. GGPY never sieve the pair (x, x+1). They sieve an admissible triple of forms in m (Basic
    Theorem; target "two of L1, L2, L3 are E2", a triangle, unblocked), and x is then c_i L_i(m) for whichever pair occurs.
  - Since lambda(c L) = lambda(c) lambda(L), every weight in the derived integers is a function of (lambda(L_i(m))). By the
    argument of rem:marg no such weight kills the triangle.
  - So the class blocks a parametrisation (a tuple of forms plus a target), not a statement. A statement is "blocked" only
    if every parametrisation that implies it is blocked.
  - Checked exactly: GGPY-b's identities (1.12), (2.2), (2.4) and (2.6)-(2.8), and the admissibility of those systems.
- E. E2 pairs at a FIXED difference d (the question GGPY-b p. 6 leaves open).
  - (i) Pure shifts, E2 values used directly. The target graph {i ~ j : |h_i - h_j| = d} is bipartite (colour h by
    floor(h/d) mod 2), so the target is blocked for every tuple. Exhaustive check: 25123 tuples (k = 2..4, shifts in
    [0,24], d in {1,2,4,6,12}), all blocked.
  - (ii) Multipliers. X = c L(m) is E2 if c = 1 and L(m) is E2, or if c is a prime and L(m) is prime. An edge with
    multipliers (c_i, c_j) needs c_i a_i = c_j a_j. It forbids the signs s = (-1)^{Omega(c)}, so s_i s_j =
    (-1)^{Omega(a_i)+Omega(a_j)}, and the product of s_i s_j around any cycle is +1.
    - Checked exactly over all 125 + 15625 signed graphs on 3 and 4 vertices (one forbidden sign pair per edge): blocked
      <=> eps_i eps_j = -s_i s_j is solvable. Hence for cycle products +1: blocked <=> the graph of forms is bipartite.
      (This is a sufficiency proof plus an exhaustive check for n <= 4; necessity is not proved in general here.)
  - (iii) **An unblocked realisation exists for 12 | d.** Take {m, m+6, m+12} (admissible) with the target "(m, m+6) both
    prime, or (m+6, m+12) both prime, or (m, m+12) both E2". Every event gives x, x+12 both E2 (2m and 2m+12,
    2m+12 and 2m+24, or m and m+12). The signed triangle has product +1, so it is unblocked (exact Farkas certificate
    c = (1,-1,1), c0 = 0).
    - For equal slopes this is forced: the only relation 1/p +- 1/q = +-1/r over {1, primes} is 1/2 + 1/2 = 1. This needs
      forms m, m+d/2, m+d, and admissibility mod 2 and mod 3 then forces 12 | d (proved by hand).
    - A search over triples with unequal slopes (a1 <= 12, a2, a3 <= 72, multipliers in {1,2,3,5,7,11,13}) found no
      admissible triangle for d in {1, 2, 4, 6, 8}, and found {m, m+12, m+6} for d = 12.
    - Longer odd cycles (k >= 5 forms) were not searched.
  - F. Numeric sanity check (m < 10^6): 16386 / 16384 / 69937 occurrences of the three events; each prime event gives an E2
    pair (asserted in the script). There are 51981 pairs n, n+2 both E2 below 10^6.

## Result
- No GGPY theorem is blocked in the coordinates in which it is proved:
  - Theorem 2 and the Basic Theorem: a triangle of E2 targets, unblocked.
  - Theorem 1: k >= C1(nu) > 2 nu asymptotically. Their finite-k functional satisfies rho < k/2 in every case computed.
  - Corollary 2 (gap 6): exactly the class's window limit H(3) = 6.
  - The Erdos-type theorems: blocked in shift coordinates (x, x+1), but proved through a triangle of linear forms, which is
    unblocked.
- What the class predicts for the open neighbours:
  - "n, n+d both E2" is blocked for every pure-shift tuple, and for every multiplier triangle we found when d is not
    divisible by 12.
  - For 12 | d it is NOT blocked, via a mixed prime/E2 triangle. No one has proved that triangle target. The pointwise
    count needs a weighted number of successes > 2 (allowed configurations reach 2). Whether GGPY-type weights achieve
    this was NOT computed; a heuristic guess (E2 ratio about 1 over three forms, prime ratios below 1) says no.
  - "E2 next to a prime" at prescribed positions is blocked for all k.

## Classification
CONSISTENT, the success criterion is met; not refuted. It confirms the criterion on a parity-even target. It also gives a
precise reading of GGPY's "overcoming the parity problem": they change coordinates, so that a blocked 2-point target
becomes an unblocked 3-form triangle. The class blocks parametrisations, not statements. That is a clarification of
the class's scope (located), not a new theorem. There is no parity-breaking content.

## First unresolved implication
Whether n, n+2 are both E2 infinitely often (more generally, E2 pairs at a fixed difference d) is OPEN. GGPY-b pp. 5-6
says "it is still unclear whether there is any theoretical obstacle which prevents us to find infinitely many pairs of
E2-numbers with a fixed difference".
- The class answers their question partly. For d = 2 there is an obstacle of PM8b type for every pure-shift tuple and for
  every three-form multiplier system in our search range.
- Unresolved: (a) whether some odd cycle of five or more forms realises d = 2 (which would remove the obstacle); (b) for
  12 | d, whether a GGPY-type sieve can prove the mixed triangle target on {m, m+6, m+12}. That would give x, x+12 both E2
  infinitely often, which is not known as far as we read.

## Possibly folklore
Tao 2014 (hull criterion), the sign flip for E2 targets, and the "change of coordinates" reading of Heath-Brown, Spiro and
GGPY are in the spirit of GGPY-b pp. 2-3 and of Heath-Brown's remark quoted there ("we avoid the parity problem, rather
than solve it"). The bipartite-in-forms observation for fixed-difference E2 pairs and the 12 | d triangle were not found in
the three sources. No wider literature search was made.

## Not to repeat
Any sign flip of a prime target to an E2 target gives the same verdict as the prime target (fairness is flip-invariant).
Future tests of this kind should fix the parametrisation (forms plus multipliers) before applying the criterion.
