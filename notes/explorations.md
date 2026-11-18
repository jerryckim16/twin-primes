# Exploration log (newest first)

Each entry: date, session, idea, what was tried, outcome (dead end / inconclusive / promising), why.
"Promising" is not a result: it goes to the ideas ledger (origin "exploration") and needs the usual checks.

## 2026-11-18, Session 31 -- The window identity in F_q[T]: what Keating-Rudnick's variance says about single shifts (function fields)
- Idea: in F_q[T] short intervals I(A;h) = A + P_{<=h} are cosets of a subspace, so they partition the monic polynomials and
  the window identity becomes an UNWEIGHTED ball sum: sum over cosets nu^2 = sum_{deg D <= h} c(D). Ask whether Keating-
  Rudnick's theorem (arXiv:1204.0708v3, Thm 2.1: Var nu ~ q^{h+1}(n-h-2) as q -> infinity, h < n-3; read pp. 1-5) can
  reach a single shift, which the integer second-difference trick cannot do at SPC precision (paper rem:gm(d)).
- Tried: code/explore/ff_ball_variance.py q n (exact, python-flint factorisation; seconds), output .out for (q,n) = (5,6),
  (7,5), (3,8). The identity holds exactly in all cases. The mean of c(D)/q^n over nonzero D of degree <= h rises to 1 with h
  (0.61, 0.89, 0.98, 0.99 for q = 5, n = 6). The KR ratio Var/(q^{h+1}(n-h-2)) is 0.67-1.28 at these small q.
- Observation: the substitution f(T) -> lambda^{-n} f(lambda T) maps monic polynomials to monic ones and sends the constant
  shift a to lambda^{-n} a. So when gcd(n, q-1) = 1 all q-1 constant shifts have the same correlation (seen: min = max at
  h = 0 for q = 7, n = 5), and the smallest-ball variance (h = 0) determines the single twin count c(1) exactly. In the large-q
  limit that ball has q elements, much more than the mean gap n. So large-q twin results live in the integer regime
  "window >> log X", where averages work, and the symmetry turns an average into a single shift. Z has no such symmetry
  (only c(h) = c(-h)).
- Outcome: INCONCLUSIVE (structural, very likely known; the large-q twin-prime literature, e.g. Bary-Soroker, was not opened).
  Nothing transfers to Z. Not promoted. Heuristic / exploratory only.

## 2026-11-17, Session 30 -- A Polya-type sign bias of lambda on shifted primes? (probabilistic models / Polya's problem)
- Idea: Polya-type bias makes partial sums of lambda negative for a long time, at relative size about x^{-1/2}. Ask whether
  S(h) = sum_{p<=X} lambda(p+h) shows a uniform sign across shifts h, and whether it depends on the parity of h (p+h odd for
  even h, even for odd h), which would be a small structured deviation from the Hardy-Littlewood-Chowla prediction S(h) = o(pi(X)).
- Tried: part 2 of code/parity/hybrid_shifted_primes.py (same run as the parity attempt; X = 2e7, h <= 64; .out).
- Outcome: INCONCLUSIVE. 39 of 64 S(h) are negative (even h: 23 of 32, mean S/pi = -0.00045; odd h: 16 of 32, mean -0.00008),
  max |S|/pi = 0.0025 (h = 42), against the random-sign scale pi(X)^{-1/2} = 0.00089 and X^{-1/2} = 0.00022. The even-h mean
  is of the order of a Polya-type term, but the S(h) share the same primes (strongly correlated across h), so no significance can
  be claimed, and one X is not a trend. Would need several X and a model of the square contribution (p+h = m^2) before saying
  anything. Not promoted. Heuristic / exploratory only.

## 2026-11-17, Session 29 -- Is there structure in the Hardy-Littlewood errors across shifts beyond S(h)? (probabilistic models of primes)
- Idea: for prime pairs (p, p+h) in (X, 2X], look at the normalised counts r(h) = c(h)/(S(h) L(h)) over 1000 even shifts and
  ask (a) whether their spread matches a Poisson (Cramer-type) model with the singular series, and (b) whether the residual
  r(h) - 1 depends on h mod small primes or on log h in a way S(h) does not explain (a hidden secondary term would be a
  handle on individual shifts).
- Tried: code/parity/mrt_averaged_hl.py (the same run as the parity attempt; .out, 39 s at X = 1e8; _1e7.out): least-squares
  fit of r(h) - 1 on [3|h], [5|h], [7|h], [11|h], [13|h], log h.
