# Route card: the large-q function-field mechanism (Pellet + Weil + Galois) and what it would need over Z (Session 41, 21 Nov 2026)

**Classification: located (literature + elementary dictionary; possibly folklore in substance).**
Not in the parity paper (v1.0 frozen). No parity-breaking content of our own.

## Question
Over F_q[x] with the degree n FIXED and q -> infinity (q odd), both the two-point Chowla conjecture
(Carmon–Rudnick) and the twin prime / Hardy–Littlewood conjecture (Bender–Pollack for pairs,
Bary-Soroker for tuples) are theorems. This is a parity-breaking mechanism that the project has not
examined (the parity paper's `sec:ss` treats only the fixed-q theorem of Sawin–Shusterman). What exactly
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
   D_f(t) = disc(f + t) has degree n - 1 in t; on each one-variable slice {f + t : t in F_q} apply Weil's
   bound |sum_t chi_2(P(t))| <= (deg P - 1) q^{1/2} (P not a constant times a square) to
   P = prod D_{f+alpha_i}(t)^{eps_i}, of degree <= 2r(n-1); the slices where this fails number at most
   3 r n^2 q^{n-2} (Prop. 2.1), and get the trivial bound q.
3. BS Theorem 1.1: pi(q, n; a) = q^n / n^r + O_{n,r}(q^{n-1/2}) for q odd, n, r fixed (a_i may depend
   on q). Proof: the Galois group of prod (F + a_i) over F_q(coefficients) is computed (square
   independence of discriminants, via CR) and an irreducibility criterion plus Lang–Weil gives the count.
4. Rudnick (2.6): the factorisation type of a random monic F of degree n has the cycle-type law of a
   random permutation in S_n up to O(1/q); "this result (2.6) gives an asymptotic only in the large
   finite field limit q -> infinity, n fixed."

## Findings (Proved here unless labelled; elementary)
1. **The slices are short intervals of relative length X^{1/n}.** Put X = q^n = |F|. The CR slice
   {f + t : t in F_q} is the "interval" {G monic : deg(G - f) < 1} of size q = X^{1/n}. CR's proof gives,
   for r = 2, alpha = (0, 1), eps = (1, 1): for all but at most 6 n^2 q^{n-2} of the q^{n-1} slices,
   |sum_{t} mu(f + t) mu(f + t + 1)| <= (4(n - 1) - 1) q^{1/2}. In words: square-root cancellation of
   the two-point Möbius correlation in all but a proportion <= 6 n^2 / H of the intervals of length
   H = X^{1/n}.
2. **The integer counterpart is at least two-point Chowla in Cesàro form.** Over Z the analogous
   statement ("for all but o(x/H) of the y <= x, sum_{y < m <= y+H} lambda(m) lambda(m+2) = o(H)",
   any H = H(x) <= x) implies sum_{m <= x} lambda(m) lambda(m+2) = o(x) by summing over a partition of
   [1, x] into intervals of length H (bounded summands; the exceptional intervals contribute o(x)).
   Over Z only the logarithmically averaged two-point statement is proved (Tao 2016, parity paper
   `prop:tao-weight` context); the large-q slice statement is far stronger (square root, every
   non-exceptional interval).
3. **The large-q ring has no small primes.** Every monic irreducible factor P of F in M_n has
   deg P >= 1, i.e. |P| >= q = X^{1/n}; so M_n plays the role of the X^{1/n}-rough integers, with
   Omega(F) <= n. The Weil step of CR is non-trivial only if (4(n-1) - 1) q^{1/2} < q, i.e. roughly
   q > 16 n^2; with n = log X / log q this says that no prime of norm below about 16 (log_q X)^2 exists.
   The fixed-q case (the true analogue of Z, n -> infinity) violates this; Sawin–Shusterman need a
   different input there (characteristic-p identity, parity paper `sec:ss`).
4. **In the rough regime, parity information is the twin-prime count.** Let x^{1/3} < z <= x^{1/2} and
   R = {m <= x : m and m + 2 have no prime factor <= z}. Every m in R has Omega(m) in {1, 2}, so
   lambda(m) = -1 iff m is prime, and
   #{m in R : m, m + 2 both prime} = (1/4) sum_{m in R} (1 - lambda(m))(1 - lambda(m+2))
   = (1/4) (|R| - sum_R lambda(m) - sum_R lambda(m+2) + sum_R lambda(m) lambda(m+2)).
   So in the integer regime that mirrors M_3 (Omega <= 2 forced by roughness), the joint parity law of
   (lambda(m), lambda(m+2)) on rough pairs, which is what Pellet + Weil delivers in F_q[x], is equivalent
   to counting twin primes among rough pairs. (Elementary; this is the classical form of the parity
   problem for rough numbers.) Over F_q[x] the analogous count is also given by BS via the Galois group
   S_n x S_n of F (F + 1).
5. **No integer Pellet of bounded complexity of the obvious kinds.** (a) Fixed modulus: lambda is
   asymptotically orthogonal to every fixed periodic function (prime number theorem in arithmetic
   progressions for lambda), so lambda(n) = g(n mod m) can hold on at most a proportion 1/2 + o(1) of
   n for any fixed m and g. (b) Digit polynomials: the Session 41 exploration (notes/explorations.md,
   code/explore/digit_pellet.py) finds no correlation between lambda(n) and mu_{F_p[x]} of the base-p
   digit polynomial of n (p = 3, 5, 7; n < 5.3e5, 3.9e5, 8.2e5; all means within 1.5 standard errors of 0).
   Not covered and not opened: correlations of mu with trace functions modulo primes of size about H on
   intervals of length H (Fouvry–Kowalski–Michel type questions); a bounded-conductor trace-function
   representation of lambda on short intervals would be the integer substitute for Pellet's step.

## Cheapest decisive check (Computed; exact enumeration)
`code/parity/large_q_pellet.py [X]` (/usr/bin/python3 -I; 3 s at X = 1e7; output `code/parity/large_q_pellet.out`):
- Pellet's formula checked for every monic F (q = 3, ..., 29, n = 3; q <= 13, n = 4; q = 3, n = 6, 8, 9): 0 failures.
- C(q, n) = sum mu(F) mu(F+1) is tiny (|C| <= 209 at q = 19, n = 3 against q^n = 6859); CR's bound is
  larger than q^n at all these q (the Weil step needs q > 16 n^2 to say anything).
- Twin count / (q^n / n^2) at n = 3: 0.72, 0.55, 0.89, 0.91, 0.93, 0.97, 0.95, 0.96 for q = 5, ..., 29;
  at fixed q = 3 and n = 6, 8, 9: 0.30, 0.35, 0.43 (for fixed q a singular-series factor enters and the
  large-q law does not apply; at q = 3, n = 4 the count is 0: a local obstruction, F(a) must equal 1 at all
  three points of F_3).
- Integers (X = 1e7): x^{1/3}-rough pairs: 142907, of which 58965 (41.3%) are twin-prime pairs; mean
  lambda(m) lambda(m+2) = +0.092 on rough pairs (n = 3), +0.007 (n = 4). Illustrative only.

## Classification and first unresolved implication
Located. The large-q mechanism is (Pellet) "mu is a quadratic character of a polynomial in the
coordinates" plus (Weil / Lang–Weil) "square-root cancellation along one coordinate", in a ring where
every prime has norm >= X^{1/n} and the factorisation type is a Frobenius cycle type in a fixed finite
monodromy group. Its integer counterpart (Findings 2 and 4) contains two-point Chowla in Cesàro form and,
in the rough regime, the twin-prime count itself. The first unresolved implication is an integer substitute
for Pellet's step: a representation of lambda on short intervals by functions of bounded conductor
to which a Riemann-hypothesis-type bound applies. None is known; the obvious candidates fail (Finding 5).
Twin primes over Z are untouched.

## Possible use
At most one sentence in a future v1.1 of the parity paper next to `sec:ss` ("the large-q theorems of
Carmon–Rudnick and Bary-Soroker break parity through Pellet's formula and Weil's bound in a ring without
small primes"), after literature-check. For the weekly review of 23 Nov.

## Audit
See the section below (fresh-context adversarial audit, Session 41).
