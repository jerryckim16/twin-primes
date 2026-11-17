# Route card: Gowers norms and the infinite complexity of twin primes (Session 28, 17 Nov 2026)

Candidate (c) of the weekly review of 16 Nov. Bounded attempt; method as in mathbox:research-attempt (not available; done by
hand, sources read here, proof audited by a fresh-context helper: notes/audit-parity-v013.md).

## Question
Green-Tao(-Ziegler) count every finite-complexity linear pattern of primes asymptotically, something sieve weights alone cannot do.
Twin primes are excluded because (n, n+2) has infinite complexity. Is this a second, separate barrier, and can it be stated
sharply? Where does Tao's log-averaged two-point Chowla theorem get around it, and does that route transfer to Lambda?

## Success / no-go criteria (fixed before work)
- Success (location): a precise, proved statement that the information "small U^s norm for every s" (all that the finite-
  complexity theory uses about lambda or the W-tricked primes) is compatible with any value of the shift-2 correlation,
  with explicit constants; plus a sourced account of how localisation (Tao 2016) sidesteps it for lambda.
- No-go: if global Gowers uniformity did constrain sum f(n) f(n+2) for 1-bounded f (then the barrier would be fake).

## Sources read (this run; PDFs not committed; SHA-256 prefixes)
- Green-Tao, Linear equations in primes, arXiv:math/0606088v2 (4cc772cf...): Def. 1.5, Lemma 1.6, "(n1, n1+2), which counts
  twin primes, has infinite complexity" (p. 7); Main Theorem (p. 9); Prop. 7.1 (generalised von Neumann); Thm 7.2
  ||Lambda'_{b,W} - 1||_{U^{s+1}[N]} = o(1) conditional on GI(s), MN(s) (p. 27); the 'binary' case is "presumably very hard" (p. 10).
- Green-Tao, The Moebius function is strongly orthogonal to nilsequences, arXiv:0807.1736v4 (1983964e...): abstract (MN(s) for
  all s), Section 6 (same for lambda).
- Tao, The logarithmically averaged Chowla and Elliott conjectures for two-point correlations, arXiv:1509.05422v4 (467329ae...):
  abstract (tools: multiplicativity at small primes, MRT averaged short-interval result, entropy decrement; higher order needs
  "short sums of multiplicative functions modulated by local nilsequences").
- Tao, Equivalence of the logarithmically averaged Chowla and Sarnak conjectures, arXiv:1605.04628v1 (0ea72ada...): local Gowers
  norm (p. 4), Conj. 1.6 (log-averaged local Gowers uniformity; d = 1 from Matomaki-Radziwill; H >= X known from GTZ and GT),
  Thm 1.8 (equivalences), Remark 3.4 (k-point needs local U^{k-1}; k = 3 from local U^2) (p. 18).

## Work
- Prop. prop:gowers-blind (paper v0.13, Proved here, folklore in substance): random block functions f(n) = s(n) eps_{(floor(n/L),
  n mod 2)} have E||f||_{U^d[N]}^{2^d} <= 2^{2d+1} (4d)^d L/N and shift-2 correlation >= 1 - 4/L - 6/N (or <= -1 + ...); and a
  {0,2}-valued g = 1 + f_- with ||g-1||_{U^d} small, mean ~1 and (1/N) sum g(n) g(n+2) <= 4/L + 2(3L/N)^{1/2} + 8/N.
- Script code/parity/gowers_twin_blocks.py (+ .out): U^2 exact, U^3 floating; block f: U^2 0.209, shift-2 0.969 at N = 32768,
  L = 64; lambda on [1e7, 1e7+N): 0.098, -0.004 (Heuristic illustration).
- Remark rem:gowers: the two barriers differ (finite-complexity counts get past parity via the Type I/II input of MN(s), GT12
  Sec. 3); Tao reformulates the problem for lambda by localising (log-averaged Chowla <=> log-averaged local Gowers uniformity,
  an equivalence of open conjectures; local U^{k-1} suffices for k >= 3); the only proved case, k = 2, uses the MRT15 bound for
  lambda(n) e(alpha n). The block function f_- is locally U^1-uniform with shift-2 correlation ~ -1. For Lambda the route has
  no analogue at the scale it
  needs: Tao's arguments "rely in an essential fashion on multiplicativity at small primes" (Tao16 p. 5), and Lambda - 1 is not
  locally uniform on intervals of length H = o(log X) (most contain no prime).
- Audit (fresh-context helper, notes/audit-parity-v013.md): the Proposition is correct with all constants (brute force over all
  sign choices for small d, N, L). 3 errors and 5 gaps in the first draft of the remark, all fixed. Notably: f_- is locally
  U^1-uniform yet has shift-2 correlation ~ -1, so local U^1 alone does not give two-point Chowla (Tao's k = 2 proof uses the
  MRT15 bound for lambda(n) e(alpha n)); Tao16b's localisation is an equivalence of open conjectures for k >= 3.

## Classification
LOCATED (proved, folklore in substance). Confirms that twin primes need information beyond global Gowers norms, just as
parity says they need information beyond Type I sums. No parity-breaking content. Entered the paper as one short subsection
(Proposition + remark), per the review rule. First unresolved implication: a short-interval (local) uniformity statement for
a function attached to Lambda at scales H >= (log X)^C, combined with a substitute for lambda(pn) = -lambda(n); no such
substitute is known.

## Not to repeat
Any attempt to get twin-prime or two-point information from global U^s norms alone (any s): blocked by the Proposition.
