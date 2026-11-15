# Which "close prime" targets does the Polymath8b parity obstruction block? (a bipartite / fractional-stable-set criterion)

- **Date:** 2026-11-15 (Session 18). Kind: attempt (locate the barrier precisely; reformulation of a known obstruction).
- **Target:** PM8b §8 blocks H_1 <= 4 with the weight (1 - lambda(n)lambda(n+2))(1 - lambda(n+2)lambda(n+6)) and, in Remark 8.1,
  any window, with a product weight "left to the reader". Question: for an arbitrary target "some configuration e in a family E of
  subsets of the tuple consists of primes", exactly when does a weight of the same kind exist? Does the criterion explain the
  number 6, and what does it say about H_m?
- **Mechanism class (stated precisely):** pattern weights omega(n) = Omega(lambda(n+h_1), ..., lambda(n+h_k)), Omega >= 0, not
  identically 0. Under the Moebius-randomness heuristic of PM8b p. 70, the twisted inputs (144)-(145) keep the same shape iff the
  singleton Fourier coefficients vanish (fake primes at each position have relative density exactly 1/2; "<= 0", density >= 1/2,
  gives the same answer). The weight blocks the target iff Omega vanishes on every pattern whose -1 set contains some e in E.
- **Success criterion:** an exact combinatorial characterisation, with proof, that reproduces PM8b's two cases (H_1 <= 4 blocked,
  DHL[3,2] not blocked). **No-go criterion:** no clean characterisation, or one that contradicts PM8b's statements.
- **Cheapest decisive check:** LP feasibility on random small graphs vs bipartiteness; PM8b Remark 8.1's weight evaluated exactly.
- **Outcome: proved (for the stated class; the class itself is the heuristic part).** Paper Prop. prop:bipartite (Proved here,
  possibly folklore):
  - a blocking weight exists iff (1/2, ..., 1/2) is a convex combination of indicator vectors of E-free sets;
  - for pairs (a graph G): iff G is bipartite (odd cycles C_{2r+1} carry at most r of an independent set, mean (2r+1)/2);
  - DHL[k, m+1] is blocked iff k <= 2m (so DHL[3,2] is not blocked, as PM8b's GEH theorem requires);
  - windows: a sieve proof of "m+1 primes in a window of length g" from the tuple H is blocked iff every such window holds <= 2m
    elements of H (alternating colouring); hence this class of obstructions forbids exactly the bounds H_m < H(2m+1), where H(k)
    is the narrowest admissible k-tuple: H(3) = 6 (the parity limit of PM8b), H(5) = 12, H(7) = 20 (brute force, witnesses
    Lean-checked admissible). For m >= 2 this is far below every known conditional H_m bound, so the class is sharp only at m = 1
    (as far as is known).
- **Literature finding (flag, minor):** PM8b Remark 8.1 (arXiv:1407.4897v4, p. 70) prints the weight as a product over
  0 <= i <= i' <= H with (n+i,3) = (n+i',3) = 1 and i' - i <= 4. Taken literally it is identically zero: the factor i = i' is
  1 - lambda(n+i)^2 = 0; and even with i < i' the positions coprime to 3 include even integers, among which there are triangles
  (e.g. n+1, n+2, n+4 for 3 | n), so the product vanishes for every n once H >= 4 (computed for n < 2000). The intended weight
  (i < i', n+i and n+i' odd, i.e. positions = +-1 mod 6, which form a path with gaps 2, 4) works: it vanishes whenever two primes
  > 3 at distance <= 4 lie in [n, n+H] (computed for n < 20000; the two exceptions n = 1, 2 involve the prime 3). The criterion
  explains why: the corrected graph is a path (bipartite); the printed one has odd cycles. Typo-level; no result changes.
- **Checks:** code/parity/bipartite_obstruction.py (400 random graphs: LP feasibility = bipartiteness in all 400; Remark 8.1 printed
  vs corrected; H(k) for k <= 9); Lean lean/TwinPrimes/Parity.lean (triangle: every non-negative fair weight killing all pairs is
  0; the PM8b path weight is non-negative, fair, kills {0,2} and {2,6}; narrow 5- and 7-tuples admissible). Audit: fresh-context
  adversarial helper (mathbox not available), see the paper changelog.
- **What this is and is not:** a sharp statement of what the PM8b-type obstruction covers. It does NOT show that non-bipartite
  targets are provable by sieves (that is the open part: only DHL[3,2] under GEH is known); it says nothing outside the class of
  Liouville-pattern weights; and it does not touch twin primes (the twin target is an edge, bipartite, blocked).
- **First unresolved implication:** whether some *other* weight class (depending on more than Liouville signs on the tuple, e.g.
  on lambda at shifts outside H together with residue classes, or on mu*1-type functions) blocks a non-bipartite target such as
  DHL[5,3] (H_2 <= 12). Marginalising shows extra Liouville coordinates do not help (stated in the paper); other classes are Open.
- **Literature-check:** two standard web searches (15 Nov) found no statement of the general criterion or of "H_m >= H(2m+1)";
  "possibly folklore".
- **Disposition:** closed (proved for the class). Continuation: the "other weight classes" question above.
