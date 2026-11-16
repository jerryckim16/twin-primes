# Route card: Pintz's parity-sensitive dichotomy with Maynard weights (Session 26, 16 Nov 2026)

## Question
Pintz (arXiv:1004.1065v1, 2010) proved, with GPY weights and Bombieri-Vinogradov, that for every admissible 6-tuple H and
r not in H, infinitely many n have two primes in n+H or a prime n+h_i with lambda(n+r) = -1; hence some even d, 0 < |d| <= 16,
has lambda(p+d) = -1 for infinitely many primes p. This is a genuine parity-sensitive statement about shifted primes that
sidesteps (does not break) the obstruction. What do Maynard's weights give, and does the bipartite criterion of the parity
paper predict exactly which such statements are reachable?

## Success / no-go criteria (set before the work)
- Success: a full proof that the dichotomy needs only theta*M_k > 1, the lambda-twisted sum controlled for Maynard weights by
  BV for lambda (Pintz Lemma 3), and M_5 > 2 certified exactly by two independent programs.
- No-go: the lambda sum cannot be controlled for Maynard's weights (e.g. W-trick or gcd issues), or the criterion is not
  linear in the prime sums.

## Cheapest decisive check
Pintz's proof (3.4)-(3.21) read in the source: the criterion is S_P > A/2, i.e. the prime sums must beat half the weight. In
Maynard's normalisation, sum_m S_2^(m) / S_1 -> (theta/2) M_k(F), so the criterion is theta M_k > 1. Maynard (8.16)-(8.17)
gives M_5 >= 1417255/708216 > 2 (read in arXiv:1311.4600v3).

## Result (classification: PROVED, modest; possibly folklore)
- Parity paper v0.11, Theorem thm:pintz-maynard, Corollary cor:pintz12: unconditionally, some even d with 0 < |d| <= 12 (Pintz: 16),
  and some even 0 < d <= 14 (Pintz: 18), have lambda(p+d) = -1 for infinitely many primes p; either liminf gaps <= 12 or
  lambda(p+d) = sigma infinitely often for some d in {+-2, +-4, -8}, each sigma; conditional thresholds 0.72154 / 0.60752 /
  0.54230 for 2-, 3-, 4-tuples (Pintz 0.729 / 0.616 / 0.554).
- Computed: code/parity/pintz_maynard.py (exact Dirichlet formula) and code/parity/pintz_maynard_check2.py (written by a helper
  without seeing the first; iterated sympy integration): Maynard's 1417255/708216 and the four optimised ratios agree exactly.
- Parity consistency (Remark rem:pintz-parity): the target is the complete graph on H ∪ {r} (not bipartite, so not blocked);
  without the two-prime alternative it is a star (bipartite, blocked), which is Pintz's remark that EH does not give one
  prescribed d.
- First unresolved implication toward twin primes: a single prescribed d (e.g. lambda(p+2) = -1 infinitely often) is a
  star target and is blocked for this whole class of arguments. Nothing here moves toward that.

## Literature check
Three web searches (Pintz odd number of prime factors p+d Maynard; lambda(p+2) Maynard-Tao weights; Pintz Maynard parity
lambda(p+d) = -1) found no improvement of Pintz's 16. Not searched: MathSciNet, later papers citing Pintz 2010 one by one.
Label: possibly folklore.

## Do not repeat
The same disjunction trick with a single extra position is done. Products lambda(n+r1)lambda(n+r2) need Chowla-type
correlations along the weight (not available). Enlarged supports do not apply directly: the lambda-twisted sum would need
moduli beyond x^{1/2} (exploration of Session 26).
