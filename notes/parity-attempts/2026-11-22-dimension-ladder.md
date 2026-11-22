# Route card: the sifting-dimension ladder from Iwaniec-type problems to twin primes (22 Nov 2026)

**Classification: located (conditional on EH and on the beta-sieve theorem as quoted; elementary; possibly folklore; computed).**
Not in the parity paper (v1.0 frozen). No progress on twin primes and no way around parity.

## Question
"p prime and p + 2 prime" is a sieve problem of dimension 1 on the sequence {p + 2}: every prime
divisor of p + 2 is forbidden. Ask instead that every prime factor of p + 2 lie in a set Q of primes
of relative density delta = 1 - kappa. Then the problem has sieve dimension kappa < 1, and the
classical case kappa = 1/2 (p + 2 a sum of two squares, or a norm from a quadratic field) is a
theorem (Linnik; Iwaniec). The question is whether the family kappa -> 1 approaches twin primes in a
way the parity barrier does not see, and, if not, where exactly the degeneration happens.

The model family: q an odd prime, Q_q = {primes l = 1 mod q}, kappa_q = (q-2)/(q-1), and

  T_q(x) = #{ p <= x : p = -1 mod q and every prime factor of p + 2 is = 1 mod q }.

- Success criterion: a lower bound for T_q (unconditional or under EH) whose sieve constant stays
  bounded below as q -> infinity, or a uniform version for q growing with x, so that the twin case is
  approached with a non-degenerating constant.
- No-go criterion: the lower-bound constant f_kappa(2) of the beta-sieve (not known to be optimal for
  1/2 < kappa < 1) tends to 0 as
  kappa -> 1 (computed), and the parity information carried by T_q (the mean of lambda(p+2) on it)
  tends to that of the twin set; then the ladder degenerates continuously into the parity barrier.

## Sources read (PDFs read by a helper agent in /tmp/claude-0/lit43/, not committed; SHA-256 of the copies)
- Gaudet, arXiv:2408.01610v1 (d5bfce37...d04e1), Prop. 5.1, pp. 10-11: the beta-sieve theorem in
  dimension kappa, quoted there from Friedlander-Iwaniec, Opera de Cribro (OdC), Thm 11.13 (OdC not opened).
- S. Blight, PhD thesis, Rutgers 2010 (80690f97...4fc004), Sect. 2.2.1, printed pp. 7-8: table of
  beta_kappa computed "using formulas (B.9), (11.42), and (11.57)" of OdC.
- K. Ford, Sieve Methods Lecture Notes, Spring 2023 (a6e8462f...e5c00e06), PDF p. 37, Sect. 3.1.
- Teräväinen, arXiv:1611.08585v2 (9198a83e...64134), pp. 3-4, 22-24.
- Shute, arXiv:2209.08949v2 (7d911211...aa16), pp. 9, 19-20, 27, 35.
- Campbell, arXiv:2603.10356v2 (fb77276f...dcb2), Lemma 2.3, p. 5 (linear-sieve closed forms).
The quotes below were extracted by the helper agent from these files; I checked them for internal
consistency and against my own computation (part (i) below), not against the PDFs page by page.

## What the sources say (Literature, opened by the helper)
1. Beta-sieve (Gaudet Prop. 5.1, citing OdC Thm 11.13). Let A_d = g(d) X + r_d, with the dimension
   condition prod_{w <= p < z} (1 - g(p))^{-1} <= K (log z / log w)^kappa. Let s = log y / log z,
   where y is the level. Then S^-(A, z) >= X V(z) (f(s) + O((log y)^{-1/6})) + R^-(y, z) for s >= beta.
   F and f are given by s^kappa F(s) = A on beta - 1 <= s <= beta + 1 and s^kappa f(s) = B at s = beta,
   with (s^kappa F)' = kappa s^{kappa-1} f(s-1) for s > beta - 1 and (s^kappa f)' = kappa s^{kappa-1} F(s-1)
   for s > beta, and F, f = 1 + O(e^{-s}). Also "B(kappa) = 0 if kappa >= 1/2".
