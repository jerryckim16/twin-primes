# Route card: the large-q function-field mechanism (Pellet + Weil + Galois) and what it would need over Z (Session 41, 21 Nov 2026)

**Classification: located (literature + elementary dictionary; possibly folklore in substance).**
Not in the parity paper (v1.0 frozen). No parity-breaking content of our own.

## Question
Over F_q[x] with the degree n FIXED and q -> infinity (q odd), both the two-point Chowla conjecture
(Carmon–Rudnick) and the twin prime / Hardy–Littlewood conjecture (Bender–Pollack for pairs,
Bary-Soroker for tuples) are theorems. The project has not examined this regime: the parity paper's
`sec:ss` treats only the fixed-q theorem of Sawin–Shusterman, which shares one ingredient (Pellet's formula)
but needs more (the characteristic-p identity (r+s^p)' = r' and Deligne-type short character sums). What exactly
does the large-q mechanism use, and what would its integer analogue have to be?

- Success criterion: an integer quantity that plays the role of Pellet's formula with bounded
  complexity (a parity-sensitive input that is not of the Liouville-pattern type), or a regime of integers
  in which the large-q argument transfers.
- No-go criterion: the mechanism's inputs translate into integer statements that already contain the
  twin-prime problem (or an open Chowla-type statement) in the corresponding regime.

## Sources read (PDFs not committed; SHA-256 of the copies read)
- Carmon, Rudnick, "The autocorrelation of the Möbius function and Chowla's conjecture for the rational
  function field", arXiv:1205.1599v3 (SHA-256 8148dcfa41774a4de2ac331a64db297f0a52ddad5ffbf86c4429fe50be8d4b86),
  pp. 1-3: Theorem 1.1, (1.3)-(1.5), Section 2.1 ((2.1)-(2.6)), Proposition 2.1.
- Bary-Soroker, "Hardy–Littlewood tuple conjecture over large finite fields", arXiv:1206.3930v3
  (SHA-256 aed115a867be797772c0131061d94ca54e3b61a2368ccc4834b5c2ae656bc1b0), pp. 1-3: Theorem 1.1,
  remarks, outline of the proof.
- Rudnick, "Some problems in analytic number theory for polynomials over a finite field",
  arXiv:1501.01769v1 (SHA-256 cc59f8c97d24f043ca02613be11e60b2f2d08885d3f6956ff25f73e16fa5c994),
  (2.5)-(2.6), Section 4.1-4.2 ((4.4)-(4.6)).

## What the sources say (Literature, opened)
1. Pellet's formula (CR (1.5), Rudnick (4.4)): for q odd, mu(F) = (-1)^{deg F} chi_2(disc F), chi_2 the
   quadratic character of F_q. So mu is a quadratic character of a polynomial in the coefficients of F.
2. CR Theorem 1.1: for r > 1, n > 1, q odd, distinct alpha_j with deg < n, eps_i in {1, 2} not all even,
   |C(alpha; n)| <= 2 r n q^{n-1/2} + 3 r n^2 q^{n-1}. Proof (Section 2.1): write F = f + t, t = F(0);
   D_f(t) = disc(f + t) has degree n - 1 in t (n - 2 if p | n and a_{n-1} != 0, CR (2.17)); on each one-variable slice {f + t : t in F_q} apply Weil's
   bound |sum_t chi_2(P(t))| <= (deg P - 1) q^{1/2} (P not a constant times a square) to
   P = prod D_{f+alpha_i}(t)^{eps_i}, of degree <= 2r(n-1); the slices outside the good set G_n (where the
   squarefree / coprimality condition fails) number at most 3 r n^2 q^{n-2} (Prop. 2.1) and get the trivial bound q.
3. BS Theorem 1.1: pi(q, n; a) = q^n / n^r + O_{n,r}(q^{n-1/2}) for q odd, n, r fixed (a_i may depend
   on q). Proof: the geometric Galois group (S_n^r) of prod (F + a_i) over F_q(coefficients) is computed (square
   independence of discriminants, via CR) and an irreducibility criterion plus Lang–Weil gives the count.
4. Rudnick (2.6): the factorisation type of a random monic F of degree n has the cycle-type law of a
   random permutation in S_n up to O(1/q); "this result (2.6) gives an asymptotic only in the large
   finite field limit q -> infinity, n fixed."

## Findings (Proved here unless labelled; elementary)
1. **The slices are short intervals of length H = X^{1/n}.** Put X = q^n = |F|. The CR slice
   {f + t : t in F_q} is the "interval" {G monic : deg(G - f) < 1} of size q = X^{1/n}. CR's proof gives,
   for r = 2, alpha = (0, 1), eps = (1, 1): for all but at most 6 n^2 q^{n-2} of the q^{n-1} slices,
   |sum_{t} mu(f + t) mu(f + t + 1)| <= (2(n - 1) - 1) q^{1/2} (with eps = (1, 1) the polynomial
   D_f(t) D_f(t+1) has degree <= 2(n-1); CR's stated constant 2r(n-1) - 1 = 4n - 5 also holds; note F + 1 lies
   in the same slice since D_{f+1}(t) = D_f(t+1)). In words: square-root cancellation of
   the two-point Möbius correlation in all but a proportion <= 6 n^2 / H of the intervals of length
   H = X^{1/n}.
2. **The integer counterpart is at least two-point Chowla in Cesàro form.** Over Z the analogous
   statement ("for all but o(x) of the y <= x, S(y) := sum_{y < m <= y+H} lambda(m) lambda(m+2) = o(H)",
   with H = o(x)) implies sum_{m <= x} lambda(m) lambda(m+2) = o(x): average over y,
   sum_{y <= x} S(y) = H sum_{m <= x} lambda(m) lambda(m+2) + O(H^2), and the exceptional y contribute
   o(x) H (bounded summands). Over Z, Cesàro two-point Chowla at every x is open; known are the
   logarithmically averaged form (Tao 2016, opened, parity paper), and, as the audit points out (not opened
   in this run), the Cesàro form at almost all scales (Tao–Teräväinen 2019) and averages over the shift
   (Matomäki–Radziwiłł–Tao 2015, opened in Session 19). The large-q slice statement is far stronger
   (square-root saving in every non-exceptional interval).
3. **The large-q ring has no small primes.** Every monic irreducible factor P of F in M_n has
   deg P >= 1, i.e. |P| >= q = X^{1/n}; so M_n plays the role of the X^{1/n}-rough integers, with
   Omega(F) <= n. The Weil step is non-trivial on a slice only if (2n - 3) q^{1/2} < q, i.e. q > (2n-3)^2,
   roughly 4 n^2 (the whole bound (1.3) with r = 2 is non-trivial only for roughly q > 27 n^2). So the
   interval length H = X^{1/n} must be large compared with the square of the maximal number n of prime
   factors; the regime is n bounded, every prime of norm >= X^{1/n}. The fixed-q case (the true analogue of
   Z, n -> infinity) violates this; Sawin–Shusterman also start from Pellet's formula but need the
   characteristic-p identity (r+s^p)' = r' to get a structured one-variable sum (parity paper `sec:ss`).
4. **In the rough regime, parity information determines the twin-prime count.** Let x^{1/3} < z <= x^{1/2}
   (with z^3 > x + 2) and R = {m <= x - 2 : m and m + 2 have no prime factor <= z}. Every m in R and m + 2
   have Omega in {1, 2} (squares p^2, p > z, have lambda = +1 and are not prime; m = 1 is excluded once
   z >= 3), so
   lambda(m) = -1 iff m is prime, and
   #{m in R : m, m + 2 both prime} = (1/4) sum_{m in R} (1 - lambda(m))(1 - lambda(m+2))
   = (1/4) (|R| - sum_R lambda(m) - sum_R lambda(m+2) + sum_R lambda(m) lambda(m+2)).
   So in the integer regime where roughness forces Omega <= 2 (it mirrors M_2, not M_3), the joint parity
   law of (lambda(m), lambda(m+2)) on rough pairs determines the number of twin primes among rough pairs
   (the converse needs also the counts of primes m and of primes m + 2 in R, which are not known
   asymptotically either). Elementary; the classical form of the parity problem for rough numbers. In
   F_q[x], CR give the correlation sum; the twin count itself needs BS (Galois group S_n x S_n plus
   Lang–Weil), except for n = 2.
5. **No integer Pellet of bounded complexity of the obvious kinds.** (a) Fixed modulus: lambda is
   asymptotically orthogonal to every fixed periodic function (prime number theorem in arithmetic
   progressions for lambda: in each class mod m each sign has density 1/2), so lambda(n) = g(n mod m)
   holds on a proportion exactly 1/2 + o(1) of n when g takes values +-1, and less where g = 0. (b) Digit polynomials: the Session 41 exploration (notes/explorations.md,
   code/explore/digit_pellet.py) finds no correlation between lambda(n) and mu_{F_p[x]} of the base-p
   digit polynomial of n (p = 3, 5, 7; n < 5.3e5, 3.9e5, 8.2e5; all means within 1.5 standard errors of 0).
   Not covered and not opened: correlations of mu with trace functions modulo primes of size about H on
   intervals of length H (Fouvry–Kowalski–Michel type questions); a bounded-conductor trace-function
   representation of lambda on short intervals would be the integer substitute for Pellet's step.

## Cheapest decisive check (Computed; exact enumeration)
`code/parity/large_q_pellet.py [X]` (/usr/bin/python3 -I; 3 s at X = 1e7; output `code/parity/large_q_pellet.out`):
- Pellet's formula checked for every monic F (q prime, 3 <= q <= 29, n = 3; q <= 13, n = 4; q = 3, n = 6, 8, 9): 0 failures.
- C(q, n) = sum mu(F) mu(F+1) is tiny (|C| <= 209 at q = 19, n = 3 against q^n = 6859); CR's bound is
  larger than q^n at all these q (the Weil step needs q > 16 n^2 to say anything).
- Twin count / (q^n / n^2) at n = 3: 0.72, 0.55, 0.89, 0.905, 0.93, 0.97, 0.95, 0.96 for q = 5, ..., 29;
  at fixed q = 3 and n = 6, 8, 9: 0.30, 0.35, 0.43 (for fixed q a singular-series factor enters and the
  large-q law does not apply; at q = 3, n = 4 the count is 0: F and F + 1 rootless forces F = 1 on F_3,
  leaving the 3 candidates 1 + (x^3 - x)(x + c), each the square of an irreducible quadratic; a small-numbers
  effect, not a local obstruction).
- Integers (X = 1e7): x^{1/3}-rough pairs: 142907, of which 58965 (41.3%) are twin-prime pairs; mean
  lambda(m) lambda(m+2) = +0.092 on rough pairs (n = 3), +0.007 (n = 4). Illustrative only.

## Classification and first unresolved implication
Located. The large-q mechanism is (Pellet) "mu is a quadratic character of a polynomial in the
coordinates" plus (Weil / Lang–Weil) "square-root cancellation along one coordinate", in a ring where
every prime has norm >= X^{1/n} and the factorisation type is a Frobenius cycle type in a fixed finite
monodromy group. Its integer counterpart (Findings 2 and 4) contains two-point Chowla in Cesàro form and,
in the rough regime, a joint parity law that determines the twin-prime count among rough pairs. The first unresolved implication is an integer substitute
for Pellet's step: a representation of lambda on short intervals by functions of bounded conductor
to which a Riemann-hypothesis-type bound applies. None is known; the obvious candidates fail (Finding 5).
Twin primes over Z are untouched.

## Possible use
At most one sentence in a future v1.1 of the parity paper next to `sec:ss` ("in the large-q limit,
Carmon–Rudnick and Bary-Soroker use Pellet's formula, also the starting point of Sawin–Shusterman, with
Weil's bound and Lang–Weil in a ring whose primes all have norm >= X^{1/n}"), after literature-check
(including Tao–Teräväinen 2019, not opened). For the weekly review of 23 Nov.

## Audit (fresh-context adversarial helper, Session 41)
Read the three sources and the scripts; re-ran its own check at q = 3, n = 4 (confirmed here with flint).
Found: 3 errors (Finding 2's partition argument and the claim "only log-averaged is known"; Finding 3's
threshold constant and paraphrase, and a wrong contrast with Sawin–Shusterman, who also use Pellet; the
q = 3, n = 4 "local obstruction" explanation), and gaps (sharp per-slice constant 2n - 3; "relative length";
degree n - 2 when p | n; geometric Galois group; Finding 4's edge case m + 2 <= x, M_2 not M_3, "equivalent"
overstated; Finding 5(a) precision). All fixed above. Literature statements 1-4 match the sources.