- Outcome: INCONCLUSIVE / DEAD END for (b): R^2 = 0.006 (X = 1e8) and 0.003 (1e7), every |t| < 2; S(h) explains the
  h-dependence at this precision. For (a) the spread is clearly SUB-Poisson: sd 0.00088 vs Poisson 0.0014 (ratio 0.62) at
  1e8, 0.0023 vs 0.0039 (0.57) at 1e7. Plausibly the known reduction of variance of primes in short intervals below the
  Cramer model (Montgomery-Soundararajan type; not read, not checked) and the common use of the same primes for all h.
  Not a result; not promoted. Heuristic / exploratory only.

## 2026-11-17, Session 28 -- Do local Gowers norms of lambda on short intervals differ from random models? (additive combinatorics / probabilistic models)
- Idea: Tao (arXiv:1605.04628, Thm 1.8, Rem. 3.4) makes log-averaged k-point Chowla equivalent to local U^{k-1} uniformity of
  lambda on [n, n+H]. Look for any measurable deviation of lambda's local U^2 / U^3 norms from i.i.d. signs and from a random
  completely multiplicative function (Rademacher signs at primes) at accessible scales.
- Tried: code/explore/local_u2_liouville.py (output .out; 2 s): X = 1e9, segment 2^18, disjoint intervals, H = 8..512 (U^2) and
  8..64 (U^3), exact integer norms. All three models agree to within 1 standard error (|z| < 1 throughout; e.g. U^2 at H = 64:
  0.4637, 0.4632, 0.4636; U^3 at H = 64: 0.7416, 0.7412, 0.7416).
- Outcome: DEAD END (expected). At these scales lambda is statistically indistinguishable from random by local Gowers norms;
  the norms decay like those of random signs, so there is no numerical handle on local U^2 uniformity here (the conjecture is
  that lambda behaves exactly like this). Heuristic / exploratory only.

## 2026-11-16, Session 27 -- Is there a "mod q" analogue of the parity obstruction? (Selberg-Delange / combinatorics of pattern weights)
- Idea: replace lambda(n) = (-1)^Omega(n) by the class of Omega(n) mod q (z = e(1/q)). If sieve weights could not see
  z^Omega either, the pattern-weight criterion would give obstructions for other targets: a fair (uniform-marginal) measure on
  (Z/q)^k with at most m coordinates equal to 1 (primes have Omega = 1) would block DHL[k, m+1].