2. Blight's table: beta_{0.5} = 1, beta_{0.6} = 1.1042161305, beta_{0.75} = 1.3981115251,
   beta_{0.8} = 1.5107489225, beta_{0.9} = 1.7489723058, beta_{0.95} = 1.8731283112, beta_1 = 2.
   In her words, "beta_kappa < 2 kappa if 1/2 < kappa < 1". Gaudet says that Irving (2014) corrected
   one value of the OdC table; which one is not known here.
3. Ford p. 37: the optimal sieving limit is known exactly only for kappa in [0, 1/2] union {1}.
4. Teräväinen p. 3: Iwaniec proved, with "a combination of the linear sieve and the semilinear sieve",
   that #{p <= N : p = x^2 + y^2 + 1} >> N (log N)^{-3/2}. Linnik proved earlier, by the dispersion
   method, that there are infinitely many. The word "parity" does not occur in that paper.
5. No paper was found that treats the general case (all prime factors of p + a in a Chebotarev set of
   density delta, dimension 1 - delta), conditionally or not. The searches are recorded in the session
   log. The closest analogues are Irving and Shute, who sieve polynomial values in two variables in
   dimension > 1/2 and need beta_i < 2 (Shute p. 27).

## Findings

### 1. The reduction: a congruence removes the last large prime (Proved here; elementary)
Let x be large, z = (x + 2)^{1/2}, A = {p + 2 : 3 <= p <= x, p = -1 mod q}, and sift A by the primes
l <= z with l odd, l != q and l != 1 mod q (the audit noted that with l < z the case p + 2 = r^2 = x + 2
would survive). The prime 2 never divides p + 2 for odd p, and q does not either,
since p + 2 = 1 mod q. Let m = p + 2 survive. Then m has at most one prime factor r outside Q_q,
because two such factors would both be > z and give m > z^2 = x + 2. If r exists, then m = r · m'
with every prime factor of m' = 1 mod q, so m' = 1 mod q. Since m = 1 mod q, also r = 1 mod q, a
contradiction. Hence

  T_q(x) = S(A, z).

The same congruence trick works for any abelian Q (primes splitting completely in an abelian field):
the leftover prime is detected by a character. It is the device that makes the half-dimensional
problems tractable without a switching step (compare Iwaniec's x^2 + y^2 + 1, where the sifting primes are 3 mod 4).

### 2. Under EH every rung kappa < 1 is reached (Proved here, conditional; possibly folklore)
The sifting density is g(l) = 1/(l - 1) on the sifting primes. By the prime number theorem in
progressions mod q, the dimension condition holds with kappa = kappa_q. Under the Elliott-Halberstam
conjecture for primes, with moduli up to x^{1-eps}, the remainders r_d of the progressions p = -2 mod d
inside p = -1 mod q satisfy sum_{d <= x^{1-eps}} mu^2(d) |r_d| << x (log x)^{-C}. The level is then
y = x^{1-eps}, so s = log y / log z -> 2. The beta-sieve (Source 1) gives, for each fixed q >= 5,

  T_q(x) >= (f_{kappa_q}(2) - o_eps(1)) |A| V_q(z) >> x / (log x)^{1 + kappa_q},

provided beta_{kappa_q} < 2. This holds at every tabulated kappa < 1 (Source 2) and at every kappa_q
computed below. A proof of beta_kappa < 2 for all kappa < 1 was not found in the sources: it is
"visible in the table" only, so this step is Computed (numerical), not proved.
The theorem is applied at s = 2 - 2 eps, which is fine because f_kappa is continuous at 2 when beta_kappa < 2.
Unconditionally (Bombieri-Vinogradov, plain level 1/2) the beta-sieve only gets s -> 1 <= beta_kappa for every
kappa >= 1/2, so this naive argument proves nothing for any q. A well-factorable level beyond 1/2
(Bombieri-Friedlander-Iwaniec type) is not excluded by this remark; it was not examined. At q = 3 (kappa = 1/2, beta = 1) it sits exactly on
the boundary, where Iwaniec's extra device is needed (Source 4; Iwaniec's paper itself was not opened).

