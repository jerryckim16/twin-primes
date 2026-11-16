# Route card: Chen's theorem as a consistency test of the bipartite criterion (Session 27, 16 Nov 2026)

Candidate (b) of the weekly review of 16 Nov. Bounded attempt; method as in mathbox:research-attempt (not available; done by
hand, literature by a helper agent, proofs audited by a fresh-context helper).

## Question
Prop. bipartite (parity paper) says which close-prime targets Liouville-pattern weights block. Chen's theorem (infinitely many
primes p with p+2 in P_2) is a theorem proved by sieve methods (with Chen's switching). Does the criterion predict, correctly,
that Chen's target is NOT blocked? And what does it predict for the two halves (p+2 prime; p+2 = exactly two primes)?

## Success / no-go criteria (fixed before work)
- Success (consistency): the class does not block Chen's target; then record the prediction for the halves and compare with the
  literature (is "p+2 exactly semiprime infinitely often" open, as the class would predict?).
- No-go (inconsistency, would be a real finding): the class blocks Chen's target, i.e. a non-negative fair weight kills it.
  That would mean the heuristic class is too strong (it would "block" a theorem).

## Work
- Positions (n, n+2), signs (e1, e2). Primes have lambda = -1; P_2 numbers have either sign. A weight that kills Chen's target
  vanishes on both patterns with e1 = -1, so its first singleton coefficient is sum w(1, .) > 0 unless w = 0: no non-negative
  weakly fair weight exists. Lean-checked: chen_no_weakly_fair_weight (lean/TwinPrimes/Parity.lean).
- Halves: 1 - e1 e2 is fair and kills (-1,-1) (twin primes); 1 + e1 e2 is fair and kills (-1,+1) (n prime, n+2 with lambda = +1,
  e.g. exactly two prime factors). Lean-checked: chen_twin_half_weight, chen_semiprime_half_weight (decide, no axioms).
- Literature (notes/sources-chen-parity.md, read by a helper this run): Tao 2007 blog ("cannot hope to use plain sieve theory to
  just count primes, or just count semiprimes"); Pintz arXiv:1004.1065v1 p. 1 (not known whether infinitely many p with p+2 having
  an odd number of prime factors); Tao 2015 Supplement 5, Theorem 5 (Chen). Constants: Chen-type lower bound 1.104 Pi(x) (Wu
  2004), 1.2759 Pi(x) (R. Li arXiv:2405.05727v4, preprint); twin upper bound 3.29956 Pi(x) (Lichtman, ANT 2025). Lower < upper,
  so Chen does not give either half alone.
- Under EH, the parity paper's Prop. bomb-twin(1) is the quantitative form for the mirror target (n+2 prime, n in P_2):
  the halves weighted by Lambda log and Lambda*Lambda add up to 4 C_2 x log x (Tao 2016 notes: delta_x and 2 - delta_x).

## Classification
CONSISTENT (success criterion met). Confirms the criterion against a theorem; no new mathematics; folklore in substance (Tao 2007
says the same in words). Entered the paper as one short remark (rem:chen), per the review rule. First unresolved implication:
none new (each half is the parity problem itself).

## Not to repeat
Any "union of the two parity halves" target (P_2, or "Omega(p+2) <= r") is unblocked for the same reason; any target fixing
lambda(p+2) is blocked. No further attempts of this kind.