- Tried: code/explore/omega_mod_q_weights.py (output .out; 14 s). (A) LP over (Z/q)^k, q = 2, 3, 4, k <= 6, m = 1, 2, with an
  exact rational witness (independent random injections into Z/q on blocks of q coordinates): a fair killing weight exists iff
  k <= q m (q = 2 recovers Prop. bipartite (b)). For q = 3, m = 1 it would "block" DHL[3,2], which Polymath8b proves under GEH,
  so the randomness heuristic must fail for z = e(1/3). (B) Why: Selberg-Delange, sum_{n<=x} z^Omega(n) ~ x (log x)^{z-1}
  G(z)/Gamma(z), and 1/Gamma(z) vanishes only at z = 0, -1, -2, ...: among |z| = 1 only z = -1 has a negligible mean. At
  x = 1e7 the partial sums match the predicted main term to 3-9% (ratio 0.97-0.27i for e(1/3), 0.91-0.11i for i, 0.95-0.01i for
  e(1/6)), while for z = -1 the prediction is 0 and |S|/x = 8e-5. With a one-dimensional Selberg-type weight
  nu = (sum_{d|n, d<=x^0.4} mu(d) log(R/d)/log R)^2, the normalised twisted sum is -0.058 for z = -1 (Selberg's example: small)
  but has modulus 0.44, 0.61, 0.75 for z = e(1/3), i, e(1/6): the sieve sees z^Omega as a sieve problem of dimension z.
- Outcome: DEAD END for new obstructions (as expected), with a clean explanation of why parity is special: the only twists
  invisible to sieve weights among z^Omega are z = +-1, because 1/Gamma(z) = 0 exactly there. Almost certainly folklore (the
  literature helper of this run searched for a source; see notes/sources-chen-parity.md). Heuristic / exploratory only; not for
  a paper unless a source is found, and then at most a footnote.

## 2026-11-16, Session 26 -- Can the Pintz-Maynard dichotomy reach 4-tuples (|d| <= 8)? (levels of distribution / enlarged supports)
- Idea: the dichotomy of this run's parity attempt needs theta M_k > 1. For k = 4 that is theta > 1/M_4 >= ... = 0.54230
  (deg-6 vector; the true M_4 is about 1.845, so about 0.542 at best). Risky question: do known level-of-distribution results
  for sieve weights, or Polymath8b's enlarged supports (which work with BV alone for the bounded-gaps criterion), reach it?
- Tried: (a) the best published level for smooth moduli: Stadlmann arXiv:2309.00425 (abstract read on arXiv, 16 Nov): moduli up
  to x^{1/2+1/40} = x^{0.525}; (b) the enlarged-support argument on paper.
- Outcome: DEAD END with current inputs. (a) 0.525 < 0.5423, and the lambda-analogue of such an estimate is also needed (not
  checked in any source). (b) Enlarged supports need only an upper bound for S_1 and lower bounds for the prime sums, but the
  lambda-twisted sum sum w_n lambda(n+r) must be o(S_1) in absolute value, and for weights of level beyond x^{1/4} (moduli
  beyond x^{1/2}) BV for lambda does not give that. The 2026 claimed inputs (Stadlmann 240 etc.) were not examined for a
  lambda-analogue. Heuristic / exploratory only.

## 2026-11-16, Session 25 -- Do small values of L(1, chi) come with few small split primes? (class numbers / Siegel-zero heuristics)
- Idea: the parity attempt of this run (route card 2026-11-16-siegel-world-typeI.md) leaves open whether a Siegel character
  must have few small split primes (sum_{w<p<R0, chi(p)=1} 1/p < 1/4). Risky question: in the actual world, do the
  characters with the smallest L(1, chi) have s'(q) = sum_{3<p<=q^{1/4}, chi(p)=1} 1/p < 1/4? Also, can the class-number
  bound (reduced forms of norm < sqrt(q)/2 are inequivalent) control the reciprocal sum of small split primes?
- Tried: code/explore/l1_small_split.py (all 9005 primes q = 3 mod 4, 3 < q <= 2e5; h from h = -(1/q) sum a chi(a); output
  l1_small_split.out, 11 s). Plus the reduced-form argument on paper.
- Outcome: INCONCLUSIVE, and the data cannot decide it. corr(log L(1), s') = +0.36. Bottom 1% of L(1) (<= 0.308): mean
  s' = 0.029, none with s' >= 1/4. Bottom 5%: 0.4% have s' >= 1/4. All q: 53%. The twelve smallest L(1) have s' = 0 except one
  (0.053). This is close to tautological: in the actual world log L(1, chi) is dominated by sum chi(p)/p over small primes. In
  a Siegel world, L(1) is small because of the large primes in [R0, x] (TT Cor. 3.6), and the data cannot see that regime.
  The reduced-form argument bounds the NUMBER of split primes below sqrt(q)/2 by about 2h(-q), and
  h ~ sqrt(q) log q / eta is huge, so it gives no control of the reciprocal sum (counts vs 1/p-sums; small split primes are
  unconstrained). A Wirsing-type lower bound for split-smooth numbers would need a lower-bound sieve of dimension ~1 up to
  the full range, which is exactly the parity problem again. Heuristic / exploratory only.

## 2026-11-15, Session 24 -- Does mu(p-2) show a parity bias in progressions that Hooley's condition would see? (numerical experiment / probabilistic model)
- Idea: Ford's open case (parity paper open question 7) asks whether EH plus Hooley's averaged absence of parity bias,
  sum_{d <= x^alpha} |sum_{p <= x, p = 2 (d)} mu(p-2) log p| << x (log x)^{-B}, suffices. Risky question: does the twin sequence
  show any structure (bias in classes, correlation across d) beyond square-root cancellation, which might either refute the
  condition numerically or suggest a mechanism?
- Tried: code/explore/hooley_twin_parity.py (.out): the sum against a random-sign model on the same support (squarefree p-2,
  4 seeds), x = 1e6 and 1e7, alpha = 0.25, 0.4, 0.5.
- Outcome: inconclusive (no structure): ratio actual / random model = 1.54, 1.27 at x = 1e6 and 0.73, 0.85, 0.90 at x = 1e7;
  i.e. square-root cancellation, as the random model predicts (H/x ~ x^{(alpha-1)/2}, so Hooley's condition is "true by
  heuristics" for every alpha < 1). Nothing to exploit; proving it remains the Moebius-on-shifted-primes problem.

## 2026-11-15, Session 23 -- Is the constant of the k = 3 Schur problem a closed form? (numerical experiment / constants)
- Idea: the 1D Schur problem of parity paper Prop. prop:unc-ceiling is scale-invariant, so the supremum of the k = 3 problem
  without marginal condition is (numerically) 3/2 + kappa (1-eps) for eps in [1/4, 1/2). A closed form for kappa would give
  the exact threshold eps* = 1 - 1/(2 kappa) where it crosses 2.
- Tried: code/explore/kappa_closed_form.py (piecewise-linear Nystrom at N = 100..800, Richardson; mpmath.identify).
- Outcome: dead end for the closed form: kappa = 0.8901675 (about 8 digits stable), eps* = 0.438308; identify returns only
  overfitted combinations of pi, e, logs (noise). Useful by-product (rigorous, in the paper as Cor. cor:k3-linear): by scaling,
  the single certificate at eps = 0.439 gives sigma_3(eps) <= 3/2 + (4999/5610)(1-eps) for all eps in [1/4, 1/2).

## 2026-11-15, Session 22 -- Does the k = 3 extremal of Polymath8b's Theorem 3.14 keep the k = 2 structure (constant marginal)? (variational structure / spectral)
- Idea: at k = 2 the extremal step function F_eps has marginal f = 1 on the whole J-interval [0, 1-eps]. If the k = 3 extremal
  also had (nearly) constant marginal on {t2+t3 <= 1-eps}, the supremum would reduce to a minimum-norm problem (min I subject
  to f_i = 1 on the J-region and f_i = 0 on the forbidden region), whose dual is a finite set of fibre equations: a possible
  route to the exact k = 3 value (open question 6).
- Tried: code/explore/k3_extremal_marginal.py (floating point, cube grid n = 24, eps = 1/4 and 1/8; output .out): the marginal
  of the grid eigenvector, and the exact minimum-norm F with constant marginal.
- Outcome: dead end. The extremal marginal is far from constant (relative std 0.43 at eps = 1/4, 0.48 at eps = 1/8; it falls
  from about 2.65 at the origin to 0.5 at the corner of the J-region), and the constant-marginal ansatz gives only 1.736
  (eps = 1/4) and 1.457 (eps = 1/8) against 1.959 / 1.934 for the same grid. The k = 2 structure does not persist at k = 3;
  this matches the route card 2026-11-15-k3-dual-orthogonal.md (the overlap constraints change the problem).

## 2026-11-15, Session 21 -- How far above the parity value is Polymath8b's k = 3 criterion? (numerical experiment / variational structure)
- Idea: this run proved (parity paper Thm thm:k2) that the Thm 3.14 ratio at k = 2 is exactly the parity value 2. At k = 3 PM8b's
  Thm 3.15 certificate gives J/I = 2 + 5.77e-8 (exact fraction re-checked), i.e. barely above 2. Risky question: is the true k = 3
  supremum also (essentially) 2, which would make H_1 <= 6 under GEH a knife-edge, or is there visible room?
- Tried: code/explore/k3_thm314_grid.py (floating point; symmetric piecewise-constant F on cubes of side 1/n inside (3/2)R_3,
  vanishing marginal imposed on every cell meeting the forbidden region, J only on cells fully inside (1-eps)R_2; eps = 1/4).
  Output code/explore/k3_thm314_grid.out: n = 16, 20, 24 give 1.9366, 1.9500, 1.9589 (lower bounds for the grid class only).
- Outcome: inconclusive, leaning "room exists but is small". Linear and quadratic extrapolation in 1/n both give about 2.003, so the
  supremum at eps = 1/4 looks like roughly 2.003 (Heuristic), consistent with PM8b's > 2 and far below our ceiling c(3) = 2.472. The grid
  class converges slowly (boundary loss O(1/n)); no certificate. Not promising enough for a flag.
- Next if resumed: optimise over eps and use piecewise-linear elements on PM8b's polytope decomposition (their Sec. 7.4) to get an honest
  lower bound above 2 and a dual (upper) certificate; that would answer open question 6 of the parity paper.

## 2026-11-15, bonus run (Session 20) -- Barban-Davenport-Halberstam variance for lambda(n)lambda(n+2): can L^2 information reach the twisted Type I input beyond level 1/2? (large sieve / probabilistic models)
- Idea: the twisted Type I input of the parity obstruction is a statement about sum_{n = 0 (d)} lambda(n)lambda(n+2) for d up to x^theta.
  An L^2 (BDH-type) statement over all classes might be easier than a pointwise one. The BDH variance
  V(Q) = sum_{W<=Q} sum_b |sum_{n=b (W)} f(n)|^2 with f = lambda(n)lambda(n+2) is governed by the four-point "parallelogram"
  correlations C(d) = sum_n f(n)f(n+d).
- Tried: code/explore/bdh_twin_liouville.py at N = 10^7 (49 s). C(d)/sqrt(N) for d <= 2000 has rms 1.000 and max 3.47, the same
  for even and odd d. V(200)/(200 N) = 0.983, against 1 for random signs. The deduction: by Cauchy-Schwarz,
  sum_{d<=Q} |S(d,0)| <= (Q V(Q))^{1/2}, and even the random-sign value V = QN gives Q sqrt(N), which beats the trivial bound
  x log Q only for Q < sqrt(x).
- Outcome: dead end (as expected). L^2 / large-sieve information about lambda(n)lambda(n+2) cannot go past level 1/2, whatever
  the four-point correlations are, so it cannot replace the pointwise input. The numerics are consistent with randomness and
  show no structure.

## 2026-11-15, Session 19 -- Do Liouville signs at extra linear forms enlarge the class of parity weights? (optimisation duality / LP)
- Idea: open question 2 of the parity paper asks for weights outside the Liouville-pattern class. The cheapest enlargement is to let
  the weight also depend on lambda(L(n)) at further linear forms L (independent ones, or dependent ones such as
  lambda(2(n+h_1)) = -lambda(n+h_1)), hoping that the extra coordinates make DHL[5,3] blockable.
- Tried: exact-support LPs (code/explore/aux_forms_lp.py, scipy HiGHS, floating point) for DHL[4,3], DHL[5,3], DHL[3,2] and the
  PM8b path target, with 0, 1, 2 auxiliary coordinates and one dependent one; results code/explore/aux_forms_lp.json.
- Outcome: dead end, and provably so. Fairness and the kill condition involve only the law of the set {i : lambda(n+h_i) = -1} on
  the tuple coordinates (singleton coefficients and the support), so the tuple marginal of any enlarged weight is an ordinary
  pattern weight with the same properties: auxiliary coordinates never help. The LPs agree (DHL[4,3] and the path blocked,
  DHL[5,3] and DHL[3,2] not, for every number of auxiliary coordinates). With the stronger all-orders notion (--full) nothing is
  blocked, not even the PM8b target: that notion makes Omega constant, so it is the wrong one.
- Why it matters: it narrows open question 2. Any weight that could block DHL[5,3] must change the twisted main terms themselves
  (functions whose values at primes are not fixed, or non-fair residue-class dependence), not just add more Liouville signs.
  Too elementary for the paper; not added there.

## 2026-11-15, Session 18 -- Can residue-class-dependent parity weights beat the k <= 2m criterion? (optimisation duality / LP)
- Idea: the parity paper's Prop. prop:bipartite covers weights that depend only on Liouville signs. A weight may also depend on
  n mod q; in classes where p | n + h_j the position j cannot hold a prime, so it needs no fairness and no kill condition. Risky
  question: does this extra freedom block targets the criterion leaves open, e.g. DHL[3,2]?
- Tried: code/explore/residue_parity_lp.py (exact LP feasibility, scipy/HiGHS, toy model with uniform true masses; output
  code/explore/residue_parity_lp.json; 11 s). Two fairness notions: GLOBAL (one density constant per position, class weights free)
  and CLASSWISE (uniform class weights, fake-prime density 1/2 at each alive position in each class).
- Outcome: dead end, but instructive. One prime p > k: no integer gain in either model (global gives k <= 2m p/(p-1) < 2m+1).
  Several primes: the GLOBAL model becomes feasible for k = 3, m = 1 at q = 5*7*11 and 5*7*11*13 (bound ~ 2m/prod(1-1/p)), i.e.
  it would "block" DHL[3,2], which Polymath8b prove under GEH; so global fairness is the wrong notion (such a weight changes the
  Type I main terms class by class, which the sieve sees). CLASSWISE fairness is infeasible in every case tested, and in general it
  reduces to the criterion class by class (alive positions only), so no gain. Heuristic / exploratory; not in a paper.
- Use: supports Remark rem:marg's scope statement and the new open question of the parity paper (weights outside the class).

## 2026-11-15, Session 17 -- What does a Selberg/GPY weight see of the parity of n(n+2)? (probabilistic models / parity)
- Idea: weight odd n <= X by the GPY-type Selberg weight w(n) = (sum_{d | n(n+2), d <= X^theta} mu(d)(log(R/d)/log R)^2)^2 and
  measure the weighted correlation of lambda(n)lambda(n+2), the split of the weight by parity pattern, and the residue-class
  distribution of the two parity-twisted measures w(1 +- lambda(n)lambda(n+2))/2.
- Tried: code/explore/parity_weighted_liouville.py at X = 1e6, 1e7, 1e8, theta = 0.20, 0.25 (log runs/explore_parity_weighted.log;
  each run under a minute, < 2 GB).
- Outcome: inconclusive / as expected. B/A = sum w lambda lambda / sum w falls from 6e-4 (1e7) to 4e-5 (1e8); the two twisted measures
  have equal mass and the same class shares mod 3, 5, 7 to two or three decimals, while all twin pairs (3-5% of the weight) lie in
  the "+" measure: Selberg's phenomenon, visible but proving nothing. It suggested the parity attempt of this run (Tao's two-point
  theorem along periodic weights, paper Prop. prop:tao-weight) and is the numerical illustration of the parity paper (Sec. 4,
  Heuristic).

## 2026-11-14, Session 16 -- A "pretentious twin" statistic: how far is lambda from the Siegel-zero world lambda ~ chi_D? (Siegel zeros)
- Idea: in Heath-Brown's Siegel-zero argument the parity obstruction for twin primes disappears because
  lambda(n) ~ chi_D(n) on most of the range, so lambda(n)lambda(n+2) ~ chi_D(n)chi_D(n+2), whose mean is not zero.
  Risky question: for the nine class-number-one discriminants -D (the conductors where L(1, chi_D) = pi h/sqrt(D)
  is smallest relative to D), is there any measurable "Siegel-world" signal in the twin correlation itself, i.e. in
  S2(X) = sum_{n<=X} lambda(n)lambda(n+2) chi_D(n)chi_D(n+2), which would be about X in that world?
- Tried: code/explore/siegel_pretentious_twin.py (numpy sieve to X = 2e7; Kronecker symbols; output
  code/explore/siegel_pretentious_twin.json). Also S1 = sum lambda chi_D, the squared pretentious distance
  sum_{p<=X} (1 + chi_D(p))/p, and the Chowla sum S3 = sum lambda(n)lambda(n+2). Check: L(1, chi_{-163}) from the
  Hurwitz-zeta formula agrees with pi/sqrt(163) to 1e-10.
- Outcome: DEAD END for twin primes. |S2|/sqrt(X) <= 1.8 for every D at X = 2e7 (S2/X <= 4e-4 and decreasing), and
  |S3|/sqrt(X) <= 1: square-root cancellation, no pretentious twin correlation at these scales, as expected.
  The one large signal is S1 for D = 163: S1/sqrt(X) = 25.7, 27.9, 27.7, 27.4 at X = 1e5, 1e6, 1e7, 2e7 (stable, not
  growing). Explanation checked in part: the pole of L(2s, chi_0) = zeta(2s)(1 - D^{-2s}) at s = 1/2 gives a term
  (1 - 1/D) sqrt(X)/L(1/2, chi_D) = 14.50 sqrt(X) (L(1/2, chi_{-163}) = 0.06853, mpmath); the excess is consistent
  with the unusually low zero of L(s, chi_{-163}) near 1/2 + 0.2 i (|L| = 0.0019 there on a 1/40 grid), whose term
  rotates slowly in log X. Not pursued further: this is a known kind of secondary term, and it says nothing about
  the twin correlation. Heuristic / exploratory only; no literature opened for the low zero, so no claim about it.

## 2026-11-14, Session 15 -- Moebius autocorrelations and twin irreducibles in F_2[T] at small degree (function fields)
- Idea: in F_q[T] the twin-prime analogue is proved for large q (Sawin-Shusterman), but q = 2 is the most
  "integer-like" case and characteristic 2 is known to be special for Chowla-type sums. Risky question: at the
  degrees we can reach, does F_2[T] show any parity-type structure in sum mu(f) mu(f + h), or any deviation of the twin
  count from the Hardy-Littlewood shape, that could point to a mechanism with an integer analogue?
- Tried: code/explore/ff_chowla.py (sieve for mu and irreducibility over F_2, polynomials as bit masks, checked against
  trial-division factorisation for deg <= 10 and the count 99 of irreducibles of degree 10). Output for n <= 22 in
  code/explore/ff_chowla_out22.txt. Shift 1 is NOT admissible over F_2 (f(0) = f(1) = 1 forces T | f + 1), so the
  twin count uses H = T^2 + T, with singular series S(H) = 3.3315 (product over irreducibles of degree <= 22).
- Outcome: INCONCLUSIVE, no usable mechanism. (i) P_2^H(n) / (S 2^n / n^2) = 1.016, 1.001, 0.995 at n = 20, 21, 22
  (HL shape fits). (ii) |C_h(n)| / 2^{n/2} stays between 0 and 2.3 for h in {1, T, T+1, T^2+T}, n = 12..22:
  square-root-size cancellation, no sign of a non-vanishing correlation at these degrees. (iii) C_T = C_{T+1}
  identically (the automorphism T -> T+1). (iv) A small curiosity: C_1(n) > 0 for every even n in 12..22 (largest
  4660 = 2.28 * 2^11 at n = 22), mixed signs for odd n; with six data points this may be noise. The characteristic-2
  literature on Chowla sums (Carmon-Rudnick; Conrad-Conrad-Gross) was NOT opened this session, so no comparison is
  claimed. Heuristic / exploratory only. If revisited: open those sources first, then test whether the even-degree
  sign pattern persists to n = 26 (bytearray sieve needs ~2^27 bytes, a few minutes).

## 2026-11-14, Session 14 -- Is there enough slack in Song-Yue's exponent conditions to save one step k = 48 -> 47? (exponential sums / Type III)
- Idea: the D182 level theta = 253/500 (omega = 3/1000) is set by many exponent inequalities of [SY26, Sec. 4],
  and the audit (notes/audit-sy236-thm418/) lists their exact margins. If one margin were loose, raising omega a
  little might move the variational criterion from k = 48 to k = 47 (a smaller tuple). Compare the omega the
  k = 47 criterion would need with the omega the printed margins allow.
- Tried: code/explore/level_slack.py. Criterion M_{k,eps} * 2 theta > 4 (eps = 15/506 as in
  cert_kin48_capfree_D22e). M_{47,eps} - M_{48,eps} at degree 16: 3.909715 vs 3.925064 (mk_general, Session 14),
  so M_{47,eps}(D22) is about 3.94356; k = 47 needs theta >= 0.507157, i.e. d omega >= 5.8e-4. With all other
  parameters fixed, the Type III margin (52) (1 - 1/3000, coefficient 7/3 on omega) allows d omega <= 1.4e-4 and
  the IIa margin (33) at gamma = 11/25 allows <= 2.2e-5.
- Outcome: DEAD END. The needed increase is 4 times the loosest margin and 26 times the IIa one, before the
  cap cost (about 3e-4 in the ratio) and before re-tuning eps and the caps to the new omega. Saving one k needs a
  genuinely stronger equidistribution estimate, not tighter bookkeeping. Heuristic only (the margins can be
  re-balanced by moving eta2, tau0, s3, eta3, which this toy does not do).

## 2026-11-13, Session 13 -- Primes in translates of the 236-tuple vs Hardy-Littlewood (probabilistic models of primes)
- Idea: test the probabilistic (Hardy-Littlewood) model directly on the Lean-checked admissible 48-tuple narrow48
  (diameter 236) that the conditional 236 rests on, and ask whether numerical data could say anything about
  DHL[48,2] (infinitely many n with at least 2 primes among n + h_i).
- Tried: code/explore/tuple_counts_hl.py (numpy sieve; HL 2-tuple prediction sum_{i<j} S(h_j - h_i) int dt/(log t log(t+d))).
  X = 1e6 / 1e7 / 1e8: prime pairs in translates 15612870 / 111570638 / 837030982, ratio to HL 0.99642 / 0.99885 /
  0.99969; n <= X with >= 2 primes in n + H: 496425 / 4903811 / 48078484 (about 48% of n at X = 1e8).
- Outcome: DEAD END (as expected). HL fits to 3e-4, which is well known. The data cannot bear on DHL[48,2]: the
  average number of primes in a translate is about 48/log X, which stays above 1 until X is about e^48 = 7e20, so in
  any computable range "two primes in a translate" is the typical event, not a rare one; the content of DHL is
  asymptotic. Not worth repeating with other tuples. Heuristic only.

## 2026-11-13, Session 12 -- Per-m caps in the toy capped problem: do caps on SUMS cause a large regain? (variational)
- Idea: Session 11's toy (one uniform cap) left open whether the 31% regain at k = 45 (Lemma 9.1 caps, Session 9)
  comes from the per-m pattern of the caps (separate caps on single coordinates and on sums of several). Smallest
  test: k = 3, T = {t >= 0, sum t <= 1, t_i <= c1, t_i + t_j <= c2}, symmetric polynomials of degree d = 5, 8.
- Tried: code/explore/toy_capped_perm.py (floating point; fibre in t_1 split into the four polytopes where
  min(c1, 1 - y2 - y3, c2 - y2, c2 - y3) is attained). Sanity: c2 = 1 reproduces Session 11's uniform-cap numbers
  (c1 = 0.8: trunc 1.614592, regain 0.101). Log: runs/explore_toy_capped_perm.log. d = 5 and d = 8 agree to 2 digits.
  regain: pair caps only (c1 = 1): c2 = 0.9 / 0.8 / 0.75 / 0.7 -> 0.085 / 0.067 / 0.051 / 0.037 (it FALLS as the
  pair cap tightens); mixed c1/c2 = 0.6/0.9, 0.6/0.8, 0.7/0.8, 0.5/0.9 -> 0.131, 0.110, 0.081, 0.126; single cap
  c1 = 0.6 -> 0.126.
- Outcome: DEAD END for the hypothesis. In the toy, caps on sums give a SMALLER regain than caps on single
  coordinates, and mixing them never exceeds about 13%. So the cap pattern alone does not explain the 31% regain at
  k = 45; remaining candidates are the enlarged (L > 1) part of the hybrid support and the size of k, which a k = 3
  toy cannot show. Not worth more toy work; if the question returns, test on the real k = 45 support with fewer caps
  switched on (the adjoint Gram machinery of capped_gram.py does this exactly). Heuristic only.

## 2026-11-13, Session 11 -- Toy model of the capped problem: what decides the "regain" fraction? (variational/spectral)
- Idea: Session 9's registered prediction failed because re-optimising on the capped support regained 31% of the
  truncation loss at k = 45 (Lemma 9.1 caps) against 9% at k = 49. Is the regain fraction a property of k, of the
  cap severity, or of the cap pattern? Test in the smallest model where everything is cheap: region
  T_c = {t >= 0, sum t <= 1, t_i <= c} (one uniform cap, no enlarged support), symmetric polynomials of degree d.
- Tried: code/explore/toy_capped.py (floating point, Delaunay + collapsed Gauss quadrature, exact for these degrees;
  sanity check M_2 = 1.3859333, M_3 = 1.646440 as in Polymath8b). Log: runs/explore_toy_capped.log.
  regain = (opt_T - trunc)/(opt_free - trunc), degrees d = 6, 10 (k = 2) and d = 5, 8 (k = 3) agree to 2 digits:
  k = 2: c = 0.95 / 0.9 / 0.8 / 0.7 / 0.6 -> 0.045 / 0.069 / 0.088 / 0.089 / 0.080.
  k = 3: c = 0.95 / 0.9 / 0.8 / 0.7 / 0.6 / 0.5 / 0.45 -> 0.025 / 0.060 / 0.101 / 0.120 / 0.126 / 0.126 / 0.120.
- Outcome: INCONCLUSIVE. With one uniform cap the regain stays small (<= 13%) and plateaus as the cap tightens,
  rising slowly with k; this fits k = 49 (9%, uniform cap 0.6 on Stadlmann's support) but not k = 45 (31%), which
  suggests the large regain there comes from the non-uniform per-m caps of Lemma 9.1 (different caps for m = 1, 2,
  3+), not from k. Not tested: per-m caps in the toy (needs k >= 3 with caps on sums of pairs) -- the natural next
  step if this question matters again. Heuristic only; nothing enters a paper.

## 2026-11-13, Session 10 -- Is Song-Yue's objection to [Sta26, Lemma 5] real? (exponential sums / Type I-II area)
- Idea: [SY26, Remark 4.23] says the large-gamma step of the proof of [Sta26, Lemma 5] (Baker-Irving Type I)
  applies the Type IIa lemma with the factors swapped, although Type IIa needs the shorter factor to be
  Siegel-Walfisz and Lemma 5 assumes nothing about it. Read the arXiv v1 text (fetched 13 Nov, pdftotext) and
  check the claim against the statements.
- What we read (arXiv:2608.31126v1, Sec. 3.2, 3.3.5, Def. 9, proof of Prop. 3, Case I):
  * Lemma 3 (Polymath Type II): f = alpha * beta, beta at scale N = x^gamma <= x^{1/2}, "Suppose also that beta has
    the Siegel-Walfisz property".
  * Lemma 5 (Baker-Irving Type I): alpha an arbitrary coefficient sequence at scale M, beta smooth at scale
    N = x^gamma; no Siegel-Walfisz hypothesis on alpha.
  * Proof of Lemma 5, range gamma in (1/2, 1/2 + 2 omega + eps]: "we can apply our Lemma 3 (with the roles of alpha
    and beta swapped and gamma replaced by 1 - gamma)". After the swap the shorter factor is alpha (scale x^{1-gamma}
    <= x^{1/2}), so Lemma 3 needs alpha to be Siegel-Walfisz.
  * Definition 9 (I) and Case I of the proof of Prop. 3 apply Lemma 5 to "alpha a coefficient sequence at scale M"
    (again no Siegel-Walfisz hypothesis); Case (II) states the hypothesis explicitly for both factors.
- Outcome: INCONCLUSIVE, but the textual gap is CONFIRMED: as written in v1, that step uses a hypothesis that neither
  Lemma 5 nor Def. 9 (I) provides. Whether it matters is open: the alpha's that occur in a Harman-sieve
  decomposition are usually built from primes / rough numbers and may well be Siegel-Walfisz (then adding the
  hypothesis to Def. 9 (I) for that gamma-range repairs the proof); alternatively that gamma-range might be covered
  differently. We have not checked either repair. Status for the paper: "possible gap in the analytic input of 240,
  raised by [SY26, Rem. 4.23]; the cited step reads as they say (checked against arXiv v1); repair not checked".
- Why it matters: 240 (and 236, which reuses Stadlmann's estimates) rests on this analytic input; our reproduced
  240 is already labelled conditional on it.