### 3. The lower constant degenerates linearly as kappa -> 1 (Computed, numerical)
Script: code/parity/dim_ladder.py, part (i). It solves the system of Source 1 by the method of steps,
with beta fixed by the exponential decay of F - f, at three step sizes (2e-3, 1e-3, 5e-4); output in code/parity/dim_ladder.out. beta is quantised to
the grid, so f_kappa(2) is accurate to about 1% for kappa <= 0.9 and about 5% near kappa = 0.99 (audit).
The source fixes s^kappa F = A only on [beta - 1, beta + 1]; the script sets it on (0, beta + 1], which
changes nothing because F(s - 1) is used only for s > beta.

- Validation at kappa = 1: beta = 2 up to the grid step, and A = 2e^gamma to a relative 6e-4. With beta = 2
  imposed, f(3) = 2e^gamma log 2 / 3 to 6 digits; this checks the integrator, not the choice of beta.
- Cross-check against Blight's table: beta_{0.75} = 1.3983 here (h = 5e-4) against her 1.39811, and beta_{0.9} = 1.7488
  against 1.74897. The agreement is to the grid resolution.

| q | kappa_q | beta_kappa (h = 5e-4) | f_kappa(2) | F_kappa(2) | f_kappa(2)/(1-kappa) |
|---|---|---|---|---|---|
| 5 | 0.750 | 1.3983 | 0.712 | 1.310 | 2.85 |
| 7 | 0.833 | 1.5883 | 0.553 | 1.437 | 3.32 |
| 11 | 0.900 | 1.7488 | 0.376 | 1.559 | 3.76 |
| 13 | 0.917 | 1.7903 | 0.323 | 1.593 | 3.88 |
| 31 | 0.967 | 1.9153 | 0.142 | 1.702 | 4.26 |
| 101 | 0.990 | 1.9743 | 0.045 (±5%) | 1.757 | 4.46 |

So f_kappa(2) lies between 2.8 (1 - kappa) and about 4.6 (1 - kappa) on this range, the ratio drifting
upwards (heuristically towards e^gamma lim (2 - beta_kappa)/(1 - kappa), about 4.5), and F_kappa(2) -> e^gamma = 1.781.
At kappa = 1 this is the linear sieve's f(2) = 0, which Selberg's parity example (lambda-twisted weights) shows to be optimal.
Uniformity in q is trivially impossible for q > z: then no sifting prime up to z is = 1 mod q, the problem is
twin primes in a progression, and f_1(2) = 0. For intermediate q it is open; the beta-sieve constant there is
about f_{kappa_q}(2), i.e. of order 1/q, and a uniform dimension condition would also need Brun-Titchmarsh-type
control of the primes = 1 mod q. With q = x^delta, delta < 1/2, the target allows Omega(p + 2) of both parities
and is not blocked by the parity class, so its failure on this route is a sieve limit, not parity. For
delta >= 1/2 it forces p + 2 prime and is blocked. (Chen-type results need switching, which this route does not provide.)

### 4. Parity neutrality degenerates too (Heuristic + Computed at finite X)
The parity class of the paper (fair lambda-pattern weights) does not block T_q for any fixed q. The
condition "all prime factors in Q_q" does not fix lambda(p + 2), so the target is effectively the
single vertex "p prime", and the bipartite criterion does not apply. It becomes the edge {p, p+2} only
in the limit, where it is blocked. Quantitatively, a Selberg-Delange heuristic for
sum_{n in S_q} lambda(n) n^{-s} = prod_{l = 1 (q)} (1 + l^{-s})^{-1} ≈ zeta(s)^{-delta} G(s) gives a
mean of lambda on S_q (the integers composed of primes = 1 mod q) of about c_q (log x)^{-2 delta}, where
c_q = (Gamma(delta)/Gamma(-delta)) times a ratio of convergent Euler products. The ratio also involves zeta^{2 delta}, i.e. L-values mod q,
so it is not purely a convergent product. Since Gamma(delta)/Gamma(-delta) ≈ -1 for small delta, the mean is
negative. Heuristically it tends to -1, the twin value, in a joint limit with delta log log x -> 0. This is not
uniform in delta: at fixed x and q > x the set is {1}. The shift p + 2 and the primality of p are ignored here,
and the data below do not support the constant: at X = 1e8 the observed |mean| is 4.2, 1.6, 1.6, 1.3, 1.3 times the
prediction for q = 3, 5, 7, 11, 13, with c_q = Gamma(delta)/Gamma(-delta) and the Euler-product factor set to 1. The class claim needs both signs of lambda(p + 2) to occur with positive density on
T_q, which the heuristic supplies.
Data at X = 1e8 (code/parity/dim_ladder.py part (ii)), share of lambda(p+2) = +1 on T_q:

| q | #T_q | + share |
|---|---|---|
| 3 | 1115569 | 0.443 |
| 5 | 229835 | 0.310 |
| 7 | 112283 | 0.201 |
| 11 | 57803 | 0.146 |
| 13 | 44954 | 0.107 |
| twins | 440312 | 0 |

The sieve-normalised counts #T_q/(|A| V_q(z)) are 1.066, 1.033, 1.005, 0.987, 0.980, and 0.951 for
twins. For q >= 5 they lie inside [f_kappa(2), F_kappa(2)], which is consistent with the sieve picture; this is
finite-X data only. For twins the Hardy-Littlewood prediction is e^gamma/2 ≈ 0.89 in this normalisation, reached slowly.

## Conclusion and first unresolved implication
The ladder passes into the parity barrier continuously, and along two separate axes at once. The first is
the beta-sieve's lower constant f_kappa(2), between 2.8(1 - kappa) and 4.6(1 - kappa). The second is the
lambda-bias of the target: the mean of lambda(p + 2) is heuristically about -c_q (log x)^{-2(1-kappa)} with
c_q ≈ 1. So at fixed kappa the target tends to parity-neutral as x -> infinity, and its distance from
parity-fixed is 1 - c_q (log x)^{-2(1-kappa)}. Neither axis gives anything at kappa = 1.
The first unresolved implication is a lower bound for T_q uniform in q -> infinity with a constant
>> 1/q. That would give p + 2 composed of primes = 1 mod q for slowly growing q, which is still far
from twins. It is blocked by the sieve limit, not by the parity class. Twins themselves remain the
kappa = 1 endpoint, where f_1(2) = 0 exactly.

## Not done / caveats
- beta_kappa < 2 for all kappa < 1 is taken from Blight's table and our own computation (numerical),
  not from a proof. The beta-sieve theorem is quoted from Gaudet's quote of OdC (OdC not opened).
- The EH step assumes EH in the form sum over moduli of max |error| for primes in progressions to
  moduli up to x^{1-eps}, including the fixed extra modulus q. That is standard but stated here without a source.
- Whether Finding 2 is in the literature: not found (searches recorded). Classify as possibly folklore.
- Audit: a fresh-context adversarial referee (22 Nov) found 3 errors (q = x^delta with delta >= 1/2 is
  blocked; the fixed-x limit of the lambda-mean; z^2 = x + 2 and p = 2 edge cases), 5 gaps (grid
  quantisation of beta, the s^{-2 kappa} mode, continuity of f at 2, the heuristic's constant against the
  data, the wording of the normalised counts) and wording fixes. All were applied above. No script bug changed
  the results; the z-edge, bracket check and three step sizes were added to the script.
- Exploration companion (same session): block entropies of lambda(p_j + 2) along consecutive primes (dead end).
